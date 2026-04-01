# AGENTS

## Scope

This file applies to everything under `scripts/lib/artifacts/`.

## Ownership Map

- `build/`: build FMUs or native artifacts from checked-in sources
- `package/`: package already-built artifacts into distributable outputs
- `sysml_export/`: export architecture-derived generated artifacts such as headers, model descriptions, and snapshots

Choose the directory by the primary action:

- Building compiled outputs: edit `build/`
- Packaging files for delivery: edit `package/`
- Exporting generated metadata from architecture or interface definitions: edit `sysml_export/`

## Edit Rules

- Do not create sibling modules with names that differ only slightly from existing ones.
- Do not add thin wrappers around existing build, package, or export functions.
- Prefer extending the module that already owns the artifact type.
- If a CLI command already maps to one of these modules, keep that mapping direct.

## File Selection Heuristics

- Native FMU or native library build logic belongs under `build/native.py`
- Modelica FMU build logic belongs under `build/modelica.py`
- Native FMU packaging belongs under `package/native.py`
- SSP packaging belongs under `package/ssp.py`
- Architecture snapshot and generated header/model description export belong under `sysml_export/`

## Before Adding A File

Only add a new module if one of these is true:

- the artifact type is genuinely new
- the existing file would otherwise combine different artifact lifecycles
- the existing file would become difficult to understand because it mixes unrelated abstractions

If none of those apply, edit the existing module instead.
