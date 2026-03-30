# FlightGear interactive bridge

This document records the recommended solution for adding an interactive visual layer and manual steering to the airplane SSP without replacing the existing simulation stack.

## Decision

Use:

- `ssp4sim` as the simulation master and execution engine
- `FlightGear` as the visual frontend and pilot I/O frontend
- a `FlightGearBridge` adapter component integrated into the vehicle simulation architecture
- FlightGear `generic` socket communication for the first implementation

The intent is to preserve the existing SSP/FMU-based aircraft composition while adding a live visualization and manual control path.

For the initial runtime, use the existing `ssp4sim` realtime mode to provide timing. Do not add new synchronization methods to the Python API yet.

## Why this approach

The current airplane package is already organized around:

- subsystem FMUs packaged into a SSP
- `ssp4sim`/`pyssp4sim` execution
- a manual-input path via `ControlInterface`
- an autopilot-input path via `AutopilotModule`
- state generation via `Environment`

This makes it practical to add an adapter around the existing simulation instead of replacing the dynamics stack with a separate game or robotics simulator.

## High-level architecture

The target runtime architecture is:

`FlightGear <-> FlightGearBridge <-> ssp4sim SSP`

Roles:

- `FlightGear` renders the aircraft, camera views, HUD overlays, and captures pilot controls.
- `FlightGearBridge` translates between FlightGear socket messages and simulation signals.
- `ssp4sim` remains the co-simulation master for the packaged aircraft SSP.

## Why use FlightGear generic communication first

FlightGear native protocol slaving is viable, but the initial implementation should prefer `generic` communication because it is easier to control and debug during integration.

Benefits of `generic` communication:

- explicit field selection instead of packing a larger native protocol structure
- easier inspection of values during early integration
- simpler mapping from local simulation signals to frontend properties
- lower coupling while the bridge interface is still evolving

The native protocol can still be adopted later if tighter FlightGear coupling becomes valuable.

## Bridge responsibilities

The bridge functionality must still exist even when it is embedded into the modeled system.

The bridge is responsible for:

- coordinating with the running simulation time
- reading aircraft state from the SSP
- writing pilot/manual command values back into the SSP
- converting local `x_km/y_km/z_km` coordinates into a geodetic frame suitable for FlightGear
- mapping FlightGear control channels into the airplane `PilotCommand` structure
- handling manual/autopilot mode selection without altering the rest of the vehicle architecture

## Recommended model integration

Model the bridge as a dedicated adapter component, for example `FlightGearBridge`, rather than placing socket/protocol logic directly inside the airframe or autopilot models.

The first concrete implementation in this repository uses a dedicated native FMI 2.0 co-simulation FMU written in C++ for `FlightGearBridge`. This keeps the network/socket logic out of ordinary Modelica equations while preserving the same architectural boundary in the SSP.

Recommended signal responsibilities:

- inputs from simulation:
  - environment position
  - environment orientation
  - flight status
  - optional mission status / fuel / engine state for overlay and diagnostics
- outputs into simulation:
  - manual stick roll
  - manual stick pitch
  - manual rudder
  - throttle
  - auxiliary throttle / afterburner intent
  - mode switch / autopilot enable

This keeps:

- aircraft dynamics in the existing aircraft subsystem models
- pilot-command semantics in the control path
- external protocol handling in a single adapter

## Suggested repository-level design

Recommended additions:

1. Add a new bridge component to the architecture and generated interfaces.
2. Connect environment and status outputs into the bridge for visualization.
3. Route bridge-produced manual control values into the manual input path used by `MissionComputer`.
4. Keep the autopilot path unchanged so manual and autopilot modes can coexist.

The current `ControlInterface` model is a scripted placeholder and should be treated as the first candidate for replacement or refactoring when introducing live manual input.

## Timing model

The bridge must be non-blocking from the simulation master's perspective.

Recommended timing behavior:

- use `ssp4sim` realtime execution to pace the simulation as the starting point
- sample FlightGear input once per realtime update
- update outgoing visualization state once per realtime update
- avoid letting socket reads block the simulation loop

The initial implementation should avoid adding extra synchronization methods to `pyssp4sim`.

Documented follow-up plans:

1. add a `doStep(t)` method to the Python API so a caller can drive communication-step timing explicitly
2. add an external package sync mechanism only when there is a concrete need to synchronize against another runtime or timing source

Until then, realtime pacing should come from the existing `ssp4sim` capability rather than a new custom synchronization layer.

## Coordinate and signal mapping

The current aircraft model exposes a local frame:

- `x_km`: north
- `y_km`: east
- `z_km`: up

FlightGear visualization will usually expect:

- latitude
- longitude
- altitude
- attitude/orientation in its property/protocol conventions

Therefore the bridge must choose a reference origin and perform:

- local-to-geodetic position conversion
- orientation/sign convention mapping
- normalization mapping between FlightGear controls and `PilotCommand`

## Traceability to current models

This solution is aligned with the current airplane package structure and the first standalone migration step:

- `models/control_interface/modelica/ControlInterfaceFMU/ControlInterface.mo`
- `models/mission_computer/modelica/MissionComputerFMU/MissionComputer.mo`
- `models/environment/modelica/EnvironmentFMU/Environment.mo`
- `models/input_output/modelica/InputOutputFMU/InputOutput.mo`
- `architecture/aircraft.sysml`
- `scripts/workflows/simulate_scenario.py`

These files already define the manual-input path, autopilot path, environment state, telemetry taps, and SSP workflow needed by the bridge design.

## Build workflow alignment

The repository workflow is architecture-first:

1. export all generated artifacts from `architecture/`
2. build all Modelica and native FMUs
3. package the SSP
4. run the simulation workflow

`scripts.generation.build_native_fmus` now follows that same contract. Native FMUs are discovered from the architecture composition plus `models/<snake_case_part>/native/`, and their staged `modelDescription.xml` files come from the shared SysML-driven generator instead of native-script-local metadata.

## Implementation notes

Initial implementation priority:

1. establish outbound visualization from simulation state to FlightGear
2. establish inbound manual control from FlightGear into the manual input path
3. support explicit switching between manual control and autopilot
4. add optional cockpit/status overlays after the control loop is stable

The first implementation should prioritize observability and stable signal mapping over visual polish.
