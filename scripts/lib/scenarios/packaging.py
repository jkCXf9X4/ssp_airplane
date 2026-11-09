"""SSP packaging helpers for scenario simulation runs.

Array member names are natively one-based (``waypointX_km[1..10]``), matching
the array indices OMC-built FMUs declare in their ``modelDescription.xml``; the
scenario SSV and analysis SSM carry the same one-based names, so the prepared
parameter set is bound into the baseline SSP unchanged.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from pyssp_standard import SSP


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

    The scenario set and the analysis SSM are natively one-based, so they bind
    unchanged. When ``analysis_descriptor_path`` is given, the descriptor plus
    the bound scenario SSV and SSM are emitted next to the prepared SSP
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
    bound_ssv = parameter_set_path
    bound_ssm = ssm_path

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