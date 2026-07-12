from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.config.settings import load_config
from src.geocoding.geocode_cache import institution_city_key
from src.linkage.author_institution_linkage import process_records
from src.linkage.schema import SchemaError, read_csv_rows, validate_required_fields, validate_schema_files
from src.validation.coverage import compute_coverage


def load_inputs():
    input_dir = ROOT / "data" / "synthetic_sample"
    return (
        read_csv_rows(input_dir / "author_work_institution.csv"),
        read_csv_rows(input_dir / "works.csv"),
        read_csv_rows(input_dir / "institutions.csv"),
        read_csv_rows(input_dir / "source_comparison.csv"),
    )


def run_process(config_path: Path = ROOT / "config" / "config.example.json"):
    config = load_config(config_path, ROOT)
    return process_records(*load_inputs(), config)


def audit_by_record():
    return {row["record_id"]: row for row in run_process()[2]}


def test_schema_files_are_valid():
    assert "author_work_institution_schema.json" in validate_schema_files(ROOT / "data" / "expected_schema")


def test_schema_fields_present():
    fields = validate_required_fields(ROOT / "data" / "synthetic_sample" / "author_work_institution.csv", ROOT / "data" / "expected_schema", "author_work_institution_schema.json")
    assert "record_id" in fields


def test_schema_missing_field_raises(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("record_id,author_id\nR1,A1\n", encoding="utf-8")
    with pytest.raises(SchemaError):
        validate_required_fields(bad, ROOT / "data" / "expected_schema", "author_work_institution_schema.json")

def test_normal_match_is_valid():
    row = audit_by_record()["R001"]
    assert row["linkage_valid"] == "true"
    assert row["geocoding_valid"] == "true"


def test_missing_author_id():
    assert audit_by_record()["R002"]["exclusion_reason"] == "missing_author_id"


def test_missing_work_id():
    assert audit_by_record()["R003"]["exclusion_reason"] == "missing_work_id"


def test_missing_institution_id():
    assert audit_by_record()["R004"]["exclusion_reason"] == "missing_institution_id"


def test_work_not_found():
    assert audit_by_record()["R005"]["exclusion_reason"] == "work_not_found"


def test_institution_not_found():
    assert audit_by_record()["R006"]["exclusion_reason"] == "institution_not_found"


def test_invalid_coordinates_are_geocoding_invalid():
    row = audit_by_record()["R009"]
    assert row["linkage_valid"] == "true"
    assert row["geocoding_valid"] == "false"
    assert "invalid_coordinates" in row["qa_notes"]


def test_low_confidence_threshold():
    row = audit_by_record()["R010"]
    assert row["linkage_valid"] == "false"
    assert row["qa_status"] == "low_confidence"


def test_duplicate_record_flag_and_exclusion():
    rows = audit_by_record()
    assert rows["R011"]["duplicate_flag"] == "true"
    assert rows["R012"]["duplicate_excluded"] == "true"
    assert rows["R012"]["exclusion_reason"] == "duplicate_record"


def test_empty_input_has_zero_coverage():
    metrics = {row["metric"]: row["value"] for row in compute_coverage([])}
    assert metrics["total_input_rows"] == 0
    assert metrics["linkage_coverage"] == "0.0000"


def test_multi_affiliation_retained():
    rows = audit_by_record()
    assert rows["R013"]["multi_affiliation_flag"] == "true"
    assert rows["R014"]["multi_affiliation_flag"] == "true"


def test_source_conflict_flag():
    assert audit_by_record()["R018"]["source_conflict_flag"] == "true"


def test_coverage_calculation_contains_required_metrics():
    metrics = {row["metric"]: row["value"] for row in compute_coverage(run_process()[2])}
    assert metrics["total_input_rows"] == 18
    assert metrics["duplicate_rows"] == 1
    assert "geocoding_coverage_among_valid_links" in metrics


def test_config_threshold_changes_result(tmp_path):
    config = json.loads((ROOT / "config" / "config.example.json").read_text(encoding="utf-8"))
    config["minimum_confidence_score"] = 0.40
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    audit = {row["record_id"]: row for row in run_process(config_path)[2]}
    assert audit["R010"]["linkage_valid"] == "true"


def test_config_deduplicate_false_changes_result(tmp_path):
    config = json.loads((ROOT / "config" / "config.example.json").read_text(encoding="utf-8"))
    config["deduplicate_records"] = False
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    audit = {row["record_id"]: row for row in run_process(config_path)[2]}
    assert audit["R012"]["duplicate_excluded"] == "false"


def test_same_city_name_distinguished_by_country():
    institutions = read_csv_rows(ROOT / "data" / "synthetic_sample" / "institutions.csv")
    keys = {row["institution_id"]: institution_city_key(row) for row in institutions}
    assert keys["Inst_I008"] == "springfield|exampleland"
    assert keys["Inst_I009"] == "springfield|samplestan"
    assert keys["Inst_I008"] != keys["Inst_I009"]


def test_pipeline_command_runs_and_output_schema_matches_expected():
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "run_example_pipeline.py"), "--config", str(ROOT / "config" / "config.example.json")], cwd=ROOT, check=False, capture_output=True, text=True)
    assert result.returncode == 0
    for name in ["linked_author_institution_city.csv", "record_level_audit.csv", "coverage_summary.csv", "source_comparison_summary.csv"]:
        produced = ROOT / "outputs" / "example_outputs" / name
        expected = ROOT / "examples" / "expected_outputs" / name
        assert produced.exists()
        if expected.exists():
            with produced.open(newline="", encoding="utf-8") as a, expected.open(newline="", encoding="utf-8") as b:
                assert next(csv.reader(a)) == next(csv.reader(b))
