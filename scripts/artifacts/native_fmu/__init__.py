"""Native FMU build and packaging helpers."""

from .build import build_native_library
from .package import package_native_fmu, stage_native_fmu_sources
from .projects import (
    DEFAULT_BUILD_ROOT,
    DEFAULT_OUTPUT_DIR,
    GENERATED_INTERFACE_DIR,
    GENERATED_MODEL_DESCRIPTION_DIR,
    NativeFmuProject,
    discover_native_projects,
    generated_model_description_paths,
)

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
