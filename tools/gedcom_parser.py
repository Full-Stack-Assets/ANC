"""Minimal GEDCOM 5.5.1 parser. Stdlib only, Python 3.9+.

Ancestry's tree export is plain GEDCOM: one node per line,
``LEVEL [@XREF@] TAG [VALUE]``, nested by level number. This module turns a
.ged file into a tree of Node objects and provides typed extractors for the
record kinds we care about (individuals, families, sources).

Deliberately not a full spec implementation — it handles what Ancestry
actually emits, and unknown tags pass through as generic nodes rather than
erroring.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterator, Optional

LINE_RE = re.compile(r"^(\d+)\s+(?:(@[^@]+@)\s+)?(\S+)(?:\s(.*))?$")

# GEDCOM event tags -> our lowercase event names. Anything else under an
# individual that carries a DATE or PLAC child is emitted as type "other".
EVENT_TAGS = {
    "BIRT": "birth",
    "DEAT": "death",
    "BURI": "burial",
    "CHR": "christening",
    "BAPM": "baptism",
    "RESI": "residence",
    "CENS": "census",
    "IMMI": "immigration",
    "EMIG": "emigration",
    "NATU": "naturalization",
    "OCCU": "occupation",
    "EDUC": "education",
    "RELI": "religion",
    "MILI": "military",
    "_MILT": "military",
    "EVEN": "other",
}

VITAL_TYPES = ("birth", "death", "burial")

DATE_QUALIFIERS = ("ABT", "EST", "CAL", "BEF", "AFT", "BET", "FROM")


@dataclass
class Node:
    level: int
    tag: str
    value: str = ""
    xref: Optional[str] = None
    children: list["Node"] = field(default_factory=list)

    def child(self, tag: str) -> Optional["Node"]:
        for c in self.children:
            if c.tag == tag:
                return c
        return None

    def all(self, tag: str) -> list["Node"]:
        return [c for c in self.children if c.tag == tag]

    def child_value(self, tag: str) -> Optional[str]:
        c = self.child(tag)
        return c.value if c is not None and c.value != "" else None


def _strip_xref(xref: Optional[str]) -> Optional[str]:
    if xref is None:
        return None
    return xref.strip("@")


def parse_lines(lines: Iterator[str]) -> list[Node]:
    """Parse GEDCOM lines into a list of level-0 records.

    CONC (concatenation, no separator) and CONT (continuation, newline) lines
    are folded into their parent node's value rather than kept as children.
    """
    roots: list[Node] = []
    stack: list[Node] = []
    for lineno, raw in enumerate(lines, 1):
        line = raw.lstrip("﻿").rstrip("\r\n")
        if not line.strip():
            continue
        m = LINE_RE.match(line.strip())
        if not m:
            raise ValueError(f"unparseable GEDCOM line {lineno}: {line!r}")
        level, xref, tag, value = int(m.group(1)), m.group(2), m.group(3), m.group(4) or ""

        if tag in ("CONC", "CONT"):
            if not stack:
                raise ValueError(f"{tag} with no preceding line at line {lineno}")
            target = stack[-1]
            target.value += value if tag == "CONC" else "\n" + value
            continue

        node = Node(level=level, tag=tag, value=value, xref=_strip_xref(xref))
        while stack and stack[-1].level >= level:
            stack.pop()
        if level == 0:
            roots.append(node)
        else:
            if not stack:
                raise ValueError(f"orphan level-{level} line at line {lineno}: {line!r}")
            stack[-1].children.append(node)
        stack.append(node)
    return roots


def parse_file(path: str) -> list[Node]:
    # Ancestry exports UTF-8 (sometimes with BOM); latin-1 fallback for old files.
    try:
        with open(path, encoding="utf-8-sig") as f:
            return parse_lines(iter(f))
    except UnicodeDecodeError:
        with open(path, encoding="latin-1") as f:
            return parse_lines(iter(f))


# ---------------------------------------------------------------------------
# Value parsing helpers
# ---------------------------------------------------------------------------

def parse_date(raw: Optional[str]) -> Optional[dict]:
    """Parse a GEDCOM DATE value into {raw, year, year_end, qualifier}.

    Keeps the verbatim string; extracts a best-effort year (range start for
    BET/FROM forms) and range end. Never raises on weird input.
    """
    if not raw:
        return None
    text = raw.strip()
    upper = text.upper()
    qualifier = next((q for q in DATE_QUALIFIERS if upper.startswith(q + " ")), None)
    years = [int(y) for y in re.findall(r"\b(\d{3,4})\b", upper)]
    year = years[0] if years else None
    year_end = years[1] if qualifier in ("BET", "FROM") and len(years) > 1 else None
    return {"raw": text, "year": year, "year_end": year_end, "qualifier": qualifier}


def parse_place(raw: Optional[str]) -> Optional[dict]:
    if not raw:
        return None
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    return {"raw": raw.strip(), "parts": parts}


def parse_citations(node: Node) -> list[dict]:
    """SOUR citations attached to an event or individual node."""
    citations = []
    for sour in node.all("SOUR"):
        citations.append(
            {"source_id": _strip_xref(sour.value.strip("@")) or sour.value, "page": sour.child_value("PAGE")}
        )
    return citations


def parse_event(node: Node, event_type: str) -> dict:
    date = parse_date(node.child_value("DATE"))
    place = parse_place(node.child_value("PLAC"))
    sources = parse_citations(node)
    note = node.child_value("NOTE")
    return {
        "type": event_type,
        "date": date,
        "place": place,
        "value": node.value or None,
        "note": note,
        "sources": sources,
        "confidence": "documented" if sources else "inferred",
    }


# ---------------------------------------------------------------------------
# Record extractors
# ---------------------------------------------------------------------------

def parse_name(indi: Node) -> dict:
    name_node = indi.child("NAME")
    given = surname = suffix = None
    full = ""
    if name_node is not None:
        raw = name_node.value
        m = re.match(r"^(?P<given>[^/]*?)\s*/(?P<surname>[^/]*)/\s*(?P<suffix>.*)$", raw)
        if m:
            given = m.group("given").strip() or None
            surname = m.group("surname").strip() or None
            suffix = m.group("suffix").strip() or None
        else:
            given = raw.strip() or None
        # Structured subrecords win over the value-line split when present.
        given = name_node.child_value("GIVN") or given
        surname = name_node.child_value("SURN") or surname
        suffix = name_node.child_value("NSFX") or suffix
        full = " ".join(p for p in (given, surname, suffix) if p)
    return {"given": given, "surname": surname, "suffix": suffix, "full": full or "(unknown)"}


def extract_individual(indi: Node) -> dict:
    """Individual record minus relationships (those need the FAM pass)."""
    vitals: dict = {}
    events: list[dict] = []
    for child in indi.children:
        event_type = EVENT_TAGS.get(child.tag)
        if event_type is None:
            continue
        ev = parse_event(child, event_type)
        if child.tag == "EVEN":
            ev["type"] = (child.child_value("TYPE") or "other").lower()
        if event_type in VITAL_TYPES and event_type not in vitals:
            vitals[event_type] = ev
        else:
            events.append(ev)

    sex = indi.child_value("SEX")
    notes = [n.value for n in indi.all("NOTE") if n.value]

    return {
        "id": indi.xref,
        "name": parse_name(indi),
        "sex": sex if sex in ("M", "F", "X", "U") else None,
        "vitals": vitals,
        "relationships": {"parents": [], "spouses": [], "children": []},
        "events": events,
        "sources": [],  # filled in by the emitter from top-level SOUR records
        "notes": notes,
        "confidence": "inferred",  # rolled up by the emitter
        "famc": [_strip_xref(n.value) for n in indi.all("FAMC")],
        "fams": [_strip_xref(n.value) for n in indi.all("FAMS")],
        "citations": parse_citations(indi),
    }


def extract_family(fam: Node) -> dict:
    marriage = None
    marr = fam.child("MARR")
    if marr is not None:
        marriage = parse_event(marr, "marriage")
    return {
        "id": fam.xref,
        "husband": _strip_xref(fam.child_value("HUSB")),
        "wife": _strip_xref(fam.child_value("WIFE")),
        "children": [_strip_xref(c.value) for c in fam.all("CHIL")],
        "marriage": marriage,
    }


def extract_source(sour: Node) -> dict:
    repo = sour.child("REPO")
    repository = None
    if repo is not None:
        repository = repo.child_value("NAME") or repo.value or None
    return {
        "id": sour.xref,
        "title": (sour.child_value("TITL") or "").replace("\n", " ").strip() or None,
        "author": sour.child_value("AUTH"),
        "publication": sour.child_value("PUBL"),
        "repository": repository,
    }


@dataclass
class Gedcom:
    individuals: dict[str, dict]
    families: dict[str, dict]
    sources: dict[str, dict]

    @classmethod
    def load(cls, path: str) -> "Gedcom":
        individuals: dict[str, dict] = {}
        families: dict[str, dict] = {}
        sources: dict[str, dict] = {}
        for record in parse_file(path):
            if record.tag == "INDI" and record.xref:
                individuals[record.xref] = extract_individual(record)
            elif record.tag == "FAM" and record.xref:
                families[record.xref] = extract_family(record)
            elif record.tag == "SOUR" and record.xref:
                sources[record.xref] = extract_source(record)
        cls._link_families(individuals, families)
        return cls(individuals=individuals, families=families, sources=sources)

    @staticmethod
    def _link_families(individuals: dict[str, dict], families: dict[str, dict]) -> None:
        for person in individuals.values():
            rel = person["relationships"]
            for fam_id in person.pop("famc"):
                fam = families.get(fam_id)
                if not fam:
                    continue
                for parent in (fam["husband"], fam["wife"]):
                    if parent and parent in individuals and parent not in rel["parents"]:
                        rel["parents"].append(parent)
            for fam_id in person.pop("fams"):
                fam = families.get(fam_id)
                if not fam:
                    continue
                partner = fam["wife"] if fam["husband"] == person["id"] else fam["husband"]
                if partner and partner in individuals:
                    spouse: dict = {"id": partner}
                    if fam["marriage"]:
                        spouse["marriage"] = fam["marriage"]
                    rel["spouses"].append(spouse)
                for child in fam["children"]:
                    if child and child in individuals and child not in rel["children"]:
                        rel["children"].append(child)
