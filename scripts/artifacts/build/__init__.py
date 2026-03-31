"""Artifact build entrypoints and helpers."""

from .native_fmu_build import build_native_library
from .native_fmu_discovery import discover_native_projects
from .native_fmu_project import (
    DEFAULT_BUILD_ROOT,
    DEFAULT_OUTPUT_DIR,
    GENERATED_INTERFACE_DIR,
    GENERATED_MODEL_DESCRIPTION_DIR,
    NativeFmuProject,
)
from scripts.artifacts.package.native_fmu import package_native_fmu, stage_native_fmu_sources
from scripts.artifacts.sysml_export.native_fmu import generated_model_description_paths

__all__ = [
    "DEFAULT_BUILD_ROOT",
    "DEFAULT_OUTPUT_DIR",
    "GENERATED_INTERFACE_DIR",
    "GENERATED_MODEL_DESCRIPTION_DIR",
    "NativeFmuProject",
    "build_native_library",
    "discover_native_projects",
    "generated_model_description_paths",
    "package_native_fmu",
    "stage_native_fmu_sources",
]
