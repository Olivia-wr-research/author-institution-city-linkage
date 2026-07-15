"""Subject-count export validation and merging."""
from __future__ import annotations

from ..exceptions import ToolkitError

REQUIRED_SUBJECT_FIELDS = ["city", "country", "period", "subject", "count"]


def validate_subject_counts(rows: list[dict[str, str]]) -> None:
    for idx, row in enumerate(rows, start=1):
        missing = [field for field in REQUIRED_SUBJECT_FIELDS if field not in row]
        if missing:
            raise ToolkitError(f"subject row {idx} missing fields: {', '.join(missing)}")
        int(row["count"])


def merge_subject_exports(exports: list[list[dict[str, str]]]) -> list[dict[str, str]]:
    rows = [row for export in exports for row in export]
    validate_subject_counts(rows)
    return sorted(rows, key=lambda r: (r["period"], r["city"], r["country"], r["subject"]))
