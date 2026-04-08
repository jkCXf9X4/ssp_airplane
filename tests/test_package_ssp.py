from __future__ import annotations

import subprocess
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_package_ssp_collects_fmus_referenced_by_ssd(tmp_path: Path):
    ssd = tmp_path / "SystemStructure.ssd"
    ssd.write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<ssd:SystemStructureDescription xmlns:ssd="http://ssp-standard.org/SSP1/SystemStructureDescription">
  <ssd:System name="AircraftComposition">
    <ssd:Elements>
      <ssd:Component name="control_interface" source="resources/ControlInterface.fmu" />
      <ssd:Component name="flightgear_bridge" source="resources/FlightGearBridge.fmu" />
    </ssd:Elements>
  </ssd:System>
</ssd:SystemStructureDescription>
""",
        encoding="utf-8",
    )

    native_dir = tmp_path / "fmus"
    native_dir.mkdir()
    (native_dir / "FlightGearBridge.fmu").write_text("native", encoding="utf-8")
    (native_dir / "ControlInterface.fmu").write_text("modelica", encoding="utf-8")

    output = tmp_path / "aircraft.ssp"
    subprocess.run(
        [
            "cmake",
            f"-DSSD_PATH={ssd}",
            f"-DFMU_DIR={native_dir}",
            f"-DOUTPUT_PATH={output}",
            f"-DSTAGE_DIR={tmp_path / 'stage'}",
            "-P",
            str(REPO_ROOT / "cmake" / "PackageSsp.cmake"),
        ],
        check=True,
    )

    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())

    assert "SystemStructure.ssd" in names
    assert "resources/ControlInterface.fmu" in names
    assert "resources/FlightGearBridge.fmu" in names
