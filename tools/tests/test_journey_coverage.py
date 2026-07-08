"""Tests for tools/journey_coverage.py."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from journey_coverage import build_minimal_journey, missing_journey_ids, seed_missing_journeys


def person(pid: str, name: str) -> dict:
    return {
        "id": pid,
        "name": {"full": name},
        "sex": "U",
        "vitals": {
            "birth": {
                "type": "birth",
                "date": {"raw": "1961", "year": 1961},
                "place": None,
                "confidence": "inferred",
            },
        },
        "relationships": {"parents": [], "children": [], "spouses": []},
        "events": [],
        "sources": [],
        "confidence": "inferred",
    }


def test_missing_journey_ids():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "people").mkdir()
        (root / "journeys").mkdir()
        (root / "people" / "I1.json").write_text("{}")
        (root / "people" / "I2.json").write_text("{}")
        (root / "journeys" / "I1.json").write_text("{}")
        assert missing_journey_ids(root) == ["I2"]


def test_seed_missing_creates_minimal_shell():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        people_dir = root / "people"
        journeys_dir = root / "journeys"
        people_dir.mkdir()
        journeys_dir.mkdir()
        payload = person("I9", "Bette Lyons")
        (people_dir / "I9.json").write_text(json.dumps(payload))

        placed, minimal, skipped = seed_missing_journeys(root)
        assert placed == 0
        assert minimal == 1
        assert skipped == 0

        journey = json.loads((journeys_dir / "I9.json").read_text())
        assert journey["status"] == "seeded"
        assert journey["waypoints"] == []
        assert journey["person"] == "Bette Lyons"


def test_build_minimal_journey_shape():
    journey = build_minimal_journey(person("I1", "Example Person"))
    assert journey["id"] == "I1"
    assert journey["waypoints"] == []
