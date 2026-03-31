"""Registry for standalone Modelica FMU packages."""
from __future__ import annotations

from scripts.lib.paths import (
    DEFAULT_MODELICA_MODELS,
    MODELICA_MODEL_SPECS,
    ModelicaModelSpec,
    spec_by_model_name,
)

__all__ = [
    "DEFAULT_MODELICA_MODELS",
    "MODELICA_MODEL_SPECS",
    "ModelicaModelSpec",
    "spec_by_model_name",
]
