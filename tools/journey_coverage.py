#!/usr/bin/env python3
"""Report (and optionally backfill) missing data/journeys/ files.

Usage:
    python3 tools/journey_coverage.py [--data data] [--home I182195856751]
    python3 tools/journey_coverage.py --seed-missing [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from build_game_bundle import walk_ancestors
from gedcom_to_people import build_journey_seed, write_json
from people_io import load_people

ROOT = Path(__file__).resolve().parent.parent
PERSON_ID_RE = re.compile(r"\bI\d+\b")


def missing_journey_ids(data_dir: Path) -> list[str]:
    people = sorted(p.stem for p in (data_dir / "people").glob("I*.json"))
    journeys = {p.stem for p in (data_dir / "journeys").glob("*.json")}
    return [pid for pid in people if pid not in journeys]


def dossier_ids(research_dir: Path) -> set[str]:
    ids: set[str] = set()
    for path in research_dir.glob("**/*.md"):
        ids.update(PERSON_ID_RE.findall(path.read_text(encoding="utf-8", errors="ignore")))
    return ids


def build_minimal_journey(person: dict) -> dict:
    return {
        "id": person["id"],
        "person": person["name"]["full"],
        "status": "seeded",
        "summary": None,
        "waypoints": [],
        "notes": None,
    }


def seed_missing_journeys(data_dir: Path, *, dry_run: bool = False) -> tuple[int, int, int]:
    """Create journey files for people missing them. Returns placed, minimal, skipped."""
    people = load_people(data_dir)
    placed = minimal = skipped = 0

    for pid in missing_journey_ids(data_dir):
        person = people.get(pid)
        if person is None:
            skipped += 1
            continue
        event_seed = build_journey_seed(person)
        if event_seed:
            seed = event_seed
            placed += 1
        else:
            seed = build_minimal_journey(person)
            minimal += 1
        if not dry_run:
            write_json(data_dir / "journeys" / f"{pid}.json", seed)

    return placed, minimal, skipped


def report(data_dir: Path, home_id: str, research_dir: Path) -> str:
    people = load_people(data_dir)
    missing = missing_journey_ids(data_dir)
    ancestry = walk_ancestors(people, home_id) if home_id in people else {}
    ancestor_ids = set(ancestry)
    dossiers = dossier_ids(research_dir)

    direct_missing = [pid for pid in missing if pid in ancestor_ids]
    dossier_missing = [pid for pid in missing if pid in dossiers]

    lines = [
        "# Journey coverage",
        "",
        f"{len(people)} people, {len(list((data_dir / 'journeys').glob('*.json')))} journeys, "
        f"{len(missing)} missing journey files.",
        "",
        f"- Direct ancestors of `{home_id}` missing journeys: {len(direct_missing)}",
        f"- Missing journeys with a research dossier mentioning them: {len(dossier_missing)}",
        "",
    ]
    if missing:
        lines.append("## Missing journey files")
        lines.append("")
        for pid in missing[:50]:
            gen = ancestry[pid]["generation"] if pid in ancestry else None
            flags = []
            if pid in dossiers:
                flags.append("dossier")
            if gen is not None:
                flags.append(f"gen {gen}")
            suffix = f" ({', '.join(flags)})" if flags else ""
            lines.append(f"- `{pid}` {people[pid]['name']['full']}{suffix}")
        if len(missing) > 50:
            lines.append(f"- ... and {len(missing) - 50} more")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", default=str(ROOT / "data"))
    ap.add_argument("--home", default="I182195856751")
    ap.add_argument("--research", default=str(ROOT / "docs" / "research" / "ancestors"))
    ap.add_argument("--out", help="write markdown report to this path")
    ap.add_argument("--seed-missing", action="store_true",
                    help="create journey files for people missing them")
    ap.add_argument("--dry-run", action="store_true",
                    help="with --seed-missing, report counts without writing files")
    args = ap.parse_args(argv)

    data_dir = Path(args.data)
    if args.seed_missing:
        placed, minimal, skipped = seed_missing_journeys(data_dir, dry_run=args.dry_run)
        verb = "would seed" if args.dry_run else "seeded"
        print(f"{verb} {placed + minimal} journeys ({placed} from events, {minimal} minimal shells)"
              + (f", {skipped} skipped" if skipped else ""))
        return 0

    text = report(data_dir, args.home, Path(args.research))
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"report written to {out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
