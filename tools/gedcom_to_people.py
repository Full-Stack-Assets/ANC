#!/usr/bin/env python3
"""Populate data/people/ (and optionally seed data/journeys/) from a GEDCOM export.

Usage:
    python3 tools/gedcom_to_people.py data/gedcom/tree.ged [--out data] [--seed-journeys] [--person I123]

Re-run safety:
  - people files are regenerated wholesale, except each file's `manual` block,
    which is preserved verbatim;
  - journey files are seeded only if absent — an existing journey is never touched.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gedcom_parser import VITAL_TYPES, Gedcom

# Journey seeding: waypoints come from events that have a place. Sort by year
# when known; undated vitals pin to the ends, everything else floats between.
_UNDATED_SORT = {"birth": -10_000, "christening": -9_999, "baptism": -9_999,
                 "death": 9_998, "burial": 9_999}


def _event_key(ev: dict) -> tuple:
    return (ev["type"], (ev.get("date") or {}).get("raw"),
            (ev.get("place") or {}).get("raw"), ev.get("value"))


def _dedupe_events(vitals: dict, events: list[dict]) -> list[dict]:
    """Ancestry exports repeat events for every merged hint/tree. Collapse
    exact duplicates (same type, date, place, value), merging their source
    citations into the surviving event."""
    kept: dict[tuple, dict] = {_event_key(ev): ev for ev in vitals.values()}
    result = []
    for ev in events:
        key = _event_key(ev)
        if key in kept:
            survivor = kept[key]
            for c in ev["sources"]:
                if c not in survivor["sources"]:
                    survivor["sources"].append(c)
            if survivor["sources"]:
                survivor["confidence"] = "documented"
        else:
            kept[key] = ev
            result.append(ev)
    return result


def build_person(raw: dict, sources: dict[str, dict]) -> dict:
    """Assemble the final person record from a parsed individual."""
    raw["events"] = _dedupe_events(raw["vitals"], raw["events"])
    marriage_events = [s["marriage"] for s in raw["relationships"]["spouses"] if s.get("marriage")]
    all_events = list(raw["vitals"].values()) + raw["events"] + marriage_events

    used_source_ids: list[str] = []
    for citation_list in [ev["sources"] for ev in all_events] + [raw["citations"]]:
        for c in citation_list:
            if c["source_id"] not in used_source_ids:
                used_source_ids.append(c["source_id"])

    documented = any(ev["sources"] for ev in all_events) or bool(raw["citations"])

    return {
        "id": raw["id"],
        "name": raw["name"],
        "sex": raw["sex"],
        "vitals": raw["vitals"],
        "relationships": raw["relationships"],
        "events": raw["events"],
        "sources": [
            sources.get(sid, {"id": sid, "title": None, "author": None,
                              "publication": None, "repository": None})
            for sid in used_source_ids
        ],
        "notes": raw["notes"],
        "confidence": "documented" if documented else "inferred",
    }


def build_journey_seed(person: dict) -> dict | None:
    """Derive an initial journey from the person's placed events, or None if
    there is nothing to map."""
    candidates = []
    for ev in list(person["vitals"].values()) + person["events"] + [
        s["marriage"] for s in person["relationships"]["spouses"] if s.get("marriage")
    ]:
        # Vitals contribute only their preferred record; alternate birth/death
        # events (conflicting places from merged trees) stay in the person
        # file but don't become waypoints.
        if ev.get("place") and (ev["type"] not in VITAL_TYPES or ev in person["vitals"].values()):
            candidates.append(ev)

    # Collapse repeats of the same stop (same event kind, place, year).
    seen: set = set()
    unique = []
    for ev in candidates:
        key = (ev["type"], ev["place"]["raw"].lower(),
               (ev.get("date") or {}).get("year") if ev.get("date") else None)
        if key not in seen:
            seen.add(key)
            unique.append(ev)
    candidates = unique
    if not candidates:
        return None

    def sort_key(item):
        index, ev = item
        date = ev.get("date")
        if date and date.get("year") is not None:
            return (date["year"], index)
        return (_UNDATED_SORT.get(ev["type"], 5_000), index)

    ordered = [ev for _, ev in sorted(enumerate(candidates), key=sort_key)]

    waypoints = []
    for seq, ev in enumerate(ordered, 1):
        place = dict(ev["place"])
        place.setdefault("lat", None)
        place.setdefault("lng", None)
        waypoints.append({
            "seq": seq,
            "place": place,
            "date": ev.get("date"),
            "event": ev["type"],
            "narrative": None,
            "confidence": ev["confidence"],
            "sources": ev["sources"],
        })

    return {
        "id": person["id"],
        "person": person["name"]["full"],
        "status": "seeded",
        "summary": None,
        "waypoints": waypoints,
        "notes": None,
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("gedcom", help="path to the .ged export")
    ap.add_argument("--out", default="data", help="output root (default: data)")
    ap.add_argument("--seed-journeys", action="store_true",
                    help="also create data/journeys/{id}.json for people that don't have one yet")
    ap.add_argument("--person", action="append", metavar="ID",
                    help="only process this GEDCOM id (repeatable), e.g. --person I123")
    args = ap.parse_args(argv)

    ged = Gedcom.load(args.gedcom)
    out = Path(args.out)
    people_dir, journeys_dir = out / "people", out / "journeys"

    ids = args.person or sorted(ged.individuals)
    written = seeded = 0
    for pid in ids:
        raw = ged.individuals.get(pid)
        if raw is None:
            print(f"warning: no individual {pid!r} in {args.gedcom}", file=sys.stderr)
            continue
        person = build_person(raw, ged.sources)

        person_path = people_dir / f"{pid}.json"
        if person_path.exists():
            try:
                existing = json.loads(person_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                existing = {}
            if isinstance(existing.get("manual"), dict):
                person["manual"] = existing["manual"]
        write_json(person_path, person)
        written += 1

        if args.seed_journeys:
            journey_path = journeys_dir / f"{pid}.json"
            if not journey_path.exists():
                seed = build_journey_seed(person)
                if seed is not None:
                    write_json(journey_path, seed)
                    seeded += 1

    print(f"{written} people written to {people_dir}/"
          + (f", {seeded} journeys seeded to {journeys_dir}/" if args.seed_journeys else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
