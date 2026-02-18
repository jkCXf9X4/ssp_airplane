# ssp_airplane

System Structure and simulation workflow for an F-16-inspired aircraft model.  
The repository combines:

- SysML v2 architecture (`architecture/`)
- Modelica subsystem models (`models/Aircraft/`)
- Python tooling to generate SSP artifacts, verify consistency, and run scenarios (`scripts/`)

## Prerequisites

- Python 3.11+
- OpenModelica (`omc`) for FMU export
- `pyssp4sim` runtime (installed by `requirements.txt` via a Linux wheel URL)

## Setup

### Standard setup

```bash
python3.11 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

### Local dependency setup (submodules)

Use this when working on vendored dependencies in `3rd_party/`.

```bash
git submodule update --init --recursive
python3.11 -m venv venv
. venv/bin/activate
pip install -r requirements_local.txt
```

## Quickstart

Build FMUs + SSD + SSP and run the reference scenario:

```bash
. venv/bin/activate
./scripts/workflows/build.sh
```

The build script removes `build/` at the start, then regenerates artifacts.

Main outputs:

- SSP archive: `build/ssp/aircraft.ssp`
- FMUs: `build/fmus/*.fmu`
- Generated SSD: `generated/SystemStructure.ssd`
- Scenario results: `build/results/*`

## Common Commands

| Task | Command |
| --- | --- |
| Merge SysML into JSON | `python3 -m scripts.generation.save_architecture --output generated/arch_def.json` |
| Generate SSD | `python3 -m scripts.generation.generate_ssd --output generated/SystemStructure.ssd` |
| Generate default parameter set | `python3 -m scripts.generation.generate_parameter_set --output generated/parameters.ssv` |
| Export FMUs | `python3 -m scripts.generation.build_fmus --omc-path omc` |
| Validate SSD XML | `python3 -m scripts.verification.verify_ssd_xml_compliance --ssd generated/SystemStructure.ssd` |
| Package SSP | `python3 -m scripts.generation.package_ssp --fmu-dir build/fmus --ssd generated/SystemStructure.ssd --output build/ssp/aircraft.ssp` |
| Run scenario | `python3 -m scripts.workflows.simulate_scenario --scenario resources/scenarios/test_scenario.json` |
| Re-evaluate existing results only | `python3 -m scripts.workflows.simulate_scenario --scenario resources/scenarios/test_scenario.json --reuse-results` |
| Plot scenario outputs | `python3 -m scripts.plot_results --results-csv build/results/test_scenario_results.csv --scenario resources/scenarios/test_scenario.json --plot-path --plot-3d --plot-fuel-altitude` |

## Architecture Inputs

SysML sources currently used by the generators:

- `architecture/aircraft.sysml`
- `architecture/part_definition.sysml`
- `architecture/port_definitions.sysml`
- `architecture/requirements.sysml`
- `architecture/simulation.sysml`

The parser is provided by `py_sysml_v2_cps` (installed from GitHub in `requirements.txt`, or from submodule in local mode).

## Simulation Workflow

1. Create or choose a scenario JSON from `resources/scenarios/` (or generate one with `scripts.generation.generate_scenario`).
2. Build/regenerate SSP artifacts (`./scripts/workflows/build.sh` or individual generation commands).
3. Run:

```bash
python3 -m scripts.workflows.simulate_scenario --scenario resources/scenarios/test_scenario.json
```

`simulate_scenario` writes:

- CSV timeseries: `build/results/<scenario>_results.csv`
- Summary JSON: `build/results/<scenario>_summary.json`
- Waypoint parameter set: `build/results/<scenario>_waypoints.ssv`

Requirement checks in the summary include:

- `REQ_Performance`
- `REQ_Fuel`
- `REQ_Control`
- `REQ_Mission`
- `REQ_Propulsion`

See `docs/results_and_evaluation.md` for metric definitions and interpretation.

## Verification and Tests

Verification helpers:

- `python3 -m scripts.verification.verify_connections`
- `python3 -m scripts.verification.verify_model_equations --omc /path/to/omc`
- `python3 -m scripts.verification.verify_modelica_variables`
- `python3 -m scripts.verification.verify_fmu_ios`
- `python3 -m scripts.verification.verify_ssd_xml_compliance`

Run tests:

```bash
pytest
```

Useful focused test:

```bash
pytest tests/test_autopilot_logic.py
```

## Repository Layout

- `architecture/`: SysML architecture sources
- `models/`: Modelica package used for FMU export
- `scripts/generation/`: SSP/FMU/interface/scenario generation
- `scripts/verification/`: static and artifact checks
- `scripts/workflows/`: end-to-end orchestration
- `resources/scenarios/`: curated scenario JSONs
- `docs/`: supplementary design and evaluation notes
