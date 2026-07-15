from __future__ import annotations

from pathlib import Path

from scopus_toolkit.publications.parsers import parse_abstract_response, parse_search_response
from scopus_toolkit.schemas import read_json

ROOT = Path(__file__).resolve().parents[1]


def test_search_response_and_publication_year():
    rows = parse_search_response(read_json(ROOT / "data/synthetic/scopus_search_fixture.json"))
    assert rows[0]["normalized_work_key"] == "synthetic001"
    assert rows[0]["publication_year"] == "2024"


def test_abstract_response_multi_affiliation_and_missing_fields():
    roster, links = parse_abstract_response(read_json(ROOT / "data/synthetic/scopus_abstract_fixture.json"))
    assert len(roster) == 4
    assert len(links) == 5
    assert any("source_author_id" in row["missing_fields"] for row in links)
    assert any("city" in row["missing_fields"] for row in links)


def test_empty_and_malformed_response():
    assert parse_search_response({"search-results": {"entry": []}}) == []
    assert parse_abstract_response({"unexpected": []}) == ([], [])
