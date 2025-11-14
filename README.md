# ssp_airplane

This repository tracks an SSP for an F-16 Fighting Falcon inspired single-seat multirole fighter, re-parameterized from the earlier loyal-wingman concept.

# System requirements:
- Maintain F-16 class geometry (≈15 m length, 10 m span) with nine external hardpoints
- Integrate an F100/F110-class augmented turbofan supplying both thrust and electrical power
- Provide full HOTAS pilot inputs, fly-by-wire flight-control channels, and autopilot hold modes
- Support Mach 2 dash performance, 9 g maneuver envelope, and mission computer driven stores management

# Architecture
The architecture is captured as SysML v2 textual notation split across:

- `architecture/drone_architecture.sysml` – package metadata and part definitions
- `architecture/data_definitions.sysml` – all structured payload definitions
- `architecture/system_connections.sysml` – all `connect` statements
- `architecture/requirements.sysml` – top-level capability requirements

`scripts/sysml_loader.py` stitches these sections together for [PySysML2](https://github.com/DAF-Digital-Transformation-Office/PySysML2) so the package remains the single source of truth for composition, payload schemas, and connectivity.

## Components

The system is defined on a high level of abstraction with low fidelity models
It contains models for:
 - F-16 composite/aluminum airframe
 - cropped-delta wing and control surfaces
 - F100/F110 turbofan propulsion module
 - mission computer with HOTAS, stores management, and flight control exports
 - optional autopilot module (attitude/altitude/heading hold)
 - power distribution system sized for 270 VDC generation
 - cockpit HOTAS interface

# Build

all sub-systems are to be exported into into Functional mockup units, FMUs. Packaged into a SSP for executing the simulation in the optimization loop.

## Models

All subsystem FMUs are generated from the `models/WingmanDrone` Modelica package using the OpenModelica compiler (`omc`).

## The SSD

The ssd is build by a script that parses the architecture and creates a system structure definition (SSD)

## SSP 

FMUs and SSD are packaged into a zip file, renamed *.ssp


# Simulation 

Utilize OMSimulator as simulation engine, via python

## Scenario workflow

1. Generate mission waypoints via `python3 scripts/generate_scenario.py --output build/scenarios/demo.json`.
2. Rebuild the FMUs/SSD/SSP with the helper scripts whenever the models change.
3. Run `python3 scripts/simulate_scenario.py --scenario build/scenarios/demo.json` to execute OMSimulator (append `--dry-run` to perform the analytic approximation instead of invoking OMSimulator or pass a custom `--ssp`).
4. Execute `pytest` to run the scenario-based unit tests and validate requirement coverage (range, fuel exhaustion).

## Verification helpers

- `python3 scripts/verify_modelica_interfaces.py`
- `python3 scripts/verify_connections.py`
- `python3 scripts/verify_model_equations.py --omc /path/to/omc`
- `python3 scripts/simulate_scenario.py --scenario ... --ssp ...`


# File disposition

architecture/ - the system architecture 
models/ - all models are located here
scripts/ - all scripts used to build this setup is located here

# Development

The tracking of tasks for this project is defined in the file todo.md
