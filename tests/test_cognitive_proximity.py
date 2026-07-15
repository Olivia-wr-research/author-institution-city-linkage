from __future__ import annotations

from pathlib import Path

from scopus_toolkit.proximity.cognitive_similarity import compute_cognitive_proximity
from scopus_toolkit.proximity.subject_exports import merge_subject_exports
from scopus_toolkit.schemas import read_csv

ROOT = Path(__file__).resolve().parents[1]


def test_cognitive_proximity_symmetry_diagonal_zero_vector_and_same_city():
    rows = merge_subject_exports([read_csv(ROOT / "data/synthetic/subject_counts.csv")])
    long_rows, matrix_rows, quality = compute_cognitive_proximity(rows)
    pairs = {(r["period"], r["source_city"], r["source_country"], r["target_city"], r["target_country"]): r["cosine_similarity"] for r in long_rows}
    assert pairs[("2020-2022", "SYNTH_CITY_ALPHA", "Exampleland", "SYNTH_CITY_ALPHA", "Exampleland")] == "1.000000"
    assert pairs[("2020-2022", "SYNTH_CITY_ALPHA", "Exampleland", "SYNTH_CITY_BETA", "Samplestan")] == pairs[("2020-2022", "SYNTH_CITY_BETA", "Samplestan", "SYNTH_CITY_ALPHA", "Exampleland")]
    assert pairs[("2020-2022", "SYNTH_CITY_ZERO", "Nowheria", "SYNTH_CITY_ZERO", "Nowheria")] == "0.000000"
    assert any(r["city"] == "Springfield" and r["country"] == "Exampleland" for r in matrix_rows)
    assert any(r["metric"] == "zero_vector" for r in quality)
