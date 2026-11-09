from __future__ import annotations

import sys
from pathlib import Path

from pyssp_sysml2.artifacts.ssd import generate_ssd
from pyssp_standard import SSD

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.lib.common.xml import normalize_ssd_xml  # type: ignore  # noqa: E402

COMPOSITION = "AircraftModel"


def _read_components(output_path: Path):
    with SSD(output_path, mode="r") as ssd:
        assert ssd.system is not None
        return {component.name: component for component in ssd.system.elements}


def test_parameter_connectors_emitted_for_attributes(tmp_path: Path):
    output = tmp_path / "SystemStructure.ssd"
    generate_ssd(REPO_ROOT / "architecture", output, COMPOSITION, base_index=1)
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
    generate_ssd(REPO_ROOT / "architecture", output, COMPOSITION, base_index=1)
    normalize_ssd_xml(output)
    components = _read_components(output)

    control = components["control_interface"]
    string_params = [
        connector
        for connector in control.connectors
        if connector.name == "input_scheme"
        and connector.kind == "parameter"
        and connector.type_name == "String"
    ]
    assert string_params


def test_list_parameters_infer_numeric_type(tmp_path: Path):
    output = tmp_path / "SystemStructure.ssd"
    generate_ssd(REPO_ROOT / "architecture", output, COMPOSITION, base_index=1)
    normalize_ssd_xml(output)
    components = _read_components(output)

    autopilot = components["autopilot_module"]
    real_arrays = {
        connector.name
        for connector in autopilot.connectors
        if connector.kind == "parameter" and connector.type_name == "Real"
    }
    expected = {f"waypoint{axis}_km[{idx}]" for axis in ("X", "Y", "Z") for idx in range(1, 11)}
    missing = expected - real_arrays
    assert not missing, f"Waypoint vector parameters should be exposed as Real connectors, missing: {sorted(missing)}"


def test_composition_name_is_aircraft_model(tmp_path: Path):
    output = tmp_path / "SystemStructure.ssd"
    generate_ssd(REPO_ROOT / "architecture", output, COMPOSITION, base_index=1)
    with SSD(output, mode="r") as ssd:
        assert ssd.system is not None
        assert ssd.system.name == "AircraftModel"
