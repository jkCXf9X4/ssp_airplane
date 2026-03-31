# FlightGear bridge architecture decision

This document records the architectural decision behind the FlightGear integration.

## Decision

Use:

- `ssp4sim` as the simulation master and execution engine
- `FlightGear` as the visual frontend and pilot I/O frontend
- a dedicated `FlightGearBridge` adapter component in the aircraft architecture
- FlightGear `generic` socket communication for the first implementation

The goal is to preserve the existing SSP/FMU-based aircraft composition while adding live visualization and manual control.

## Why this approach

The repository already has:

- subsystem FMUs packaged into a SSP
- `ssp4sim` or `pyssp4sim` execution
- a manual-input path through `ControlInterface`
- an autopilot-input path through `AutopilotModule`
- state generation through `Environment`

That makes an adapter-based integration materially simpler than replacing the simulation stack with another runtime.

## Runtime architecture

The intended runtime structure is:

`FlightGear <-> FlightGearBridge <-> ssp4sim SSP`

Responsibilities:

- `FlightGear` renders the aircraft, views, and HUD information and captures pilot controls
- `FlightGearBridge` translates between FlightGear socket messages and simulation signals
- `ssp4sim` remains the co-simulation master for the packaged aircraft SSP

## Why start with generic socket communication

The initial implementation prefers FlightGear `generic` communication over protocol slaving because it is easier to inspect, debug, and evolve during integration.

Benefits:

- explicit field selection
- simpler signal mapping
- easier value inspection during debugging
- lower coupling while the interface is still evolving

The native protocol can still be adopted later if tighter integration becomes necessary.

## Separation of concerns

The bridge should remain a dedicated adapter instead of embedding socket or protocol logic into vehicle dynamics or autopilot models.

This keeps:

- aircraft dynamics in the existing subsystem models
- pilot-command semantics in the control path
- external protocol handling in one boundary component

## Timing decision

For the initial runtime:

- use `ssp4sim` realtime execution for pacing
- sample FlightGear input once per realtime update
- publish visualization state once per realtime update
- avoid blocking socket reads inside the simulation loop

The design intentionally avoids adding new synchronization APIs to `pyssp4sim` until a concrete integration need appears.
