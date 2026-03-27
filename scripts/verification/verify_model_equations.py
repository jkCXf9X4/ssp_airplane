#!/usr/bin/env python3
"""Run OpenModelica checkModel across the Aircraft package."""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import MODELS_DIR, REPO_ROOT

PACKAGE_FILE = MODELS_DIR / "Aircraft" / "package.mo"
DEFAULT_MODELS = [
    "Aircraft.CompositeAirframe",
    "Aircraft.TurbofanPropulsion",
    "Aircraft.AdaptiveWingSystem",
    "Aircraft.MissionComputer",
    "Aircraft.AutopilotModule",
    "Aircraft.FuelSystem",
    "Aircraft.ControlInterface",
]


def build_script(models: Iterable[str]) -> str:
    lines = [f'loadFile("{PACKAGE_FILE.as_posix()}");', "getErrorString();"]
    for model in models:
        lines.append(f'print(\"Checking {model}\\n\");')
        lines.append(f"result := checkModel({model});")
        lines.append("print(result + \"\\n\");")
        lines.append("getErrorString();")
    return "\n".join(lines)


def run_omc(omc: str, models: Iterable[str]) -> int:
    script = build_script(models)
    with tempfile.NamedTemporaryFile("w", suffix=".mos", delete=False) as handle:
        handle.write(script)
        mos_path = Path(handle.name)
    try:
        subprocess.run([omc, str(mos_path)], check=True, cwd=REPO_ROOT)
    except FileNotFoundError as exc:
        raise SystemExit("OpenModelica 'omc' executable not found. Install OpenModelica or pass --omc.") from exc
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc)
    finally:
        mos_path.unlink(missing_ok=True)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--omc", default="omc", help="Path to the omc executable.")
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS, help="Fully qualified Modelica classes to check.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_omc(args.omc, args.models)


if __name__ == "__main__":
    main()
