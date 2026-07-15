"""Toolkit-specific exceptions."""
from __future__ import annotations


class ToolkitError(ValueError):
    """Raised when toolkit inputs fail validation."""


class TransportError(RuntimeError):
    """Raised when a mock or optional live transport request fails."""
