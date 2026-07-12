"""Configuration loading for the synthetic public demonstration."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    input_dir: Path
    output_dir: Path
    network_access: bool
    minimum_confidence_score: float
    deduplicate_records: bool
    require_valid_coordinates: bool


def load_config(config_path: Path, root: Path) -> PipelineConfig:
    data = json.loads(config_path.read_text(encoding="utf-8"))
    if data.get("network_access") is not False:
        raise ValueError("The public demonstration requires network_access=false.")
    return PipelineConfig(
        input_dir=(root / data["input_dir"]).resolve(),
        output_dir=(root / data["output_dir"]).resolve(),
        network_access=bool(data["network_access"]),
        minimum_confidence_score=float(data["minimum_confidence_score"]),
        deduplicate_records=bool(data["deduplicate_records"]),
        require_valid_coordinates=bool(data["require_valid_coordinates"]),
    )
