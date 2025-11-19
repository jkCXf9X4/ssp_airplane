#!/usr/bin/env python3
"""Bundle FMUs and the SSD into a single SSP archive."""
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import BUILD_DIR, GENERATED_DIR, ensure_parent_dir

DEFAULT_SSD = GENERATED_DIR / "SystemStructure.ssd"
DEFAULT_FMU_DIR = BUILD_DIR / "fmus"
DEFAULT_OUTPUT = BUILD_DIR / "ssp" / "aircraft.ssp"

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fmu-dir", type=Path, default=DEFAULT_FMU_DIR)
    parser.add_argument("--ssd", type=Path, default=DEFAULT_SSD)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.ssd.exists():
        raise SystemExit(f"SSD file not found: {args.ssd}")
    if not args.fmu_dir.exists():
        raise SystemExit(f"FMU directory not found: {args.fmu_dir}")

    ensure_parent_dir(args.output)
    fmu_files = sorted(args.fmu_dir.glob("*.fmu"))
    if not fmu_files:
        raise SystemExit(f"No FMUs found under {args.fmu_dir}")

    with zipfile.ZipFile(args.output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(args.ssd, arcname="SystemStructure.ssd")
        for fmu in fmu_files:
            arcname = f"resources/{fmu.name}"
            archive.write(fmu, arcname=arcname)
            print(f"Added {arcname}")

    print(f"Packaged SSP written to {args.output}")


if __name__ == "__main__":
    main()
