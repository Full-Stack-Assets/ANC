"""Tests for tools/audit_tree.py."""

from __future__ import annotations

from audit_tree import audit


def person(
    pid: str,
    name: str,
    *,
    sex: str = "M",
    birth: int | None = None,
    death: int | None = None,
    parents: list[str] | None = None,
    children: list[str] | None = None,
    spouses: list[dict] | None = None,
    events: list[dict] | None = None,
) -> dict:
    vitals: dict = {}
    if birth is not None:
        vitals["birth"] = {
            "type": "birth",
            "date": {"raw": str(birth), "year": birth},
            "confidence": "inferred",
        }
    if death is not None:
        vitals["death"] = {
            "type": "death",
            "date": {"raw": str(death), "year": death},
            "confidence": "inferred",
        }
    return {
        "id": pid,
        "name": {"full": name},
        "sex": sex,
        "vitals": vitals,
        "relationships": {
            "parents": parents or [],
            "children": children or [],
            "spouses": spouses or [],
        },
        "events": events or [],
        "sources": [],
        "confidence": "inferred",
    }


def kinds(findings: list[dict]) -> set[str]:
    return {finding["kind"] for finding in findings}


def test_death_before_birth():
    people = {"I1": person("I1", "Bad Dates", birth=1900, death=1890)}
    assert "death-before-birth" in kinds(audit(people))


def test_parent_too_young():
    people = {
        "P": person("P", "Parent", sex="F", birth=1900, children=["C"]),
        "C": person("C", "Child", birth=1905),
    }
    assert "parent-too-young" in kinds(audit(people))


def test_child_before_parent():
    people = {
        "P": person("P", "Parent", birth=1900, children=["C"]),
        "C": person("C", "Child", birth=1890),
    }
    assert "child-before-parent" in kinds(audit(people))


def test_child_after_death():
    people = {
        "P": person("P", "Parent", birth=1850, death=1880, children=["C"]),
        "C": person("C", "Child", birth=1890),
    }
    assert "child-after-death" in kinds(audit(people))


def test_anachronistic_place():
    people = {
        "I1": person(
            "I1",
            "Early Pennsylvanian",
            birth=1650,
            events=[{
                "type": "birth",
                "date": {"raw": "1650", "year": 1650},
                "place": {"raw": "Philadelphia, Pennsylvania"},
                "confidence": "inferred",
            }],
        ),
    }
    assert "anachronistic-place" in kinds(audit(people))


def test_duplicate_person_detection():
    people = {
        "I1": person("I1", "John Smith", birth=1800),
        "I2": person("I2", "John Smith", birth=1800),
        "M0001": person("M0001", "Manual Person", birth=1800),
    }
    dupes = [f for f in audit(people) if f["kind"] == "duplicate-person"]
    assert len(dupes) == 1
    assert "`I1`" in dupes[0]["detail"]
    assert "`I2`" in dupes[0]["detail"]
    assert "M0001" not in dupes[0]["detail"]
