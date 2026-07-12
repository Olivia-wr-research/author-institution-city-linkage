# Reproducibility

The public candidate is reproducible for the synthetic data only.

Run:

```bash
python scripts/run_smoke_test.py
python scripts/run_example_pipeline.py --config config/config.example.json
python -m pytest -q
```

Runtime outputs are written to `outputs/example_outputs/`. Fixed review outputs are stored in `examples/expected_outputs/`.
