# V2 Changelog

- Created a new V2 public-candidate folder without modifying V1.
- Repositioned the repository as a reproducible synthetic demonstration and measurement audit framework.
- Removed `.env.example` and unused API/email configuration placeholders.
- Replaced YAML config with JSON config that is actually read by the pipeline.
- Expanded synthetic data to cover missing IDs, not-found IDs, geocoding gaps, invalid coordinates, low confidence, duplicates, multi-affiliation records, same-name cities, source agreement, and source conflict.
- Made `data/expected_schema/*.json` the authoritative schema source.
- Added record-level QA fields and enhanced coverage diagnostics.
- Added fixed expected outputs under `examples/expected_outputs/` and runtime outputs under `outputs/example_outputs/`.
- Expanded pytest coverage beyond 12 meaningful tests.
- Updated README, docs, citation metadata, release notes, redaction log, and code ownership review.
