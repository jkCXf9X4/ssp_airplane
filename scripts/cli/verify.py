#!/usr/bin/env python3
"""Verification commands."""
from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("model-equations", help="Run OpenModelica model equation checks.")
    subparsers.add_parser("modelica-variables", help="Verify Modelica interface variables against SysML.")
    subparsers.add_parser("ssd-xml", help="Validate SSD XML compliance.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args, remaining = parser.parse_known_args(argv)
    if args.command == "model-equations":
        from scripts.lib.verify import model_equations

        return model_equations.main(remaining)
    if args.command == "modelica-variables":
        from scripts.lib.verify import modelica_variables

        return modelica_variables.main(remaining)
    if args.command == "ssd-xml":
        from scripts.lib.verify import ssd_xml

        return ssd_xml.main(remaining)
    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
