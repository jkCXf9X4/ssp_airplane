# FlightGear Bridge Decision

This page records the architecture decision for the FlightGear integration.

## Decision

Use:

- `ssp4sim` as the simulation master
- `FlightGear` as the visualization and pilot I/O frontend
- a dedicated `FlightGearBridge` adapter component in the aircraft architecture
- FlightGear `generic` socket communication for the initial implementation

## Reasoning

The repository already has subsystem FMUs, packaged SSP execution, an existing manual-input path, and an autopilot-input path. An adapter is therefore simpler and lower risk than replacing the runtime stack.

## Runtime shape

`FlightGear <-> FlightGearBridge <-> ssp4sim SSP`

## Boundary rule

Keep protocol handling inside the bridge component. Keep aircraft dynamics and pilot-command semantics in the existing subsystem models.

## Timing rule

For the initial runtime:

- let `ssp4sim` provide realtime pacing
- sample FlightGear input once per realtime update
- publish visualization state once per realtime update
- avoid blocking socket reads inside the simulation loop
