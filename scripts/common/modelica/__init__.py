"""Modelica/OpenModelica shared helpers."""

from .omc import run_omc
from .specs import DEFAULT_MODELICA_MODELS, MODELICA_MODEL_SPECS, ModelicaModelSpec, spec_by_model_name

__all__ = [
    "DEFAULT_MODELICA_MODELS",
    "MODELICA_MODEL_SPECS",
    "ModelicaModelSpec",
    "run_omc",
    "spec_by_model_name",
]
