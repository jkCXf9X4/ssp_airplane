# Documentation usability plan

To keep the restructured CLI scripts discoverable, the following five-step plan was executed and recorded:

1. **Describe the new script grouping** – README now explains the `scripts/generation`, `scripts/verification`, `scripts/workflows`, and `scripts/utils` directories so contributors know where to add or find tooling.
2. **Adopt module-based invocation examples** – Every command reference in README and docs now uses `python3 -m scripts.<module>` so imports keep working after the package split.
3. **Add a quick command reference** – README includes a table that maps common tasks (saving the architecture, generating SSD/SSV, building FMUs, packaging SSPs, simulating scenarios, and running verifications) to their exact entry points.
4. **Clarify the scenario workflow** – The scenario workflow section now walks through generation, rebuild, simulation, and testing with updated commands and context on outputs.
5. **Refresh topic-specific docs** – `docs/autopilot.md` and `docs/results_and_evaluation.md` reference the new modules and highlight how to reuse results, generate waypoint strings, and produce plots without re-running OMSimulator.

Any future documentation updates can be cross-checked against this plan to ensure the CLI structure remains obvious to new users.
