"""Command line entry points for deterministic synthetic demos."""
from __future__ import annotations

import argparse
from pathlib import Path

from .affiliations.openalex_parser import parse_openalex_work
from .affiliations.scopus_parser import normalize_scopus_links
from .affiliations.source_comparison import compare_sources
from .author_index.cleaning import normalize_author_records
from .city_year.aggregation import collect_city_year_counts, fill_missing_years
from .city_year.lagged_controls import build_lagged_controls
from .proximity.cognitive_similarity import compute_cognitive_proximity
from .proximity.subject_exports import merge_subject_exports
from .publications.author_paper import build_author_paper_links
from .publications.parsers import parse_abstract_response, parse_search_response
from .schemas import FIXED_RUN_ID, read_csv, read_json, write_csv, write_json
from .transport import MockTransport

ROOT = Path(__file__).resolve().parents[2]


def default_input_dir() -> Path:
    return ROOT / "data" / "synthetic"


def default_output_dir() -> Path:
    return ROOT / "outputs" / "scopus_demo"


def _paths(args: argparse.Namespace) -> tuple[Path, Path]:
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    if not input_dir.is_absolute():
        input_dir = ROOT / input_dir
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir
    return input_dir, output_dir


def run_affiliation_demo(input_dir: Path, output_dir: Path) -> dict[str, Path]:
    _, raw_links = parse_abstract_response(read_json(input_dir / "scopus_abstract_fixture.json"))
    scopus_links = normalize_scopus_links(raw_links)
    openalex_links = parse_openalex_work(read_json(input_dir / "openalex_work_fixture.json"))
    comparison = compare_sources(scopus_links, openalex_links)
    paths = {
        "author_institution_links": output_dir / "author_institution_links.csv",
        "institution_city_mapping": output_dir / "institution_city_mapping.csv",
        "affiliation_quality_summary": output_dir / "affiliation_quality_summary.csv",
        "source_comparison": output_dir / "source_comparison.csv",
    }
    write_csv(paths["author_institution_links"], scopus_links, [
        "source_system", "source_work_id", "normalized_work_key", "source_author_id", "normalized_author_key",
        "source_institution_id", "normalized_institution_key", "institution_name", "city", "country",
        "city_country_key", "affiliation_position", "multi_affiliation_flag", "parser_status", "missing_fields", "qa_notes",
    ])
    mapping = {}
    for row in scopus_links:
        mapping[row["normalized_institution_key"]] = {
            "normalized_institution_key": row["normalized_institution_key"],
            "institution_name": row["institution_name"],
            "city": row["city"],
            "country": row["country"],
            "city_country_key": row["city_country_key"],
        }
    write_csv(paths["institution_city_mapping"], mapping.values(), ["normalized_institution_key", "institution_name", "city", "country", "city_country_key"])
    summary = [
        {"metric": "scopus_affiliation_links", "value": len(scopus_links), "notes": "synthetic"},
        {"metric": "openalex_affiliation_links", "value": len(openalex_links), "notes": "synthetic"},
        {"metric": "links_with_missing_fields", "value": sum(1 for r in scopus_links if r["missing_fields"]), "notes": "paper_affiliation_only"},
    ]
    write_csv(paths["affiliation_quality_summary"], summary, ["metric", "value", "notes"])
    write_csv(paths["source_comparison"], comparison, ["normalized_work_key", "normalized_author_key", "scopus_records", "openalex_records", "comparison_status", "qa_notes"])
    return paths


def run_author_paper_demo(input_dir: Path, output_dir: Path) -> dict[str, Path]:
    authors = normalize_author_records(read_csv(input_dir / "authors.csv"))
    search_rows = parse_search_response(read_json(input_dir / "scopus_search_fixture.json"))
    roster, _ = parse_abstract_response(read_json(input_dir / "scopus_abstract_fixture.json"))
    links = build_author_paper_links(roster)
    paths = {
        "normalized_author_records": output_dir / "normalized_author_records.csv",
        "author_paper_links": output_dir / "author_paper_links.csv",
        "publication_records": output_dir / "publication_records.csv",
    }
    write_csv(paths["normalized_author_records"], authors, ["source_author_id", "normalized_author_key", "display_name", "home_country", "author_id_status", "duplicate_author_flag", "qa_notes"])
    write_csv(paths["author_paper_links"], links, ["source_author_id", "normalized_author_key", "source_work_id", "normalized_work_key", "author_position", "duplicate_author_work_flag", "qa_notes"])
    write_csv(paths["publication_records"], search_rows, ["source_work_id", "normalized_work_key", "title", "publication_year", "document_type", "parser_status"])
    return paths


