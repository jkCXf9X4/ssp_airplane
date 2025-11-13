#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"
source venv/bin/activate

echo "Exporting architecture"
python3 scripts/save_architecture.py

echo "Generating Modelica interfaces..."
python3 scripts/generate_interface_defs.py

echo "Verifying Modelica interfaces and SysML connections..."
python3 scripts/verify_connections.py

echo "Verifying models"
python3 scripts/verify_model_equations.py

echo "Building FMUs..."
python3 scripts/build_fmus.py

echo "Regenerating SSD..."
python3 scripts/generate_ssd.py

echo "Validating SSD schema..."
python scripts/verify_ssd_xml_compliance.py

echo "Packaging SSP..."
python3 scripts/package_ssp.py

echo "Running pytest scenarios..."
pytest -q

echo "Build pipeline completed successfully."

echo "Simulate scenario!"
python3 scripts/simulate_scenario.py --scenario build/scenarios/test_scenario.json --ssp build/ssp/wingman_drone.ssp

