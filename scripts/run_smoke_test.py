#!/usr/bin/env python3
"""No-network smoke test for the public synthetic example."""
from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.linkage.schema import validate_required_fields, validate_schema_files

INPUT_SCHEMAS = {
    "author_work_institution.csv": "author_work_institution_schema.json",
    "works.csv": "works_schema.json",
    "institutions.csv": "institutions_schema.json",
    "institution_aliases.csv": "institution_aliases_schema.json",
    "source_comparison.csv": "source_comparison_schema.json",
}


def assert_csv_has_rows(path: Path) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise AssertionError(f"{path} has no data rows")


def main() -> int:
    schema_dir = ROOT / "data" / "expected_schema"
    validate_schema_files(schema_dir)
    input_dir = ROOT / "data" / "synthetic_sample"
    for filename, schema_name in INPUT_SCHEMAS.items():
        path = input_dir / filename
        validate_required_fields(path, schema_dir, schema_name)
        assert_csv_has_rows(path)
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "run_example_pipeline.py"), "--config", str(ROOT / "config" / "config.example.json")], check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)
    for filename in ["linked_author_institution_city.csv", "record_level_audit.csv", "coverage_summary.csv", "source_comparison_summary.csv"]:
        assert_csv_has_rows(ROOT / "outputs" / "example_outputs" / filename)
    print("Smoke test passed without network access.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
