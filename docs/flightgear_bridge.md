# FlightGear bridge integration guide

This document explains how the FlightGear bridge fits into the repository and where to look when working on the integration.

For the architectural rationale, see `docs/flightgear_bridge_decision.md`.
For current implementation status and follow-up work, see `docs/flightgear_bridge_status.md`.

## Bridge responsibilities

The bridge is the adapter between FlightGear and the packaged aircraft SSP. It is responsible for:

- reading aircraft state from the SSP
- writing pilot or manual command values back into the SSP
- converting local `x_km/y_km/z_km` coordinates into a geodetic frame suitable for FlightGear
- mapping FlightGear control channels into the airplane `PilotCommand` structure
- handling manual versus autopilot mode selection without changing the rest of the vehicle architecture

## Model integration

Keep the bridge as a dedicated adapter component rather than placing socket or protocol logic inside airframe or autopilot models.

In this repository, the first concrete implementation is a native FMI 2.0 co-simulation FMU written in C++ for `FlightGearBridge`. That keeps the network logic out of ordinary Modelica equations while preserving the same architectural boundary in the SSP.

## Coordinate and signal mapping

The current aircraft model exposes a local frame:

- `x_km`: north
- `y_km`: east
- `z_km`: up

FlightGear typically expects:

- latitude
- longitude
- altitude
- attitude or orientation values in FlightGear conventions

The bridge therefore needs:

- a reference origin for local-to-geodetic conversion
- orientation and sign-convention mapping
- control normalization between FlightGear inputs and `PilotCommand`

## Repository traceability

The current bridge work connects to these files:

- `models/flightgear_bridge/native/src/FlightGearBridge.cpp`
- `models/flightgear_bridge/native/src/BridgeRuntime.cpp`
- `models/flightgear_bridge/modelica/FlightGearBridgeFMU/FlightGearBridge.mo`
- `models/control_interface/modelica/ControlInterfaceFMU/ControlInterface.mo`
- `models/mission_computer/modelica/MissionComputerFMU/MissionComputer.mo`
- `models/environment/modelica/EnvironmentFMU/Environment.mo`
- `models/input_output/modelica/InputOutputFMU/InputOutput.mo`
- `architecture/aircraft.sysml`
- `scripts/workflows/simulate_scenario.py`

These define the manual-input path, autopilot path, environment state, telemetry taps, and SSP workflow that the bridge depends on.

## Build workflow alignment

The repository remains architecture-first:

1. export generated artifacts from `architecture/`
2. build Modelica and native FMUs
3. package the SSP
4. run the simulation workflow

`scripts.generation.build_native_fmus` follows that contract. Native FMUs are discovered from the architecture composition plus `models/<snake_case_part>/native/`, and their staged `modelDescription.xml` files come from the shared SysML-driven generator instead of local bridge-specific metadata.
