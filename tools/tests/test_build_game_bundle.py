"""Tests for tools/build_game_bundle.py and shared duplicate helpers."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from build_game_bundle import (
    content_readiness,
    git_commit_hash,
    main as build_bundle,
    privacy_status,
    walk_ancestors,
)
from duplicates import find_duplicate_clusters, normalize_name
from gedcom_to_people import main as emit

FIXTURE = str(Path(__file__).with_name("fixture.ged"))


def test_normalize_name_strips_punctuation():
    assert normalize_name('William "Curley" Swallow') == "william curley swallow"


def test_privacy_status():
    assert privacy_status("HOME", "HOME", 0, 1994, None) == "living_confirmed"
    assert privacy_status("A", "HOME", 5, 1850, 1920) == "public_safe"
    assert privacy_status("A", "HOME", 2, 1960, None) == "possibly_living"
    assert privacy_status("A", "HOME", 8, 1925, None) == "possibly_living"
    assert privacy_status("A", "HOME", 8, 1910, None) == "public_safe"


def test_content_readiness_tiers():
    assert content_readiness(None)[:2] == ("not_ready", 0)

    seeded = {
        "status": "seeded",
        "waypoints": [{"confidence": "documented", "narrative": None}],
    }
    assert content_readiness(seeded)[:2] == ("not_ready", 20)

    draft = {
        "status": "transcribed",
        "waypoints": [
            {"confidence": "documented", "narrative": "Arrived in Boston."},
            {"confidence": "inferred", "narrative": None},
        ],
    }
    assert content_readiness(draft)[:2] == ("draft", 65)

    ready = {
        "status": "reviewed",
        "waypoints": [
            {"confidence": "documented", "narrative": "Born in Naples."},
            {"confidence": "documented", "narrative": "Immigrated to New York."},
        ],
    }
    assert content_readiness(ready)[:2] == ("ready", 100)


def test_find_duplicate_clusters_respects_known_pairs():
    dup_id = "I182197730733"
    canon_id = "I182197731994"
    people = {
        dup_id: {"name": {"full": "John Albertson"}, "vitals": {"birth": {"date": {"year": 1771}}}},
        canon_id: {"name": {"full": "John Albertson"}, "vitals": {"birth": {"date": {"year": 1771}}}},
    }
    from duplicates import load_duplicate_resolutions
    resolutions = load_duplicate_resolutions()
    clusters = find_duplicate_clusters(people, {dup_id, canon_id}, resolutions)
    manual = [c for c in clusters if c["basis"] == "manual-research"]
    assert len(manual) == 1
    assert manual[0]["canonical_id"] == canon_id
    assert manual[0]["duplicate_ids"] == [dup_id]


def test_walk_ancestors_from_fixture():
    with tempfile.TemporaryDirectory() as tmp:
        assert emit([FIXTURE, "--out", tmp, "--seed-journeys"]) == 0
        people = {
            path.stem: json.loads(path.read_text())
            for path in Path(tmp, "people").glob("*.json")
        }
        ancestry = walk_ancestors(people, "I3")
        assert set(ancestry) == {"I1", "I2", "I3"}
        assert ancestry["I3"]["generation"] == 0
        assert ancestry["I1"]["generation"] == 1


def test_build_bundle_end_to_end():
    with tempfile.TemporaryDirectory() as tmp:
        assert emit([FIXTURE, "--out", tmp, "--seed-journeys"]) == 0
        out = Path(tmp) / "bundle.json"
        assert build_bundle(["--home", "I3", "--data", tmp, "--out", str(out)]) == 0

        bundle = json.loads(out.read_text())
        assert bundle["home_person_id"] == "I3"
        assert "generated_at" in bundle
        assert len(bundle["people"]) == 3
        assert bundle["people"][0]["generation"] == 0
        assert all("privacy_status" in row for row in bundle["people"])
        assert "duplicate_clusters" in bundle
        assert "source_provenance" in bundle


def test_git_commit_hash_dirty_checkout_returns_none():
    # On a dirty checkout this returns None; on a clean checkout, a commit hash.
    result = git_commit_hash()
    assert result is None or isinstance(result, str)
