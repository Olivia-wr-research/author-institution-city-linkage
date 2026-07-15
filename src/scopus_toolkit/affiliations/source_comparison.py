"""Offline Scopus-OpenAlex source comparison."""
from __future__ import annotations


VALID_STATUSES = {
    "agreement",
    "partial_agreement",
    "scopus_only",
    "openalex_only",
    "institution_conflict",
    "geography_conflict",
    "insufficient_information",
}


def compare_sources(scopus_rows: list[dict[str, object]], openalex_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    def key(row: dict[str, object]) -> tuple[str, str]:
        return (str(row.get("normalized_work_key", "")), str(row.get("normalized_author_key", "")))

    s_map: dict[tuple[str, str], list[dict[str, object]]] = {}
    o_map: dict[tuple[str, str], list[dict[str, object]]] = {}
    for row in scopus_rows:
        s_map.setdefault(key(row), []).append(row)
    for row in openalex_rows:
        o_map.setdefault(key(row), []).append(row)
    output = []
    for pair in sorted(set(s_map) | set(o_map)):
        s_rows = s_map.get(pair, [])
        o_rows = o_map.get(pair, [])
        status = "agreement"
        if not s_rows:
            status = "openalex_only"
        elif not o_rows:
            status = "scopus_only"
        else:
            s_inst = {str(r.get("normalized_institution_key", "")) for r in s_rows if r.get("normalized_institution_key")}
            o_inst = {str(r.get("normalized_institution_key", "")) for r in o_rows if r.get("normalized_institution_key")}
            s_geo = {str(r.get("city_country_key", "")) for r in s_rows if r.get("city_country_key")}
            o_geo = {str(r.get("city_country_key", "")) for r in o_rows if r.get("city_country_key")}
            if not s_inst or not o_inst:
                status = "insufficient_information"
            elif s_inst == o_inst and s_geo == o_geo:
                status = "agreement"
            elif s_inst & o_inst:
                status = "partial_agreement" if s_geo & o_geo else "geography_conflict"
            else:
                status = "institution_conflict"
        output.append(
            {
                "normalized_work_key": pair[0],
                "normalized_author_key": pair[1],
                "scopus_records": len(s_rows),
                "openalex_records": len(o_rows),
                "comparison_status": status,
                "qa_notes": "agreement_is_field_level_not_truth" if status == "agreement" else "offline_source_difference",
            }
        )
    return output
