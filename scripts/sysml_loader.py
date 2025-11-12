"""SysML v2 architecture loader backed by PySysML2."""
from __future__ import annotations

import sys
from pathlib import Path
import tempfile
from typing import Any, Dict, List, Optional, Tuple

THIRD_PARTY = Path(__file__).resolve().parents[1] / "third_party"
if THIRD_PARTY.exists() and str(THIRD_PARTY) not in sys.path:
    sys.path.insert(0, str(THIRD_PARTY))

from anytree import PreOrderIter
from pysysml2.modeling import Model

# Map SysML part names to their canonical component identifiers.
COMPONENT_ID_MAP: Dict[str, str] = {
    "WingmanDrone": "comp.airframe",
    "CompositeAirframe": "comp.fuselage",
    "TurbofanPropulsion": "comp.propulsion",
    "AdaptiveWingSystem": "comp.wings",
    "MissionComputer": "comp.mission_computer",
    "AutopilotModule": "comp.autopilot",
    "PowerSystem": "comp.power",
    "FuelSystem": "comp.fuel",
    "ControlInterface": "comp.control_interface",
}

# Map SysML part names to Modelica classes used when sourcing FMUs.
MODEL_CLASS_MAP: Dict[str, str] = {
    "CompositeAirframe": "WingmanDrone.CompositeAirframe",
    "TurbofanPropulsion": "WingmanDrone.TurbofanPropulsion",
    "AdaptiveWingSystem": "WingmanDrone.AdaptiveWingSystem",
    "MissionComputer": "WingmanDrone.MissionComputer",
    "AutopilotModule": "WingmanDrone.AutopilotModule",
    "PowerSystem": "WingmanDrone.PowerSystem",
    "FuelSystem": "WingmanDrone.FuelSystem",
    "ControlInterface": "WingmanDrone.ControlInterface",
}

_ANALYSIS_PART_NAMES = {"AnalysisParameters", "OptimizationSettings", "VariableRange"}


def _preprocess_sysml_source(path: Path) -> Path:
    """Strip constructs unsupported by the current PySysML2 grammar (e.g., data def)."""
    text = path.read_text().splitlines()
    sanitized_lines: List[str] = []
    skip_depth = 0
    skipping = False
    for line in text:
        stripped = line.lstrip()
        if stripped.startswith("data def "):
            skipping = True
            skip_depth = stripped.count("{") - stripped.count("}")
            continue
        if skipping:
            skip_depth += line.count("{") - line.count("}")
            if skip_depth <= 0 and "}" in line:
                skipping = False
            continue
        sanitized_lines.append(line)

    tmp = Path(tempfile.mkstemp(prefix="sysml_sanitized_", suffix=".sysml")[1])
    tmp.write_text("\n".join(sanitized_lines))
    return tmp


def load_architecture(path: Path) -> Dict[str, Any]:
    """Parse the SysML v2 model and return a dictionary compatible with the former YAML schema."""
    model = Model()
    sanitized = _preprocess_sysml_source(path)
    try:
        model.from_sysml2_file(str(sanitized))
    finally:
        sanitized.unlink(missing_ok=True)
    ctx_lookup = {idx: ctx for idx, (_, ctx) in model.sysml2_visitor.element_ctxs.items()}
    package = _find_package(model)

    metadata = _parse_metadata(package)
    requirements = _parse_requirements(package)
    components, port_index = _parse_components(model, ctx_lookup)
    analysis_parameters = _parse_analysis(model, ctx_lookup)
    connectors = _parse_connectors(model, port_index)

    return {
        "metadata": metadata,
        "requirements": requirements,
        "components": components,
        "connectors": connectors,
        "analysis_parameters": analysis_parameters,
    }


def _find_package(model: Model):
    for node in PreOrderIter(model):
        if getattr(node, "sysml2_type", None) == "package":
            return node
    raise ValueError("No SysML package found in architecture model")


def _parse_metadata(package_node) -> Dict[str, Any]:
    attrs = _attribute_map(package_node)
    return {
        "language": attrs.get("language", "SysML v2"),
        "system": attrs.get("system_name", _clean_name(package_node.name)),
        "description": _doc_text(package_node),
        "author": attrs.get("author"),
    }


def _parse_requirements(package_node) -> List[Dict[str, Any]]:
    requirements: List[Dict[str, Any]] = []
    for child in package_node.children:
        if getattr(child, "sysml2_type", None) != "comment":
            continue
        req_id = _requirement_id(_clean_name(child.name))
        requirements.append(
            {
                "id": req_id,
                "text": (child.element_text or "").strip(),
            }
        )
    return requirements


def _parse_components(model: Model, ctx_lookup) -> Tuple[List[Dict[str, Any]], Dict[Tuple[str, str], Dict[str, Any]]]:
    components: List[Dict[str, Any]] = []
    port_index: Dict[Tuple[str, str], Dict[str, Any]] = {}

    for node in PreOrderIter(model):
        if getattr(node, "sysml2_type", None) != "part":
            continue
        keywords = set(getattr(node, "keywords", []) or [])
        name = _clean_name(node.name)
        if "def" not in keywords:
            continue
        if name in _ANALYSIS_PART_NAMES:
            continue

        parameters = _attribute_map(node)
        ports = _port_definitions(node)
        parts = _part_references(node, ctx_lookup)
        component = {
            "name": name,
            "id": COMPONENT_ID_MAP.get(name, _default_component_id(name)),
            "type": "block",
            "description": _doc_text(node),
            "parameters": parameters,
            "ports": ports,
            "parts": parts,
        }
        components.append(component)
        for port in ports:
            port_index[(name, port["name"])] = port
    return components, port_index


