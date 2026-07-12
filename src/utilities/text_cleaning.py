"""Small text-normalization helpers for synthetic linkage examples."""
from __future__ import annotations

import re
import unicodedata


def normalize_text(value: object) -> str:
    """Return a conservative lowercase ASCII key for deterministic examples."""
    if value is None:
        return ""
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", " ", text).strip().lower()
    return re.sub(r"\s+", " ", text)


def is_blank(value: object) -> bool:
    return normalize_text(value) == ""


def as_bool(value: object) -> bool:
    return normalize_text(value) in {"true", "1", "yes", "y"}
