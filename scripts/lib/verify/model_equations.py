"""Run OpenModelica `checkModel` across the Aircraft package."""
from __future__ import annotations

from typing import Iterable

from scripts.lib.common.modelica import DEFAULT_MODELICA_MODELS, run_omc, spec_by_model_name

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
