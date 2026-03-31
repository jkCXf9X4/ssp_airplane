# Results

When `scripts.workflows.simulate_scenario` runs, it writes output artifacts into `build/results/`.

## Main artifacts

- `<scenario>_results.csv`: full timeseries exported by the simulation
- `<scenario>_summary.json`: compact requirement-oriented summary
- `<scenario>_waypoints.txt`: waypoint values prepared for parameter injection and quick inspection

## Summary JSON

The summary JSON is the fastest artifact to inspect when you want to know whether a scenario met its intended requirements.

Important fields include:

- `requirements`: pass or fail status with short evidence strings
- `metrics.max_mach` and `metrics.max_load_factor_g`: performance evidence
- `metrics.fuel_*`: fuel usage and reserve evidence
- `metrics.autopilot_limit_max` and `metrics.control_surface_excursion_deg`: control activity evidence
- `metrics.waypoint_*`: path-following evidence

## Reuse results vs. rerun simulation

- Use `--reuse-results` when a matching CSV already exists and you only need post-processing.
- Omit `--reuse-results` when you need a new simulation run from the SSP.
- On a clean checkout, `pytest` seeds the basic test scenario and reference CSV into `build/` so the reuse path works immediately.

## Plots

Generate a path plot with:

```bash
python3 -m scripts.plot_results \
  --results-csv build/results/<scenario>_results.csv \
  --scenario resources/scenarios/<scenario>.json \
  --plot-path
```

Optional flags:

- `--plot-3d` for a 3D path
- `--plot-fuel-altitude` for altitude and fuel over time

## Related Docs

- Scenario catalog: `scenarios.md`
- Full command list: `../command_reference.md`
