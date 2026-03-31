"""Native shared-library build helpers for FMUs."""
from __future__ import annotations

from pathlib import Path
import subprocess

from scripts.common.paths import REPO_ROOT
from scripts.artifacts.build.native_fmu_project import NativeFmuProject


def build_native_library(project: NativeFmuProject, build_dir: Path) -> Path:
    subprocess.run(
        ["cmake", "-S", str(project.source_root), "-B", str(build_dir), "-DCMAKE_BUILD_TYPE=Release"],
        check=True,
        cwd=REPO_ROOT,
    )
    subprocess.run(
        ["cmake", "--build", str(build_dir), "--config", "Release"],
        check=True,
        cwd=REPO_ROOT,
    )

    candidates = sorted(
        path for path in build_dir.rglob("*.so")
        if path.is_file() and "CMakeFiles" not in path.parts
    )
    if not candidates:
        raise SystemExit(f"Native library not found under {build_dir}")
    if len(candidates) == 1:
        return candidates[0]

    exact_matches = [path for path in candidates if path.stem == project.model_identifier]
    if len(exact_matches) == 1:
        return exact_matches[0]
    raise SystemExit(
        f"Expected one native library for {project.model_identifier}, found: {[path.name for path in candidates]}"
    )
