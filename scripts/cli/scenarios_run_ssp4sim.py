#!/usr/bin/env python3
"""CLI for running pyssp4sim from an existing config file."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.lib.scenarios.runtime import run_simulation_with_pyssp4sim


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run pyssp4sim with an existing config JSON.")
    parser.add_argument("--config-path", type=Path, required=True, help="Path to an existing config JSON.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    run_simulation_with_pyssp4sim(args.config_path)
    print(json.dumps({"config_path": str(args.config_path), "status": "completed"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
