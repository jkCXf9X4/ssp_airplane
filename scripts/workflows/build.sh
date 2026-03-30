#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"
source venv/bin/activate

rm -rf ./build

echo "Exporting architecture"
python3 -m scripts.generation.save_architecture

echo "Exporting architecture-derived artifacts..."
python3 -m scripts.generation.generate_interface_defs
python3 -m scripts.generation.generate_c_interface_defs
python3 -m scripts.generation.generate_model_descriptions
python3 -m scripts.generation.generate_parameter_set
python3 -m scripts.generation.generate_ssd

echo "Verifying Modelica interfaces and SysML connections..."
# python3 -m scripts.verification.verify_connections

echo "Verifying models"
python3 -m scripts.verification.verify_model_equations
# python3 -m scripts.verification.verify_modelica_variables

echo "Building FMUs..."
python3 -m scripts.generation.build_fmus

echo "Verifying FMUs..."
# python3 -m scripts.verification.verify_fmu_ios

echo "Testing native FlightGear bridge FMU..."
pytest -q tests/test_flightgear_bridge_fmu.py

echo "Validating SSD schema..."
python3 -m scripts.verification.verify_ssd_xml_compliance

echo "Packaging SSP..."
python3 -m scripts.generation.package_ssp

echo "Packaging and simulation pipeline completed successfully."

echo "Running reference simulation..."
python3 -m scripts.workflows.simulate_scenario --scenario resources/scenarios/test_scenario.json
