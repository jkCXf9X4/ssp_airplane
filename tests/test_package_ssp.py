from __future__ import annotations

import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.lib.scenarios.preparation import emit_waypoint_parameter_set  # type: ignore  # noqa: E402
from scripts.lib.scenarios.packaging import package_ssp_with_parameters  # type: ignore  # noqa: E402

SSD_NS = "http://ssp-standard.org/SSP1/SystemStructureDescription"


@pytest.fixture
def baseline_ssp() -> Path:
    baseline = REPO_ROOT / "build" / "ssp" / "aircraft.ssp"
    if not baseline.is_file():
        pytest.skip(f"Baseline SSP not built: {baseline}")
    return baseline


def test_package_ssp_binds_scenario_resources_and_one_based_indices(tmp_path: Path, baseline_ssp: Path) -> None:
    parameter_set_path = tmp_path / "waypoints.ssv"
    emit_waypoint_parameter_set(
        [
            {"x_km": 0.0, "y_km": 0.0, "z_km": 0.1},
            {"x_km": 12.5, "y_km": -3.0, "z_km": 1.2},
            {"x_km": 20.0, "y_km": 4.0, "z_km": 2.5},
        ],
        parameter_set_path,
        waypoint_proximity_km=2.5,
        target_airspeed_mps=240.0,
    )

    results_dir = tmp_path / "results"
    prepared = package_ssp_with_parameters(
        ssp_path=baseline_ssp,
        parameter_set_path=parameter_set_path,
        scenario_stem="test_scenario",
        results_dir=results_dir,
        ssm_path=REPO_ROOT / "generated" / "analysis" / "HighAltitudeIntercept.ssm",
        analysis_descriptor_path=REPO_ROOT / "generated" / "analysis" / "analysis.json",
    )
    assert prepared.is_file()

    with zipfile.ZipFile(prepared) as archive:
        names = set(archive.namelist())
        assert "resources/MissionScenario.ssv" in names
        assert "resources/HighAltitudeIntercept.ssm" in names

        ssd_root = ET.fromstring(archive.read("SystemStructure.ssd"))
        binding = ssd_root.find(f".//{{{SSD_NS}}}ParameterBinding")
        assert binding is not None
        assert binding.get("source") == "resources/MissionScenario.ssv"
        mapping = binding.find(f"{{{SSD_NS}}}ParameterMapping")
        assert mapping is not None
        assert mapping.get("source") == "resources/HighAltitudeIntercept.ssm"

        bound_ssv = archive.read("resources/MissionScenario.ssv").decode()
        assert "waypointX_km[0]" not in bound_ssv
        assert 'name="waypointX_km[1]"' in bound_ssv
        assert 'name="waypointX_km[10]"' in bound_ssv


def test_package_ssp_collects_fmus_referenced_by_ssd(tmp_path: Path, baseline_ssp: Path) -> None:
    with zipfile.ZipFile(baseline_ssp) as archive:
        names = set(archive.namelist())
    assert "SystemStructure.ssd" in names
    assert "resources/ControlInterface.fmu" in names
    assert "resources/Ros2UdpBridge.fmu" in names