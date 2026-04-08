# Scripts

This directory has three roles:

- `scripts/cli/`: supported user-facing commands
- `scripts/workflows/`: multi-step orchestration entrypoints
- `scripts/lib/`: internal implementation modules used by the command entrypoints

Phase ownership:

- Python owns generation and verification into `generated/`
- CMake owns build and packaging of FMUs plus the baseline SSP
- Python owns simulation and analysis through `ssp4sim`

Use the CLI entrypoints as the canonical interface. Examples:

```bash
. venv/bin/activate && python -m scripts.cli.scenarios_prepare_waypoints --scenario resources/scenarios/test_scenario.json
. venv/bin/activate && python -m scripts.cli.scenarios_package_ssp --parameter-set build/results/test_scenario_waypoints.ssv --scenario-stem test_scenario
. venv/bin/activate && python -m scripts.cli.scenarios_write_config --prepared-ssp build/results/test_scenario_run/test_scenario.ssp --result-file build/results/test_scenario_results.csv --stop-time 120
. venv/bin/activate && python -m scripts.cli.scenarios_run_ssp4sim --config-path build/results/config.json
. venv/bin/activate && python -m scripts.cli.scenarios_evaluate_results --scenario resources/scenarios/test_scenario.json --results-csv build/results/test_scenario_results.csv
. venv/bin/activate && python -m scripts.cli.analyze_plot --results-csv build/results/test_scenario_results.csv --scenario resources/scenarios/test_scenario.json --plot-path
. venv/bin/activate && python -m scripts.cli.artifacts_export
. venv/bin/activate && python -m scripts.workflows.rebuild_from_source
```

Avoid adding new Python wrappers for CMake build or packaging steps. Prefer direct `cmake` targets for those phases.

Canonical command-to-library ownership:

| Command family | Canonical implementation |
| --- | --- |
| `scripts.cli.scenarios_*` | `scripts/lib/scenarios/` |
| `scripts.cli.verify_*` | `scripts/lib/verify/` |
| `scripts.cli.artifacts_*` | `scripts/lib/artifacts/` |
| `scripts.cli.analyze_plot` | `scripts/lib/results/` |

Within `scripts/lib/artifacts/`, prefer the existing subpackage that already owns the task:

- `sysml_export/` for generated export artifacts
