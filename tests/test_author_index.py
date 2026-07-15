from __future__ import annotations

import pytest

from scopus_toolkit.author_index.cleaning import normalize_author_records, scopus_author_id_status
from scopus_toolkit.exceptions import ToolkitError


def test_author_schema_and_missing_id():
    rows = [{"author_id": "", "display_name": "Synthetic Author MissingId", "home_country": "Nowheria"}]
    out = normalize_author_records(rows)
    assert out[0]["author_id_status"] == "missing"


def test_author_id_format_rejects_non_synthetic():
    with pytest.raises(ToolkitError):
        scopus_author_id_status("NOT_A_SYNTHETIC_AUTHOR")
