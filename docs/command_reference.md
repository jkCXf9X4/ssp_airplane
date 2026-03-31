# Command Reference

This page is reference material. If you are new to the repository, start with `getting_started.md`.

## Setup

| Task | Command |
| --- | --- |
| Minimal setup for reuse and plotting | `python3.11 -m venv venv && . venv/bin/activate && python -m pip install --upgrade pip && python -m pip install -r requirements.txt` |
| Full developer setup with vendored modules | `git submodule update --init --recursive && python3.11 -m venv venv && . venv/bin/activate && python -m pip install --upgrade pip && python -m pip install -r requirements_local.txt` |

## Common workflows

| Task | Command |
| --- | --- |
| Reuse existing results | `python3 -m scripts.cli.scenarios_simulate --scenario resources/scenarios/test_scenario.json --reuse-results` |
| Run the full architecture-first workflow | `python3 -m scripts.workflows.rebuild_from_source` |
| Plot a path overlay | `python3 -m scripts.cli.analyze_plot --results-csv build/results/test_scenario_results.csv --scenario resources/scenarios/test_scenario.json --plot-path` |
| Run tests | `pytest` |

## Generation and packaging

| Task | Command |
| --- | --- |
| Export all architecture-derived artifacts | `python3 -m scripts.cli.artifacts_export` |
| Export architecture snapshot | `python3 -m scripts.cli.artifacts_save_architecture --output generated/arch_def.json` |
| Generate Modelica interfaces | `python3 -m scripts.cli.artifacts_generate_interface_defs` |
| Generate model descriptions with upstream tooling | `python3 -m pyssp_sysml2.cli generate fmi --architecture architecture --composition AircraftComposition --output-dir generated/model_descriptions` |
| Generate SSD with upstream tooling | `python3 -m pyssp_sysml2.cli generate ssd --architecture architecture --composition AircraftComposition --output generated/SystemStructure.ssd` |
| Generate parameter set with upstream tooling | `python3 -m pyssp_sysml2.cli generate ssv --architecture architecture --composition AircraftComposition --output generated/parameters.ssv` |
| Build Modelica FMUs | `python3 -m scripts.cli.artifacts_build_modelica_fmus --omc-path omc` |
| Build native shared libraries only | `python3 -m scripts.cli.artifacts_build_native_fmus --build-root build/native` |
| Package native FMUs | `python3 -m scripts.cli.artifacts_package_native_fmus --output-dir build/fmus --build-root build/native` |
| Package SSP | `python3 -m scripts.cli.artifacts_package_ssp --fmu-dir build/fmus --ssd generated/SystemStructure.ssd --output build/ssp/aircraft.ssp` |

## Verification

| Task | Command |
| --- | --- |
| Validate SSD XML | `python3 -m scripts.cli.verify_ssd_xml --ssd generated/SystemStructure.ssd` |
| Check autopilot waypoint math | `pytest tests/test_autopilot_logic.py` |
| Check FlightGear bridge FMU packaging | `pytest -q tests/test_flightgear_bridge_fmu.py` |
