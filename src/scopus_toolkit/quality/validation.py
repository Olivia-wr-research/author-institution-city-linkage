"""Validation helpers for public release safety."""
from __future__ import annotations

import re
from pathlib import Path

PRIVATE_PATTERNS = [
    "/" + "Users" + "/" + "olivia" + "/",
    "Research" + "_" + "Agent",
    "python" + "Project5",
    "/" + "Volumes" + "/" + "PhiHardisk H1",
    "Authorization" + ":",
    "scopus" + "_config" + ".ini",
]


def scan_text_for_private_markers(text: str) -> list[str]:
    hits = [pattern for pattern in PRIVATE_PATTERNS if pattern in text]
    hits.extend(re.findall(r"10\.(?!0000/synthetic)[0-9]{4,9}/\\S+", text, flags=re.I))
    hits.extend(re.findall(r"\\b\\d{10,11}\\b", text))
    return sorted(set(hits))


def scan_repo(paths: list[Path]) -> dict[str, list[str]]:
    findings: dict[str, list[str]] = {}
    for path in paths:
        if path.is_file():
            try:
                hits = scan_text_for_private_markers(path.read_text(encoding="utf-8"))
            except UnicodeDecodeError:
                continue
            if hits:
                findings[str(path)] = hits
    return findings
