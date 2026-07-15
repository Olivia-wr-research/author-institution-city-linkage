"""Shared schemas and lightweight CSV/JSON helpers."""
from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from .exceptions import ToolkitError

FIXED_RUN_ID = "SYNTHETIC_RUN_2026_07_15"


@dataclass(frozen=True)
class AuthorInstitutionLink:
    source_system: str
    source_work_id: str
    normalized_work_key: str
    source_author_id: str
    normalized_author_key: str
    source_institution_id: str
    normalized_institution_key: str
    institution_name: str
    city: str
    country: str
    affiliation_position: str
    multi_affiliation_flag: str
    parser_status: str
    missing_fields: str
    qa_notes: str


@dataclass
class RequestTask:
    task_id: str
    query: str
    status: str = "pending"
    attempts: int = 0
    checkpoint: str = ""
    error: str = ""


def normalize_key(value: object) -> str:
    text = "" if value is None else str(value)
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def normalize_work_key(value: object) -> str:
    return normalize_key(str(value).replace("2-s2.0-", ""))


def normalize_author_key(value: object) -> str:
    return normalize_key(value)


def require_fields(row: dict[str, str], fields: Iterable[str], label: str = "row") -> None:
    missing = [field for field in fields if field not in row]
    if missing:
        raise ToolkitError(f"{label} missing fields: {', '.join(missing)}")


def missing_field_names(row: dict[str, str], fields: Iterable[str]) -> list[str]:
    return [field for field in fields if not str(row.get(field, "")).strip()]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sorted_rows(rows: Iterable[dict[str, object]], keys: list[str]) -> list[dict[str, object]]:
    return sorted(rows, key=lambda row: tuple(str(row.get(key, "")) for key in keys))


def qa_row(metric: str, value: object, notes: str = "") -> dict[str, object]:
    return {"metric": metric, "value": value, "notes": notes}
