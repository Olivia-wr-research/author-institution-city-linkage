"""Scopus-style author-affiliation normalization."""
from __future__ import annotations

from ..schemas import normalize_author_key, normalize_work_key
from .normalization import normalize_city_country, normalize_institution_name


def normalize_scopus_links(raw_links: list[dict[str, object]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, str], int] = {}
    for row in raw_links:
        key = (str(row.get("source_work_id", "")), str(row.get("source_author_id", "")))
        groups[key] = groups.get(key, 0) + 1
    seen: set[tuple[str, str, str]] = set()
    output = []
    for row in raw_links:
        work_id = str(row.get("source_work_id", ""))
        author_id = str(row.get("source_author_id", ""))
        inst_id = str(row.get("source_institution_id", ""))
        key = (work_id, author_id, inst_id)
        duplicate = key in seen
        seen.add(key)
        notes = []
        if duplicate:
            notes.append("duplicate_author_institution_link")
        if not author_id:
            notes.append("missing_author_id")
        if not inst_id:
            notes.append("missing_institution_id")
        output.append(
            {
                "source_system": "scopus",
                "source_work_id": work_id,
                "normalized_work_key": normalize_work_key(work_id),
                "source_author_id": author_id,
                "normalized_author_key": normalize_author_key(author_id or row.get("author_name", "")),
                "source_institution_id": inst_id,
                "normalized_institution_key": normalize_institution_name(str(row.get("institution_name", inst_id))),
                "institution_name": row.get("institution_name", ""),
                "city": row.get("city", ""),
                "country": row.get("country", ""),
                "city_country_key": normalize_city_country(str(row.get("city", "")), str(row.get("country", ""))),
                "affiliation_position": row.get("affiliation_position", ""),
                "multi_affiliation_flag": str(groups[(work_id, author_id)] > 1).lower(),
                "parser_status": row.get("parser_status", "parsed"),
                "missing_fields": row.get("missing_fields", ""),
                "qa_notes": ";".join(notes) or "paper_affiliation_not_employment",
            }
        )
    return sorted(output, key=lambda r: (r["source_work_id"], r["source_author_id"], str(r["affiliation_position"]), r["source_institution_id"]))
