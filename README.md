# ssp_airplane

System structure and simulation workflow for an F-16-inspired aircraft model.

The repository combines:

- SysML architecture sources in `architecture/`
- standalone Modelica FMU packages in `models/`
- native FMU implementations in `models/*/native/`
- Python generation, verification, and workflow tooling in `scripts/`

## Documentation Map

- Setup, build, and common commands: this README
- Mission scenarios and requirement traceability: `docs/use_cases.md`
- Simulation outputs and result interpretation: `docs/results_and_evaluation.md`
- Autopilot waypoint behavior and quick checks: `docs/autopilot.md`
- FlightGear bridge architecture decision: `docs/flightgear_bridge_decision.md`
- FlightGear bridge integration details: `docs/flightgear_bridge.md`
- FlightGear bridge current status: `docs/flightgear_bridge_status.md`

## Prerequisites

- Python 3.11+
- `cmake`
- a C++17 compiler
- OpenModelica (`omc`)

Typical Debian/Ubuntu setup:

```bash
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv cmake build-essential openmodelica
```

## Setup

Choose one setup path:

### Minimal user setup

Use this path if you want to inspect scenarios, reuse canned results, run most Python tests, or post-process existing simulation outputs.

```bash
python3.11 -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Full developer setup

Use this path if you want the repository to use the vendored modules in `3rd_party/` and match the architecture-first workflow used by the build scripts.

```bash
git submodule update --init --recursive
python3.11 -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements_local.txt
```

## Common Workflows

### Reuse existing reference results

This is the lowest-friction way to explore the repository after setup:

```bash
. venv/bin/activate
python3 -m scripts.workflows.simulate_scenario \
  --scenario resources/scenarios/test_scenario.json \
  --reuse-results
```

This reuses the reference CSV when present and writes derived outputs such as summary JSON and waypoint parameter files into `build/results/`.

## Quickstart

### Full architecture-first workflow

Run this when you want to regenerate artifacts, rebuild FMUs, package the SSP, and execute the reference scenario from scratch.

```bash
. venv/bin/activate
./scripts/workflows/build.sh
```

What `./scripts/workflows/build.sh` does:

1. export all architecture-derived artifacts
2. run verification scripts
3. build all Modelica and native FMUs
4. package the SSP
5. run the reference simulation

The script expects:

- a local virtual environment at `venv/`
- the Python dependencies already installed
- OpenModelica available as `omc`
- permission to delete and recreate `build/`

The architecture export stage is also available directly:

```bash
python3 -m scripts.generation.export_artifacts
```

Main outputs:

- SSP archive: `build/ssp/aircraft.ssp`
- FMUs: `build/fmus/*.fmu`
- generated SSD: `generated/SystemStructure.ssd`
- generated model descriptions: `generated/model_descriptions/*/modelDescription.xml`
- scenario results: `build/results/*`

## Common Commands

| Task | Command |
| --- | --- |
| Export all architecture-derived artifacts | `python3 -m scripts.generation.export_artifacts` |
| Export architecture snapshot | `python3 -m scripts.generation.save_architecture --output generated/arch_def.json` |
| Generate Modelica interfaces | `python3 -m scripts.generation.generate_interface_defs` |
| Generate model descriptions | `python3 -m scripts.generation.generate_model_descriptions` |
| Generate SSD | `python3 -m scripts.generation.generate_ssd --output generated/SystemStructure.ssd` |
| Generate parameter set | `python3 -m scripts.generation.generate_parameter_set --output generated/parameters.ssv` |
| Build FMUs | `python3 -m scripts.generation.build_fmus --omc-path omc` |
| Build native FMUs discovered from the architecture | `python3 -m scripts.generation.build_native_fmus --output-dir build/fmus` |
| Package SSP | `python3 -m scripts.generation.package_ssp --fmu-dir build/fmus --ssd generated/SystemStructure.ssd --output build/ssp/aircraft.ssp` |
| Run scenario from source scenario file | `python3 -m scripts.workflows.simulate_scenario --scenario resources/scenarios/test_scenario.json` |
| Reuse existing scenario results without re-running `ssp4sim` | `python3 -m scripts.workflows.simulate_scenario --scenario resources/scenarios/test_scenario.json --reuse-results` |
| Plot a reused or generated scenario result | `python3 -m scripts.plot_results --results-csv build/results/test_scenario_results.csv --scenario resources/scenarios/test_scenario.json --plot-path` |
| Validate SSD XML | `python3 -m scripts.verification.verify_ssd_xml_compliance --ssd generated/SystemStructure.ssd` |
| Run tests | `pytest` |

## Notes

- Use the virtual environment for all helper modules.
- `requirements.txt` is sufficient for most Python-side exploration; `requirements_local.txt` is the better fit when working on the bundled dependencies in `3rd_party/`.
- `scripts.generation.build_fmus` builds the standalone Modelica FMUs and any native FMUs discovered from the architecture/model layout.
- `scripts.generation.build_native_fmus` derives native build targets from `architecture/` plus `models/<snake_case_part>/native/`, stages the generated headers/model descriptions automatically, and packages each discovered native FMU without hard-coded source file lists.
- The FlightGear bridge uses the repo-local FMI 2.0 headers in `3rd_party/fmi_headers/`.
