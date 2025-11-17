# Mission Use Cases

The following mission-driven use cases connect the SysML requirements to concrete simulation scenarios stored in `resources/scenarios/`. Each use case is backed by deterministic waypoint files so unit tests and OMSimulator runs can validate requirement coverage.

| Use case | Scenario file | Linked requirements | Summary |
| --- | --- | --- | --- |
| High-altitude intercept | `resources/scenarios/high_altitude_intercept.json` | `REQ_Performance`, `REQ_Control` | Scramble from an alert base, climb above 9 km, and dash at Mach 2 to intercept a fast mover while keeping HOTAS/autopilot channels online. |
| Deep strike penetration | `resources/scenarios/deep_strike_penetration.json` | `REQ_Performance`, `REQ_Fuel`, `REQ_Mission` | Execute a 3,100 km ingress/egress with heavy stores, demonstrating the fuel reserve margin and long-range capability within the design range. |
| CAS multi-store support | `resources/scenarios/cas_multi_store_support.json` | `REQ_Control`, `REQ_Mission` | Fly a loitering close air support pattern while powering all nine stations and honoring HOTAS/fly-by-wire control authority. |

These curated scenarios are referenced by the simulation tests so regressions that break requirement coverage are caught early. Each OMS run produces a CSV and a requirements-oriented summary JSON; see `docs/results_and_evaluation.md` for how to interpret the outputs.
