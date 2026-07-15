# Scopus Research Data Toolkit

Author–institution linkage, publication panels, city-year controls, cognitive proximity, and data-quality audits.

## Project Overview

This repository is an independent research-code toolkit organized around public-safe, reusable Scopus-oriented data workflows. It contains only synthetic demonstration data, deterministic expected outputs, tests, and documentation.

It is not an Elsevier or Scopus official tool. It does not include real Scopus data, real API responses, real authors, real papers, credentials, publication-level results, or manuscript outputs.

## Why The Repository Is Organized Around Scopus

The shared lifecycle is Scopus-style bibliographic data processing: parse API-shaped records, normalize author-paper-affiliation links, build publication panels, aggregate city-year publication controls, compare offline source coverage, and audit measurement quality.

## Module Map

- `scopus_toolkit.author_index`: author input validation and synthetic candidate normalization.
- `scopus_toolkit.publications`: Scopus-style search and abstract parsing plus author-paper bipartite links.
- `scopus_toolkit.affiliations`: paper-affiliation parsing, normalization, and offline Scopus-OpenAlex comparison.
- `scopus_toolkit.city_year`: query construction, mock pagination, retry state, aggregation, and lagged controls.
- `scopus_toolkit.proximity`: subject-count vectors and cosine cognitive proximity.
- `scopus_toolkit.quality`: coverage, duplicates, validation, manifests, and SQLite resume state.

## Repository Structure

```text
config/                 compatible synthetic pipeline config
data/synthetic/          synthetic Scopus-style fixtures
data/synthetic_sample/   original v0.1.0 synthetic linkage demo
examples/expected_outputs/ deterministic outputs for demos and tests
src/scopus_toolkit/      v0.2.0 toolkit package
src/linkage/             preserved v0.1.0 compatibility modules
scripts/                 compatible and toolkit demo entry points
tests/                   pytest suite
docs/                    architecture, boundaries, schemas, reproducibility
audit/                   release review records
```

## Installation

Runtime editable install:

```bash
python -m pip install -e .
```

Conda:

```bash
conda env create -f environment.yml
conda activate scopus-research-data-toolkit
```

Test and development install:

```bash
python -m pip install -e ".[test]"
```

`pyproject.toml` is the dependency source of truth. `requirements.txt` is kept only as a development convenience for test tooling.

## Quick Start

```bash
python -m scopus_toolkit --help
python -m scopus_toolkit all-demo
python -m pytest -q
```

Compatible v0.1.0 commands remain available:

```bash
python scripts/run_smoke_test.py
python scripts/run_example_pipeline.py --config config/config.example.json
```

## Author-Institution Linkage

The toolkit parses paper-level author-affiliation links with explicit fields for source system, work ID, author ID, institution ID, city, country, affiliation position, missing fields, parser status, and QA notes. A Scopus paper affiliation is not treated as verified employment.

## Author-Publication Pipeline

Synthetic author records are validated, Scopus-style search entries are normalized, publication years are parsed, and author-paper bipartite links are deduplicated. The demo does not search for real people or claim manual identity verification.

## City-Year Publication Controls

The city-year module builds escaped Scopus-style queries, applies article/review filters, runs deterministic mock pagination and retry behavior, aggregates publication counts, fills missing years, and builds strict pre-event lagged controls.

## Cognitive Proximity

Cognitive proximity is computed as cosine similarity over synthetic city-period-subject count vectors. It is a measurement based on subject distributions and must not be interpreted as causal evidence.

## Scopus-OpenAlex Source Comparison

OpenAlex is included only as an offline comparison source for author-affiliation fields. Statuses include `agreement`, `partial_agreement`, `scopus_only`, `openalex_only`, `institution_conflict`, `geography_conflict`, and `insufficient_information`. Agreement means synthetic fields match; it is not ground truth.

## Synthetic Data

All records, identifiers, institutions, cities, publication counts, subject profiles, and API-style responses under `data/synthetic/` are synthetic, non-resolving demonstration data.

## Output Schemas

Toolkit demos create normalized author records, author-paper links, author-institution links, institution-city mappings, source comparisons, city-year counts, failures, manifests, lagged controls, cognitive proximity long and matrix outputs, and run summaries.

## Testing

```bash
python -m compileall src scripts
python -m pytest -q
```

The tests do not access Scopus, OpenAlex, or any network resource.

## Reproducibility

Expected outputs are deterministic. The demos use fixed synthetic fixtures, fixed row ordering, fixed run IDs, no random numbers, and no current timestamps.

## Scopus API And Data Boundaries

Default demos use `MockTransport` only. Optional live Scopus access is deferred in v0.2.0. Users are responsible for complying with applicable API, license, privacy, and data-access terms.

## Measurement Boundaries

Publication affiliations are paper addresses, not verified employment institutions. Paper cities are not career-mobility destinations. Source agreement is not factual verification.

## Privacy And Security

The repository does not contain real credentials, private paths, API caches, raw API responses, real DOI/EID/ORCID/Scopus Author IDs, private email addresses, unpublished model coefficients, tables, or figures.

## Limitations

This is a reusable synthetic toolkit candidate, not a production Scopus collector and not an empirical database. Live adapter behavior, licensed data handling, and project-specific validation remain outside this public release.

## Citation

Use `CITATION.cff`.

## Author

Ran Wang.
