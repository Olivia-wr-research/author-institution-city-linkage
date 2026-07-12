#!/usr/bin/env python3
"""Run the synthetic no-network author-institution-city linkage pipeline."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.config.settings import load_config
from src.linkage.author_institution_linkage import run_linkage
from src.validation.coverage import write_diagnostics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the synthetic author-institution-city pipeline.")
    parser.add_argument("--config", default="config/config.example.json", help="Path to JSON config relative to repository root or absolute path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = ROOT / config_path
    config = load_config(config_path, ROOT)
    paths = run_linkage(ROOT, config)
    paths.update(write_diagnostics(ROOT, config.output_dir))
    created = ", ".join(path.name for path in paths.values())
    print(f"Synthetic pipeline complete: {created}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
