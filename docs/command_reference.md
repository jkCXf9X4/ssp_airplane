# Command Reference

This page is reference material. If you are new to the repository, start with `getting_started.md`.

Methodology summary:

- Python is the canonical tool for generating architecture-derived artifacts and for running simulations with `ssp4sim`.
- CMake is the canonical tool for building and packaging FMUs and the baseline SSP.
- Python packaging commands listed below are compatibility commands, not the preferred workflow.

## Setup

| Task | Command |
| --- | --- |
| Minimal setup for reuse and plotting | `python3.11 -m venv venv && . venv/bin/activate && python -m pip install --upgrade pip && python -m pip install -r requirements.txt` |
| Source build prerequisites | `sudo apt-get update && sudo apt-get install -y cmake build-essential openmodelica` |

## Common workflows

| Task | Command |
| --- | --- |
| Prepare scenario waypoints | `. venv/bin/activate && python -m scripts.cli.scenarios_prepare_waypoints --scenario resources/scenarios/test_scenario.json` |
| Package scenario SSP | `. venv/bin/activate && python -m scripts.cli.scenarios_package_ssp --parameter-set build/results/test_scenario_waypoints.ssv --scenario-stem test_scenario` |
| Write simulator config | `. venv/bin/activate && python -m scripts.cli.scenarios_write_config --prepared-ssp build/results/test_scenario_run/test_scenario.ssp --result-file build/results/test_scenario_results.csv --stop-time 120` |
| Run simulator | `. venv/bin/activate && python -m scripts.cli.scenarios_run_ssp4sim --config-path build/results/config.json` |
| Evaluate results against requirements | `. venv/bin/activate && python -m scripts.cli.scenarios_evaluate_results --scenario resources/scenarios/test_scenario.json --results-csv build/results/test_scenario_results.csv` |
| Configure source builds under `build/cmake` | `cmake -S . -B build/cmake` |
| Build all FMUs from `build/cmake` | `cmake --build build/cmake` |
| Plot a path overlay | `. venv/bin/activate && python -m scripts.cli.analyze_plot --results-csv build/results/test_scenario_results.csv --scenario resources/scenarios/test_scenario.json --plot-path` |
| Run tests | `. venv/bin/activate && pytest` |

## Generation and packaging

| Task | Command |
| --- | --- |
| Export architecture-derived artifacts | `. venv/bin/activate && python -m scripts.cli.artifacts_export` |
| Verify SysML versus Modelica interfaces | `. venv/bin/activate && python -m scripts.cli.verify_modelica_variables` |
| Verify Modelica equations | `. venv/bin/activate && python -m scripts.cli.verify_model_equations` |
| Build and package all FMUs plus the baseline SSP | `cmake --build build/cmake` |
| Package all simulation artifacts explicitly | `cmake --build build/cmake --target package_simulation_artifacts` |
| Build Modelica FMUs only | `cmake --build build/cmake --target adaptive_wing_system_fmu autopilot_module_fmu composite_airframe_fmu control_interface_fmu environment_fmu fuel_system_fmu input_output_fmu mission_computer_fmu turbofan_propulsion_fmu` |
| Build the native shared library only | `cmake --build build/cmake --target FlightGearBridge` |
| Package the native bridge FMU from CMake outputs | `cmake --build build/cmake --target FlightGearBridge_fmu` |
| Package the baseline SSP from built FMUs | `cmake --build build/cmake --target aircraft_ssp` |

## Verification

| Task | Command |
| --- | --- |
| Validate SSD XML | `. venv/bin/activate && python -m scripts.cli.verify_ssd_xml --ssd generated/SystemStructure.ssd` |
| Check autopilot waypoint math | `. venv/bin/activate && pytest tests/test_autopilot_logic.py` |
| Check native bridge FMU packaging | `. venv/bin/activate && pytest -q tests/test_flightgear_bridge_fmu.py` |
