# FlightGear bridge implementation status

This document distinguishes what is already present in the repository from follow-up work.

## Present in the repository

- A dedicated native FMI 2.0 co-simulation FMU exists for `FlightGearBridge`
- The bridge is represented as its own modeled component
- Native FMU packaging follows the architecture-first workflow used elsewhere in the repo
- Generated interface headers and `modelDescription.xml` files come from the shared SysML-driven generation flow

Relevant files:

- `models/flightgear_bridge/native/src/FlightGearBridge.cpp`
- `models/flightgear_bridge/native/src/BridgeRuntime.cpp`
- `models/flightgear_bridge/modelica/FlightGearBridgeFMU/FlightGearBridge.mo`
- `generated/interfaces/Aircraft_FlightGearBridge.h`
- `generated/model_descriptions/FlightGearBridge/modelDescription.xml`

## Expected signal responsibilities

Inputs from the simulation side:

- environment position
- environment orientation
- flight status
- optional mission, fuel, or engine state for overlays and diagnostics

Outputs into the simulation side:

- manual stick roll
- manual stick pitch
- manual rudder
- throttle
- auxiliary throttle or afterburner intent
- mode selection or autopilot enable

## Follow-up work

- Complete outbound visualization from simulation state to FlightGear
- Complete inbound manual control mapping into the manual input path
- Support explicit manual versus autopilot switching
- Add optional cockpit or status overlays after the control loop is stable

## Current limitations to keep in mind

- FlightGear integration should be treated as an adapter around the existing SSP workflow, not a replacement for it
- Realtime pacing currently comes from `ssp4sim`
- Any extra synchronization API work should be driven by an identified runtime need, not added preemptively
