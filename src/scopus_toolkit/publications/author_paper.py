"""Author-publication panel construction."""
from __future__ import annotations

from ..schemas import normalize_author_key, normalize_work_key


def build_author_paper_links(roster_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    seen: set[tuple[str, str]] = set()
    output = []
    for row in roster_rows:
        work_id = str(row.get("source_work_id", ""))
        author_id = str(row.get("source_author_id", ""))
        key = (normalize_author_key(author_id), normalize_work_key(work_id))
        duplicate = key in seen
        seen.add(key)
        output.append(
            {
                "source_author_id": author_id,
                "normalized_author_key": key[0],
                "source_work_id": work_id,
                "normalized_work_key": key[1],
                "author_position": row.get("author_position", ""),
                "duplicate_author_work_flag": str(duplicate).lower(),
                "qa_notes": "duplicate_author_work" if duplicate else "synthetic_author_work",
            }
        )
    return sorted(output, key=lambda r: (r["normalized_author_key"], r["normalized_work_key"], str(r["author_position"])))
