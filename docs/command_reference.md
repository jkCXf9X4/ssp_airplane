# Command Reference

This page is reference material. If you are new to the repository, start with `getting_started.md`.

## Setup

| Task | Command |
| --- | --- |
| Minimal setup for reuse and plotting | `python3.11 -m venv venv && . venv/bin/activate && python -m pip install --upgrade pip && python -m pip install -r requirements.txt` |
| Source build prerequisites | `sudo apt-get update && sudo apt-get install -y cmake build-essential openmodelica` |

## Common workflows

| Task | Command |
| --- | --- |
| Reuse existing results | `python3 -m scripts.cli.scenarios_simulate --scenario resources/scenarios/test_scenario.json --reuse-results` |
| Configure source builds under `build/cmake` | `cmake -S . -B build/cmake` |
| Build all FMUs from `build/cmake` | `cmake --build build/cmake` |
| Plot a path overlay | `python3 -m scripts.cli.analyze_plot --results-csv build/results/test_scenario_results.csv --scenario resources/scenarios/test_scenario.json --plot-path` |
| Run tests | `pytest` |

## Generation and packaging

| Task | Command |
| --- | --- |
| Build Modelica FMUs | `cmake --build build/cmake --target adaptive_wing_system_fmu autopilot_module_fmu composite_airframe_fmu control_interface_fmu environment_fmu fuel_system_fmu input_output_fmu mission_computer_fmu turbofan_propulsion_fmu` |
| Build the native shared library only | `cmake --build build/cmake --target FlightGearBridge` |
| Package the native FMU | `python3 -m scripts.cli.artifacts_package_native_fmus --output-dir build/fmus --build-root build/native` |
| Package SSP | `python3 -m scripts.cli.artifacts_package_ssp --fmu-dir build/fmus --ssd generated/SystemStructure.ssd --output build/ssp/aircraft.ssp` |

## Verification

| Task | Command |
| --- | --- |
| Validate SSD XML | `python3 -m scripts.cli.verify_ssd_xml --ssd generated/SystemStructure.ssd` |
| Check autopilot waypoint math | `pytest tests/test_autopilot_logic.py` |
| Check FlightGear bridge FMU packaging | `pytest -q tests/test_flightgear_bridge_fmu.py` |
