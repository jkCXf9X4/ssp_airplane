# Scripts

This directory has three roles:

- `scripts/cli/`: supported user-facing commands
- `scripts/workflows/`: multi-step orchestration entrypoints
- `scripts/lib/`: internal implementation modules used by the command entrypoints

Use the CLI entrypoints as the canonical interface. Examples:

```bash
. venv/bin/activate && python -m scripts.cli.scenarios_simulate --scenario resources/scenarios/test_scenario.json --reuse-results
. venv/bin/activate && python -m scripts.cli.analyze_plot --results-csv build/results/test_scenario_results.csv --scenario resources/scenarios/test_scenario.json --plot-path
. venv/bin/activate && python -m scripts.cli.artifacts_export
. venv/bin/activate && python -m scripts.workflows.rebuild_from_source
```

Canonical command-to-library ownership:

| Command family | Canonical implementation |
| --- | --- |
| `scripts.cli.scenarios_*` | `scripts/lib/scenarios/` |
| `scripts.cli.verify_*` | `scripts/lib/verify/` |
| `scripts.cli.artifacts_*` | `scripts/lib/artifacts/` |
| `scripts.cli.analyze_plot` | `scripts/lib/results/` |

Within `scripts/lib/artifacts/`, prefer the existing subpackage that already owns the task:

- `build/` for builds
- `package/` for packaging
- `sysml_export/` for generated export artifacts
