"""Strict lagged city-year controls."""
from __future__ import annotations


def build_lagged_controls(counts: list[dict[str, object]], event_candidates: list[dict[str, str]], lags: int = 2) -> list[dict[str, object]]:
    by_key = {(str(r["city"]), str(r["country"]), int(r["year"])): int(r.get("publication_count", 0)) for r in counts}
    output = []
    for event in sorted(event_candidates, key=lambda r: (r["candidate_id"], r["event_year"])):
        year = int(event["event_year"])
        values = [by_key.get((event["city"], event["country"], year - lag), 0) for lag in range(1, lags + 1)]
        output.append(
            {
                "candidate_id": event["candidate_id"],
                "city": event["city"],
                "country": event["country"],
                "event_year": year,
                "lag_window": f"t-1_to_t-{lags}",
                "lagged_publication_count_sum": sum(values),
                "lagged_publication_count_mean": f"{(sum(values) / lags):.4f}",
                "qa_notes": "strict_pre_event_window",
            }
        )
    return output
