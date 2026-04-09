#!/usr/bin/env python3
"""Run the full architecture-first rebuild workflow."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.paths import BUILD_DIR, REPO_ROOT


def run_step(*args: str) -> None:
    print(" ".join(args))
    subprocess.run(args, cwd=REPO_ROOT, check=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-simulation",
        action="store_true",
        help="Run simulation",
    )

    args = parser.parse_args(argv)

    omc_path = os.environ.get("OMC") or shutil.which("omc")
    if not omc_path:
        raise SystemExit(
            "omc executable not found. Install OpenModelica or set OMC to its full path."
        )
    cmake_build_dir = BUILD_DIR / "cmake"

    print("Exporting architecture-derived artifacts...")
    run_step(
        sys.executable,
        "-m",
        "scripts.cli.artifacts_export",
    )

    print("Verifying Modelica interfaces...")
    run_step(
        sys.executable,
        "-m",
        "scripts.cli.verify_modelica_variables",
    )

    print("Verifying models...")
    run_step(
        sys.executable,
        "-m",
        "scripts.cli.verify_model_equations",
    )

    print("Configuring CMake build...")
    run_step(
        "cmake",
        "-S",
        ".",
        "-B",
        str(cmake_build_dir),
        f"-DOMC_EXECUTABLE={omc_path}",
    )

    print("Building and packaging FMUs and the baseline SSP...")
    run_step(
        "cmake",
        "--build",
        str(cmake_build_dir),
    )

    print("Testing native FlightGear bridge FMU...")
    run_step(
        "pytest",
        "-q",
        "tests/test_flightgear_bridge_fmu.py",
    )

    print("Validating SSD schema...")
    run_step(
        sys.executable,
        "-m",
        "scripts.cli.verify_ssd_xml",
    )

    print("Running reference simulation...")
    results_dir = BUILD_DIR / "results"
    scenario_path = REPO_ROOT / "resources" / "scenarios" / "test_scenario.json"
    parameter_set_path = results_dir / "test_scenario_waypoints.ssv"
    prepared_ssp_path = results_dir / "test_scenario_run" / "test_scenario.ssp"
    result_file = results_dir / "test_scenario_results.csv"
    config_path = results_dir / "config.json"
    run_step(
        sys.executable,
        "-m",
        "scripts.cli.scenarios_prepare_waypoints",
        "--scenario",
        str(scenario_path),
    )
    run_step(
        sys.executable,
        "-m",
        "scripts.cli.scenarios_package_ssp",
        "--parameter-set",
        str(parameter_set_path),
        "--scenario-stem",
        "test_scenario",
    )
    run_step(
        sys.executable,
        "-m",
        "scripts.cli.scenarios_write_config",
        "--prepared-ssp",
        str(prepared_ssp_path),
        "--result-file",
        str(result_file),
        "--stop-time",
        "120.0",
        "--config-path",
        str(config_path),
    )
    if args.run_simulation:
        run_step(
            sys.executable,
            "-m",
            "scripts.cli.scenarios_run_ssp4sim",
            "--config-path",
            str(config_path),
        )
        run_step(
            sys.executable,
            "-m",
            "scripts.cli.scenarios_evaluate_results",
            "--scenario",
            str(scenario_path),
            "--results-csv",
            str(result_file),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
