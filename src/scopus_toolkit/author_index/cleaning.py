"""Synthetic author input validation and normalization."""
from __future__ import annotations

import re

from ..exceptions import ToolkitError
from ..schemas import normalize_author_key, require_fields


AUTHOR_FIELDS = ["author_id", "display_name", "home_country"]


def validate_author_rows(rows: list[dict[str, str]]) -> None:
    for index, row in enumerate(rows, start=1):
        require_fields(row, AUTHOR_FIELDS, f"author row {index}")


def scopus_author_id_status(value: str) -> str:
    if not value.strip():
        return "missing"
    if re.fullmatch(r"SYNTH_AUTHOR_\d{3}", value.strip()):
        return "synthetic_valid"
    raise ToolkitError("Public fixtures must use SYNTH_AUTHOR_### identifiers.")


def normalize_author_records(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    validate_author_rows(rows)
    output = []
    seen: set[str] = set()
    for row in rows:
        status = scopus_author_id_status(row.get("author_id", ""))
        key = normalize_author_key(row["author_id"] or row["display_name"])
        duplicate = key in seen
        seen.add(key)
        output.append(
            {
                "source_author_id": row.get("author_id", ""),
                "normalized_author_key": key,
                "display_name": row.get("display_name", ""),
                "home_country": row.get("home_country", ""),
                "author_id_status": status,
                "duplicate_author_flag": str(duplicate).lower(),
                "qa_notes": "synthetic_author_record",
            }
        )
    return output
