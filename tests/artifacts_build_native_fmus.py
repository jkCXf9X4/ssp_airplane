"""Slim test-local wrapper for configuring and building native FMU libraries."""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from scripts.lib.paths import (
    BUILD_DIR,
    REPO_ROOT,
    ensure_directory,
)

DEFAULT_TEST_NATIVE_BUILD_ROOT = BUILD_DIR / "native"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build native FMU shared libraries for tests.")
    parser.add_argument("--build-root", type=Path, default=DEFAULT_TEST_NATIVE_BUILD_ROOT)
    parser.add_argument(
        "--models",
        nargs="+",
        help="Optional part definition names to build, for example FlightGearBridge",
    )
    return parser.parse_args(argv)


def build_native_fmus(
    build_root: Path = DEFAULT_TEST_NATIVE_BUILD_ROOT,
    models: list[str] | None = None,
) -> list[Path]:
    wanted = set(models or ["FlightGearBridge"])
    supported_targets = {
        "FlightGearBridge": "FlightGearBridge_fmu",
    }
    targets = [supported_targets[model] for model in sorted(wanted) if model in supported_targets]
    if not targets:
        return []

    cmake_build_dir = ensure_directory(build_root / "cmake")
    subprocess.run(
        ["cmake", "-S", str(REPO_ROOT), "-B", str(cmake_build_dir)],
        check=True,
    )
    subprocess.run(
        ["cmake", "--build", str(cmake_build_dir), "--target", *targets],
        check=True,
    )

    output_dir = ensure_directory(build_root / "fmus")
    built: list[Path] = []
    for model in sorted(wanted):
        if model not in supported_targets:
            continue
        packaged_fmu = REPO_ROOT / "build" / "fmus" / f"{model}.fmu"
        destination = output_dir / packaged_fmu.name
        shutil.copy2(packaged_fmu, destination)
        built.append(destination)
    return built


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    built = build_native_fmus(
        build_root=args.build_root,
        models=args.models,
    )
    if not built:
        print("No native projects discovered.")
        return 0
    for path in built:
        print(f"Built native FMU: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
