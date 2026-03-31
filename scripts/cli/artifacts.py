#!/usr/bin/env python3
"""Artifact generation, build, and packaging commands."""
from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("export", help="Export all architecture-derived artifacts.")
    subparsers.add_parser("save-architecture", help="Write a JSON snapshot of the architecture.")
    subparsers.add_parser("generate-interface-defs", help="Generate Modelica interface definitions.")
    subparsers.add_parser("generate-c-interface-defs", help="Generate native C/C++ interface headers.")
    subparsers.add_parser("build-modelica-fmus", help="Build only Modelica FMUs.")
    subparsers.add_parser("build-native-fmus", help="Build only native shared libraries.")
    subparsers.add_parser("package-native-fmus", help="Package built native shared libraries into FMUs.")
    bridge = subparsers.add_parser("build-flightgear-bridge-fmu", help="Build only the FlightGear bridge FMU.")
    bridge.add_argument("--output", type=Path, required=True, help="Target FMU path.")
    bridge.add_argument("--build-dir", type=Path, required=True, help="Build directory for the native FMU.")
    subparsers.add_parser("package-ssp", help="Package FMUs and the SSD into an SSP archive.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args, remaining = parser.parse_known_args(argv)
    if args.command == "export":
        from scripts.lib.artifacts.sysml_export import export_artifacts

        return export_artifacts.main(remaining)
    if args.command == "save-architecture":
        from scripts.lib.artifacts.sysml_export import save_architecture

        return save_architecture.main(remaining)
    if args.command == "generate-interface-defs":
        from scripts.lib.artifacts.sysml_export import generate_interface_defs

        return generate_interface_defs.main(remaining)
    if args.command == "generate-c-interface-defs":
        from scripts.lib.artifacts.sysml_export import generate_c_interface_defs

        return generate_c_interface_defs.main(remaining)
    if args.command == "build-modelica-fmus":
        from scripts.lib.artifacts.build import modelica_fmu

        return modelica_fmu.main(remaining)
    if args.command == "build-native-fmus":
        from scripts.lib.artifacts.build import native_fmus

        return native_fmus.main(remaining)
    if args.command == "package-native-fmus":
        from scripts.lib.artifacts.package import native_fmu

        return native_fmu.main(remaining)
    if args.command == "build-flightgear-bridge-fmu":
        from scripts.lib.artifacts.build import native_fmus

        output = native_fmus.build_flightgear_bridge_fmu(
            output_fmu=args.output,
            build_dir=args.build_dir,
        )
        print(output)
        return 0
    if args.command == "package-ssp":
        from scripts.lib.artifacts.package import ssp as package_ssp

        return package_ssp.main(remaining)
    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
