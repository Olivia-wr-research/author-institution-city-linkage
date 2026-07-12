"""Author-work-institution-city linkage for the synthetic public demonstration."""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

from src.config.settings import PipelineConfig
from src.geocoding.geocode_cache import geocoding_valid, institution_city_key
from src.linkage.aliases import enrich_alias_rows
from src.linkage.schema import read_csv_rows, schema_fields, validate_required_fields, write_csv_rows
from src.utilities.text_cleaning import as_bool, is_blank, normalize_text


def standardize_match_status(value: object) -> str:
    text = normalize_text(value)
    if text in {"matched", "exact", "id matched", "confirmed"}:
        return "matched"
    if text in {"missing institution", "missing institution id"}:
        return "missing_institution_id"
    if not text:
        return "unknown"
    return text.replace(" ", "_")


def _confidence(row: dict[str, str]) -> float:
    try:
        return float(row.get("confidence_score", ""))
    except ValueError:
        return 0.0


def _duplicate_counts(rows: list[dict[str, str]]) -> Counter[tuple[str, str, str]]:
    keys = []
    for row in rows:
        key = (row.get("author_id", ""), row.get("work_id", ""), row.get("institution_id", ""))
        if all(key):
            keys.append(key)
    return Counter(keys)


def _source_conflicts(source_rows: list[dict[str, str]]) -> dict[str, bool]:
    return {row.get("record_id", ""): as_bool(row.get("expected_conflict_flag")) for row in source_rows}


def _multi_affiliations(rows: list[dict[str, str]]) -> set[tuple[str, str]]:
    institutions_by_author_work: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in rows:
        author_id, work_id, institution_id = row.get("author_id", ""), row.get("work_id", ""), row.get("institution_id", "")
        if author_id and work_id and institution_id:
            institutions_by_author_work[(author_id, work_id)].add(institution_id)
    return {key for key, values in institutions_by_author_work.items() if len(values) > 1}


def _qa_status(linkage_valid: bool, geocode_ok: bool, low_confidence: bool, source_conflict: bool, duplicate_excluded: bool, exclusion_reason: str) -> str:
    if duplicate_excluded:
        return "duplicate_excluded"
    if exclusion_reason:
        return "linkage_failed"
    if low_confidence:
        return "low_confidence"
    if source_conflict:
        return "source_conflict"
    if linkage_valid and not geocode_ok:
        return "linkage_valid_geocoding_incomplete"
    if linkage_valid and geocode_ok:
        return "ready_for_demo_analysis"
    return "review_needed"


