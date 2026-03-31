"""Check that the generated SSD complies with the SSP XML schema."""
from __future__ import annotations

from pathlib import Path

from pyssp_standard.ssd import SSD

from scripts.lib.paths import GENERATED_DIR

DEFAULT_SSD_PATH = GENERATED_DIR / "SystemStructure.ssd"


def verify_ssd_xml(ssd_path: Path) -> int:
    if not ssd_path.exists():
        raise SystemExit(f"SSD file not found: {ssd_path}")
    with SSD(ssd_path) as handle:
        handle.__check_compliance__()
    print(f"SSD XML compliance verified for {ssd_path}")
    return 0
