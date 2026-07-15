"""Transport abstractions decoupled from query, retry, and parser logic."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol

from .exceptions import TransportError


@dataclass(frozen=True)
class TransportResponse:
    status_code: int
    payload: dict[str, object]
    retryable: bool = False


class Transport(Protocol):
    def request(self, query: str, start: int = 0, count: int = 25) -> TransportResponse:
        """Return a response for a query without exposing credential handling."""


class MockTransport:
    """Deterministic Scopus-style transport for examples and tests."""

    def __init__(self) -> None:
        self.calls: dict[str, int] = {}

    def request(self, query: str, start: int = 0, count: int = 25) -> TransportResponse:
        key = f"{query}|{start}"
        self.calls[key] = self.calls.get(key, 0) + 1
        if "RETRY_429" in query and self.calls[key] == 1:
            return TransportResponse(429, {"error": "synthetic rate limit"}, True)
        if "RETRY_500" in query and self.calls[key] == 1:
            return TransportResponse(500, {"error": "synthetic server error"}, True)
        if "PERMANENT_FAIL" in query:
            return TransportResponse(500, {"error": "synthetic permanent failure"}, False)
        if "MISSING_FIELDS" in query:
            return TransportResponse(200, {"search-results": {}}, False)
        if "EMPTY_CITY" in query:
            return TransportResponse(200, {"search-results": {"opensearch:totalResults": "0", "entry": []}}, False)
        total = 3 if "MULTIPAGE_CITY" in query else 1
        entries = [{"eid": f"2-s2.0-SYNTHETIC_PAGE_{start}_{i}", "prism:coverDate": "2024-01-01"} for i in range(min(count, max(total - start, 0)))]
        return TransportResponse(200, {"search-results": {"opensearch:totalResults": str(total), "entry": entries}}, False)


class LiveScopusTransport:
    """Optional placeholder enforcing environment-only credentials.

    This adapter is intentionally not wired into demos or tests.
    """

    def __init__(self) -> None:
        self.api_key = os.environ.get("SCOPUS_API_KEY", "")
        if not self.api_key:
            raise TransportError("SCOPUS_API_KEY is not set; live transport is disabled.")

    def request(self, query: str, start: int = 0, count: int = 25) -> TransportResponse:
        raise TransportError("Live Scopus transport is deferred for public-safe v0.2.0.")
