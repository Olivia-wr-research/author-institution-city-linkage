"""Schema utilities. JSON files under data/expected_schema are authoritative."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable


class SchemaError(ValueError):
    """Raised when an input or output file does not satisfy the expected schema."""


def load_schema(schema_dir: Path, schema_name: str) -> dict[str, object]:
    path = schema_dir / schema_name
    data = json.loads(path.read_text(encoding="utf-8"))
    fields = data.get("required_fields")
    if not isinstance(fields, list) or not all(isinstance(field, str) for field in fields):
        raise SchemaError(f"{schema_name} must contain a string list named required_fields")
    return data


def schema_fields(schema_dir: Path, schema_name: str) -> list[str]:
    return list(load_schema(schema_dir, schema_name)["required_fields"])


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv_rows(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def validate_required_fields(path: Path, schema_dir: Path, schema_name: str) -> list[str]:
    required_fields = schema_fields(schema_dir, schema_name)
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
    missing = [field for field in required_fields if field not in fields]
    if missing:
        raise SchemaError(f"{path.name} missing required fields: {', '.join(missing)}")
    return fields


def validate_schema_files(schema_dir: Path) -> list[str]:
    checked = []
    for path in sorted(schema_dir.glob("*_schema.json")):
        load_schema(schema_dir, path.name)
        checked.append(path.name)
    if not checked:
        raise SchemaError("No schema files found")
    return checked
