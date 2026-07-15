"""Scopus-style city-year query construction."""
from __future__ import annotations

import re


def escape_query_text(value: str) -> str:
    return value.strip().replace("\\", "\\\\").replace('"', '\\"')


def build_city_year_query(city: str, country: str, year: int, subject: str = "", all_fields: bool = True) -> str:
    city_q = escape_query_text(city)
    country_q = escape_query_text(country)
    field = "ALL" if all_fields else "AFFIL"
    parts = [f'{field}("{city_q}")', f'AFFILCOUNTRY("{country_q}")', f"PUBYEAR = {year}", '(DOCTYPE(ar) OR DOCTYPE(re))']
    if subject:
        parts.append(f"SUBJAREA({escape_query_text(subject)})")
    return " AND ".join(parts)


def city_task_id(city: str, country: str, year: int, subject: str = "") -> str:
    safe = re.sub(r"[^A-Za-z0-9]+", "_", f"{city}_{country}_{year}_{subject}").strip("_")
    return f"TASK_{safe.upper()}"
