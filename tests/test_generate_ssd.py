from __future__ import annotations

import sys
from pathlib import Path

from pyssp_sysml2.ssd import generate_ssd
from pyssp_standard.ssd import SSD

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.artifacts.normalize_generated_metadata import normalize_ssd_xml  # type: ignore  # noqa: E402


def _read_components(output_path: Path):
    with SSD(output_path, mode="r") as ssd:
        assert ssd.system is not None
        return {component.name: component for component in ssd.system.elements}


def test_parameter_connectors_emitted_for_attributes(tmp_path: Path):
    output = tmp_path / "SystemStructure.ssd"
    generate_ssd(REPO_ROOT / "architecture", output, "AircraftComposition")
    normalize_ssd_xml(output)
    components = _read_components(output)

    propulsion = components["turbofan_propulsion"]
    names = {connector.name for connector in propulsion.connectors if connector.kind == "parameter"}

    expected = {
        "max_thrust_kn",
        "dry_thrust_kn",
        "specific_fuel_consumption",
        "fuel_capacity_kg",
        "generator_output_kw",
    }
    assert expected.issubset(names)


def test_string_parameters_preserve_type(tmp_path: Path):
    output = tmp_path / "SystemStructure.ssd"
    generate_ssd(REPO_ROOT / "architecture", output, "AircraftComposition")
    normalize_ssd_xml(output)
    components = _read_components(output)

    control = components["control_interface"]
    string_params = [
        connector
        for connector in control.connectors
        if connector.name == "input_scheme"
        and connector.kind == "parameter"
        and connector.type_.__class__.__name__ == "TypeString"
    ]
    assert string_params


def test_list_parameters_infer_numeric_type(tmp_path: Path):
    output = tmp_path / "SystemStructure.ssd"
    generate_ssd(REPO_ROOT / "architecture", output, "AircraftComposition")
    normalize_ssd_xml(output)
    components = _read_components(output)

    autopilot = components["autopilot_module"]
    real_arrays = {
        connector.name
        for connector in autopilot.connectors
        if connector.kind == "parameter" and connector.type_.__class__.__name__ == "TypeReal"
    }
    expected = {f"waypoint{axis}_km[{idx}]" for axis in ("X", "Y", "Z") for idx in range(10)}
    missing = expected - real_arrays
    assert not missing, f"Waypoint vector parameters should be exposed as Real connectors, missing: {sorted(missing)}"
