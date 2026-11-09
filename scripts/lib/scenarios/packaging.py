"""SSP packaging helpers for scenario simulation runs.

Array index mapping follows the FMUs, not a fixed convention: the scenario
dialect emits zero-based array member names (``waypointX_km[0..9]``) while
OMC-built FMUs export one-based FMI variables (``waypointX_km[1..10]``). At
bind time the mapping is derived from each component's ``modelDescription.xml``
inside the baseline SSP archive — the declared index at ordinal position *k* of
the sorted index sequence is the truth for member *k*. No component identity
and no fixed shift is assumed; a component or base absent from the map is left
untouched.
"""

from __future__ import annotations

import io
import json
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from pyssp_standard import SSM, SSP, SSV

SSD_NS = "http://ssp-standard.org/SSP1/SystemStructureDescription"
_SSD_ENTRY = "SystemStructure.ssd"

_ARRAY_INDEX_RE = re.compile(r"^(?P<base>.+)\[(?P<index>\d+)\]$")
_FMU_SUFFIX = ".fmu"


def _fmu_declared_array_indices(ssp_path: Path) -> dict[str, dict[str, tuple[int, ...]]]:
    """Read each FMU's declared array indices from inside the baseline SSP.

    Returns ``{component: {base: (index, ...)}}`` where the indices are the
    sorted numeric indices the component's own FMU declares (e.g.
    ``{"autopilot_module": {"waypointX_km": (1, 2, ..., 10)}}``). Components
    without a readable model description, or without array parameters, simply
    contribute nothing and are left untouched at bind time.
    """
    component_bases: dict[str, dict[str, tuple[int, ...]]] = {}
    with zipfile.ZipFile(ssp_path) as archive:
        try:
            ssd_root = ET.fromstring(archive.read(_SSD_ENTRY))
        except KeyError as exc:
            raise ValueError(f"Baseline SSP has no {_SSD_ENTRY}: {ssp_path}") from exc
        for component in ssd_root.iter(f"{{{SSD_NS}}}Component"):
            source = component.get("source") or ""
            if not (source.startswith("resources/") and source.endswith(_FMU_SUFFIX)):
                continue
            try:
                fmu_bytes = archive.read(source)
            except KeyError:
                continue
            with zipfile.ZipFile(io.BytesIO(fmu_bytes)) as fmu:
                try:
                    md_root = ET.fromstring(fmu.read("modelDescription.xml"))
                except (KeyError, zipfile.BadZipFile):
                    continue
            bases: dict[str, list[int]] = {}
            for scalar in md_root.iter("ScalarVariable"):
                match = _ARRAY_INDEX_RE.match(scalar.get("name", ""))
                if match is not None:
                    bases.setdefault(match.group("base"), []).append(int(match.group("index")))
            component_bases[component.get("name", "")] = {
                base: tuple(sorted(indices)) for base, indices in bases.items()
            }
    return component_bases


def _ordinal_index_map(indices: tuple[int, ...]) -> dict[int, int]:
    """Map ordinal position in the zero-based canonical sequence to a declared index."""
    return {ordinal: index for ordinal, index in enumerate(indices)}


def _consensus_base_map(
    component_bases: dict[str, dict[str, tuple[int, ...]]],
) -> dict[str, dict[int, int]]:
    """Per bare base, the ordinal->index map agreed by every declaring component.

    A base whose components disagree about their index sequences is omitted so
    its members stay untouched: no single bare-name rename would be correct.
    """
    by_base: dict[str, list[tuple[int, ...]]] = {}
    for bases in component_bases.values():
        for base, indices in bases.items():
            by_base.setdefault(base, []).append(indices)
    return {
        base: _ordinal_index_map(indices[0])
        for base, indices in by_base.items()
        if all(sequence == indices[0] for sequence in indices[1:])
    }


def _renamed_name(
    name: str,
    *,
    component_bases: dict[str, dict[str, tuple[int, ...]]],
    base_map: dict[str, dict[int, int]],
) -> str:
    """Rebase ``name``'s bracketed array index onto its FMU's declared index.

    Bare member names (SSV parameters, SSM sources) use the consensus per-base
    map; component-qualified names (SSM targets) use the declaring component's
    own FMU sequence. Names without a matching mapping are returned unchanged.
    """
    match = _ARRAY_INDEX_RE.match(name)
    if match is None:
        return name
    base = match.group("base")
    ordinal = int(match.group("index"))
    if "." in base:
        component, member = base.split(".", 1)
        indices = component_bases.get(component, {}).get(member)
        if indices is None:
            return name
        mapping = _ordinal_index_map(indices)
    else:
        mapping = base_map.get(base)
        if mapping is None:
            return name
    declared = mapping.get(ordinal)
    if declared is None:
        return name
    return f"{base}[{declared}]"


