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
    parser.parse_args(argv)

    omc_path = os.environ.get("OMC") or shutil.which("omc")
    if not omc_path:
        raise SystemExit("omc executable not found. Install OpenModelica or set OMC to its full path.")
    cmake_build_dir = BUILD_DIR / "cmake"

    print("Exporting architecture-derived artifacts...")
    run_step(sys.executable, "-m", "scripts.cli.artifacts_export")

    print("Verifying Modelica interfaces...")
    run_step(sys.executable, "-m", "scripts.cli.verify_modelica_variables")

    print("Verifying models...")
    run_step(sys.executable, "-m", "scripts.cli.verify_model_equations")

    print("Configuring CMake build...")
    run_step("cmake", "-S", ".", "-B", str(cmake_build_dir), f"-DOMC_EXECUTABLE={omc_path}")

    print("Building and packaging FMUs and the baseline SSP...")
    run_step("cmake", "--build", str(cmake_build_dir))

    print("Testing native FlightGear bridge FMU...")
    run_step("pytest", "-q", "tests/test_flightgear_bridge_fmu.py")

    print("Validating SSD schema...")
    run_step(sys.executable, "-m", "scripts.cli.verify_ssd_xml")

    print("Running reference simulation...")
    run_step(
        sys.executable,
        "-m",
        "scripts.cli.scenarios_simulate",
        "--scenario",
        "resources/scenarios/test_scenario.json",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
