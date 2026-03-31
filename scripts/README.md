# Scripts

This directory has three roles:

- `scripts/cli/`: supported user-facing commands
- `scripts/workflows/`: multi-step orchestration entrypoints
- `scripts/lib/`: internal implementation modules used by the command entrypoints

Use the CLI entrypoints as the canonical interface. Examples:

```bash
python3 -m scripts.cli.scenarios simulate --scenario resources/scenarios/test_scenario.json --reuse-results
python3 -m scripts.cli.analyze plot --results-csv build/results/test_scenario_results.csv --scenario resources/scenarios/test_scenario.json --plot-path
python3 -m scripts.cli.artifacts export
python3 -m scripts.workflows.rebuild_from_source
```
