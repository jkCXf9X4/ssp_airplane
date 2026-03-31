# FlightGear Bridge Overview

The FlightGear bridge is an adapter between FlightGear and the packaged aircraft SSP.

## Responsibility

The bridge is responsible for:

- reading aircraft state from the SSP
- writing manual command values back into the SSP
- converting local `x_km/y_km/z_km` coordinates into a geodetic frame
- mapping FlightGear control channels into the aircraft command interface
- handling manual versus autopilot mode selection at the integration boundary

## Why it is a separate component

The bridge is kept as a dedicated adapter so socket and protocol logic do not leak into the airframe, autopilot, or other subsystem models.

In this repository, the bridge is implemented first as a native FMI 2.0 co-simulation FMU written in C++.

## Where to look in the repository

- `models/flightgear_bridge/native/src/FlightGearBridge.cpp`
- `models/flightgear_bridge/native/src/BridgeRuntime.cpp`
- `models/flightgear_bridge/modelica/FlightGearBridgeFMU/FlightGearBridge.mo`
- `architecture/aircraft.sysml`

## Related Docs

- `decision.md`: why this architecture was chosen
- `status.md`: what is implemented and what remains
