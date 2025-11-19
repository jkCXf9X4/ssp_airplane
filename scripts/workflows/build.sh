#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"
source venv/bin/activate

rm -rf ./build

echo "Exporting architecture"
python3 -m scripts.generation.save_architecture

echo "Generating Modelica interfaces..."
python3 -m scripts.generation.generate_interface_defs

echo "Verifying Modelica interfaces and SysML connections..."
python3 -m scripts.verification.verify_connections

echo "Verifying models"
python3 -m scripts.verification.verify_model_equations
python3 -m scripts.verification.verify_modelica_variables

echo "Building FMUs..."
python3 -m scripts.workflows.build_fmus

echo "Verifying FMUs..."
python3 -m scripts.verification.verify_fmu_ios

echo "Regenerating SSD..."
python3 -m scripts.generation.generate_ssd

echo "Validating SSD schema..."
python3 -m scripts.verification.verify_ssd_xml_compliance

echo "Packaging SSP..."
python3 -m scripts.workflows.package_ssp

echo "Running pytest scenarios..."
pytest -q

echo "Build pipeline completed successfully."

echo "Simulate scenario!"
python3 -m scripts.workflows.simulate_scenario --scenario build/scenarios/test_scenario.json
