"""Simulation runtime helpers built on pyssp_simulate."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Optional

from pyssp_simulate import SimulationSpec

# Airplane scenario defaults. The spec carries every value pyssp_simulate
# models (paths, times, step, tolerance, realtime, recording, logging); the
# executor block is the one engine setting the public SimulationSpec surface
# does not expose, so it is named once here instead of inline in the payload.
_SSP4SIM_TIMESTEP = 0.1
_SSP4SIM_TOLERANCE = 1e-4
_SSP4SIM_RECORDING_INTERVAL = 0.25
_SSP4SIM_EXECUTOR: dict[str, Any] = {
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
}


def create_simulation_config(
    ssp_path: Path,
    result_file: Path,
    stop_time: float,
    log_fmu: bool = False,
    realtime: bool = False,
    recording_interval: float = _SSP4SIM_RECORDING_INTERVAL,
) -> dict[str, Any]:
    spec = SimulationSpec(
        ssp=ssp_path,
        stop_time=stop_time,
        step_size=_SSP4SIM_TIMESTEP,
        tolerance=_SSP4SIM_TOLERANCE,
        result_file=result_file,
        realtime=realtime,
        recording_interval=recording_interval,
        log_fmu=log_fmu,
    )
    return {
        "simulation": {
            "ssp": spec.ssp.as_posix(),
            "ssd": "SystemStructure.ssd",
            "start_time": spec.start_time,
            "stop_time": spec.stop_time,
            "timestep": spec.effective_step_size(),
            "tolerance": spec.tolerance,
            "realtime": spec.realtime,
            "executor": copy.deepcopy(_SSP4SIM_EXECUTOR),
            "recording": {
                "wait_for": True,
                "csv": {
                    "enable": True,
                    "file": spec.result_file.as_posix(),
                    "interval": spec.recording_interval,
                },
            },
            "log": {
                "file": "./build/results/sim.log",
                "fmu": spec.log_fmu,
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
