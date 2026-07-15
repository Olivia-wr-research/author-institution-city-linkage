from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cli_help_and_all_demo(tmp_path):
    help_result = subprocess.run([sys.executable, "-m", "scopus_toolkit", "--help"], cwd=ROOT, capture_output=True, text=True, check=False)
    assert help_result.returncode == 0
    out_dir = tmp_path / "out"
    result = subprocess.run([sys.executable, "-m", "scopus_toolkit", "all-demo", "--input-dir", "data/synthetic", "--output-dir", str(out_dir)], cwd=ROOT, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    assert (out_dir / "toolkit_run_summary.json").exists()
    assert (out_dir / "source_comparison.csv").exists()
