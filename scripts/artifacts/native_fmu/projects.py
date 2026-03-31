"""Project discovery and shared paths for native FMU builds."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from pycps_sysmlv2 import NodeType, SysMLParser
from pyssp_sysml2.fmi import generate_model_descriptions

from scripts.common.paths import ARCHITECTURE_DIR, BUILD_DIR, COMPOSITION_NAME, GENERATED_DIR, MODELS_DIR, REPO_ROOT
from scripts.artifacts.generate_c_interface_defs import common_header_name, part_header_name
from scripts.artifacts.normalize_generated_metadata import normalize_model_description_timestamps

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


def _snake_case(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def discover_native_projects(
    architecture_path: Path = ARCHITECTURE_DIR,
    composition: str = COMPOSITION_NAME,
    build_root: Path = DEFAULT_BUILD_ROOT,
) -> list[NativeFmuProject]:
    system = SysMLParser(architecture_path).parse().get_def(NodeType.Part, composition)
    projects: list[NativeFmuProject] = []
    for instance_name, part_ref in system.refs(NodeType.Part).items():
        folder_name = instance_name
        source_root = MODELS_DIR / folder_name / "native"
        if not (source_root / "CMakeLists.txt").exists():
            folder_name = _snake_case(part_ref.type)
            source_root = MODELS_DIR / folder_name / "native"
        if not (source_root / "CMakeLists.txt").exists():
            continue
        projects.append(
            NativeFmuProject(
                instance_name=instance_name,
                model_identifier=part_ref.type,
                source_root=source_root,
                build_dir=build_root / folder_name,
            )
        )
    return projects


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
