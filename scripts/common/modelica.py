"""Shared helper utilities for working with SysML architectures."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from scripts.common.paths import REPO_ROOT


MODELICA_TYPE_MAP = {
    "real": "Real",
    "float": "Real",
    "float32": "Real",
    "float64": "Real",
    "double": "Real",
    "integer": "Integer",
    "int": "Integer",
    "int8": "Integer",
    "int32": "Integer",
    "uint8": "Integer",
    "uint32": "Integer",
    "boolean": "Boolean",
    "bool": "Boolean",
    "string": "String",
}


def map_modelica_type(type_name: Optional[str], default: str = "Real") -> str:
    """Return a canonical primitive name (Real/Integer/Boolean/String) for SysML types."""
    if not type_name:
        return default
    key = type_name.strip().lower()
    return MODELICA_TYPE_MAP.get(key, default)


def run_omc(omc_path: str, mos_content: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".mos", delete=False) as handle:
        handle.write(mos_content)
        mos_file = Path(handle.name)

    try:
        proc = subprocess.run(
            [omc_path, str(mos_file)],
            check=True,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise SystemExit("omc executable not found. Install OpenModelica or pass --omc-path") from exc
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.stderr or exc.stdout) from exc
    finally:
        mos_file.unlink(missing_ok=True)

    return proc.stdout
