"""Pagination and retry orchestration for transport responses."""
from __future__ import annotations

from ..transport import Transport, TransportResponse


def total_results(payload: dict[str, object]) -> int:
    search = payload.get("search-results")
    if not isinstance(search, dict):
        return 0
    try:
        return int(str(search.get("opensearch:totalResults", "0")))
    except ValueError:
        return 0


def fetch_all_pages(query: str, transport: Transport, page_size: int = 2, max_retries: int = 2) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    entries: list[dict[str, object]] = []
    manifest: list[dict[str, object]] = []
    start = 0
    total = None
    while total is None or start < total:
        attempts = 0
        response: TransportResponse | None = None
        while attempts <= max_retries:
            attempts += 1
            response = transport.request(query, start=start, count=page_size)
            if response.status_code == 200:
                break
            if not response.retryable or attempts > max_retries:
                manifest.append({"query": query, "start": start, "status": "permanent_failure", "attempts": attempts, "http_status": response.status_code})
                return entries, manifest
        assert response is not None
        total = total_results(response.payload)
        search = response.payload.get("search-results", {})
        page_entries = search.get("entry", []) if isinstance(search, dict) else []
        if not isinstance(page_entries, list):
            page_entries = []
        entries.extend([e for e in page_entries if isinstance(e, dict)])
        manifest.append({"query": query, "start": start, "status": "completed", "attempts": attempts, "http_status": response.status_code})
        if total == 0 or not page_entries:
            break
        start += page_size
    return entries, manifest
