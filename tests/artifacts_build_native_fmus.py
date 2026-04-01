"""Slim test-local wrapper for configuring and building native FMU libraries."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from scripts.lib.paths import (
    ARCHITECTURE_DIR,
    COMPOSITION_NAME,
    DEFAULT_NATIVE_BUILD_ROOT,
    GENERATED_INTERFACE_DIR,
    discover_native_projects,
    ensure_directory,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build native FMU shared libraries for tests.")
    parser.add_argument("--architecture", type=Path, default=ARCHITECTURE_DIR)
    parser.add_argument("--composition", default=COMPOSITION_NAME)
    parser.add_argument("--build-root", type=Path, default=DEFAULT_NATIVE_BUILD_ROOT)
    parser.add_argument(
        "--models",
        nargs="+",
        help="Optional part definition names to build, for example FlightGearBridge",
    )
    return parser.parse_args(argv)


def build_native_fmus(
    architecture_path: Path = ARCHITECTURE_DIR,
    composition: str = COMPOSITION_NAME,
    build_root: Path = DEFAULT_NATIVE_BUILD_ROOT,
    models: list[str] | None = None,
) -> list[Path]:
    from scripts.lib.artifacts.sysml_export.c_headers import generate_headers

    generate_headers(architecture_path, GENERATED_INTERFACE_DIR)
    projects = discover_native_projects(architecture_path, composition, build_root)
    if models:
        wanted = set(models)
        projects = [project for project in projects if project.model_identifier in wanted]

    built: list[Path] = []
    for project in projects:
        ensure_directory(project.build_dir)
        subprocess.run(
            ["cmake", "-S", str(project.source_root), "-B", str(project.build_dir)],
            check=True,
        )
        subprocess.run(["cmake", "--build", str(project.build_dir)], check=True)
        built.append(project.build_dir)
    return built


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    built = build_native_fmus(
        architecture_path=args.architecture,
        composition=args.composition,
        build_root=args.build_root,
        models=args.models,
    )
    if not built:
        print("No native projects discovered.")
        return 0
    for path in built:
        print(f"Built native project: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
