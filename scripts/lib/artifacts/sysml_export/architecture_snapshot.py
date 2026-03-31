"""Write a JSON snapshot of the merged SysML architecture."""
from __future__ import annotations

from pathlib import Path

from scripts.lib.paths import ARCHITECTURE_DIR, GENERATED_DIR, ensure_parent_dir
from pycps_sysmlv2 import SysMLParser, json_dumps

DEFAULT_ARCH_DIR = ARCHITECTURE_DIR
DEFAULT_OUTPUT = GENERATED_DIR / "arch_def.json"

def save_architecture(
    source: Path = DEFAULT_ARCH_DIR,
    output: Path = DEFAULT_OUTPUT,
) -> Path:
    architecture = SysMLParser(source).parse()
    ensure_parent_dir(output)
    output.write_text(json_dumps(architecture, []))
    return output
