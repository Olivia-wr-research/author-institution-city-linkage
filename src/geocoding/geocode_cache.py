"""Local institution geocoding helpers for synthetic data.

No network geocoder is called. Public examples should use local, reviewed lookup tables.
"""
from __future__ import annotations

from src.utilities.text_cleaning import is_blank, normalize_text


def institution_city_key(row: dict[str, str]) -> str:
    """Create a city-country key that preserves same-name cities across countries."""
    return f"{normalize_text(row.get('city'))}|{normalize_text(row.get('country'))}"


def has_valid_coordinates(row: dict[str, str]) -> bool:
    try:
        lat = float(row.get("latitude", ""))
        lon = float(row.get("longitude", ""))
    except ValueError:
        return False
    return -90 <= lat <= 90 and -180 <= lon <= 180


def geocoding_valid(row: dict[str, str], require_valid_coordinates: bool = True) -> tuple[bool, str]:
    """Return geocoding validity and a standardized note."""
    if is_blank(row.get("city")):
        return False, "missing_city"
    if is_blank(row.get("country")):
        return False, "missing_country"
    if require_valid_coordinates and not has_valid_coordinates(row):
        return False, "invalid_coordinates"
    return True, "geocoding_valid"