def _parse_connectors(model: Model, port_index: Dict[Tuple[str, str], Dict[str, Any]]) -> List[Dict[str, Any]]:
    connectors: List[Dict[str, Any]] = []
    for node in PreOrderIter(model):
        if getattr(node, "sysml2_type", None) != "connect":
            continue
        endpoints = _connection_endpoints(node)
        if len(endpoints) != 2:
            continue
        start_comp, start_port = endpoints[0]
        end_comp, end_port = endpoints[1]
        start_key = COMPONENT_ID_MAP.get(start_comp, _default_component_id(start_comp))
        end_key = COMPONENT_ID_MAP.get(end_comp, _default_component_id(end_comp))
        start_port_data = port_index.get((start_comp, start_port))
        connectors.append(
            {
                "name": _clean_name(node.name),
                "from": f"{start_key}.{start_port}",
                "to": f"{end_key}.{end_port}",
                "kind": (start_port_data or {}).get("kind"),
            }
        )
    return connectors


def _parse_analysis(model: Model, ctx_lookup) -> Dict[str, Any]:
    analysis_node = _find_part_definition(model, "AnalysisParameters")
    if not analysis_node:
        return {}

    analysis = _attribute_map(analysis_node)
    optimization_node = _find_part_definition(model, "OptimizationSettings")
    optimization_vars: List[Dict[str, Any]] = []
    if optimization_node:
        for child in optimization_node.children:
            if getattr(child, "sysml2_type", None) != "specializes":
                continue
            if "part" not in (getattr(child, "keywords", []) or []):
                continue
            name = _clean_name(child.name)
            attrs = _attribute_map(child)
            optimization_vars.append(
                {
                    "name": name,
                    "min": attrs.get("min"),
                    "max": attrs.get("max"),
                }
            )
    if optimization_vars:
        analysis["optimization_variables"] = optimization_vars
    return analysis


def _find_part_definition(model: Model, name: str):
    for node in PreOrderIter(model):
        if getattr(node, "sysml2_type", None) != "part":
            continue
        keywords = set(getattr(node, "keywords", []) or [])
        if "def" not in keywords:
            continue
        if _clean_name(node.name) == name:
            return node
    return None


def _doc_text(node) -> Optional[str]:
    for child in node.children:
        if getattr(child, "sysml2_type", None) == "doc" and child.element_text:
            return child.element_text.strip()
    return None


def _attribute_map(node) -> Dict[str, Any]:
    attrs: Dict[str, Any] = {}
    for child in node.children:
        if getattr(child, "sysml2_type", None) != "attribute":
            continue
        name = _clean_name(child.name)
        attrs[name] = _convert_constant((child.constants or [None])[0])
    return attrs


def _port_definitions(node) -> List[Dict[str, Any]]:
    ports: List[Dict[str, Any]] = []
    for child in node.children:
        if getattr(child, "sysml2_type", None) != "port":
            continue
        port_attrs = _attribute_map(child)
        ports.append(
            {
                "name": _clean_name(child.name),
                "kind": port_attrs.get("kind"),
                "direction": port_attrs.get("direction"),
            }
        )
    return ports


def _part_references(node, ctx_lookup) -> List[Dict[str, Any]]:
    refs: List[Dict[str, Any]] = []
    for child in node.children:
        if getattr(child, "sysml2_type", None) != "specializes":
            continue
        if "part" not in (getattr(child, "keywords", []) or []):
            continue
        ctx = ctx_lookup.get(child.idx)
        target = _specialization_target(ctx)
        refs.append(
            {
                "name": _clean_name(child.name),
                "ref": COMPONENT_ID_MAP.get(target, _default_component_id(target)) if target else None,
                "type": target,
            }
        )
    return [ref for ref in refs if ref["ref"]]


def _specialization_target(ctx) -> Optional[str]:
    if ctx is None:
        return None
    ids = ctx.ID()
    if not ids or len(ids) < 2:
        return None
    return ids[1].getText().strip("'\"")


def _connection_endpoints(node) -> List[Tuple[str, str]]:
    endpoints: List[Tuple[str, str]] = []
    for entry in getattr(node, "related_element_name", []) or []:
        if ":" not in entry:
            continue
        _, payload = entry.split(":", 1)
        payload = payload.strip()
        if "." not in payload:
            continue
        comp, port = payload.split(".", 1)
        endpoints.append((comp.strip(), port.strip()))
    return endpoints


def _requirement_id(raw: str) -> str:
    if raw.startswith("Requirement_"):
        token = raw[len("Requirement_") :]
        return token.replace("_", "-")
    return raw


def _clean_name(raw: Optional[str]) -> str:
    if not raw:
        return ""
    return raw.split("@", 1)[0]


def _convert_constant(value: Optional[str]) -> Any:
    if value is None:
        return None
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    try:
        if "." not in value and lowered not in {"nan", "inf", "-inf"}:
            return int(value)
        return float(value)
    except ValueError:
        return value


def _default_component_id(name: str) -> str:
    slug = "".join(ch if ch.isalnum() else "_" for ch in name or "").strip("_").lower()
    if not slug:
        slug = "component"
    return f"comp.{slug}"
