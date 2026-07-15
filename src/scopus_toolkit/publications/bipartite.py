"""Author-work bipartite edge utilities."""
from __future__ import annotations

from .author_paper import build_author_paper_links


def build_bipartite_edges(roster_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return build_author_paper_links(roster_rows)
