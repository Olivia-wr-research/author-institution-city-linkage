# Code Ownership Review

Ownership review confirmed by Ran Wang on 2026-07-12.

Ran Wang confirms that the research design, measurement framework, workflow logic, and included public materials were developed under her direction and are not copied from an advisor, collaborator, or third-party codebase. Codex was used to restructure, document, test, and sanitize the public repository. AI-assisted restructuring does not create an additional human coauthor or contributor claim, and Ran Wang remains responsible for the final code and documentation.

| Public file or group | Research/logic origin | AI-assisted restructuring | Third-party code identified | Public release decision | Ownership status |
| --- | --- | --- | --- | --- | --- |
| `README.md` and `docs/` | Ran Wang's project framing and measurement boundaries | Yes | No | Release under MIT | CONFIRMED_BY_AUTHOR |
| `src/linkage/author_institution_linkage.py` | Ran Wang's linkage and QA workflow design | Yes | No | Release under MIT | CONFIRMED_BY_AUTHOR |
| `src/geocoding/geocode_cache.py` | Ran Wang's local geocoding-validation requirements | Yes | No | Release under MIT | CONFIRMED_BY_AUTHOR |
| `src/validation/coverage.py` | Ran Wang's coverage-audit framework | Yes | No | Release under MIT | CONFIRMED_BY_AUTHOR |
| `src/linkage/schema.py` and configuration utilities | Public demonstration implementation under Ran Wang's direction | Yes | No | Release under MIT | CONFIRMED_BY_AUTHOR |
| `scripts/` and `tests/` | Public reproducibility and validation implementation under Ran Wang's direction | Yes | No | Release under MIT | CONFIRMED_BY_AUTHOR |
| `data/synthetic_sample/` | Fully synthetic examples created for this repository | Yes | No | Release under MIT | CONFIRMED_BY_AUTHOR |
| `data/expected_schema/` and `examples/expected_outputs/` | Public demonstration schemas and synthetic outputs | Yes | No | Release under MIT | CONFIRMED_BY_AUTHOR |

## Boundaries

The ownership confirmation applies only to files included in this repository. It does not grant rights to Scopus, Elsevier, OpenAlex, ROR, or other third-party datasets, API responses, documentation, trademarks, or database contents. No such restricted materials are included. Future contributions from other people must be reviewed before relicensing or release.
