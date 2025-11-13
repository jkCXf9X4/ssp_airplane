# ssp_airplane

This repository tracks an SSP for a loyal-wingman style autonomous drone modeled after MQ-28 / Hellsing CA-1 concepts.

# System requirements:
- MQ-28 class geometry (≈11.7 m length, 7.3 m span) to operate as a loyal wingman
- Conventional turbofan propulsion with generator support for avionics
- Accepts pilot-style (game/simulator) control inputs while still supporting an onboard autopilot
- Optimization focuses on range, loiter/escort scenarios, payload configuration, and now tracks orientation/location states for scenario planning

# Architecture
The architecture is captured as SysML v2 textual notation split across:

- `architecture/aircraft_architecture.sysml` – package metadata and requirements
- `architecture/data_definitions.sysml` – all structured payload definitions
- `architecture/part_definitions.sysml` – the block/port declarations
- `architecture/system_connections.sysml` – all `connect` statements

`scripts/sysml_loader.py` stitches these sections together for [PySysML2](https://github.com/DAF-Digital-Transformation-Office/PySysML2) so the package remains the single source of truth for composition, payload schemas, and connectivity.

## Components

The system is defined on a high level of abstraction with low fidelity models
It contains models for:
 - composite airframe
 - adaptive wing system
 - turbofan propulsion module
 - mission computer with manual + autonomy inputs plus orientation/location tracking
 - optional autopilot module
 - power distribution system
 - control interface for HOTAS / gamepad style inputs

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