def run_city_year_demo(input_dir: Path, output_dir: Path) -> dict[str, Path]:
    cities = read_csv(input_dir / "cities.csv")
    events = read_csv(input_dir / "event_candidates.csv")
    years = [2022, 2023, 2024]
    counts, failures, manifest = collect_city_year_counts(cities, years, MockTransport())
    counts = fill_missing_years(counts, years)
    controls = build_lagged_controls(counts, events, lags=2)
    paths = {
        "city_year_publication_counts": output_dir / "city_year_publication_counts.csv",
        "city_year_failures": output_dir / "city_year_failures.csv",
        "collection_manifest": output_dir / "collection_manifest.json",
        "lagged_city_year_controls": output_dir / "lagged_city_year_controls.csv",
    }
    write_csv(paths["city_year_publication_counts"], counts, ["city", "country", "year", "publication_count", "subject", "qa_notes"])
    write_csv(paths["city_year_failures"], failures, ["city", "country", "year", "failure_status", "qa_notes"])
    write_json(paths["collection_manifest"], {"run_id": FIXED_RUN_ID, "network_access": False, "requests": manifest})
    write_csv(paths["lagged_city_year_controls"], controls, ["candidate_id", "city", "country", "event_year", "lag_window", "lagged_publication_count_sum", "lagged_publication_count_mean", "qa_notes"])
    return paths


def run_proximity_demo(input_dir: Path, output_dir: Path) -> dict[str, Path]:
    rows = merge_subject_exports([read_csv(input_dir / "subject_counts.csv")])
    long_rows, matrix_rows, quality = compute_cognitive_proximity(rows)
    matrix_fields = sorted({key for row in matrix_rows for key in row})
    matrix_fields = ["period", "city", "country"] + [field for field in matrix_fields if field not in {"period", "city", "country"}]
    paths = {
        "cognitive_proximity_long": output_dir / "cognitive_proximity_long.csv",
        "cognitive_proximity_matrix": output_dir / "cognitive_proximity_matrix.csv",
        "cognitive_proximity_quality_summary": output_dir / "cognitive_proximity_quality_summary.csv",
    }
    write_csv(paths["cognitive_proximity_long"], long_rows, ["period", "source_city", "source_country", "target_city", "target_country", "cosine_similarity"])
    write_csv(paths["cognitive_proximity_matrix"], matrix_rows, matrix_fields)
    write_csv(paths["cognitive_proximity_quality_summary"], quality, ["period", "city", "country", "metric", "value", "notes"])
    return paths


def run_all_demo(input_dir: Path, output_dir: Path) -> dict[str, Path]:
    paths: dict[str, Path] = {}
    paths.update(run_author_paper_demo(input_dir, output_dir))
    paths.update(run_affiliation_demo(input_dir, output_dir))
    paths.update(run_city_year_demo(input_dir, output_dir))
    paths.update(run_proximity_demo(input_dir, output_dir))
    summary = {
        "run_id": FIXED_RUN_ID,
        "network_access": False,
        "files_created": sorted(path.name for path in paths.values()),
    }
    summary_path = output_dir / "toolkit_run_summary.json"
    report_path = output_dir / "toolkit_demo_report.md"
    write_json(summary_path, summary)
    report_path.write_text(
        "# Synthetic Toolkit Demo Report\n\n"
        "This deterministic run used only synthetic fixtures and MockTransport.\n\n"
        f"Files created: {len(paths) + 2}\n",
        encoding="utf-8",
    )
    paths["toolkit_run_summary"] = summary_path
    paths["toolkit_demo_report"] = report_path
    return paths


def _run(command: str, args: argparse.Namespace) -> int:
    input_dir, output_dir = _paths(args)
    output_dir.mkdir(parents=True, exist_ok=True)
    runners = {
        "affiliation-demo": run_affiliation_demo,
        "author-paper-demo": run_author_paper_demo,
        "city-year-demo": run_city_year_demo,
        "proximity-demo": run_proximity_demo,
        "all-demo": run_all_demo,
    }
    paths = runners[command](input_dir, output_dir)
    print(f"{command} complete: " + ", ".join(sorted(path.name for path in paths.values())))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m scopus_toolkit", description="Synthetic Scopus Research Data Toolkit demos.")
    subparsers = parser.add_subparsers(dest="command")
    for name in ["affiliation-demo", "author-paper-demo", "city-year-demo", "proximity-demo", "all-demo"]:
        sub = subparsers.add_parser(name)
        sub.add_argument("--input-dir", default=str(default_input_dir()))
        sub.add_argument("--output-dir", default=str(default_output_dir()))
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 0
    return _run(args.command, args)
