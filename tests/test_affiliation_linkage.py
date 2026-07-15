from __future__ import annotations

from pathlib import Path

from scopus_toolkit.affiliations.scopus_parser import normalize_scopus_links
from scopus_toolkit.publications.parsers import parse_abstract_response
from scopus_toolkit.schemas import read_json

ROOT = Path(__file__).resolve().parents[1]


def test_author_affiliation_links_do_not_expand_paper_affiliations_to_all_authors():
    _, raw_links = parse_abstract_response(read_json(ROOT / "data/synthetic/scopus_abstract_fixture.json"))
    rows = normalize_scopus_links(raw_links)
    beta_links = [r for r in rows if r["source_author_id"] == "SYNTH_AUTHOR_002"]
    assert [r["source_institution_id"] for r in beta_links] == ["SYNTH_INST_003"]


def test_multi_affiliation_and_duplicate_flags():
    _, raw_links = parse_abstract_response(read_json(ROOT / "data/synthetic/scopus_abstract_fixture.json"))
    rows = normalize_scopus_links(raw_links)
    alpha = [r for r in rows if r["source_author_id"] == "SYNTH_AUTHOR_001"]
    assert any(r["multi_affiliation_flag"] == "true" for r in alpha)
    assert any("duplicate_author_institution_link" in r["qa_notes"] for r in alpha)
