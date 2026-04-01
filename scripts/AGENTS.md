# AGENTS

## Scope

This file applies to everything under `scripts/`.

## Directory Roles

- `cli/`: canonical user-facing command entrypoints
- `workflows/`: multi-step orchestration entrypoints that combine several library operations
- `lib/`: internal implementation modules used by `cli/` and `workflows/`

Agents should start from the CLI or workflow entrypoint that matches the task, then follow imports into `lib/`.

## Canonical Entry Points

- Scenario commands live in `cli/scenarios_*.py` and delegate to `lib/scenarios/`
- Verification commands live in `cli/verify_*.py` and delegate to `lib/verify/`
- Artifact commands live in `cli/artifacts_*.py` and delegate to `lib/artifacts/`
- Plotting commands live in `cli/analyze_plot.py` and delegate to `lib/results/`
- End-to-end rebuild orchestration lives in `workflows/rebuild_from_source.py`

## Phase Ownership

- Python generation and verification own `architecture/ -> generated/`
- CMake owns `generated/ + models/ -> packaged FMUs + baseline SSP`
- Python simulation owns `baseline SSP + scenario -> results` through `ssp4sim`

Python packaging commands under `cli/artifacts_*package*` are compatibility tooling, not the canonical workflow.

## Edit Rules

- Do not add new top-level command families under `cli/` when an existing family already owns the task.
- Prefer extending the existing library module that already owns the noun and verb pair.
- Only add a new file when the existing file would otherwise mix unrelated responsibilities or abstraction levels.
- Avoid compatibility wrappers, alias modules, and thin pass-through helpers. Change references directly.
- Keep command parsing in `cli/` and business logic in `lib/`.
- Do not move packaging responsibilities into scenario or analysis code.
- Do not make Python the canonical build/package path when CMake is the clearer owner.

## Search First

Before editing:

1. Use `rg` to find the existing command or implementation path.
2. Identify the canonical module that already owns the behavior.
3. Extend that module unless there is a clear abstraction reason not to.

Useful starting points:

- `rg "argparse|ArgumentParser" scripts/cli`
- `rg "def .*simulate|def .*generate|def .*verify" scripts/lib`
- `rg "artifacts_" scripts/cli scripts/lib`

## Environment

- Use the repo-local `venv` when present.
- Prefer `. venv/bin/activate && python -m ...` for commands, tests, and scripts.
