"""OpenModelica execution helpers."""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from scripts.common.paths import REPO_ROOT


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
