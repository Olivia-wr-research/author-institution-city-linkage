"""City-year count aggregation and panel materialization."""
from __future__ import annotations

from .pagination import fetch_all_pages
from .query_builder import build_city_year_query, city_task_id
from ..schemas import sorted_rows
from ..transport import Transport


def collect_city_year_counts(cities: list[dict[str, str]], years: list[int], transport: Transport) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    counts = []
    failures = []
    manifest = []
    for city in sorted(cities, key=lambda r: (r.get("city", ""), r.get("country", ""))):
        for year in years:
            query = build_city_year_query(city["city"], city["country"], year, city.get("subject", ""))
            if city.get("scenario"):
                query = f"{query} {city['scenario']}"
            entries, pages = fetch_all_pages(query, transport)
            manifest.extend({"task_id": city_task_id(city["city"], city["country"], year, city.get("subject", "")), **page} for page in pages)
            failed = any(page["status"] == "permanent_failure" for page in pages)
            if failed:
                failures.append({"city": city["city"], "country": city["country"], "year": year, "failure_status": "permanent_failure", "qa_notes": "synthetic_transport_failure"})
            counts.append({"city": city["city"], "country": city["country"], "year": year, "publication_count": 0 if failed else len(entries), "subject": city.get("subject", ""), "qa_notes": "failed" if failed else "mock_count"})
    return sorted_rows(counts, ["city", "country", "year"]), sorted_rows(failures, ["city", "country", "year"]), manifest


def fill_missing_years(counts: list[dict[str, object]], years: list[int]) -> list[dict[str, object]]:
    by_city = {(row["city"], row["country"]) for row in counts}
    existing = {(row["city"], row["country"], int(row["year"])): row for row in counts}
    output = []
    for city, country in sorted(by_city):
        for year in years:
            output.append(existing.get((city, country, year), {"city": city, "country": country, "year": year, "publication_count": 0, "subject": "", "qa_notes": "filled_missing_year"}))
    return output
