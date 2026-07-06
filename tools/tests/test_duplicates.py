"""Tests for tools/duplicates.py resolution loading."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from duplicates import (
    _group_is_resolved,
    duplicate_person_findings,
    find_duplicate_clusters,
    load_duplicate_resolutions,
)


def test_load_duplicate_resolutions():
    resolutions = load_duplicate_resolutions()
    assert resolutions["I182197730733"] == "I182197731994"
    assert resolutions["I182197730682"] == "I182197732094"


def test_resolved_duplicate_group_suppressed():
    people = {
        "A": {"name": {"full": "John Albertson"}, "vitals": {"birth": {"date": {"year": 1771}}}},
        "B": {"name": {"full": "John Albertson"}, "vitals": {"birth": {"date": {"year": 1771}}}},
    }
    resolutions = {"A": "B"}
    assert _group_is_resolved(["A", "B"], resolutions)
    assert duplicate_person_findings(people, resolutions=resolutions) == []


def test_find_duplicate_clusters_manual_resolution(tmp_path: Path):
    resolutions_path = tmp_path / "duplicate_resolutions.json"
    resolutions_path.write_text(json.dumps({
        "DUP": {"canonical": "CANON", "basis": "test", "resolved": "2026-07-06"},
    }))
    people = {
        "DUP": {"name": {"full": "Test Person"}, "vitals": {"birth": {"date": {"year": 1800}}}},
        "CANON": {"name": {"full": "Test Person"}, "vitals": {"birth": {"date": {"year": 1800}}}},
    }
    loaded = json.loads(resolutions_path.read_text())
    resolutions = {dup: entry["canonical"] for dup, entry in loaded.items()}
    clusters = find_duplicate_clusters(people, {"DUP", "CANON"}, resolutions)
    manual = [c for c in clusters if c["basis"] == "manual-research"]
    assert len(manual) == 1
    assert manual[0]["canonical_id"] == "CANON"
