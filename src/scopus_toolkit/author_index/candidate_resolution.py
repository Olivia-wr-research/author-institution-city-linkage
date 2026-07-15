"""Author candidate normalization without automated real-person selection."""
from __future__ import annotations

from ..schemas import normalize_author_key


def normalize_candidates(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    output = []
    for row in rows:
        output.append(
            {
                "input_author_key": normalize_author_key(row.get("input_name", "")),
                "candidate_author_id": row.get("candidate_author_id", ""),
                "candidate_name": row.get("candidate_name", ""),
                "candidate_institution": row.get("candidate_institution", ""),
                "candidate_country": row.get("candidate_country", ""),
                "match_status": "candidate_only_not_verified",
            }
        )
    return sorted(output, key=lambda r: (r["input_author_key"], r["candidate_author_id"]))
