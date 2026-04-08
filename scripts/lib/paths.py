"""Shared repository path and model registry helpers used across CLI scripts."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parents[2]
ARCHITECTURE_DIR = REPO_ROOT / "architecture"
GENERATED_DIR = REPO_ROOT / "generated"
BUILD_DIR = REPO_ROOT / "build"
MODELS_DIR = REPO_ROOT / "models"
RESOURCES_DIR = REPO_ROOT / "resources"
THIRD_PARTY_DIR = REPO_ROOT / "3rd_party"
FMI_HEADERS_DIR = THIRD_PARTY_DIR / "fmi_headers"

PACKAGE_NAME = "Aircraft"
COMPOSITION_NAME = "AircraftComposition"

GENERATED_MODELICA_DIR = GENERATED_DIR / "modelica"
GENERATED_MODELICA_COMMON_DIR = GENERATED_MODELICA_DIR / "AircraftCommon"
GENERATED_MODELICA_INTERFACE_FILE = GENERATED_MODELICA_COMMON_DIR / "GeneratedInterfaces.mo"


def _camel_case(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


def common_header_name(package: str = PACKAGE_NAME) -> str:
    return f"{package}_InterfaceCommon.h"


def part_header_name(package: str, part_name: str) -> str:
    return f"{package}_{part_name}.h"


@dataclass(frozen=True)
class RepositoryModelSpec:
    folder_name: str
    root: Path
    component_name: str
    native_source_dir: Path | None = None
    modelica_package_dir: Path | None = None
    modelica_package_name: str | None = None

    @property
    def has_native(self) -> bool:
        return self.native_source_dir is not None

    @property
    def has_modelica(self) -> bool:
        return self.modelica_package_dir is not None

    @property
    def modelica_class_name(self) -> str | None:
        if not self.modelica_package_name or not self.modelica_package_name.endswith("FMU"):
            return None
        class_name = self.modelica_package_name[:-3]
        if self.modelica_package_dir is None:
            return None
        model_file = self.modelica_package_dir / f"{class_name}.mo"
        if not model_file.exists():
            return None
        return class_name

    @property
    def categories(self) -> tuple[str, ...]:
        categories: list[str] = []
        if self.has_native:
            categories.append("native")
        if self.modelica_class_name:
            categories.append("modelica_fmu")
        elif self.has_modelica:
            categories.append("modelica_support")
        if not categories:
            categories.append("uncategorized")
        return tuple(categories)


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
        return [COMMON_PACKAGE_FILE, GENERATED_MODELICA_INTERFACE_FILE, self.package_file]


def _select_modelica_package_dir(modelica_dir: Path) -> tuple[Path | None, str | None]:
    package_dirs = sorted(
        path for path in modelica_dir.iterdir()
        if path.is_dir() and (path / "package.mo").exists()
    )
    if not package_dirs:
        return None, None

    standalone_dirs = [path for path in package_dirs if path.name.endswith("FMU")]
    if len(standalone_dirs) == 1:
        return standalone_dirs[0], standalone_dirs[0].name
    if len(package_dirs) == 1:
        return package_dirs[0], package_dirs[0].name
    return None, None


def _infer_native_component_name(native_source_dir: Path, fallback: str) -> str:
    cmake_path = native_source_dir / "CMakeLists.txt"
    try:
        contents = cmake_path.read_text(encoding="utf-8")
    except OSError:
        return fallback

    output_match = re.search(r'OUTPUT_NAME\s+"([^"]+)"', contents)
    if output_match:
        return output_match.group(1)

    target_match = re.search(r"add_library\(\s*([A-Za-z0-9_]+)\s+SHARED", contents)
    if target_match:
        return target_match.group(1)

    return fallback


def _discover_repository_model_specs() -> list[RepositoryModelSpec]:
    specs: list[RepositoryModelSpec] = []
    for root in sorted(path for path in MODELS_DIR.iterdir() if path.is_dir()):
        native_dir = root / "native"
        native_source_dir = native_dir if (native_dir / "CMakeLists.txt").exists() else None

        modelica_dir = root / "modelica"
        modelica_package_dir: Path | None = None
        modelica_package_name: str | None = None
        if modelica_dir.exists():
            modelica_package_dir, modelica_package_name = _select_modelica_package_dir(modelica_dir)

        component_name = _camel_case(root.name)
        if modelica_package_name and modelica_package_name.endswith("FMU"):
            component_name = modelica_package_name[:-3]
        elif native_source_dir is not None:
            component_name = _infer_native_component_name(native_source_dir, component_name)

        specs.append(
            RepositoryModelSpec(
                folder_name=root.name,
                root=root,
                component_name=component_name,
                native_source_dir=native_source_dir,
                modelica_package_dir=modelica_package_dir,
                modelica_package_name=modelica_package_name,
            )
        )
    return specs


REPOSITORY_MODEL_SPECS = _discover_repository_model_specs()

DEFAULT_MODELS = [
    spec.component_name
    for spec in REPOSITORY_MODEL_SPECS
    if spec.folder_name != "common"
]

COMMON_PACKAGE_FILE = GENERATED_MODELICA_COMMON_DIR / "package.mo"

MODELICA_MODEL_SPECS = [
    ModelicaModelSpec(
        folder_name=spec.folder_name,
        package_name=spec.modelica_package_name,
        class_name=spec.modelica_class_name,
        output_name=spec.modelica_class_name,
    )
    for spec in REPOSITORY_MODEL_SPECS
    if spec.modelica_package_name is not None and spec.modelica_class_name is not None
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