def process_records(
    author_links: list[dict[str, str]],
    works: list[dict[str, str]],
    institutions: list[dict[str, str]],
    source_comparison: list[dict[str, str]],
    config: PipelineConfig,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    """Process synthetic records and return linked rows, exclusions, and audit rows."""
    work_by_id = {row["work_id"]: row for row in works if row.get("work_id")}
    inst_by_id = {row["institution_id"]: row for row in institutions if row.get("institution_id")}
    dup_counts = _duplicate_counts(author_links)
    seen_keys: set[tuple[str, str, str]] = set()
    conflict_by_record = _source_conflicts(source_comparison)
    multi_keys = _multi_affiliations(author_links)
    linked: list[dict[str, object]] = []
    excluded: list[dict[str, object]] = []
    audit: list[dict[str, object]] = []

    for row in author_links:
        record_id = row.get("record_id", "")
        author_id = row.get("author_id", "")
        work_id = row.get("work_id", "")
        institution_id = row.get("institution_id", "")
        key = (author_id, work_id, institution_id)
        duplicate_flag = bool(all(key) and dup_counts[key] > 1)
        duplicate_excluded = bool(config.deduplicate_records and duplicate_flag and key in seen_keys)
        if all(key):
            seen_keys.add(key)
        source_conflict = bool(conflict_by_record.get(record_id, False))
        multi_affiliation = (author_id, work_id) in multi_keys
        confidence = _confidence(row)
        low_confidence = confidence < config.minimum_confidence_score
        exclusion_reason = ""
        qa_notes: list[str] = []
        work = work_by_id.get(work_id)
        inst = inst_by_id.get(institution_id)

        if is_blank(author_id):
            exclusion_reason = "missing_author_id"
        elif is_blank(work_id):
            exclusion_reason = "missing_work_id"
        elif is_blank(institution_id):
            exclusion_reason = "missing_institution_id"
        elif work is None:
            exclusion_reason = "work_not_found"
        elif inst is None:
            exclusion_reason = "institution_not_found"
        elif duplicate_excluded:
            exclusion_reason = "duplicate_record"

        linkage_valid = not exclusion_reason and not low_confidence
        geocode_ok = False
        geocode_note = "not_geocoded_due_to_linkage_failure"
        city_country_key = ""
        if inst is not None and not is_blank(institution_id):
            geocode_ok, geocode_note = geocoding_valid(inst, config.require_valid_coordinates)
            city_country_key = institution_city_key(inst)
        if low_confidence:
            qa_notes.append("confidence_below_threshold")
        if source_conflict:
            qa_notes.append("source_city_or_country_conflict")
        if duplicate_flag:
            qa_notes.append("duplicate_author_work_institution_key")
        if multi_affiliation:
            qa_notes.append("author_has_multiple_institutions_on_same_work")
        if geocode_note != "geocoding_valid":
            qa_notes.append(geocode_note)
        if exclusion_reason:
            qa_notes.append(exclusion_reason)

        status = _qa_status(linkage_valid, geocode_ok, low_confidence, source_conflict, duplicate_excluded, exclusion_reason)
        audit_row = {
            "record_id": record_id,
            "author_id": author_id,
            "work_id": work_id,
            "institution_id": institution_id,
            "source": row.get("source", ""),
            "confidence_score": row.get("confidence_score", ""),
            "linkage_valid": str(linkage_valid).lower(),
            "geocoding_valid": str(geocode_ok).lower(),
            "duplicate_flag": str(duplicate_flag).lower(),
            "duplicate_excluded": str(duplicate_excluded).lower(),
            "source_conflict_flag": str(source_conflict).lower(),
            "multi_affiliation_flag": str(multi_affiliation).lower(),
            "qa_status": status,
            "qa_notes": ";".join(dict.fromkeys(qa_notes)),
            "exclusion_reason": exclusion_reason,
        }
        audit.append(audit_row)

        if exclusion_reason:
            excluded.append({
                "record_id": record_id,
                "author_id": author_id,
                "work_id": work_id,
                "institution_id": institution_id,
                "exclusion_reason": exclusion_reason,
                "qa_notes": audit_row["qa_notes"],
            })
            continue
        if work is None or inst is None:
            continue
        linked.append({
            "record_id": record_id,
            "author_id": author_id,
            "work_id": work_id,
            "publication_year": work.get("publication_year", ""),
            "institution_id": institution_id,
            "institution_name": inst.get("institution_name", ""),
            "city": inst.get("city", ""),
            "country": inst.get("country", ""),
            "city_country_key": city_country_key,
            "latitude": inst.get("latitude", ""),
            "longitude": inst.get("longitude", ""),
            "source": row.get("source", ""),
            "match_status_standardized": standardize_match_status(row.get("match_status", "")),
            "confidence_score": row.get("confidence_score", ""),
            "linkage_valid": str(linkage_valid).lower(),
            "geocoding_valid": str(geocode_ok).lower(),
            "duplicate_flag": str(duplicate_flag).lower(),
            "source_conflict_flag": str(source_conflict).lower(),
            "multi_affiliation_flag": str(multi_affiliation).lower(),
            "qa_status": status,
            "qa_notes": audit_row["qa_notes"],
        })
    return linked, excluded, audit


def run_linkage(root: Path, config: PipelineConfig) -> dict[str, Path]:
    schema_dir = root / "data" / "expected_schema"
    input_dir = config.input_dir
    output_dir = config.output_dir
    validate_required_fields(input_dir / "author_work_institution.csv", schema_dir, "author_work_institution_schema.json")
    validate_required_fields(input_dir / "works.csv", schema_dir, "works_schema.json")
    validate_required_fields(input_dir / "institutions.csv", schema_dir, "institutions_schema.json")
    validate_required_fields(input_dir / "institution_aliases.csv", schema_dir, "institution_aliases_schema.json")
    validate_required_fields(input_dir / "source_comparison.csv", schema_dir, "source_comparison_schema.json")

    author_links = read_csv_rows(input_dir / "author_work_institution.csv")
    works = read_csv_rows(input_dir / "works.csv")
    institutions = read_csv_rows(input_dir / "institutions.csv")
    source_comparison = read_csv_rows(input_dir / "source_comparison.csv")
    _ = enrich_alias_rows(read_csv_rows(input_dir / "institution_aliases.csv"))
    linked, excluded, audit = process_records(author_links, works, institutions, source_comparison, config)

    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "linked": output_dir / "linked_author_institution_city.csv",
        "excluded": output_dir / "excluded_records.csv",
        "audit": output_dir / "record_level_audit.csv",
    }
    write_csv_rows(paths["linked"], linked, schema_fields(schema_dir, "linked_author_institution_city_schema.json"))
    write_csv_rows(paths["excluded"], excluded, schema_fields(schema_dir, "excluded_records_schema.json"))
    write_csv_rows(paths["audit"], audit, schema_fields(schema_dir, "record_level_audit_schema.json"))
    return paths
