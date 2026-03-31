"""Project model and shared paths for native FMU builds."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from scripts.common.paths import BUILD_DIR, GENERATED_DIR, REPO_ROOT
from scripts.artifacts.sysml_export.generate_c_interface_defs import common_header_name, part_header_name

DEFAULT_OUTPUT_DIR = BUILD_DIR / "fmus"
DEFAULT_BUILD_ROOT = BUILD_DIR / "native"
GENERATED_INTERFACE_DIR = REPO_ROOT / "generated" / "interfaces"
GENERATED_MODEL_DESCRIPTION_DIR = GENERATED_DIR / "model_descriptions"


@dataclass(frozen=True)
class NativeFmuProject:
    instance_name: str
    model_identifier: str
    source_root: Path
    build_dir: Path

    @property
    def output_name(self) -> str:
        return f"{self.model_identifier}.fmu"

    @property
    def generated_model_header(self) -> Path:
        return GENERATED_INTERFACE_DIR / part_header_name("Aircraft", self.model_identifier)

    @property
    def generated_common_header(self) -> Path:
        return GENERATED_INTERFACE_DIR / common_header_name("Aircraft")

    @property
    def model_description_path(self) -> Path:
        return GENERATED_MODEL_DESCRIPTION_DIR / self.model_identifier / "modelDescription.xml"
