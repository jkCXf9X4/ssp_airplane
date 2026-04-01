from __future__ import annotations

import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.lib.artifacts.package.ssp import package_ssp  # type: ignore  # noqa: E402


def test_package_ssp_resolves_modelica_fmu_prefix(tmp_path: Path):
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

    modelica_dir = tmp_path / "cmake" / "fmus"
    modelica_dir.mkdir(parents=True)
    (modelica_dir / "Aircraft_ControlInterface.fmu").write_text("modelica", encoding="utf-8")

    output = tmp_path / "aircraft.ssp"
    package_ssp(fmu_dir=native_dir, ssd=ssd, output=output)

    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())

    assert "SystemStructure.ssd" in names
    assert "resources/ControlInterface.fmu" in names
    assert "resources/FlightGearBridge.fmu" in names
