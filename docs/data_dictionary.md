# Data Dictionary

`data/synthetic/` contains synthetic inputs: authors, cities, event candidates, subject counts, Scopus-style fixtures, OpenAlex-style fixtures, and a manifest.

Input fields:

- `author_id`, `display_name`, `home_country`: synthetic author records.
- `city`, `country`, `subject`, `scenario`: city-year query inputs and mock response scenarios.
- `candidate_id`, `event_year`: event-candidate panel inputs.
- `period`, `subject`, `count`: subject-profile vectors for cognitive proximity.

Output fields:

- `normalized_author_key`, `normalized_work_key`, `normalized_institution_key`: stable normalized identifiers.
- `city_country_key`: normalized same-name city disambiguation key.
- `parser_status`, `missing_fields`, `qa_notes`: parser and quality diagnostics.
- `publication_count`: synthetic city-year count.
- `lagged_publication_count_sum`, `lagged_publication_count_mean`: strict pre-event controls.
- `cosine_similarity`: subject-vector similarity.

All IDs with `SYNTH` or `SYNTHETIC` are non-resolving demonstration identifiers.
