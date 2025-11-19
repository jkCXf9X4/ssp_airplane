# ssp_airplane

This repository tracks an SSP for an F-16 Fighting Falcon inspired single-seat multirole fighter, re-parameterized from the earlier loyal-wingman concept.

# Getting started

- Ensure Python 3.11+ and ssp4sim runtime are available. The Python API for ssp4sim is installed via the editable dependency in `requirements.txt` (points to `../ssp4sim/build/public/python_api` by default).
- Create a virtual environment and install deps:
  ```
  python3 -m venv venv
  venv/bin/pip install -r requirements.txt
  ```
- Always use the virtual environment when running helper modules to avoid missing `pyssp4sim` (`python3 -m scripts.<module>` or `source venv/bin/activate` first).
- Prebuilt SSPs live in `build/ssp/`; the default is `build/ssp/aircraft.ssp`.
- Curated mission scenarios live in `resources/scenarios/` (see `docs/use_cases.md` for requirement linkage).
- Regenerate the SSD with parameter connectors plus a fresh default parameter set via:
  - `python3 -m scripts.generation.generate_ssd --output generated/SystemStructure.ssd`
  - `python3 -m scripts.generation.generate_parameter_set --output generated/parameters.ssv`
  These outputs expose every component attribute as a parameter connector so you can bind SSVs in OMSimulator or CI runs without hand-editing XML.

## Script catalog

Scripts are grouped by intent under `scripts/`:

- `scripts/generation/` – emit SysML-derived artifacts (architecture JSON, SSD, parameter sets, terminals, Modelica interfaces, scenarios).
- `scripts/verification/` – statically inspect SysML connectors, FMU I/O, Modelica definitions, and SSD XML compliance.
- `scripts/workflows/` – orchestration utilities for building FMUs, packaging SSPs, and simulating mission scenarios.
- `scripts/utils/` – shared helpers such as the SysML v2 parser.

Common entry points:

| Task | Command | Purpose |
| --- | --- | --- |
| Merge SysML sections into JSON | `python3 -m scripts.generation.save_architecture --output generated/arch_def.json` | Creates a single architecture snapshot for downstream tooling. |
| Generate SSD and parameter set | `python3 -m scripts.generation.generate_ssd` / `python3 -m scripts.generation.generate_parameter_set` | Produces SSP-compliant descriptions with parameter connectors. |
| Build FMUs via OpenModelica | `python3 -m scripts.generation.build_fmus --omc omc` | Exports each Modelica component into `build/fmus`. |
| Package SSP archive | `python3 -m scripts.generation.package_ssp --fmu-dir build/fmus --ssd generated/SystemStructure.ssd` | Bundles FMUs and SSD into `build/ssp/aircraft.ssp`. |
| Simulate a scenario | `python3 -m scripts.workflows.simulate_scenario --scenario build/scenarios/test_scenario.json` | Runs OMSimulator (or reuses results) and emits summaries/plots. |
| Verify architecture and FMUs | `python3 -m scripts.verification.verify_connections`, `python3 -m scripts.verification.verify_fmu_ios`, etc. | Guards against connector, FMU, and SSD regressions. |


# Architecture
The architecture is captured as SysML v2 textual notation split across:

- `architecture/architecture.sysml` – package metadata and part definitions
- `architecture/data_definitions.sysml` – all structured payload definitions
- `architecture/system_connections.sysml` – all `connect` statements
- `architecture/requirements.sysml` – top-level capability requirements
- `architecture/simulation.sysml` – top-level simulation arch requirements and design choices

## Components

The system is defined on a high level of abstraction with low fidelity models
It contains models for:
 - F-16 composite/aluminum airframe
 - cropped-delta wing and control surfaces
 - F100/F110 turbofan propulsion module
 - mission computer with HOTAS, stores management, and flight control exports
 - autopilot module, to navigate around points in space
 - power distribution system sized for 270 VDC generation
 - cockpit HOTAS interface
 - telemetry sink (`InputOutput`) that taps the environment state, autopilot outputs (pilot command + mission status), and flight status for logging and validation

# Build

all sub-systems are to be exported into into Functional mockup units, FMUs. Packaged into a SSP for executing the simulation in the optimization loop.

