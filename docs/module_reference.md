# Module Reference

- `author_index.cleaning`: validates synthetic author inputs and normalizes author keys.
- `publications.parsers`: parses Scopus-style search and abstract fixtures.
- `publications.author_paper`: creates deduplicated author-work links.
- `affiliations.scopus_parser`: converts paper-affiliation references into normalized rows.
- `affiliations.openalex_parser`: parses OpenAlex-shaped offline fixtures for comparison only.
- `affiliations.source_comparison`: reports field-level source agreement and conflicts.
- `city_year.query_builder`: constructs escaped Scopus-style queries.
- `city_year.pagination`: handles mock pagination and retry manifests.
- `city_year.aggregation`: aggregates city-year publication counts.
- `city_year.lagged_controls`: builds strict pre-event lagged controls.
- `proximity.cognitive_similarity`: creates cosine similarity long and matrix outputs.
- `quality.manifests`: provides SQLite task checkpoint and resume state.
