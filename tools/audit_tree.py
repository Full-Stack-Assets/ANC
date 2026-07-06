#!/usr/bin/env python3
"""Internal consistency audit over data/people/.

Flags records whose dates or places are impossible or genealogically
implausible. Pure heuristics on year values — approximate dates (ABT/BET)
use their best single year, so treat findings as leads, not verdicts.

Usage:
    python3 tools/audit_tree.py [--out report.md] [--data data]
"""

from __future__ import annotations

import argparse
from pathlib import Path

from duplicates import duplicate_person_findings
from people_io import load_people

MAX_LIFESPAN = 105
FATHER_MIN, FATHER_MAX = 14, 80
MOTHER_MIN, MOTHER_MAX = 13, 50
MARRIAGE_MIN = 12

# (state name fragment, first plausible year for a record naming it).
# "USA"/"United States" suffixes are deliberately NOT flagged: Ancestry
# normalizes historical places to modern names, so a 1650 event "..., USA"
# is notation, not a claim. Colony names predating their founding are kept —
# they usually mark a bad merge (e.g. born in Pennsylvania before 1681).
ANACHRONISTIC_PLACES = [
    ("pennsylvania", 1681),
    ("new jersey", 1664),
    ("delaware", 1638),
]


def year_of(ev) -> int | None:
    if not ev:
        return None
    d = ev.get("date")
    return d.get("year") if d else None


def place_of(ev) -> str:
    if not ev:
        return ""
    p = ev.get("place")
    return (p.get("raw") if p else "") or ""


def audit(people: dict[str, dict]) -> list[dict]:
    findings = []

    def flag(pid, kind, detail):
        findings.append({"id": pid, "name": people[pid]["name"]["full"],
                         "kind": kind, "detail": detail})

    for pid, p in people.items():
        birth = p["vitals"].get("birth")
        death = p["vitals"].get("death")
        by, dy = year_of(birth), year_of(death)

        if by is not None and dy is not None:
            if dy < by:
                flag(pid, "death-before-birth", f"born {by}, died {dy}")
            elif dy - by > MAX_LIFESPAN:
                flag(pid, "impossible-lifespan", f"lifespan {dy - by} years ({by}-{dy})")

        # anachronistic places on any dated event
        events = list(p["vitals"].values()) + p["events"]
        for ev in events:
            y, pl = year_of(ev), place_of(ev).lower()
            if y is None or not pl:
                continue
            for frag, first_year in ANACHRONISTIC_PLACES:
                if frag in pl and y < first_year:
                    flag(pid, "anachronistic-place",
                         f"{ev['type']} {y} at '{place_of(ev)}' — '{frag}' not a plausible "
                         f"place name before {first_year}")

        # marriage age
        for s in p["relationships"]["spouses"]:
            my = year_of(s.get("marriage"))
            if my is not None and by is not None and my - by < MARRIAGE_MIN:
                flag(pid, "married-as-child", f"born {by}, married {my} (age {my - by})")

        # parent/child plausibility
        for cid in p["relationships"]["children"]:
            c = people.get(cid)
            if c is None:
                continue
            cby = year_of(c["vitals"].get("birth"))
            if cby is None:
                continue
            cname = c["name"]["full"]
            if by is not None:
                age = cby - by
                lo, hi = (MOTHER_MIN, MOTHER_MAX) if p["sex"] == "F" else (FATHER_MIN, FATHER_MAX)
                if age < 0:
                    flag(pid, "child-before-parent", f"child {cname} b.{cby} before parent b.{by}")
                elif age < lo:
                    flag(pid, "parent-too-young", f"age {age} at birth of {cname} ({cby})")
                elif age > hi:
                    flag(pid, "parent-too-old", f"age {age} at birth of {cname} ({cby})")
            if dy is not None:
                grace = 1 if p["sex"] == "M" else 0
                if cby > dy + grace:
                    flag(pid, "child-after-death",
                         f"child {cname} b.{cby}, parent died {dy}")

    findings.extend(duplicate_person_findings(people))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data")
    ap.add_argument("--out", default=None, help="write markdown report here")
    args = ap.parse_args()

    people = load_people(Path(args.data))
    findings = audit(people)

    by_kind: dict[str, list[dict]] = {}
    for f in findings:
        by_kind.setdefault(f["kind"], []).append(f)

    lines = [f"# Tree consistency audit", "",
             f"{len(people)} people checked, {len(findings)} findings "
             f"on {len({f['id'] for f in findings})} distinct people.", ""]
    for kind in sorted(by_kind, key=lambda k: -len(by_kind[k])):
        rows = by_kind[kind]
        lines.append(f"## {kind} ({len(rows)})")
        lines.append("")
        for f in sorted(rows, key=lambda r: r["name"]):
            lines.append(f"- `{f['id']}` **{f['name']}** — {f['detail']}")
        lines.append("")

    report = "\n".join(lines)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(report, encoding="utf-8")
        print(f"{len(findings)} findings ({', '.join(f'{k}: {len(v)}' for k, v in sorted(by_kind.items()))})")
        print(f"report written to {args.out}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
