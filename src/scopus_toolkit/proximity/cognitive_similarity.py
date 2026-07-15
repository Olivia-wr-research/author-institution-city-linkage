"""Cosine similarity over city-period-subject vectors."""
from __future__ import annotations

import math


def subject_vectors(rows: list[dict[str, str]]) -> dict[tuple[str, str, str], dict[str, int]]:
    vectors: dict[tuple[str, str, str], dict[str, int]] = {}
    for row in rows:
        key = (row["period"], row["city"], row["country"])
        vectors.setdefault(key, {})[row["subject"]] = int(row["count"])
    return vectors


def cosine(a: dict[str, int], b: dict[str, int], subjects: list[str]) -> float:
    va = [a.get(s, 0) for s in subjects]
    vb = [b.get(s, 0) for s in subjects]
    dot = sum(x * y for x, y in zip(va, vb))
    na = math.sqrt(sum(x * x for x in va))
    nb = math.sqrt(sum(y * y for y in vb))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def compute_cognitive_proximity(rows: list[dict[str, str]]) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    vectors = subject_vectors(rows)
    subjects = sorted({row["subject"] for row in rows})
    long_rows = []
    matrix_rows = []
    quality = []
    for period in sorted({key[0] for key in vectors}):
        city_keys = sorted([key for key in vectors if key[0] == period], key=lambda k: (k[1], k[2]))
        for source in city_keys:
            matrix_row: dict[str, object] = {"period": period, "city": source[1], "country": source[2]}
            zero = sum(vectors[source].values()) == 0
            if zero:
                quality.append({"period": period, "city": source[1], "country": source[2], "metric": "zero_vector", "value": 1, "notes": "similarities_set_to_zero"})
            for target in city_keys:
                sim = 1.0 if source == target and not zero else cosine(vectors[source], vectors[target], subjects)
                sim_text = f"{sim:.6f}"
                long_rows.append(
                    {
                        "period": period,
                        "source_city": source[1],
                        "source_country": source[2],
                        "target_city": target[1],
                        "target_country": target[2],
                        "cosine_similarity": sim_text,
                    }
                )
                matrix_row[f"{target[1]}|{target[2]}"] = sim_text
            matrix_rows.append(matrix_row)
    quality.append({"period": "all", "city": "", "country": "", "metric": "subject_count", "value": len(subjects), "notes": "synthetic_subjects"})
    return long_rows, matrix_rows, quality
