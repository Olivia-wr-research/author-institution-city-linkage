# Data Dictionary

Authoritative schema definitions are stored in `data/expected_schema/*.json`. This document summarizes the main synthetic files and should be checked against those JSON schemas before release.

## Inputs

- `author_work_institution.csv`: synthetic record-level author-work-institution links.
- `works.csv`: synthetic work metadata.
- `institutions.csv`: synthetic institution, city, country, and coordinate metadata.
- `institution_aliases.csv`: deterministic alias-normalization examples.
- `source_comparison.csv`: synthetic source agreement and conflict examples.

## Outputs

- `linked_author_institution_city.csv`: resolvable records after configured deduplication, including linkage and geocoding QA fields.
- `record_level_audit.csv`: every input row with exclusion and QA status.
- `coverage_summary.csv`: aggregate coverage metrics.
- `source_comparison_summary.csv`: source agreement and conflict metrics.
