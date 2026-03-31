# Getting Started

This repository supports two distinct workflows:

- `reuse existing results`: inspect scenarios, generate summaries, and plot outputs without rebuilding FMUs
- `rebuild from source`: regenerate artifacts, rebuild FMUs, package the SSP, and run the reference simulation

Choose one path and ignore the other until you need it.

## Path 1: Reuse Existing Results

Use this path if your goal is to understand the repository quickly with the least setup.

### Prerequisites

- Python 3.11+

### Setup

```bash
python3.11 -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### First command to run

```bash
python3 -m scripts.scenarios.simulate_scenario \
  --scenario resources/scenarios/test_scenario.json \
  --reuse-results
```

### Expected outputs

After the command completes, inspect:

- `build/results/test_scenario_results.csv`
- `build/results/test_scenario_summary.json`
- `build/results/test_scenario_waypoints.txt`

If you want a quick plot:

```bash
python3 -m scripts.analyze.plot_results \
  --results-csv build/results/test_scenario_results.csv \
  --scenario resources/scenarios/test_scenario.json \
  --plot-path
```

## Path 2: Rebuild From Source

Use this path when you need the full architecture-first workflow.

### Additional prerequisites

- `cmake`
- a C++17 compiler
- OpenModelica (`omc`)

Typical Debian or Ubuntu setup:

```bash
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv cmake build-essential openmodelica
```

### Setup

```bash
git submodule update --init --recursive
python3.11 -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements_local.txt
```

### First full build

```bash
./scripts/rebuild_from_source.sh
```

That workflow:

1. exports architecture-derived artifacts
2. verifies generated and model consistency
3. builds Modelica and native FMUs
4. packages the SSP
5. runs the reference simulation

The script deletes and recreates `build/`.

## Which path should I use?

- Use `reuse existing results` if you are reading, testing, plotting, or learning the model layout.
- Use `rebuild from source` if you are changing architecture, FMUs, native code, or packaging.

## Next Docs

- Scenario intent: `user/scenarios.md`
- Result interpretation: `user/results.md`
- Full command list: `command_reference.md`
