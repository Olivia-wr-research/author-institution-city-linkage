from __future__ import annotations

from scopus_toolkit.city_year.query_builder import build_city_year_query


def test_query_escape_and_filters():
    query = build_city_year_query('SYNTH "CITY"', "Exampleland", 2024, "COMP")
    assert 'ALL("SYNTH \\"CITY\\"")' in query
    assert 'AFFILCOUNTRY("Exampleland")' in query
    assert "PUBYEAR = 2024" in query
    assert "(DOCTYPE(ar) OR DOCTYPE(re))" in query
    assert "SUBJAREA(COMP)" in query
