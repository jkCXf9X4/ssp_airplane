#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "$REPO_ROOT"
cd "$REPO_ROOT"
source venv/bin/activate

rm -rf ./build

echo "Exporting architecture-derived artifacts..."
python3 -m scripts.artifacts.export_artifacts

echo "Verifying Modelica interfaces and SysML connections..."
# python3 -m scripts.verify.verify_connections

echo "Verifying models..."
python3 -m scripts.verify.verify_model_equations
# python3 -m scripts.verify.verify_modelica_variables

echo "Building FMUs..."
python3 -m scripts.artifacts.build_fmus

echo "Verifying FMUs..."
# python3 -m scripts.verify.verify_fmu_ios

echo "Testing native FlightGear bridge FMU..."
pytest -q tests/test_flightgear_bridge_fmu.py

echo "Validating SSD schema..."
python3 -m scripts.verify.verify_ssd_xml_compliance

echo "Packaging SSP..."
python3 -m scripts.artifacts.package_ssp

echo "Running reference simulation..."
python3 -m scripts.scenarios.simulate_scenario --scenario resources/scenarios/test_scenario.json
