# Reproducibility

Create an environment, install the package, run tests, and regenerate deterministic outputs:

```bash
python -m pip install -e ".[test]"
python -m compileall src scripts
python -m pytest -q
python -m scopus_toolkit all-demo --input-dir data/synthetic --output-dir outputs/scopus_demo
```

Compatible original synthetic pipeline:

```bash
python scripts/run_smoke_test.py
python scripts/run_example_pipeline.py --config config/config.example.json
```

Expected outputs under `examples/expected_outputs/` are generated from synthetic fixtures only. They do not contain absolute paths, random numbers, or current timestamps.
