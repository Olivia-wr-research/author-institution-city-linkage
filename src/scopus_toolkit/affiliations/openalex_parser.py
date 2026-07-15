"""OpenAlex-style parser used only for offline source comparison."""
from __future__ import annotations

from ..schemas import normalize_author_key, normalize_work_key
from .normalization import normalize_city_country, normalize_institution_name


def parse_openalex_work(payload: dict[str, object]) -> list[dict[str, object]]:
    work_id = str(payload.get("id", ""))
    rows = []
    authorships = payload.get("authorships", [])
    if not isinstance(authorships, list):
        return rows
    for pos, authorship in enumerate(authorships, start=1):
        if not isinstance(authorship, dict):
            continue
        author = authorship.get("author", {}) if isinstance(authorship.get("author"), dict) else {}
        institutions = authorship.get("institutions", [])
        if not institutions:
            institutions = [{}]
        for inst_pos, inst in enumerate(institutions, start=1):
            if not isinstance(inst, dict):
                continue
            geo = inst.get("geo", {}) if isinstance(inst.get("geo"), dict) else {}
            rows.append(
                {
                    "source_system": "openalex",
                    "source_work_id": work_id,
                    "normalized_work_key": normalize_work_key(work_id),
                    "source_author_id": str(author.get("id", "")),
                    "normalized_author_key": normalize_author_key(author.get("id", author.get("display_name", ""))),
                    "source_institution_id": str(inst.get("id", "")),
                    "normalized_institution_key": normalize_institution_name(str(inst.get("display_name", ""))),
                    "institution_name": str(inst.get("display_name", "")),
                    "city": str(geo.get("city", "")),
                    "country": str(geo.get("country", "")),
                    "city_country_key": normalize_city_country(str(geo.get("city", "")), str(geo.get("country", ""))),
                    "affiliation_position": inst_pos,
                    "multi_affiliation_flag": str(len(institutions) > 1).lower(),
                    "parser_status": "parsed",
                    "missing_fields": "",
                    "qa_notes": "offline_source_comparison_only",
                }
            )
    return rows
