"""Shared duplicate-person detection heuristics."""

from __future__ import annotations

import re

# Pairs already confirmed as the same person during hand research this
# project — not re-derived by the name+birth-year heuristic, just recorded.
KNOWN_DUPLICATES = {
    "I182197730733": "I182197731994",  # John Albertson (Find-a-Grave copy -> primary)
    "I182197730682": "I182197732094",  # Ann Pine (Find-a-Grave copy -> primary)
}


def normalize_name(name: str) -> str:
    return " ".join(re.sub(r"[^a-z ]", "", name.lower()).split())


def birth_year(person: dict) -> int | None:
    return ((person.get("vitals", {}).get("birth") or {}).get("date") or {}).get("year")


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


def find_duplicate_clusters(
    people: dict[str, dict],
    scope_ids: set[str],
    known_duplicates: dict[str, str] | None = None,
) -> list[dict]:
    """Return duplicate clusters for game-bundle export."""
    known = KNOWN_DUPLICATES if known_duplicates is None else known_duplicates
    groups = group_by_name_and_birth_year(people, scope_ids)
    clusters: list[dict] = []
    covered: set[str] = set()

    for ids in groups.values():
        if len(ids) <= 1:
            continue
        canonical = ids[0]
        for pid in ids:
            if pid in known:
                canonical = known[pid]
                break
        dup_ids = [pid for pid in ids if pid != canonical]
        clusters.append({
            "canonical_id": canonical,
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
) -> list[dict]:
    """Return audit-style findings for unmerged duplicate candidates."""
    groups = group_by_name_and_birth_year(people, scope_ids)
    findings: list[dict] = []
    for (_, year), ids in sorted(groups.items()):
        if len(ids) <= 1:
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
