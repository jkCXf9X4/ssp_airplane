# Results and requirement evaluation

When `scripts/simulate_scenario.py` runs, it always writes two artifacts into `build/results/`:

1) `<scenario>_results.csv` — full OMSimulator timeseries for every exported variable.  
2) `<scenario>_summary.json` — compact requirement view with evidence and key metrics for humans and LLM agents.

## Summary JSON fields

```json
{
  "scenario": "high_altitude_intercept",
  "distance_km": 516.23,
  "duration_s": 199.0,
  "fuel_capacity_kg": 2600.0,
  "fuel_required_kg": 119.2,
  "requirements": [
    {"id": "REQ_Performance", "passed": false, "evidence": "mach=0.76, g-load=1.00"},
    {"id": "REQ_Fuel", "passed": true, "evidence": "final fuel=1975.9 kg, reserve=208.0 kg"},
    {"id": "REQ_Control", "passed": true, "evidence": "autopilot_limit=0, control_excursion=2.57 deg"},
    {"id": "REQ_Mission", "passed": true, "evidence": "stores_available=9"},
    {"id": "REQ_Propulsion", "passed": true, "evidence": "thrust=60.5 kN, mass_flow=0.65 kg/s"}
  ],
  "metrics": {
    "max_mach": 0.76,
    "max_load_factor_g": 1.0,
    "fuel_initial_kg": 3160.0,
    "fuel_final_kg": 1975.9,
    "fuel_used_kg": 1184.1,
    "stores_available": 9,
    "autopilot_limit_max": 0,
    "thrust_kn_max": 60.5,
    "mass_flow_kgps_max": 0.65,
    "control_surface_excursion_deg": 2.57
  }
}
```

### Metric notes

- `max_mach` and `max_load_factor_g` capture the highest achieved performance for REQ_Performance.
- `fuel_*` values are derived from turbofan fuel telemetry; reserve limit uses an 8% fraction of `fuel_capacity_kg`.
- `stores_available` is computed from the bitmask in `StoresManagementSystem.storesTelemetry.store_present_mask`, so deviations from 9 indicate missing/powered-down stations.
- `autopilot_limit_max` and `control_surface_excursion_deg` ensure control authority and fly-by-wire activity for REQ_Control.
- `thrust_kn_max` and `mass_flow_kgps_max` provide propulsion evidence.
- `waypoint_miss_*`, `waypoint_hits`, `waypoint_total`, `waypoint_within_threshold_fraction`, and `waypoints_followed` quantify how closely the simulated path tracked the scenario waypoints (10 km threshold by default).

### Waypoint strings and plots

- Each scenario’s waypoints are also exported to `build/results/<scenario>_waypoints.txt` as a comma-separated `x_km,y_km,z_km,...` string, ready for Modelica `stringToRealVector` consumption in the autopilot parameter set.
- Passing `--plot` to `simulate_scenario.py` generates `build/results/<scenario>_path.png`, overlaying the simulated local X/Y path against the supplied waypoints for a quick visual verification.

## Reusing results vs. re-simulating

- Use `--reuse-results` to only post-process an existing `<scenario>_results.csv` without invoking OMSimulator. This keeps CI fast and allows offline exploration of prior runs.
- Drop `--reuse-results` (or delete the CSV) to regenerate results from the SSP; pass `--stop-time` to control simulation horizon.

## Scenario provenance

- Curated scenarios and their linked requirements are documented in `docs/use_cases.md`.
- A pre-generated dataset for `build/scenarios/test_scenario.json` is kept in `build/results/` so `pytest` can run without invoking OMSimulator.
