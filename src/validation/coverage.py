"""Coverage diagnostics for linked synthetic author-institution-city records."""
from __future__ import annotations

from collections import Counter
from pathlib import Path

from src.linkage.schema import read_csv_rows, schema_fields, write_csv_rows
from src.utilities.text_cleaning import as_bool


def _metric(name: str, value: object) -> dict[str, object]:
    return {"metric": name, "value": value}


def compute_coverage(audit_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    total = len(audit_rows)
    duplicate_rows = sum(1 for row in audit_rows if as_bool(row.get("duplicate_excluded")))
    unique_rows = total - duplicate_rows
    linkage_valid = sum(1 for row in audit_rows if as_bool(row.get("linkage_valid")) and not as_bool(row.get("duplicate_excluded")))
    geocoding_valid = sum(1 for row in audit_rows if as_bool(row.get("geocoding_valid")) and not as_bool(row.get("duplicate_excluded")))
    low_conf = sum(1 for row in audit_rows if "confidence_below_threshold" in row.get("qa_notes", "") and not as_bool(row.get("duplicate_excluded")))
    source_conf = sum(1 for row in audit_rows if as_bool(row.get("source_conflict_flag")) and not as_bool(row.get("duplicate_excluded")))
    multi = sum(1 for row in audit_rows if as_bool(row.get("multi_affiliation_flag")) and not as_bool(row.get("duplicate_excluded")))
    rows = [
        _metric("total_input_rows", total),
        _metric("unique_input_rows", unique_rows),
        _metric("duplicate_rows", duplicate_rows),
        _metric("linkage_valid_rows", linkage_valid),
        _metric("linkage_invalid_rows", unique_rows - linkage_valid),
        _metric("geocoding_valid_rows", geocoding_valid),
        _metric("geocoding_invalid_rows", unique_rows - geocoding_valid),
        _metric("low_confidence_rows", low_conf),
        _metric("source_conflict_rows", source_conf),
        _metric("multi_affiliation_rows", multi),
        _metric("linkage_coverage", f"{(linkage_valid / unique_rows):.4f}" if unique_rows else "0.0000"),
        _metric("geocoding_coverage_among_valid_links", f"{(geocoding_valid / linkage_valid):.4f}" if linkage_valid else "0.0000"),
    ]
    status_counts = Counter(row.get("qa_status", "unknown") for row in audit_rows)
    for status, count in sorted(status_counts.items()):
        rows.append(_metric(f"qa_status_{status}", count))
    return rows


def compute_source_summary(source_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    total = len(source_rows)
    conflicts = sum(1 for row in source_rows if as_bool(row.get("expected_conflict_flag")))
    return [
        _metric("source_comparison_rows", total),
        _metric("source_agreement_rows", total - conflicts),
        _metric("source_conflict_rows", conflicts),
        _metric("source_conflict_share", f"{(conflicts / total):.4f}" if total else "0.0000"),
    ]


def write_diagnostics(root: Path, output_dir: Path) -> dict[str, Path]:
    schema_dir = root / "data" / "expected_schema"
    audit_rows = read_csv_rows(output_dir / "record_level_audit.csv")
    source_rows = read_csv_rows(root / "data" / "synthetic_sample" / "source_comparison.csv")
    coverage_path = output_dir / "coverage_summary.csv"
    source_path = output_dir / "source_comparison_summary.csv"
    write_csv_rows(coverage_path, compute_coverage(audit_rows), schema_fields(schema_dir, "coverage_summary_schema.json"))
    write_csv_rows(source_path, compute_source_summary(source_rows), schema_fields(schema_dir, "source_comparison_summary_schema.json"))
    return {"coverage": coverage_path, "source_summary": source_path}
