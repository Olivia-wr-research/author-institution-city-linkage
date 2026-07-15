"""Parsers for Scopus-style synthetic search and abstract fixtures."""
from __future__ import annotations

from ..schemas import missing_field_names, normalize_work_key


def parse_search_response(payload: dict[str, object]) -> list[dict[str, object]]:
    search = payload.get("search-results")
    if not isinstance(search, dict):
        return []
    entries = search.get("entry", [])
    if not isinstance(entries, list):
        return []
    rows = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        eid = str(entry.get("eid", ""))
        cover_date = str(entry.get("prism:coverDate", ""))
        year = cover_date[:4] if cover_date[:4].isdigit() else ""
        rows.append(
            {
                "source_work_id": eid,
                "normalized_work_key": normalize_work_key(eid),
                "title": str(entry.get("dc:title", "")),
                "publication_year": year,
                "document_type": str(entry.get("subtypeDescription", "")),
                "parser_status": "parsed" if eid else "missing_work_id",
            }
        )
    return rows


def parse_abstract_response(payload: dict[str, object]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    root = payload.get("abstracts-retrieval-response", payload)
    if not isinstance(root, dict):
        return [], []
    core = root.get("coredata", {}) if isinstance(root.get("coredata"), dict) else {}
    work_id = str(core.get("eid", root.get("eid", "")))
    authors = root.get("authors", {}).get("author", []) if isinstance(root.get("authors"), dict) else []
    if isinstance(authors, dict):
        authors = [authors]
    affiliations = root.get("affiliation", [])
    if isinstance(affiliations, dict):
        affiliations = [affiliations]
    aff_by_id = {str(a.get("@id", a.get("afid", ""))): a for a in affiliations if isinstance(a, dict)}
    roster = []
    links = []
    for pos, author in enumerate(authors, start=1):
        if not isinstance(author, dict):
            continue
        author_id = str(author.get("@auid", author.get("authid", "")))
        roster.append({"source_work_id": work_id, "source_author_id": author_id, "author_position": pos, "author_name": str(author.get("ce:indexed-name", ""))})
        refs = author.get("affiliation", [])
        if isinstance(refs, dict):
            refs = [refs]
        for ref_pos, ref in enumerate(refs, start=1):
            if not isinstance(ref, dict):
                continue
            afid = str(ref.get("@id", ref.get("afid", "")))
            aff = aff_by_id.get(afid, {})
            missing = missing_field_names(
                {
                    "source_work_id": work_id,
                    "source_author_id": author_id,
                    "source_institution_id": afid,
                    "city": str(aff.get("affiliation-city", "")),
                    "country": str(aff.get("affiliation-country", "")),
                },
                ["source_work_id", "source_author_id", "source_institution_id", "city", "country"],
            )
            links.append(
                {
                    "source_system": "scopus",
                    "source_work_id": work_id,
                    "source_author_id": author_id,
                    "source_institution_id": afid,
                    "institution_name": str(aff.get("affilname", "")),
                    "city": str(aff.get("affiliation-city", "")),
                    "country": str(aff.get("affiliation-country", "")),
                    "affiliation_position": ref_pos,
                    "missing_fields": ";".join(missing),
                    "parser_status": "parsed_with_missing_fields" if missing else "parsed",
                }
            )
    return roster, links
