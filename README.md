# ssp_airplane

System structure and simulation workflow for an F-16-inspired aircraft model.

The repository combines:

- SysML architecture sources in `architecture/`
- standalone Modelica FMU packages in `models/`
- native FMU implementations in `models/*/native/`
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

Run the full architecture-first workflow:

```bash
. venv/bin/activate
./scripts/workflows/build.sh
```

The default workflow is:

1. export all architecture-derived artifacts
2. build all Modelica and native FMUs
3. package the SSP
4. run the reference simulation

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
| Run scenario | `python3 -m scripts.workflows.simulate_scenario --scenario resources/scenarios/test_scenario.json` |
| Validate SSD XML | `python3 -m scripts.verification.verify_ssd_xml_compliance --ssd generated/SystemStructure.ssd` |
| Run tests | `pytest` |

## Notes

- Use the virtual environment for all helper modules.
- `scripts.generation.build_fmus` builds the standalone Modelica FMUs and any native FMUs discovered from the architecture/model layout.
- `scripts.generation.build_native_fmus` derives native build targets from `architecture/` plus `models/<snake_case_part>/native/`, stages the generated headers/model descriptions automatically, and packages each discovered native FMU without hard-coded source file lists.
- The FlightGear bridge uses the repo-local FMI 2.0 headers in `3rd_party/fmi_headers/`.
