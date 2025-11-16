#!/usr/bin/env python3
"""Simulate a waypoint scenario with OMSimulator or an analytic dry-run."""

from __future__ import annotations

import argparse
import json
import math
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import pyssp4sim

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SSP = REPO_ROOT / "build" / "ssp" / "aircraft.ssp"
DEFAULT_RESULTS = REPO_ROOT / "build" / "results"


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())


def haversine_distance_km(points: List[Dict[str, float]]) -> float:
    def radians(point: Dict[str, float]) -> tuple[float, float]:
        return math.radians(point["latitude_deg"]), math.radians(point["longitude_deg"])

    total = 0.0
    for i in range(len(points) - 1):
        lat1, lon1 = radians(points[i])
        lat2, lon2 = radians(points[i + 1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        h = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        total += 2 * 6371.0 * math.asin(min(1.0, math.sqrt(h)))
    return total


def estimate_duration(distance_km: float, cruise_speed_mps: float) -> float:
    return max(60.0, (distance_km * 1000.0) / max(1.0, cruise_speed_mps))


@dataclass
class ScenarioResult:
    scenario_path: Path
    total_distance_km: float
    estimated_duration_s: float
    fuel_capacity_kg: float
    fuel_burn_rate_kgps: float
    fuel_required_kg: float
    fuel_exhausted: bool
    meets_range_requirement: bool
    used_oms: bool
    result_file: Optional[Path]


def run_with_simulator(ssp_path: Path, result_file: Path, stop_time: float) -> None:

    config = f"""
{{
    "simulation" :
    {{
        "ssp": "{ssp_path.as_posix()}",
        "ssd": "SystemStructure.ssd",
        "start_time":0.0,
        "stop_time":{stop_time},
        "timestep": 1.0,
        "tolerance": 1e-4,

        "executor": 
        {{
            "method":"jacobi",
            
            "thread_pool_workers": 5,
            "forward_derivatives": true,

            "jacobi":
            {{
                "parallel": true,
                "method" : 1
            }},
            "seidel":
            {{
                "parallel": false
            }}
            
        }},

        "recording":
        {{
            "enable": true,
            "wait_for": false,
            "interval": 0.25,
            "result_file": "{result_file.as_posix()}"
        }},

        "log":
        {{
            "file": "./build/results/sim.log"
        }}
    }}
}}
"""
    temp_config = DEFAULT_RESULTS / "config.json"
    with open(temp_config, "w") as f:
        f.write(config) 

    sim = pyssp4sim.Simulator(temp_config.as_posix())
    sim.init()
    sim.simulate()


def simulate_scenario(
    scenario_path: Path,
    ssp_path: Path = None,
    results_dir: Path = DEFAULT_RESULTS,
) -> ScenarioResult:
    scenario = load_json(scenario_path)
    if "points" not in scenario:
        raise ValueError("Scenario file must contain a 'points' list.")

    total_distance = scenario.get("total_distance_km") or haversine_distance_km(
        scenario["points"]
    )
    if not ssp_path:
        ssp_path = DEFAULT_SSP
    if not ssp_path.exists():
        raise FileNotFoundError(f"SSP file not found: {ssp_path}")
    
    results_dir.mkdir(parents=True, exist_ok=True)
    result_file = results_dir / f"{scenario_path.stem}_results.csv"
    run_with_simulator(ssp_path, result_file, 3600)

    return ScenarioResult(
        scenario_path=scenario_path,
        total_distance_km=total_distance,
        result_file=result_file,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario", type=Path, required=True, help="Path to scenario JSON file."
    )
    parser.add_argument(
        "--ssp", type=Path, default=DEFAULT_SSP, help="Path to the SSP archive."
    )
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = simulate_scenario(
        scenario_path=args.scenario,
        ssp_path=args.ssp,
        results_dir=args.results_dir,
    )
    print(
        json.dumps(
            {
                "scenario": str(result.scenario_path),
                "distance_km": round(result.total_distance_km, 2),
                "duration_s": round(result.estimated_duration_s, 1),
                "fuel_required_kg": round(result.fuel_required_kg, 1),
                "fuel_exhausted": result.fuel_exhausted,
                "meets_range_requirement": result.meets_range_requirement,
                "used_oms": result.used_oms,
                "result_file": str(result.result_file) if result.result_file else None,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
