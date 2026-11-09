"""Build the standalone Modelica FMUs via pyssp_workflow and pyssp_standard.

Replaces the removed ``cmake/AddModelicaFmu.cmake`` glue. Each model spec's
package files are loaded in order into its own omc subprocess (one loadFile per
file, AircraftCommon first), and the unpacked FMU the build step returns is
packaged deterministically into ``build/fmus/``.
"""
from __future__ import annotations

import tempfile
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from pyssp_standard import package_archive
from pyssp_workflow.authoring.fmu import build_fmu_from_modelica

from scripts.lib.common.modelica.specs import (
    DEFAULT_MODELICA_MODELS,
    ModelicaModelSpec,
    spec_by_model_name,
)
from scripts.lib.paths import BUILD_DIR

DEFAULT_MODELICA_FMU_DIR = BUILD_DIR / "fmus"

#: Default omc build timeout, matching pyssp_workflow's authoring default.
DEFAULT_TIMEOUT_SECONDS = 1800.0


def _build_one(
    spec: ModelicaModelSpec,
    *,
    omc: str,
    output_dir: Path,
    timeout: float,
) -> Path:
    fmu_path = output_dir / f"{spec.output_name}.fmu"
    with tempfile.TemporaryDirectory(prefix=f"{spec.output_name}_fmu_") as temp_dir:
        unpacked = Path(temp_dir) / "fmu"
        build_fmu_from_modelica(
            source_file=spec.package_files[0],
            source_files=spec.package_files,
            class_name=spec.model_name,
            fmu_dir=unpacked,
            file_name_prefix=spec.output_name,
            omc=omc,
            timeout=timeout,
        )
        package_archive(unpacked, fmu_path)
    return fmu_path


def build_modelica_fmus(
    output_dir: str | Path | None = None,
    *,
    omc: str,
    model_specs: Iterable[ModelicaModelSpec] | None = None,
    max_workers: int = 4,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> list[Path]:
    """Build and deterministically package every standalone Modelica FMU.

    Args:
        output_dir: Target directory for the ``.fmu`` files (default:
            ``build/fmus``). The ``file_name_prefix`` equals the spec's
            ``output_name`` so the archive becomes ``<output_name>.fmu`` and the
            modelIdentifier matches the previously CMake-built FMUs.
        omc: Path to the ``omc`` executable.
        model_specs: The specs to build (default: all standalone models).
        max_workers: Parallel omc subprocesses; each build is independent.
        timeout: Per-omc timeout in seconds.

    Returns:
        The packaged ``.fmu`` paths, sorted.
    """
    specs = list(
        model_specs
        if model_specs is not None
        else (spec_by_model_name(name) for name in DEFAULT_MODELICA_MODELS)
    )
    output = Path(output_dir) if output_dir is not None else DEFAULT_MODELICA_FMU_DIR
    output.mkdir(parents=True, exist_ok=True)

    built: list[Path] = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                _build_one,
                spec,
                omc=omc,
                output_dir=output,
                timeout=timeout,
            ): spec
            for spec in specs
        }
        for future in as_completed(futures):
            spec = futures[future]
            fmu_path = future.result()  # propagate build failures as-is
            built.append(fmu_path)
            print(f"Built Modelica FMU: {fmu_path}")
    built.sort()
    return built


__all__ = ["DEFAULT_MODELICA_FMU_DIR", "build_modelica_fmus"]
