"""Helpers for compiling Modelica and native build artifacts."""

from .native_project import (
    DEFAULT_BUILD_ROOT,
    DEFAULT_OUTPUT_DIR,
    GENERATED_INTERFACE_DIR,
    GENERATED_MODEL_DESCRIPTION_DIR,
    NativeFmuProject,
)

__all__ = [
    "DEFAULT_BUILD_ROOT",
    "DEFAULT_OUTPUT_DIR",
    "GENERATED_INTERFACE_DIR",
    "GENERATED_MODEL_DESCRIPTION_DIR",
    "NativeFmuProject",
]
