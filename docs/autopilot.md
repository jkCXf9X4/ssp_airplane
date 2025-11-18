# Autopilot waypoint logic

`AutopilotModule` now steers toward each waypoint using a local X/Y/Z grid in kilometers (`waypointX_km[]`, `waypointY_km[]`, `waypointZ_km[]`) provided by the scenario SSV bundle emitted by `scripts/simulate_scenario.py`. The module:

- Computes bearing and distance directly in the local grid (x=North, y=East, z=Up).
- Normalizes heading error into `[-180, 180]` before applying the roll command so the aircraft turns the short way.
- Drives the pitch command toward the target waypoint altitude and advances to the next waypoint once within `waypointProximity_km` (10 km default).
- Latches `MissionStatus` (`waypoint_index`, `distance_to_waypoint_km`, `arrived`, `complete`) so downstream logging can trace progress.
- The SSD generator now expands list-valued SysML attributes such as `waypointX_km`/`waypointY_km`/`waypointZ_km` into indexed real parameter connectors (`waypointX_km[1]`..`[10]`, etc.), keeping the array defaults intact for OMSimulator parameter binding.

## Quick checks without OMSimulator

- `pytest tests/test_autopilot_logic.py` runs the same heading/distance math in Python to guard against regressions in the navigation arithmetic without rebuilding FMUs.
- `python3 scripts/simulate_scenario.py --scenario build/scenarios/test_scenario.json --reuse-results` exercises the parameter-injection path and produces `build/results/test_scenario_waypoints.txt` so you can confirm the FMU receives the expected waypoint list (now X/Y/Z kilometers).
