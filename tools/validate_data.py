#!/usr/bin/env python3
"""Validate data/people/ and data/journeys/ JSON against repo schemas.

Usage:
    python3 tools/validate_data.py [--data data]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent


def load_schema(name: str) -> dict:
    return json.loads((ROOT / "schema" / f"{name}.schema.json").read_text(encoding="utf-8"))


def validate_dir(
    data_dir: Path,
    subdir: str,
    glob: str,
    schema: dict,
    label: str,
) -> list[tuple[Path, str]]:
    errors: list[tuple[Path, str]] = []
    target = data_dir / subdir
    if not target.is_dir():
        raise SystemExit(f"missing directory: {target}")

    for path in sorted(target.glob(glob)):
        try:
            instance = json.loads(path.read_text(encoding="utf-8"))
            jsonschema.validate(instance, schema)
        except json.JSONDecodeError as exc:
            errors.append((path, f"invalid JSON: {exc}"))
        except jsonschema.ValidationError as exc:
            errors.append((path, exc.message))
    return errors


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", default=str(ROOT / "data"), help="ANC data/ directory")
    args = ap.parse_args(argv)

    data_dir = Path(args.data)
    person_schema = load_schema("person")
    journey_schema = load_schema("journey")

    errors: list[tuple[Path, str]] = []
    errors.extend(validate_dir(data_dir, "people", "I*.json", person_schema, "person"))
    errors.extend(validate_dir(data_dir, "journeys", "*.json", journey_schema, "journey"))

    people_count = len(list((data_dir / "people").glob("I*.json")))
    journey_count = len(list((data_dir / "journeys").glob("*.json")))

    if errors:
        print(f"schema validation failed: {len(errors)} error(s)", file=sys.stderr)
        for path, message in errors[:50]:
            print(f"  {path}: {message}", file=sys.stderr)
        if len(errors) > 50:
            print(f"  ... and {len(errors) - 50} more", file=sys.stderr)
        return 1

    print(f"ok  {people_count} people, {journey_count} journeys")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
