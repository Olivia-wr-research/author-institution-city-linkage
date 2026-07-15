from __future__ import annotations

from pathlib import Path

from scopus_toolkit.publications.author_paper import build_author_paper_links
from scopus_toolkit.publications.parsers import parse_abstract_response
from scopus_toolkit.schemas import read_json

ROOT = Path(__file__).resolve().parents[1]


def test_author_paper_bipartite_and_duplicates():
    roster, _ = parse_abstract_response(read_json(ROOT / "data/synthetic/scopus_abstract_fixture.json"))
    links = build_author_paper_links(roster)
    assert any(row["duplicate_author_work_flag"] == "true" for row in links)
    assert {row["source_author_id"] for row in links} >= {"SYNTH_AUTHOR_001", "SYNTH_AUTHOR_002"}
