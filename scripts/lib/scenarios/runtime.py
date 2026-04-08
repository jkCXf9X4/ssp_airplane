"""Simulation runtime helpers around pyssp4sim."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

try:
    import pyssp4sim
except ImportError:
    pyssp4sim = None


def require_pyssp4sim() -> None:
    if pyssp4sim is None:
        raise RuntimeError(
            "pyssp4sim is not available; activate venv, install the ssp4sim Python API or reuse existing results."
        )


def create_simulation_config(
    ssp_path: Path,
    result_file: Path,
    stop_time: float,
    log_fmu: bool = False,
    realtime: bool = False,
) -> dict[str, Any]:
    return {
        "simulation": {
            "ssp": ssp_path.as_posix(),
            "ssd": "SystemStructure.ssd",
            "start_time": 0.0,
            "stop_time": stop_time,
            "timestep": 0.1,
            "tolerance": 1e-4,
            "realtime": realtime,
            "executor": {
                "method": "jacobi",
                "thread_pool_workers": 5,
                "forward_derivatives": True,
                "jacobi": {
                    "parallel": True,
                    "method": 1,
                },
                "seidel": {
                    "parallel": False,
                },
            },
            "recording": {
                "enable": True,
                "wait_for": True,
                "interval": 0.25,
                "result_file": result_file.as_posix(),
            },
            "log": {
                "file": "./build/results/sim.log",
                "fmu": log_fmu,
            },
        }
    }


def write_simulation_config(
    config: dict[str, Any],
    result_file: Path,
    config_path: Optional[Path] = None,
) -> Path:
    resolved_config_path = config_path or (result_file.parent / "config.json")
    resolved_config_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_config_path.write_text(json.dumps(config, indent=2))
    return resolved_config_path


def run_simulation_with_pyssp4sim(config_path: Path) -> None:
    require_pyssp4sim()
    simulator = pyssp4sim.Simulator(config_path.as_posix())
    simulator.init()
    simulator.simulate()
