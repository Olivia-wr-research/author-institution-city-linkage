from __future__ import annotations

from scopus_toolkit.city_year.lagged_controls import build_lagged_controls


def test_strict_lagged_controls():
    counts = [
        {"city": "A", "country": "B", "year": 2022, "publication_count": 2},
        {"city": "A", "country": "B", "year": 2023, "publication_count": 3},
        {"city": "A", "country": "B", "year": 2024, "publication_count": 99},
    ]
    out = build_lagged_controls(counts, [{"candidate_id": "E1", "city": "A", "country": "B", "event_year": "2024"}])
    assert out[0]["lagged_publication_count_sum"] == 5
