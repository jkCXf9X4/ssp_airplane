# Autopilot Waypoint Logic

This page is for maintainers working on waypoint following and scenario parameter injection.

## What this module does

`AutopilotModule` steers toward waypoints in a local X/Y/Z frame in kilometers:

- `x_km`: north
- `y_km`: east
- `z_km`: up

The scenario workflow emits waypoint parameter values that are injected into the autopilot during simulation setup.

## Current behavior

- Bearing and distance are computed directly in the local frame.
- Heading error is normalized into `[-180, 180]` so the aircraft turns the short way.
- Waypoint advancement requires both planar and altitude proximity.
- `MissionStatus` latches progress fields for downstream logging.
- The SSD generator expands list-valued waypoint attributes into indexed parameter connectors for SSP binding.

## Quick regression checks

- `pytest tests/test_autopilot_logic.py`
- `python3 -m scripts.cli.scenarios_simulate --scenario resources/scenarios/test_scenario.json --reuse-results`

The reuse-results command writes `build/results/test_scenario_waypoints.txt`, which is useful for confirming the generated waypoint sequence.
