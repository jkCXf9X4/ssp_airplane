from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.generation.generate_ssd import SSD_NAMESPACE, build_ssd_tree  # type: ignore  # noqa: E402
from scripts.utils.sysmlv2_arch_parser import parse_sysml_folder  # type: ignore  # noqa: E402


def test_parameter_connectors_emitted_for_attributes():
    architecture = parse_sysml_folder(REPO_ROOT / "architecture")
    tree = build_ssd_tree(architecture)
    root = tree.getroot()
    ns = {"ssd": SSD_NAMESPACE}

    propulsion = root.find(".//ssd:Component[@name='TurbofanPropulsion']", ns)
    assert propulsion is not None

    param_connectors = propulsion.findall("ssd:Connectors/ssd:Connector[@kind='parameter']", ns)
    names = {elem.get("name") for elem in param_connectors}

    expected = {
        "max_thrust_kn",
        "dry_thrust_kn",
        "specific_fuel_consumption",
        "fuel_capacity_kg",
        "generator_output_kw",
    }
    assert expected.issubset(names)


def test_string_parameters_preserve_type():
    architecture = parse_sysml_folder(REPO_ROOT / "architecture")
    tree = build_ssd_tree(architecture)
    root = tree.getroot()
    ns = {"ssd": SSD_NAMESPACE, "ssc": "http://ssp-standard.org/SSP1/SystemStructureCommon"}

    control = root.find(".//ssd:Component[@name='ControlInterface']", ns)
    assert control is not None
    connectors = control.findall("ssd:Connectors/ssd:Connector", ns)
    string_params = [
        conn
        for conn in connectors
        if conn.get("name") == "input_scheme"
        and conn.get("kind") == "parameter"
        and conn.find("ssc:String", ns) is not None
    ]
    assert string_params, "ControlInterface.input_scheme should be exposed as a String parameter connector"


def test_list_parameters_infer_numeric_type():
    architecture = parse_sysml_folder(REPO_ROOT / "architecture")
    tree = build_ssd_tree(architecture)
    root = tree.getroot()
    ns = {"ssd": SSD_NAMESPACE, "ssc": "http://ssp-standard.org/SSP1/SystemStructureCommon"}

    autopilot = root.find(".//ssd:Component[@name='AutopilotModule']", ns)
    assert autopilot is not None

    connectors = autopilot.findall("ssd:Connectors/ssd:Connector[@kind='parameter']", ns)
    real_arrays = {
        conn.get("name")
        for conn in connectors
        if conn.find("ssc:Real", ns) is not None
    }
    expected = {f"waypoint{axis}_km[{idx}]" for axis in ("X", "Y", "Z") for idx in range(1, 11)}
    missing = expected - real_arrays
    assert not missing, f"Waypoint vector parameters should be exposed as Real connectors, missing: {sorted(missing)}"
