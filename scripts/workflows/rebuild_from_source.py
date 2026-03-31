#!/usr/bin/env python3
"""Run the full architecture-first rebuild workflow."""
from __future__ import annotations

import argparse
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
    run_step(sys.executable, "-m", "scripts.cli.artifacts", "export")

    print("Verifying Modelica interfaces...")
    run_step(sys.executable, "-m", "scripts.cli.verify", "modelica-variables")

    print("Verifying models...")
    run_step(sys.executable, "-m", "scripts.cli.verify", "model-equations")

    print("Building FMUs...")
    run_step(sys.executable, "-m", "scripts.cli.artifacts", "build-fmus")

    print("Testing native FlightGear bridge FMU...")
    run_step("pytest", "-q", "tests/test_flightgear_bridge_fmu.py")

    print("Validating SSD schema...")
    run_step(sys.executable, "-m", "scripts.cli.verify", "ssd-xml")

    print("Packaging SSP...")
    run_step(sys.executable, "-m", "scripts.cli.artifacts", "package-ssp")

    print("Running reference simulation...")
    run_step(
        sys.executable,
        "-m",
        "scripts.cli.scenarios",
        "simulate",
        "--scenario",
        "resources/scenarios/test_scenario.json",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
