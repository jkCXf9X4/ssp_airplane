# ssp_airplane

System structure and simulation workflow for an F-16-inspired aircraft model.

This repository combines:

- SysML architecture sources in `architecture/`
- Modelica and native FMU implementations in `models/`
- Python generation, verification, and workflow tooling in `scripts/`

## Start Here

Pick the path that matches what you want to do:

- Reuse existing scenario results and inspect outputs:
  see `docs/getting_started.md`
- Rebuild generated artifacts, FMUs, and the SSP from source:
  see `docs/getting_started.md`
- Browse all documentation by audience and topic:
  see `docs/index.md`

## Fastest First Run

If you only want a low-friction first success, use the reuse-results path:

```bash
python3.11 -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m scripts.cli.scenarios_simulate \
  --scenario resources/scenarios/test_scenario.json \
  --reuse-results
```

That command reuses the reference CSV when present and writes derived outputs into `build/results/`.

## Repository Layout

- `architecture/`: SysML source of truth
- `models/`: Modelica and native FMU implementations
- `resources/scenarios/`: curated mission scenarios
- `resources/references/`: reference results used for reuse and tests
- `scripts/`: command entrypoints in `scripts/cli/`, workflows in `scripts/workflows/`, and internal modules in `scripts/lib/`
- `docs/`: focused user, developer, and integration documentation

## Documentation

- Getting started: `docs/getting_started.md`
- Documentation index: `docs/index.md`
- Command reference: `docs/command_reference.md`
- Workflow methodology: `docs/dev/workflow_methodology.md`
