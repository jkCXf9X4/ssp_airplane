"""Discover native build projects from the SysML architecture."""
from __future__ import annotations

from pathlib import Path
import re

from pycps_sysmlv2 import NodeType, SysMLParser

from scripts.lib.paths import ARCHITECTURE_DIR, COMPOSITION_NAME, MODELS_DIR
from scripts.lib.artifacts.build.native_project import DEFAULT_BUILD_ROOT, NativeFmuProject


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
