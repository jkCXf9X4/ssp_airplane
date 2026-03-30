# ssp_airplane

System structure and simulation workflow for an F-16-inspired aircraft model.

The repository combines:

- SysML architecture sources in `architecture/`
- standalone Modelica FMU packages in `models/`
- native bridge code in `models/flightgear_bridge/native/`
- Python generation, verification, and workflow tooling in `scripts/`

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

Standard dependency install:

```bash
python3.11 -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Local dependency setup for vendored modules in `3rd_party/`:

```bash
git submodule update --init --recursive
python3.11 -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements_local.txt
```

## Quickstart

Build the generated artifacts, FMUs, SSP archive, and run the reference scenario:

```bash
. venv/bin/activate
./scripts/workflows/build.sh
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
| Export architecture snapshot | `python3 -m scripts.generation.save_architecture --output generated/arch_def.json` |
| Generate Modelica interfaces | `python3 -m scripts.generation.generate_interface_defs` |
| Generate model descriptions | `python3 -m scripts.generation.generate_model_descriptions` |
| Generate SSD | `python3 -m scripts.generation.generate_ssd --output generated/SystemStructure.ssd` |
| Generate parameter set | `python3 -m scripts.generation.generate_parameter_set --output generated/parameters.ssv` |
| Build FMUs | `python3 -m scripts.generation.build_fmus --omc-path omc` |
| Build native bridge FMU only | `python3 -m scripts.generation.build_native_fmus --output build/fmus/Aircraft_FlightGearBridge.fmu` |
| Package SSP | `python3 -m scripts.generation.package_ssp --fmu-dir build/fmus --ssd generated/SystemStructure.ssd --output build/ssp/aircraft.ssp` |
| Run scenario | `python3 -m scripts.workflows.simulate_scenario --scenario resources/scenarios/test_scenario.json` |
| Validate SSD XML | `python3 -m scripts.verification.verify_ssd_xml_compliance --ssd generated/SystemStructure.ssd` |
| Run tests | `pytest` |

## Notes

- Use the virtual environment for all helper modules.
- `scripts.generation.build_fmus` builds the standalone Modelica FMUs and the native `Aircraft_FlightGearBridge.fmu`.
- `scripts.generation.build_native_fmus` now stages `modelDescription.xml` from `scripts.generation.generate_model_descriptions` so the native bridge stays aligned with the shared SysML-driven generation flow.
- The FlightGear bridge uses the repo-local FMI 2.0 headers in `3rd_party/fmi_headers/`.
