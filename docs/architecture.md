# Architecture

The repository is organized by data lifecycle: input validation, parsing, normalization, aggregation, quality audit, and deterministic demo output.

`transport.py` defines the boundary between request execution and business logic. Query building, pagination, retry handling, parsing, aggregation, and tests use `MockTransport` by default.

The v0.1.0 synthetic linkage modules remain in place for compatibility. The v0.2.0 `scopus_toolkit` package adds reusable Scopus-oriented modules without requiring network access.
