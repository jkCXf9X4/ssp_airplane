#!/usr/bin/env python3
"""Run the full architecture-first rebuild workflow."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from scripts.lib.paths import REPO_ROOT


def run_step(*args: str) -> None:
    subprocess.run(args, cwd=REPO_ROOT, check=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)

    print("Exporting architecture-derived artifacts...")
    run_step(sys.executable, "-m", "scripts.cli.artifacts_export")

    print("Verifying Modelica interfaces...")
    run_step(sys.executable, "-m", "scripts.cli.verify_modelica_variables")

    print("Verifying models...")
    run_step(sys.executable, "-m", "scripts.cli.verify_model_equations")

    print("Configuring CMake build...")
    run_step("cmake", ".", f"-DOMC_EXECUTABLE={os.environ.get('OMC', 'omc')}")

    print("Building Modelica FMUs and native shared libraries...")
    run_step("cmake", "--build", ".")

    print("Packaging native FMUs...")
    run_step(sys.executable, "-m", "scripts.cli.artifacts_package_native_fmus")

    print("Testing native FlightGear bridge FMU...")
    run_step("pytest", "-q", "tests/test_flightgear_bridge_fmu.py")

    print("Validating SSD schema...")
    run_step(sys.executable, "-m", "scripts.cli.verify_ssd_xml")

    print("Packaging SSP...")
    run_step(sys.executable, "-m", "scripts.cli.artifacts_package_ssp")

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
