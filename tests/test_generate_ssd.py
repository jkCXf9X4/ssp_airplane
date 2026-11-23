from __future__ import annotations

import sys
from pathlib import Path

from pycps_sysml2 import core_definitions
from pyfmi_rpr import rpr_entity
from pyssp_standard import SSD
from pyssp_sysml2.artifacts.ssd import generate_ssd

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

COMPOSITION = "AircraftModel"
INCLUDES = (core_definitions(), rpr_entity())


def _read_components(output_path: Path):
    with SSD(output_path, mode="r") as ssd:
        assert ssd.system is not None
        return {component.name: component for component in ssd.system.elements}


def test_parameter_connectors_emitted_for_attributes(tmp_path: Path):
    output = tmp_path / "SystemStructure.ssd"
    generate_ssd(
        REPO_ROOT / "architecture", output, COMPOSITION, includes=INCLUDES, base_index=1
    )
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
    generate_ssd(
        REPO_ROOT / "architecture", output, COMPOSITION, includes=INCLUDES, base_index=1
    )
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
    generate_ssd(
        REPO_ROOT / "architecture", output, COMPOSITION, includes=INCLUDES, base_index=1
    )
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
    generate_ssd(
        REPO_ROOT / "architecture", output, COMPOSITION, includes=INCLUDES, base_index=1
    )
    with SSD(output, mode="r") as ssd:
        assert ssd.system is not None
        assert ssd.system.name == "AircraftModel"


def test_rpr_state_source_broadcasts_into_rpr_entity(tmp_path: Path):
    output = tmp_path / "SystemStructure.ssd"
    generate_ssd(
        REPO_ROOT / "architecture", output, COMPOSITION, includes=INCLUDES, base_index=1
    )
    components = _read_components(output)
    assert {"rpr_state_source", "rpr_entity"} <= set(components)

    source = components["rpr_state_source"]
    outputs = {connector.name for connector in source.connectors if connector.kind == "output"}
    expected_outputs = {
        "entityState.entity_identifier_site",
        "entityState.entity_identifier_application",
        "entityState.entity_identifier_entity",
        "entityState.entity_type_kind",
        "entityState.entity_type_domain",
        "entityState.entity_type_country",
        "entityState.entity_type_category",
        "entityState.entity_type_subcategory",
        "entityState.entity_type_specific",
        "entityState.entity_type_extra",
        "entityState.marking_character_set",
        "entityState.marking_characters",
        "entityState.force",
        "entityState.spatial_world_location_x",
        "entityState.spatial_world_location_y",
        "entityState.spatial_world_location_z",
        "entityState.spatial_orientation_psi",
        "entityState.spatial_orientation_theta",
        "entityState.spatial_orientation_phi",
        "entityState.spatial_velocity_x",
        "entityState.spatial_velocity_y",
        "entityState.spatial_velocity_z",
        "entityState.spatial_acceleration_x",
        "entityState.spatial_acceleration_y",
        "entityState.spatial_acceleration_z",
        "entityState.spatial_angular_velocity_x",
        "entityState.spatial_angular_velocity_y",
        "entityState.spatial_angular_velocity_z",
        "entityState.spatial_dead_reckoning_algorithm",
        "entityState.spatial_is_frozen",
    }
    assert outputs == expected_outputs

    parameters = {connector.name for connector in source.connectors if connector.kind == "parameter"}
    assert {
        "reference_latitude_deg",
        "reference_longitude_deg",
        "reference_altitude_m",
        "entity_site",
        "entity_application",
        "entity_entity",
        "entity_type_kind",
        "entity_type_domain",
        "entity_type_country",
        "entity_type_category",
        "entity_type_subcategory",
        "entity_type_specific",
        "entity_type_extra",
        "force",
        "marking_character_set",
        "marking_characters",
    } <= parameters

    text = output.read_text()
    assert 'startElement="rpr_state_source"' in text
    assert 'startConnector="entityState.spatial_world_location_x"' in text
    assert 'endElement="rpr_entity"' in text
    assert 'endConnector="entityState.spatial_world_location_x"' in text
