# Methodology

This repository implements a synthetic measurement-audit workflow for author-institution-city linkage.

1. Validate source tables against JSON schemas.
2. Link author-work-institution records using synthetic identifiers.
3. Normalize institution aliases deterministically.
4. Validate city-country keys and coordinates.
5. Produce record-level QA flags.
6. Summarize coverage and source conflict diagnostics.

The workflow is intentionally local and no-network. It demonstrates data contracts and measurement boundaries, not full bibliographic data collection.
