# Public Release QC

Status: READY_FOR_GITHUB_PUBLICATION after author ownership confirmation and MIT license selection.

## Executed commands
- `python3 -m compileall src scripts tests`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_smoke_test.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_example_pipeline.py --config config/config.example.json`
- `PYTHONPATH=/private/tmp/pytest_for_author_linkage_v2 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q`

## Environment
- Python version: 3.14.5
- pytest was installed temporarily under `/private/tmp/pytest_for_author_linkage_v2` for this audit and was not copied into this folder.

## Test results
- compileall: PASS
- smoke test: PASS
- example pipeline: PASS
- pytest: PASS
- pytest test count: 20

## Functional checks
- configuration actually used: TRUE
- authoritative schema JSON files: 10
- fixed expected outputs present: TRUE
- runtime outputs present: TRUE
- linkage/geocoding distinction implemented: TRUE
- duplicate, low confidence, invalid coordinates, and source conflicts handled: TRUE

## Safety scans
- local_path: PASS (0 hits)
- credential_pattern: PASS (0 hits)
- phone: PASS (0 hits)
- email: PASS (0 hits)
- real_name: PASS (0 hits)
- real_institution: PASS (0 hits)
- large_file: PASS (0 hits)
- git_dir: PASS (0 hits)
- cache_dir: PASS (0 hits)
- notebook_output: PASS (0 hits)
- env_example: PASS (0 hits)
- non_public_paper_terms: PASS (0 hits)

## Data and publication status
- real data included: FALSE
- real access credentials included: FALSE
- local absolute paths included: FALSE
- non-public paper files included: FALSE
- restricted source data included: FALSE
- Git initialized: FALSE

## Blocking issues
- Blocking automated findings: 0
- Code ownership: confirmed by Ran Wang
- License: MIT selected
- Remaining work: add the final GitHub URL and release date to `CITATION.cff`

## Final status
- READY_FOR_GITHUB_PUBLICATION
