#!/usr/bin/env python3
"""Tests for the GEDCOM parser and emitter.

Run directly (`python3 tools/tests/test_parser.py`) or under pytest.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from gedcom_parser import Gedcom, parse_date  # noqa: E402
from gedcom_to_people import main as emit  # noqa: E402

FIXTURE = str(Path(__file__).with_name("fixture.ged"))
REPO = TOOLS.parent


def load() -> Gedcom:
    return Gedcom.load(FIXTURE)


def test_individuals_and_linking():
    ged = load()
    assert set(ged.individuals) == {"I1", "I2", "I3"}

    i1 = ged.individuals["I1"]
    assert i1["name"] == {"given": "Giuseppe", "surname": "Marciano", "suffix": "Sr",
                          "full": "Giuseppe Marciano Sr"}
    assert i1["sex"] == "M"
    assert i1["relationships"]["spouses"][0]["id"] == "I2"
    assert i1["relationships"]["spouses"][0]["marriage"]["place"]["parts"][0] == "New York"
    assert i1["relationships"]["children"] == ["I3"]
    assert ged.individuals["I3"]["relationships"]["parents"] == ["I1", "I2"]


def test_dates():
    assert parse_date("ABT 1848") == {"raw": "ABT 1848", "year": 1848, "year_end": None,
                                      "qualifier": "ABT"}
    assert parse_date("BET 1910 AND 1915") == {"raw": "BET 1910 AND 1915", "year": 1910,
                                               "year_end": 1915, "qualifier": "BET"}
    assert parse_date("12 MAY 1869")["year"] == 1869
    assert parse_date(None) is None


def test_conc_cont_note():
    note = load().individuals["I1"]["notes"][0]
    assert note == ("Family story: he jumped ship in Boston harbor rather than\n"
                    "returning to Naples.")


def test_event_confidence_and_sources():
    i1 = load().individuals["I1"]
    immi = next(ev for ev in i1["events"] if ev["type"] == "immigration")
    assert immi["confidence"] == "documented"
    assert immi["sources"] == [{"source_id": "S2", "page": "Line 14, SS Europa manifest"}]
    assert i1["vitals"]["death"]["confidence"] == "inferred"
    occu = next(ev for ev in i1["events"] if ev["type"] == "occupation")
    assert occu["value"] == "Stonemason"


def test_emitter_end_to_end():
    with tempfile.TemporaryDirectory() as tmp:
        assert emit([FIXTURE, "--out", tmp, "--seed-journeys"]) == 0

        p1 = json.loads(Path(tmp, "people", "I1.json").read_text())
        assert p1["confidence"] == "documented"
        assert {s["id"] for s in p1["sources"]} == {"S1", "S2"}
        assert p1["sources"][0]["title"] is not None

        # The sourced marriage comes from the family record, so it documents
        # both spouses — but the wholly uncited child stays inferred.
        p2 = json.loads(Path(tmp, "people", "I2.json").read_text())
        assert p2["confidence"] == "documented"
        p3 = json.loads(Path(tmp, "people", "I3.json").read_text())
        assert p3["confidence"] == "inferred"

        # Journey seed: waypoints ordered along the life, marriage included,
        # undated-year death (BET range -> 1910) still lands last.
        j1 = json.loads(Path(tmp, "journeys", "I1.json").read_text())
        assert j1["status"] == "seeded"
        assert [w["event"] for w in j1["waypoints"]] == [
            "birth", "immigration", "marriage", "residence", "death"]
        assert [w["seq"] for w in j1["waypoints"]] == [1, 2, 3, 4, 5]
        assert j1["waypoints"][0]["place"]["parts"] == ["Naples", "Campania", "Italy"]

        # Re-run: manual block in a person file survives, journeys untouched.
        p1["manual"] = {"notes": ["hand-written"], "confidence_override": "legend"}
        Path(tmp, "people", "I1.json").write_text(json.dumps(p1))
        j1["status"] = "transcribed"
        Path(tmp, "journeys", "I1.json").write_text(json.dumps(j1))

        assert emit([FIXTURE, "--out", tmp, "--seed-journeys"]) == 0
        p1_again = json.loads(Path(tmp, "people", "I1.json").read_text())
        assert p1_again["manual"] == {"notes": ["hand-written"], "confidence_override": "legend"}
        assert json.loads(Path(tmp, "journeys", "I1.json").read_text())["status"] == "transcribed"


DUPES_GED = """\
0 HEAD
1 CHAR UTF-8
0 @S1@ SOUR
1 TITL Parish register
0 @I9@ INDI
1 NAME Robert /Smyth/
1 BIRT
2 DATE 1590
2 PLAC Kirton, Lincolnshire, England
1 BIRT
2 DATE 1590
2 PLAC Kirton, Lincolnshire, England
2 SOUR @S1@
1 BIRT
2 DATE 1595
2 PLAC Kelstern, Lincolnshire, England
1 RESI
2 DATE 1620
2 PLAC Boston, Lincolnshire, England
1 RESI
2 DATE 1620
2 PLAC Boston, Lincolnshire, England
0 TRLR
"""


def test_ancestry_duplicate_events_collapse():
    """Merged Ancestry hints repeat events; dupes collapse, sources merge,
    and alternate vitals never become journey waypoints."""
    with tempfile.TemporaryDirectory() as tmp:
        ged = Path(tmp, "dupes.ged")
        ged.write_text(DUPES_GED)
        assert emit([str(ged), "--out", tmp, "--seed-journeys"]) == 0

        p = json.loads(Path(tmp, "people", "I9.json").read_text())
        # Preferred birth keeps its slot and absorbs the duplicate's citation.
        assert p["vitals"]["birth"]["date"]["year"] == 1590
        assert p["vitals"]["birth"]["sources"] == [{"source_id": "S1", "page": None}]
        assert p["vitals"]["birth"]["confidence"] == "documented"
        # The genuinely different 1595 birth survives as an alternate event;
        # the identical residence pair collapses to one.
        assert [(_ev["type"], (_ev["date"] or {}).get("year")) for _ev in p["events"]] == [
            ("birth", 1595), ("residence", 1620)]

        j = json.loads(Path(tmp, "journeys", "I9.json").read_text())
        assert [(w["event"], (w["date"] or {}).get("year")) for w in j["waypoints"]] == [
            ("birth", 1590), ("residence", 1620)]


def test_schema_validation():
    """Validate emitter output against the repo schemas (skips without jsonschema)."""
    try:
        import jsonschema
    except ImportError:
        print("  (jsonschema not installed — schema validation skipped)")
        return
    person_schema = json.loads((REPO / "schema" / "person.schema.json").read_text())
    journey_schema = json.loads((REPO / "schema" / "journey.schema.json").read_text())
    with tempfile.TemporaryDirectory() as tmp:
        emit([FIXTURE, "--out", tmp, "--seed-journeys"])
        for f in Path(tmp, "people").glob("*.json"):
            jsonschema.validate(json.loads(f.read_text()), person_schema)
        for f in Path(tmp, "journeys").glob("*.json"):
            jsonschema.validate(json.loads(f.read_text()), journey_schema)


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"ok   {name}")
            except AssertionError as e:
                failures += 1
                print(f"FAIL {name}: {e}")
    sys.exit(1 if failures else 0)
