#!/usr/bin/env python3
"""CLI for writing a pyssp4sim config file."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.lib.scenarios.runtime import create_simulation_config, write_simulation_config


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create and write a pyssp4sim simulation config JSON.")
    parser.add_argument("--prepared-ssp", type=Path, required=True, help="Path to the prepared SSP archive.")
    parser.add_argument("--result-file", type=Path, required=True, help="Path to the result CSV to be written.")
    parser.add_argument("--stop-time", type=float, required=True, help="Simulation stop time in seconds.")
    parser.add_argument("--config-path", type=Path, default=None, help="Path to write the config JSON.")
    parser.add_argument("--realtime", action="store_true", help="Enable realtime pacing.")
    parser.add_argument("--log-fmu", action="store_true", help="Enable FMU logging in the config.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config = create_simulation_config(
        ssp_path=args.prepared_ssp,
        result_file=args.result_file,
        stop_time=args.stop_time,
        realtime=args.realtime,
        log_fmu=args.log_fmu,
    )
    config_path = write_simulation_config(
        config=config,
        result_file=args.result_file,
        config_path=args.config_path,
    )
    print(
        json.dumps(
            {
                "prepared_ssp": str(args.prepared_ssp),
                "result_file": str(args.result_file),
                "config_path": str(config_path),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
