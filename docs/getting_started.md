# Getting Started

This repository supports two distinct workflows:

- `reuse existing results`: inspect scenarios, generate summaries, and plot outputs without rebuilding FMUs
- `build from source`: compile the checked-in Modelica and native sources into FMUs from the repository root

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
python3 -m scripts.cli.scenarios_simulate \
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
python3 -m scripts.cli.analyze_plot \
  --results-csv build/results/test_scenario_results.csv \
  --scenario resources/scenarios/test_scenario.json \
  --plot-path
```

## Path 2: Build From Source

Use this path when you need to rebuild FMUs from the checked-in sources.

### Additional prerequisites

- `cmake`
- a C++17 compiler
- OpenModelica (`omc`)

Typical Debian or Ubuntu setup:

```bash
sudo apt-get update
sudo apt-get install -y cmake build-essential openmodelica
```

### First full build

```bash
cmake -S . -B build/cmake
cmake --build build/cmake
```

This builds the default `build_fmus` target, which:

1. exports each Modelica package to an FMU under `fmus/`
2. builds the native `FlightGearBridge` shared library

Native FMU packaging remains on the Python tooling path. This path uses the checked-in `generated/` metadata for the native library build. If you change architecture-derived interfaces or model descriptions, regenerate those artifacts before rebuilding.

## Which path should I use?

- Use `reuse existing results` if you are reading, testing, plotting, or learning the model layout.
- Use `build from source` if you are changing FMUs, native code, or packaging.

## Next Docs

- Scenario intent: `user/scenarios.md`
- Result interpretation: `user/results.md`
- Full command list: `command_reference.md`
