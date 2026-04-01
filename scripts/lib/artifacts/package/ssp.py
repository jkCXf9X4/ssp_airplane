"""Bundle FMUs and the SSD into a single SSP archive."""
from __future__ import annotations

import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from scripts.lib.paths import BUILD_DIR, GENERATED_DIR, PACKAGE_NAME, ensure_parent_dir

DEFAULT_SSD = GENERATED_DIR / "SystemStructure.ssd"
DEFAULT_FMU_DIR = BUILD_DIR / "fmus"
DEFAULT_OUTPUT = BUILD_DIR / "ssp" / "aircraft.ssp"


def _ssd_fmu_sources(ssd: Path) -> list[str]:
    tree = ET.parse(ssd)
    root = tree.getroot()
    return sorted(
        {
            source
            for component in root.iter()
            if (source := component.get("source")) and source.startswith("resources/") and source.endswith(".fmu")
        }
    )


def _candidate_fmu_dirs(fmu_dir: Path) -> list[Path]:
    candidates = [fmu_dir, fmu_dir.parent / "cmake" / "fmus", BUILD_DIR / "cmake" / "fmus"]
    return [path for path in candidates if path.exists()]


def _fmu_lookup(directories: list[Path]) -> dict[str, Path]:
    lookup: dict[str, Path] = {}
    prefix = f"{PACKAGE_NAME}_"
    for directory in directories:
        for fmu in sorted(directory.glob("*.fmu")):
            lookup.setdefault(fmu.name, fmu)
            if fmu.name.startswith(prefix):
                lookup.setdefault(fmu.name[len(prefix):], fmu)
    return lookup


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
    source_names = _ssd_fmu_sources(ssd)
    if not source_names:
        raise SystemExit(f"No FMU resources referenced by {ssd}")

    lookup = _fmu_lookup(_candidate_fmu_dirs(fmu_dir))
    missing = [source for source in source_names if Path(source).name not in lookup]
    if missing:
        raise SystemExit(
            "Missing FMUs referenced by SSD: "
            + ", ".join(missing)
        )

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(ssd, arcname="SystemStructure.ssd")
        for arcname in source_names:
            fmu = lookup[Path(arcname).name]
            archive.write(fmu, arcname=arcname)
            print(f"Added {arcname}")
    return output
