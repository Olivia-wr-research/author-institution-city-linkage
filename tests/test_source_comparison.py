from __future__ import annotations

from scopus_toolkit.affiliations.source_comparison import compare_sources


def row(work, author, inst="", geo=""):
    return {"normalized_work_key": work, "normalized_author_key": author, "normalized_institution_key": inst, "city_country_key": geo}


def test_source_comparison_statuses():
    scopus = [
        row("w1", "a1", "i1", "c1"),
        row("w2", "a2", "i2", "c2"),
        row("w3", "a3", "i3", "c3"),
        row("w4", "a4", "", ""),
        row("w5", "a5", "i5", "c5"),
    ]
    openalex = [
        row("w1", "a1", "i1", "c1"),
        row("w2", "a2", "i2", "c9"),
        row("w3", "a3", "i9", "c3"),
        row("w4", "a4", "", ""),
        row("w6", "a6", "i6", "c6"),
    ]
    statuses = {(r["normalized_work_key"], r["normalized_author_key"]): r["comparison_status"] for r in compare_sources(scopus, openalex)}
    assert statuses[("w1", "a1")] == "agreement"
    assert statuses[("w2", "a2")] == "geography_conflict"
    assert statuses[("w3", "a3")] == "institution_conflict"
    assert statuses[("w4", "a4")] == "insufficient_information"
    assert statuses[("w5", "a5")] == "scopus_only"
    assert statuses[("w6", "a6")] == "openalex_only"


def test_partial_agreement():
    out = compare_sources([row("w", "a", "i1", "g1"), row("w", "a", "i2", "g2")], [row("w", "a", "i1", "g1")])
    assert out[0]["comparison_status"] == "partial_agreement"