def _write_bound_documents(
    parameter_set_path: Path,
    ssm_path: Path,
    *,
    component_bases: dict[str, dict[str, tuple[int, ...]]],
    base_map: dict[str, dict[int, int]],
    run_dir: Path,
    set_name: str,
) -> tuple[Path, Path]:
    """Rebuild the bound SSV/SSM with FMU-truth array indices, via the pyssp API."""
    bound_ssv = run_dir / f"{set_name}.ssv"
    bound_ssm = run_dir / ssm_path.name

    with SSV(parameter_set_path, mode="r") as source:
        parameters = [
            parameter.renamed(
                _renamed_name(
                    parameter.name,
                    component_bases=component_bases,
                    base_map=base_map,
                )
            )
            for parameter in source.xml.parameters
        ]
    with SSV(bound_ssv, mode="w") as target:
        target.xml.extend_parameters(parameters)

    with SSM(ssm_path, mode="r") as source:
        entries = [
            (entry.source, entry.target, entry.suppress_unit_conversion)
            for entry in source.xml.mappings
        ]
    with SSM(bound_ssm, mode="w") as target:
        for source_name, target_name, suppress_unit_conversion in entries:
            target.add_mapping(
                _renamed_name(
                    source_name,
                    component_bases=component_bases,
                    base_map=base_map,
                ),
                _renamed_name(
                    target_name,
                    component_bases=component_bases,
                    base_map=base_map,
                ),
                suppress_unit_conversion=suppress_unit_conversion,
            )

    return bound_ssv, bound_ssm


def package_ssp_with_parameters(
    ssp_path: Path,
    parameter_set_path: Path,
    scenario_stem: str,
    results_dir: Path,
    *,
    ssm_path: Path | None = None,
    analysis_descriptor_path: Path | None = None,
) -> Path:
    """Package a prepared scenario parameter set into an SSP via the pyssp API.

    The baseline ``ssp_path`` is copied to ``results_dir/<stem>_run/<stem>.ssp``
    and opened for edit; the scenario SSV is bound as an external resource and,
    when ``ssm_path`` is given, bound with the analysis SSM as the mapping so
    the bare scenario names resolve onto component parameters.

    Array member names are rebased onto each FMU's declared index sequence at
    bind time (see module docstring and ``_fmu_declared_array_indices``); the
    bound copies are what lands in the run directory and inside the SSP.

    When ``analysis_descriptor_path`` is given, the descriptor plus the bound
    scenario SSV and SSM are emitted next to the prepared SSP
    (``results_dir/<stem>_run/analysis.json``) so a downstream analysis reader
    can resolve scenario, experiment, and target SSD from one path.
    """
    run_dir = results_dir / f"{scenario_stem}_run"
    run_dir.mkdir(parents=True, exist_ok=True)
    prepared_ssp_path = run_dir / f"{scenario_stem}.ssp"

    if not ssp_path.is_file():
        raise FileNotFoundError(f"Baseline SSP not found: {ssp_path}")
    if not parameter_set_path.is_file():
        raise FileNotFoundError(f"Scenario parameter set not found: {parameter_set_path}")
    if ssm_path is not None and not ssm_path.is_file():
        raise FileNotFoundError(f"Scenario parameter mapping not found: {ssm_path}")
    if analysis_descriptor_path is not None and not analysis_descriptor_path.is_file():
        raise FileNotFoundError(f"Analysis descriptor not found: {analysis_descriptor_path}")

    if prepared_ssp_path.exists():
        prepared_ssp_path.unlink()
    shutil.copy2(ssp_path, prepared_ssp_path)

    # The bound set is named after the scenario set so the resource matches the
    # descriptor's scenario["ssv"] name.
    set_name = "MissionScenario"
    if ssm_path is not None:
        component_bases = _fmu_declared_array_indices(ssp_path)
        base_map = _consensus_base_map(component_bases)
        bound_ssv, bound_ssm = _write_bound_documents(
            parameter_set_path,
            ssm_path,
            component_bases=component_bases,
            base_map=base_map,
            run_dir=run_dir,
            set_name=set_name,
        )
    else:
        bound_ssv = parameter_set_path
        bound_ssm = None

    with SSP(prepared_ssp_path, mode="a") as ssp:
        ssp.bind_parameters(
            bound_ssv,
            mapping=bound_ssm,
            name=set_name if bound_ssm is not None else None,
            placement="external",
        )

    if analysis_descriptor_path is not None:
        descriptor = json.loads(analysis_descriptor_path.read_text(encoding="utf-8"))
        scenario = descriptor.get("scenario")
        if scenario is not None:
            if bound_ssm is not None and bound_ssm != run_dir / scenario["ssm"]:
                shutil.copy2(bound_ssm, run_dir / scenario["ssm"])
        (run_dir / "analysis.json").write_text(
            json.dumps(descriptor, indent=2) + "\n",
            encoding="utf-8",
        )

    return prepared_ssp_path