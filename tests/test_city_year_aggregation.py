from __future__ import annotations

from pathlib import Path

from scopus_toolkit.city_year.aggregation import collect_city_year_counts, fill_missing_years
from scopus_toolkit.schemas import read_csv
from scopus_toolkit.transport import MockTransport

ROOT = Path(__file__).resolve().parents[1]


def test_city_year_mock_transport_cases():
    cities = read_csv(ROOT / "data/synthetic/cities.csv")
    counts, failures, manifest = collect_city_year_counts(cities, [2024], MockTransport())
    by_city = {r["city"]: r for r in counts}
    assert by_city["SYNTH_CITY_EMPTY"]["publication_count"] == 0
    assert by_city["SYNTH_CITY_BETA"]["publication_count"] == 3
    assert any(r["failure_status"] == "permanent_failure" for r in failures)
    assert any(r["attempts"] == 2 for r in manifest if "RETRY_429" in r["query"])


def test_missing_year_fill():
    rows = fill_missing_years([{"city": "A", "country": "B", "year": 2024, "publication_count": 1}], [2023, 2024])
    assert rows[0]["publication_count"] == 0
    assert rows[1]["publication_count"] == 1
