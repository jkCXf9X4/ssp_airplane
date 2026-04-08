"""SSP packaging helpers for scenario simulation runs."""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET


def package_ssp_with_parameters(
    ssp_path: Path,
    parameter_set_path: Path,
    scenario_stem: str,
    results_dir: Path,
) -> Path:
    run_dir = results_dir / f"{scenario_stem}_run"
    unpack_dir = run_dir / "unpacked"
    if unpack_dir.exists():
        shutil.rmtree(unpack_dir)
    unpack_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(ssp_path, "r") as archive:
        archive.extractall(unpack_dir)

    resources_dir = unpack_dir / "resources"
    resources_dir.mkdir(parents=True, exist_ok=True)
    packaged_parameter_set_path = resources_dir / parameter_set_path.name
    shutil.copy(parameter_set_path, packaged_parameter_set_path)

    ssd_path = unpack_dir / "SystemStructure.ssd"
    ssd_ns = "http://ssp-standard.org/SSP1/SystemStructureDescription"
    ssc_ns = "http://ssp-standard.org/SSP1/SystemStructureCommon"
    ET.register_namespace("ssd", ssd_ns)
    ET.register_namespace("ssc", ssc_ns)
    ns = {"ssd": ssd_ns}
    tree = ET.parse(ssd_path)
    root = tree.getroot()
    system = root.find(".//ssd:System", ns)
    if system is None:
        system = root
    bindings = system.find("ssd:ParameterBindings", ns)
    if bindings is None:
        bindings = ET.SubElement(system, f"{{{ssd_ns}}}ParameterBindings")

    binding_source = f"resources/{packaged_parameter_set_path.name}"
    for existing in list(bindings):
        if existing.get("source") == binding_source:
            bindings.remove(existing)

    ET.SubElement(bindings, f"{{{ssd_ns}}}ParameterBinding", attrib={"source": binding_source})
    ET.indent(tree, space="  ")
    tree.write(ssd_path, encoding="UTF-8", xml_declaration=True)

    prepared_ssp_path = run_dir / f"{scenario_stem}.ssp"
    if prepared_ssp_path.exists():
        prepared_ssp_path.unlink()
    with zipfile.ZipFile(prepared_ssp_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in unpack_dir.rglob("*"):
            if path.is_file():
                archive.write(path, arcname=path.relative_to(unpack_dir))
    return prepared_ssp_path
