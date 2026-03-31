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
| Reuse existing results | `python3 -m scripts.workflows.simulate_scenario --scenario resources/scenarios/test_scenario.json --reuse-results` |
| Run the full architecture-first workflow | `./scripts/workflows/build.sh` |
| Plot a path overlay | `python3 -m scripts.plot_results --results-csv build/results/test_scenario_results.csv --scenario resources/scenarios/test_scenario.json --plot-path` |
| Run tests | `pytest` |

## Generation and packaging

| Task | Command |
| --- | --- |
| Export all architecture-derived artifacts | `python3 -m scripts.generation.export_artifacts` |
| Export architecture snapshot | `python3 -m scripts.generation.save_architecture --output generated/arch_def.json` |
| Generate Modelica interfaces | `python3 -m scripts.generation.generate_interface_defs` |
| Generate model descriptions with upstream tooling | `python3 -m pyssp_sysml2.cli generate fmi --architecture architecture --composition AircraftComposition --output-dir generated/model_descriptions` |
| Generate SSD with upstream tooling | `python3 -m pyssp_sysml2.cli generate ssd --architecture architecture --composition AircraftComposition --output generated/SystemStructure.ssd` |
| Generate parameter set with upstream tooling | `python3 -m pyssp_sysml2.cli generate ssv --architecture architecture --composition AircraftComposition --output generated/parameters.ssv` |
| Build FMUs | `python3 -m scripts.generation.build_fmus --omc-path omc` |
| Build native FMUs only | `python3 -m scripts.generation.build_native_fmus --output-dir build/fmus` |
| Package SSP | `python3 -m scripts.generation.package_ssp --fmu-dir build/fmus --ssd generated/SystemStructure.ssd --output build/ssp/aircraft.ssp` |

## Verification

| Task | Command |
| --- | --- |
| Validate SSD XML | `python3 -m scripts.verification.verify_ssd_xml_compliance --ssd generated/SystemStructure.ssd` |
| Check autopilot waypoint math | `pytest tests/test_autopilot_logic.py` |
| Check FlightGear bridge FMU packaging | `pytest -q tests/test_flightgear_bridge_fmu.py` |