## Models

All subsystem FMUs are generated from the `models/Aircraft` Modelica package using the OpenModelica compiler (`omc`).

## The SSD

The ssd is build by a script that parses the architecture and creates a system structure definition (SSD)

## SSP 

FMUs and SSD are packaged into a zip file, renamed *.ssp


# Simulation 

Utilize OMSimulator as simulation engine, via python

## Scenario workflow

1. Generate mission waypoints via `python3 -m scripts.generation.generate_scenario --output build/scenarios/demo.json`.
2. Rebuild the FMUs/SSD/SSP with the helper scripts whenever the models change.
3. Run `python3 -m scripts.workflows.simulate_scenario --scenario build/scenarios/demo.json` to execute OMSimulator or post-process existing results (`--reuse-results`) and optional custom `--ssp` or `--stop-time`.
4. Execute `pytest` to run the scenario-based unit tests and validate requirement coverage (range, fuel exhaustion).

## Autopilot waypoint tracking

- Waypoints are injected into `AutopilotModule` as local `x/y/z` kilometers (`waypointX_km[]/waypointY_km[]/waypointZ_km[]`); `simulate_scenario.py` emits an SSV parameter set for each scenario so the FMU receives the route automatically.
- The autopilot computes a heading and altitude error toward the active waypoint directly in this grid, advancing once the aircraft is within `waypointProximity_km` (10 km default), updating `MissionStatus` for logging and requirement evaluation.
- You can sanity-check the navigation math without rebuilding FMUs by running `pytest tests/test_autopilot_logic.py`, which mirrors the Modelica heading/error calculations.

### Simulation and results

- `scripts.workflows.simulate_scenario` always produces a timeseries CSV at `build/results/<scenario>_results.csv` and a requirement-focused summary at `build/results/<scenario>_summary.json`.
- Pass `--reuse-results` to skip OMSimulator when a CSV already exists (useful in CI and for quick requirement checks).
- Summaries include pass/fail for REQ_Performance/REQ_Fuel/REQ_Control/REQ_Mission/REQ_Propulsion plus evidence strings and key metrics (max Mach, g-load, fuel used, stores available, thrust).
- Waypoint-tracking metrics are computed from simulated local `x/y` traces (`waypoint_miss_*`, `waypoint_hits`, `waypoints_followed`), so you can verify path following directly from the summary.
- See `docs/results_and_evaluation.md` for the metric/summary fields and how to interpret them.
- Pre-generated data stored under `resources/scenarios/test_scenario.json` and `resources/references/test_scenario_results.csv` is copied into `build/` on demand so tests can run without a fresh simulation.
- Waypoints are exported as a comma-separated string to `build/results/<scenario>_waypoints.txt` (format: `x_km,y_km,z_km,...`) that feeds the Autopilot parameter set via `stringToRealVector`.
- Add `--plot` to emit `build/results/<scenario>_path.png`, overlaying simulated local X/Y traces against mission waypoints.

## Verification helpers

- `python3 -m scripts.verification.verify_modelica_variables`
- `python3 -m scripts.verification.verify_connections`
- `python3 -m scripts.verification.verify_model_equations --omc /path/to/omc`
- `python3 -m scripts.workflows.simulate_scenario --scenario ... --ssp ...`


# File disposition

architecture/ - the system architecture 
models/ - all models are located here
scripts/ - Python package containing `generation/`, `verification/`, `workflows/`, and shared `utils/`


## Results and requirement evaluation

- OMSimulator outputs a full timeseries CSV per scenario at `build/results/<scenario>_results.csv`.
- Post-processing writes `build/results/<scenario>_summary.json` with requirement evaluations (REQ_Performance, REQ_Fuel, REQ_Control, REQ_Mission, REQ_Propulsion) and key metrics such as max Mach, g-load, fuel used, and available stores.
- Use `python3 -m scripts.workflows.simulate_scenario --scenario <path> --results-dir build/results --reuse-results` to evaluate an existing OMS run without re-simulating. Sample data is kept under `resources/scenarios/test_scenario.json` and `resources/references/test_scenario_results.csv` and mirrored into `build/` when missing.

# Development

The tracking of tasks for this project is defined in the file todo.md
