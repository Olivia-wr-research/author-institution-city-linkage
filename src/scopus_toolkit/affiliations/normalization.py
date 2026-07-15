"""Institution and city normalization."""
from __future__ import annotations

from ..schemas import normalize_key


def normalize_institution_name(value: str) -> str:
    text = normalize_key(value)
    for token in ["synthetic_", "_campus", "_laboratory"]:
        text = text.replace(token, "_")
    return text.strip("_")


def normalize_city_country(city: str, country: str) -> str:
    return f"{normalize_key(city)}|{normalize_key(country)}"
