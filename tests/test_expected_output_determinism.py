from __future__ import annotations

from pathlib import Path

from scopus_toolkit.cli import run_all_demo

ROOT = Path(__file__).resolve().parents[1]

V020_EXPECTED_FILES = {
    "affiliation_quality_summary.csv",
    "author_institution_links.csv",
    "author_paper_links.csv",
    "city_year_failures.csv",
    "city_year_publication_counts.csv",
    "cognitive_proximity_long.csv",
    "cognitive_proximity_matrix.csv",
    "cognitive_proximity_quality_summary.csv",
    "collection_manifest.json",
    "institution_city_mapping.csv",
    "lagged_city_year_controls.csv",
    "normalized_author_records.csv",
    "publication_records.csv",
    "source_comparison.csv",
    "toolkit_demo_report.md",
    "toolkit_run_summary.json",
}


def test_all_demo_expected_outputs_are_byte_deterministic(tmp_path):
    output_dir = tmp_path / "all_demo"
    run_all_demo(ROOT / "data" / "synthetic", output_dir)

    produced = {path.name for path in output_dir.iterdir() if path.is_file()}
    assert produced == V020_EXPECTED_FILES

    for name in sorted(V020_EXPECTED_FILES):
        produced_bytes = (output_dir / name).read_bytes()
        expected_bytes = (ROOT / "examples" / "expected_outputs" / name).read_bytes()
        assert produced_bytes == expected_bytes, name
        if name.endswith(".csv"):
            assert b"\r\n" not in produced_bytes
            assert b"\r" not in produced_bytes
            assert produced_bytes.endswith(b"\n")
            assert not produced_bytes.endswith(b"\n\n")
