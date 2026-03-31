#!/usr/bin/env python3
"""Run OpenModelica checkModel across the Aircraft package."""
from __future__ import annotations

import argparse
import sys
from typing import Iterable

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.modelica import run_omc
from scripts.common.modelica_specs import DEFAULT_MODELICA_MODELS, spec_by_model_name

DEFAULT_MODELS = DEFAULT_MODELICA_MODELS


def build_script(models: Iterable[str]) -> str:
    lines: list[str] = ['installPackage(Modelica, "4.0.0", exactMatch=false);']
    loaded_packages: set[str] = set()
    for model in models:
        spec = spec_by_model_name(model)
        for package_file in spec.package_files:
            package_path = package_file.as_posix()
            if package_path not in loaded_packages:
                lines.append(f'loadFile("{package_path}");')
                loaded_packages.add(package_path)
    lines.append("getErrorString();")
    for model in models:
        lines.append(f'print(\"Checking {model}\\n\");')
        lines.append(f"result := checkModel({model});")
        lines.append("print(result + \"\\n\");")
        lines.append("getErrorString();")
    return "\n".join(lines)


def verify_models(omc: str, models: Iterable[str]) -> int:
    stdout = run_omc(omc, build_script(models))
    if stdout:
        print(stdout, end="")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--omc", default="omc", help="Path to the omc executable.")
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS, help="Fully qualified Modelica classes to check.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return verify_models(args.omc, args.models)


if __name__ == "__main__":
    raise SystemExit(main())
