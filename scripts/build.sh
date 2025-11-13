#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "[1/7] Generating Modelica interfaces..."
python3 scripts/generate_interface_defs.py

echo "[2/7] Building FMUs..."
python3 scripts/build_fmus.py

echo "[3/7] Regenerating SSD..."
python3 scripts/generate_ssd.py

echo "[4/7] Validating SSD schema..."
source venv/bin/activate && python scripts/verify_ssd.py

echo "[5/7] Packaging SSP..."
python3 scripts/package_ssp.py

echo "[6/7] Verifying Modelica interfaces and SysML connections..."
python3 scripts/verify_modelica_interfaces.py
python3 scripts/verify_connections.py

echo "[7/7] Running pytest scenarios..."
pytest -q

echo "Build pipeline completed successfully."

echo "Simulate scenario!"
python3 scripts/simulate_scenario.py --scenario build/scenarios/test_scenario.json --ssp build/ssp/wingman_drone.ssp

