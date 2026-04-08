# AGENTS

## Scope

This file applies to everything under `scripts/lib/artifacts/`.

## Ownership Map

- `sysml_export/`: export architecture-derived generated artifacts such as headers, model descriptions, and snapshots

Choose the directory by the primary action:

- Exporting generated metadata from architecture or interface definitions: edit `sysml_export/`

Canonical workflow note:

- CMake is the canonical owner of FMU and SSP build/package behavior.
- Do not reintroduce Python-owned FMU or SSP packaging paths under `scripts/lib/artifacts/`.

## Edit Rules

- Do not create sibling modules with names that differ only slightly from existing ones.
- Do not add thin wrappers around existing build, package, or export functions.
- Prefer extending the module that already owns the artifact type.
- If a CLI command already maps to one of these modules, keep that mapping direct.
- Do not move canonical build/package responsibilities out of CMake.

## File Selection Heuristics

- Architecture snapshot and generated header/model description export belong under `sysml_export/`
- FMU and SSP build/package logic belong in CMake under `cmake/` and model `CMakeLists.txt` files

## Before Adding A File

Only add a new module if one of these is true:

- the artifact type is genuinely new
- the existing export file would otherwise combine different artifact lifecycles
- the existing file would become difficult to understand because it mixes unrelated abstractions

If none of those apply, edit the existing module instead.
