from __future__ import annotations

from pathlib import Path

from scopus_toolkit.quality.validation import scan_repo

ROOT = Path(__file__).resolve().parents[1]


def test_synthetic_manifest_statement():
    text = (ROOT / "data/synthetic/fixture_manifest.json").read_text(encoding="utf-8")
    assert "synthetic, non-resolving demonstration data" in text


def test_no_private_markers_in_public_files():
    paths = [p for p in ROOT.rglob("*") if ".git" not in p.parts and "outputs" not in p.parts and p.is_file()]
    findings = scan_repo(paths)
    allowed = {str(ROOT / "audit/v0.2.0_release_review.md")}
    findings = {k: v for k, v in findings.items() if k not in allowed}
    assert findings == {}
