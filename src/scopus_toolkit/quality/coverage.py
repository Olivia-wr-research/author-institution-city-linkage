"""Coverage and missingness summaries."""
from __future__ import annotations

from ..schemas import qa_row


def summarize_missing(rows: list[dict[str, str]], fields: list[str]) -> list[dict[str, object]]:
    total = len(rows)
    output = [qa_row("rows", total)]
    for field in fields:
        missing = sum(1 for row in rows if not str(row.get(field, "")).strip())
        output.append(qa_row(f"missing_{field}", missing, f"{missing}/{total}"))
    return output
