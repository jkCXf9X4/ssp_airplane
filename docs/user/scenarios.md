# Scenarios

The curated scenarios in `resources/scenarios/` connect mission intent to requirement coverage.

## Available scenarios

| Use case | Scenario file | Linked requirements | Summary |
| --- | --- | --- | --- |
| High-altitude intercept | `resources/scenarios/high_altitude_intercept.json` | `REQ_Performance`, `REQ_Control` | Scramble from an alert base, climb above 9 km, and dash at high speed while keeping pilot and autopilot control paths active. |
| Deep strike penetration | `resources/scenarios/deep_strike_penetration.json` | `REQ_Performance`, `REQ_Fuel`, `REQ_Mission` | Execute a long ingress and egress with heavy stores to exercise range and reserve margins. |
| CAS multi-store support | `resources/scenarios/cas_multi_store_support.json` | `REQ_Control`, `REQ_Mission` | Fly a loitering support pattern while keeping all nine stations available and control authority intact. |
| Basic test scenario | `resources/scenarios/test_scenario.json` | smoke test and output validation | Small reference scenario used for reuse, plotting, and automated checks. |

## When to use which scenario

- Use `test_scenario.json` for your first run and for documentation examples.
- Use the named mission scenarios when you want requirement-oriented evaluation.

## How scenarios are used

- `scripts.cli.scenarios_prepare_waypoints` reads the scenario JSON and emits the waypoint artifacts in `build/results/`.
- `scripts.cli.scenarios_package_ssp` injects the generated parameter set into a prepared run SSP.
- `scripts.cli.scenarios_write_config` writes the simulator config for the prepared SSP.
- `scripts.cli.scenarios_run_ssp4sim` runs the simulation from that config.
- `scripts.cli.scenarios_evaluate_results` compares the results CSV against requirement metrics and writes the summary JSON.
- Tests reuse the curated scenarios and canned reference data to catch regressions without always running a full simulation.

## Next Doc

See `results.md` for how to interpret the generated CSV, summary JSON, and plots.
