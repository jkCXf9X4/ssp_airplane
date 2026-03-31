"""SysML-derived metadata preparation needed by native FMU builds."""
from __future__ import annotations

from pathlib import Path

from pyssp_sysml2.fmi import generate_model_descriptions

from scripts.lib.artifacts.sysml_export.normalize_generated_metadata import normalize_model_description_timestamps


def generated_model_description_paths(
    architecture_path: Path,
    output_dir: Path,
    composition: str,
) -> dict[str, Path]:
    written = generate_model_descriptions(
        architecture_path,
        output_dir,
        composition,
    )
    normalize_model_description_timestamps(written)
    return {path.parent.name: path for path in written}
