"""Shared duplicate-person detection heuristics."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RESOLUTIONS_PATH = ROOT / "data" / "manual" / "duplicate_resolutions.json"


def normalize_name(name: str) -> str:
    return " ".join(re.sub(r"[^a-z ]", "", name.lower()).split())


def birth_year(person: dict) -> int | None:
    return ((person.get("vitals", {}).get("birth") or {}).get("date") or {}).get("year")


def load_duplicate_resolutions(path: Path | None = None) -> dict[str, str]:
    """Return {duplicate_id: canonical_id} from data/manual/duplicate_resolutions.json."""
    path = path or DEFAULT_RESOLUTIONS_PATH
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {dup_id: entry["canonical"] for dup_id, entry in raw.items()}


def canonical_id(pid: str, resolutions: dict[str, str] | None = None) -> str:
    known = load_duplicate_resolutions() if resolutions is None else resolutions
    return known.get(pid, pid)


def group_by_name_and_birth_year(
    people: dict[str, dict],
    scope_ids: set[str] | None = None,
) -> dict[tuple[str, int], list[str]]:
    ids = scope_ids if scope_ids is not None else set(people)
    groups: dict[tuple[str, int], list[str]] = {}
    for pid in ids:
        if pid not in people:
            continue
        person = people[pid]
        year = birth_year(person)
        name = normalize_name(person["name"]["full"])
        if year is not None and name and name != "(unknown)":
            groups.setdefault((name, year), []).append(pid)
    return {key: sorted(ids) for key, ids in groups.items()}


def _group_is_resolved(ids: list[str], resolutions: dict[str, str]) -> bool:
    if not resolutions:
        return False
    canonicals = {resolutions[pid] for pid in ids if pid in resolutions}
    if len(canonicals) != 1:
        return False
    canon = next(iter(canonicals))
    return all(pid == canon or resolutions.get(pid) == canon for pid in ids)


def find_duplicate_clusters(
    people: dict[str, dict],
    scope_ids: set[str],
    resolutions: dict[str, str] | None = None,
) -> list[dict]:
    """Return duplicate clusters for game-bundle export."""
    known = load_duplicate_resolutions() if resolutions is None else resolutions
    groups = group_by_name_and_birth_year(people, scope_ids)
    clusters: list[dict] = []
    covered: set[str] = set()

    for ids in groups.values():
        if len(ids) <= 1 or _group_is_resolved(ids, known):
            continue
        canon = canonical_id(ids[0], known)
        for pid in ids:
            if pid in known:
                canon = known[pid]
                break
        dup_ids = [pid for pid in ids if pid != canon]
        clusters.append({
            "canonical_id": canon,
            "duplicate_ids": dup_ids,
            "basis": "name-and-birth-year-heuristic",
        })
        covered.update(ids)

    for dup_id, canon_id in known.items():
        if dup_id in scope_ids and dup_id not in covered:
            clusters.append({
                "canonical_id": canon_id,
                "duplicate_ids": [dup_id],
                "basis": "manual-research",
            })
            covered.add(dup_id)
    return clusters


def duplicate_person_findings(
    people: dict[str, dict],
    scope_ids: set[str] | None = None,
    resolutions: dict[str, str] | None = None,
) -> list[dict]:
    """Return audit-style findings for unmerged duplicate candidates."""
    known = load_duplicate_resolutions() if resolutions is None else resolutions
    groups = group_by_name_and_birth_year(people, scope_ids)
    findings: list[dict] = []
    for (_, year), ids in sorted(groups.items()):
        if len(ids) <= 1 or _group_is_resolved(ids, known):
            continue
        first = ids[0]
        findings.append({
            "id": first,
            "name": people[first]["name"]["full"],
            "kind": "duplicate-person",
            "detail": f"{len(ids)} records share name + birth year {year}: "
                      + ", ".join(f"`{pid}`" for pid in ids),
        })
    return findings
