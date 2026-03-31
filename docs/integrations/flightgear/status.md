# FlightGear Bridge Status

This page tracks the current implementation boundary and remaining work.

## Present in the repository

- A dedicated native FMI 2.0 co-simulation FMU exists for `FlightGearBridge`.
- The bridge is represented as its own modeled component.
- Native FMU packaging follows the same architecture-first workflow used elsewhere in the repo.
- Generated interface headers and `modelDescription.xml` files come from the shared SysML-driven generation flow.

## Remaining work

- complete outbound visualization from simulation state to FlightGear
- complete inbound manual control mapping into the manual input path
- support explicit manual versus autopilot switching
- add optional cockpit or status overlays after the core control loop is stable

## Current limits

- The integration is an adapter around the existing SSP workflow, not a replacement for it.
- Realtime pacing currently comes from `ssp4sim`.
- Extra synchronization APIs should only be added if a concrete runtime need appears.
