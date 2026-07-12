"""Deterministic institution alias demonstration.

This is not production-grade entity resolution or ROR parsing.
"""
from __future__ import annotations

from src.geocoding.geocode_cache import institution_city_key
from src.utilities.text_cleaning import normalize_text


def enrich_alias_rows(alias_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Normalize aliases and ensure city-country keys are explicit."""
    enriched = []
    for row in alias_rows:
        out = dict(row)
        out["normalized_name"] = out.get("normalized_name") or normalize_text(out.get("official_name"))
        out["city_country_key"] = out.get("city_country_key") or institution_city_key(out)
        enriched.append(out)
    return enriched
