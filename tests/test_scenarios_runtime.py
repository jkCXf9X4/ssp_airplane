from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.lib.scenarios.runtime import (  # type: ignore  # noqa: E402
    create_simulation_config,
    write_simulation_config,
)


def test_create_simulation_config_keeps_ssp4sim_schema(tmp_path: Path) -> None:
    ssp_path = tmp_path / "scenario.ssp"
    ssp_path.write_bytes(b"")
    result_file = tmp_path / "results" / "scenario_results.csv"

    config = create_simulation_config(
        ssp_path=ssp_path,
        result_file=result_file,
        stop_time=120.0,
        realtime=True,
        recording_interval=0.25,
        log_fmu=True,
    )

    simulation = config["simulation"]
    assert list(simulation) == [
        "ssp",
        "ssd",
        "start_time",
        "stop_time",
        "timestep",
        "tolerance",
        "realtime",
        "executor",
        "recording",
        "log",
    ]
    assert simulation["ssp"] == ssp_path.as_posix()
    assert simulation["ssd"] == "SystemStructure.ssd"
    assert simulation["start_time"] == 0.0
    assert simulation["stop_time"] == 120.0
    assert simulation["timestep"] == 0.1
    assert simulation["tolerance"] == 1e-4
    assert simulation["realtime"] is True
    assert simulation["executor"] == {
        "method": "jacobi",
        "thread_pool_workers": 5,
        "forward_derivatives": True,
        "jacobi": {"parallel": True, "method": 1},
        "seidel": {"parallel": False},
    }
    assert simulation["recording"]["wait_for"] is True
    assert simulation["recording"]["csv"] == {
        "enable": True,
        "file": result_file.as_posix(),
        "interval": 0.25,
    }
    assert simulation["log"] == {"file": "./build/results/sim.log", "fmu": True}


def test_write_simulation_config_defaults_beside_result(tmp_path: Path) -> None:
    ssp_path = tmp_path / "scenario.ssp"
    ssp_path.write_bytes(b"")
    result_file = tmp_path / "results" / "scenario_results.csv"

    config = create_simulation_config(ssp_path, result_file, stop_time=1.0)
    config_path = write_simulation_config(config, result_file)

    assert config_path == result_file.parent / "config.json"
    assert json.loads(config_path.read_text()) == config
