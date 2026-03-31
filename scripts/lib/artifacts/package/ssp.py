"""Bundle FMUs and the SSD into a single SSP archive."""
from __future__ import annotations

import zipfile
from pathlib import Path

from scripts.lib.paths import BUILD_DIR, GENERATED_DIR, ensure_parent_dir

DEFAULT_SSD = GENERATED_DIR / "SystemStructure.ssd"
DEFAULT_FMU_DIR = BUILD_DIR / "fmus"
DEFAULT_OUTPUT = BUILD_DIR / "ssp" / "aircraft.ssp"

def package_ssp(
    fmu_dir: Path = DEFAULT_FMU_DIR,
    ssd: Path = DEFAULT_SSD,
    output: Path = DEFAULT_OUTPUT,
) -> Path:
    if not ssd.exists():
        raise SystemExit(f"SSD file not found: {ssd}")
    if not fmu_dir.exists():
        raise SystemExit(f"FMU directory not found: {fmu_dir}")

    ensure_parent_dir(output)
    fmu_files = sorted(fmu_dir.glob("*.fmu"))
    if not fmu_files:
        raise SystemExit(f"No FMUs found under {fmu_dir}")

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(ssd, arcname="SystemStructure.ssd")
        for fmu in fmu_files:
            arcname = f"resources/{fmu.name}"
            archive.write(fmu, arcname=arcname)
            print(f"Added {arcname}")
    return output
