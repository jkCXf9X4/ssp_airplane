"""Shared repository path helpers used across CLI scripts."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARCHITECTURE_DIR = REPO_ROOT / "architecture"
GENERATED_DIR = REPO_ROOT / "generated"
BUILD_DIR = REPO_ROOT / "build"
MODELS_DIR = REPO_ROOT / "models"
COMMON_MODEL_DIR = MODELS_DIR / "common"
RESOURCES_DIR = REPO_ROOT / "resources"
THIRD_PARTY_DIR = REPO_ROOT / "3rd_party"
FMI_HEADERS_DIR = THIRD_PARTY_DIR / "fmi_headers"

PACKAGE_NAME = "Aircraft"
COMPOSITION_NAME = "AircraftComposition"

DEFAULT_MODELS = [
    "CompositeAirframe",
    "TurbofanPropulsion",
    "AdaptiveWingSystem",
    "MissionComputer",
    "AutopilotModule",
    "InputOutput",
    "FuelSystem",
    "Environment",
    "ControlInterface",
]

@dataclass(frozen=True)
class ModelicaModelSpec:
    folder_name: str
    package_name: str
    class_name: str
    output_name: str

    @property
    def package_file(self) -> Path:
        return MODELS_DIR / self.folder_name / "modelica" / self.package_name / "package.mo"

    @property
    def model_file(self) -> Path:
        return MODELS_DIR / self.folder_name / "modelica" / self.package_name / f"{self.class_name}.mo"

    @property
    def model_name(self) -> str:
        return f"{self.package_name}.{self.class_name}"

    @property
    def package_files(self) -> list[Path]:
        return [COMMON_PACKAGE_FILE, self.package_file]


COMMON_PACKAGE_FILE = COMMON_MODEL_DIR / "modelica" / "AircraftCommon" / "package.mo"

MODELICA_MODEL_SPECS = [
    ModelicaModelSpec("adaptive_wing_system", "AdaptiveWingSystemFMU", "AdaptiveWingSystem", "AdaptiveWingSystem"),
    ModelicaModelSpec("autopilot_module", "AutopilotModuleFMU", "AutopilotModule", "AutopilotModule"),
    ModelicaModelSpec("composite_airframe", "CompositeAirframeFMU", "CompositeAirframe", "CompositeAirframe"),
    ModelicaModelSpec("control_interface", "ControlInterfaceFMU", "ControlInterface", "ControlInterface"),
    ModelicaModelSpec("environment", "EnvironmentFMU", "Environment", "Environment"),
    ModelicaModelSpec("fuel_system", "FuelSystemFMU", "FuelSystem", "FuelSystem"),
    ModelicaModelSpec("input_output", "InputOutputFMU", "InputOutput", "InputOutput"),
    ModelicaModelSpec("mission_computer", "MissionComputerFMU", "MissionComputer", "MissionComputer"),
    ModelicaModelSpec("turbofan_propulsion", "TurbofanPropulsionFMU", "TurbofanPropulsion", "TurbofanPropulsion"),
]

DEFAULT_MODELICA_MODELS = [spec.model_name for spec in MODELICA_MODEL_SPECS]


def spec_by_model_name(model_name: str) -> ModelicaModelSpec:
    for spec in MODELICA_MODEL_SPECS:
        if spec.model_name == model_name:
            return spec
    raise KeyError(model_name)



def ensure_directory(path: Path) -> Path:
    """Create the directory (or its parent) if missing and return it for chaining."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_parent_dir(path: Path) -> Path:
    """Create the parent directory for a file path if needed and return the file path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


