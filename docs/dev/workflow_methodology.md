# Workflow Methodology

This page is for maintainers working on repository structure, build flow, and tool ownership.

The repository uses three phases with explicit handoff points.

## Phase 1: Generate

Python owns generation of architecture-derived artifacts and semantic verification.

Inputs:

- `architecture/`
- repository configuration and static resources as needed

Outputs:

- `generated/`

Typical commands:

```bash
. venv/bin/activate && python -m scripts.cli.artifacts_export
. venv/bin/activate && python -m scripts.cli.verify_modelica_variables
. venv/bin/activate && python -m scripts.cli.verify_model_equations
```

Rules:

- Python may generate SSDs, headers, model descriptions, interface definitions, and architecture snapshots.
- Python should not be the canonical packaging path for distributable FMUs or the baseline SSP.

## Phase 2: Build And Package

CMake owns compilation and packaging of distributable simulation artifacts.

Inputs:

- `models/`
- `generated/`

Outputs:

- compiled native libraries and Modelica FMUs under the build tree
- packaged FMUs
- packaged SSP

Typical commands:

```bash
cmake -S . -B build/cmake
cmake --build build/cmake
```

Rules:

- CMake is the canonical path for building Modelica FMUs and native binaries.
- CMake is the canonical path for packaging FMUs and the baseline SSP.
- Python packaging commands remain compatibility tooling for direct scripting and migration cases.

## Phase 3: Simulate And Analyze

Python owns scenario preparation, `ssp4sim` execution, and result analysis.

Inputs:

- packaged SSP
- scenario JSON files

Outputs:

- `build/results/`

Typical commands:

```bash
. venv/bin/activate && python -m scripts.cli.scenarios_prepare_waypoints --scenario resources/scenarios/test_scenario.json
. venv/bin/activate && python -m scripts.cli.scenarios_package_ssp --parameter-set build/results/test_scenario_waypoints.ssv --scenario-stem test_scenario
. venv/bin/activate && python -m scripts.cli.scenarios_write_config --prepared-ssp build/results/test_scenario_run/test_scenario.ssp --result-file build/results/test_scenario_results.csv --stop-time 120
. venv/bin/activate && python -m scripts.cli.scenarios_run_ssp4sim --config-path build/results/config.json
. venv/bin/activate && python -m scripts.cli.scenarios_evaluate_results --scenario resources/scenarios/test_scenario.json --results-csv build/results/test_scenario_results.csv
. venv/bin/activate && python -m scripts.cli.analyze_plot --results-csv build/results/test_scenario_results.csv --scenario resources/scenarios/test_scenario.json --plot-path
```

Rules:

- Simulations should run through the `ssp4sim` Python module.
- Scenario-specific parameter injection belongs to run preparation, not to the baseline packaging phase.
- A simulation run may derive a temporary run-specific SSP from the packaged baseline SSP.

## Ownership Summary

- Python owns `architecture/ -> generated/`
- CMake owns `generated/ + models/ -> packaged FMUs + packaged SSP`
- Python owns `packaged SSP + scenario -> results`

## Edit Guidance

When changing workflows:

- keep generation logic under `scripts/lib/artifacts/sysml_export/`
- keep build and packaging logic in CMake once CMake targets exist
- keep simulation and result processing under `scripts/lib/scenarios/` and `scripts/lib/results/`
- avoid moving simulation concerns into build scripts
- avoid moving packaging concerns back into Python unless the change is explicitly transitional

## Compatibility State

The repository still contains Python commands for packaging native FMUs and the SSP.

Treat them as compatibility tooling:

- they exist for direct scripting and migration cases
- they are not the preferred workflow for normal builds
- new packaging behavior should favor CMake targets
