"""Shared helpers for loading person records from data/people/."""

from __future__ import annotations

import json
from pathlib import Path


def load_people(data_dir: Path) -> dict[str, dict]:
    people: dict[str, dict] = {}
    for path in (data_dir / "people").glob("*.json"):
        people[path.stem] = json.loads(path.read_text(encoding="utf-8"))
    return people
