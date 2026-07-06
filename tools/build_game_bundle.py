#!/usr/bin/env python3
"""Build data/generated/game_bundle.json — the versioned, privacy-reviewed
export of the direct-ancestor subset of the tree, for game consumption.

This is a SEPARATE artifact from the core person/journey pipeline: it does
not change or gate data/people/ or data/journeys/, and re-running it is
always safe (it only reads existing records and overwrites its own output).

Usage:
    python3 tools/build_game_bundle.py --home I182195856751 [--out data/generated/game_bundle.json]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import deque
from pathlib import Path

from duplicates import KNOWN_DUPLICATES, find_duplicate_clusters
from people_io import load_people

ROOT = Path(__file__).resolve().parent.parent

# Direct ancestors this close to the home person with no recorded death are
# treated as possibly living regardless of birth year — near-relatives are
# the case privacy actually matters for.
LIVING_HEURISTIC_GENERATION_CUTOFF = 3
LIVING_HEURISTIC_BIRTH_YEAR_CUTOFF = 1920

READINESS_STATUS_BASE = {"seeded": 20, "transcribed": 55, "reviewed": 80}


def two_parents(people: dict, pid: str) -> list[str]:
    """Cap a person's parent list at 2, preferring one male + one female when
    the export (or a manual addition) lists more due to a tree-merge artifact."""
    parents = [p for p in people[pid]["relationships"]["parents"] if p in people]
    if len(parents) <= 2:
        return parents
    male = [p for p in parents if people[p].get("sex") == "M"][:1]
    female = [p for p in parents if people[p].get("sex") == "F"][:1]
    return (male + female) if (male or female) else parents[:2]


def walk_ancestors(people: dict, home_id: str) -> dict[str, dict]:
    """BFS from home_id outward through parents. Returns {id: {generation, side,
    lineage_path}} for every reachable ancestor, home person included at
    generation 0. First-discovery wins on revisits (pedigree collapse)."""
    result = {home_id: {"generation": 0, "side": "self", "lineage_path": [people[home_id]["name"]["full"]]}}
    queue = deque([home_id])
    while queue:
        pid = queue.popleft()
        gen = result[pid]["generation"]
        path = result[pid]["lineage_path"]
        side = result[pid]["side"]
        parents = two_parents(people, pid)
        for i, par in enumerate(parents):
            if par in result:
                continue
            if gen == 0:
                sex = people[par].get("sex")
                par_side = "paternal" if sex == "M" else ("maternal" if sex == "F" else
                           ("paternal" if i == 0 else "maternal"))
            else:
                par_side = side
            result[par] = {
                "generation": gen + 1,
                "side": par_side,
                "lineage_path": path + [people[par]["name"]["full"]],
            }
            queue.append(par)
    return result


def privacy_status(pid: str, home_id: str, generation: int, birth_year: int | None, death_year: int | None) -> str:
    if pid == home_id:
        return "living_confirmed"
    if death_year is not None:
        return "public_safe"
    if generation <= LIVING_HEURISTIC_GENERATION_CUTOFF:
        return "possibly_living"
    if birth_year is not None and birth_year >= LIVING_HEURISTIC_BIRTH_YEAR_CUTOFF:
        return "possibly_living"
    return "public_safe"


def content_readiness(journey: dict | None) -> tuple[str, int, int, dict]:
    if journey is None:
        return "not_ready", 0, 0, {"documented": 0, "inferred": 0, "legend": 0}

    waypoints = journey.get("waypoints", [])
    mix = {"documented": 0, "inferred": 0, "legend": 0}
    narrated = 0
    for w in waypoints:
        mix[w["confidence"]] = mix.get(w["confidence"], 0) + 1
        if w.get("narrative"):
            narrated += 1
    coverage = (narrated / len(waypoints)) if waypoints else 0.0

    status = journey.get("status", "seeded")
    base = READINESS_STATUS_BASE.get(status, 0)
    score = min(100, base + round(20 * coverage))

    if status == "reviewed" and waypoints and coverage == 1.0:
        tier = "ready"
    elif waypoints and coverage > 0:
        tier = "draft"
    else:
        tier = "not_ready"
    return tier, score, len(waypoints), mix


def classify_source(src: dict) -> tuple[str, str]:
    title = (src.get("title") or "").lower()
    hosted_by = " ".join(filter(None, [src.get("author"), src.get("publication")])).lower()

    # Ancestry-hosted collections (the author/publication fields are far more
    # reliable than title wording — "U.S., Cemetery and Funeral Home
    # Collection" doesn't say "Ancestry" but is one of their hosted indexes).
    if "ancestry" in hosted_by or re.search(
        r"\bcensus\b|\bfederal\b|passenger|immigration|vital records|marriage records|"
        r"death index|birth index|public records index|obituary collection|cemetery",
        title,
    ):
        return ("proprietary_commercial_collection",
                "Commercial Ancestry.com-hosted collection — cite the underlying fact; "
                "do not reproduce collection images or transcriptions verbatim in-game.")
    if re.search(
        r"quaker meeting|calendar of.*wills|abstract of.*wills|will\b|court book|history of|"
        r"sketches of|byberry|moreland|historical.*famil",
        title,
    ):
        return ("public_domain_historical_record",
                "Public-domain historical record or out-of-copyright published local history — "
                "safe to quote or paraphrase with citation.")
    if not title:
        return ("unclassified", "No title recorded — review before use.")
    return ("unclassified", "Not auto-classified — review before use.")


def build_source_provenance(people: dict, ancestor_ids: set[str]) -> list[dict]:
    seen: dict[str, dict] = {}
    for pid in ancestor_ids:
        for src in people[pid].get("sources", []):
            if src["id"] in seen:
                continue
            license_class, note = classify_source(src)
            seen[src["id"]] = {
                "source_id": src["id"], "title": src.get("title"),
                "license_class": license_class, "usage_note": note,
            }
    provenance = sorted(seen.values(), key=lambda s: s["source_id"])
    provenance.append({
        "source_id": "ANC_RESEARCH_DOSSIERS",
        "title": "docs/research/ancestors/*.md and person manual.notes (this project's own research)",
        "license_class": "original_research_derived",
        "usage_note": "Facts drawn from this project's own web research (manual.notes fields, "
                      "docs/research/ dossiers) rather than a structured ANC source citation. "
                      "Freely usable in-game with in-project attribution; underlying external "
                      "sources are named in the dossier/note text itself.",
    })
    return provenance


def git_commit_hash() -> str | None:
    try:
        status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, check=True)
        if status.stdout.strip():
            return None  # dirty checkout — not a reproducible build
        rev = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True)
        return rev.stdout.strip()
    except Exception:
        return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--home", default="I182195856751", help="home person id (default: the tree owner)")
    ap.add_argument("--data", default=str(ROOT / "data"), help="ANC data/ directory")
    ap.add_argument("--out", default=str(ROOT / "data" / "generated" / "game_bundle.json"))
    args = ap.parse_args(argv)

    data_dir = Path(args.data)
    people = load_people(data_dir)
    if args.home not in people:
        raise SystemExit(f"home person {args.home!r} not found in {data_dir/'people'}")

    ancestry = walk_ancestors(people, args.home)
    ancestor_ids = set(ancestry)

    bundle_people = []
    for pid, walk in ancestry.items():
        person = people[pid]
        vitals = person.get("vitals", {})
        by = ((vitals.get("birth") or {}).get("date") or {}).get("year")
        dy = ((vitals.get("death") or {}).get("date") or {}).get("year")

        journey_path = data_dir / "journeys" / f"{pid}.json"
        journey = json.loads(journey_path.read_text(encoding="utf-8")) if journey_path.exists() else None
        tier, score, wp_count, mix = content_readiness(journey)

        bundle_people.append({
            "id": pid,
            "name": person["name"]["full"],
            "generation": walk["generation"],
            "side": walk["side"],
            "lineage_path": walk["lineage_path"],
            "birth_year": by,
            "death_year": dy,
            "privacy_status": privacy_status(pid, args.home, walk["generation"], by, dy),
            "content_readiness": tier,
            "readiness_score": score,
            "waypoint_count": wp_count,
            "confidence_mix": mix,
            "canonical_id": KNOWN_DUPLICATES.get(pid, pid),
        })
    bundle_people.sort(key=lambda p: (p["generation"], p["name"]))

    bundle = {
        "generated_at_source_commit": git_commit_hash(),
        "home_person_id": args.home,
        "people": bundle_people,
        "source_provenance": build_source_provenance(people, ancestor_ids),
        "duplicate_clusters": find_duplicate_clusters(people, ancestor_ids),
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    ready = sum(1 for p in bundle_people if p["content_readiness"] == "ready")
    living = sum(1 for p in bundle_people if p["privacy_status"] != "public_safe")
    print(f"{len(bundle_people)} ancestors (gen 0-{max(p['generation'] for p in bundle_people)}), "
          f"{ready} game-ready, {living} flagged possibly-living/confirmed-living, "
          f"{len(bundle['duplicate_clusters'])} duplicate clusters -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
