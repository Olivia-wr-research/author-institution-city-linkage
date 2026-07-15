"""Duplicate detection helpers."""
from __future__ import annotations

from collections import Counter


def duplicate_flags(rows: list[dict[str, str]], keys: list[str]) -> list[bool]:
    counts = Counter(tuple(row.get(key, "") for key in keys) for row in rows)
    seen: set[tuple[str, ...]] = set()
    flags = []
    for row in rows:
        key = tuple(row.get(k, "") for k in keys)
        duplicate = counts[key] > 1 and key in seen
        flags.append(duplicate)
        seen.add(key)
    return flags
