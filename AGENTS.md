# AGENTS

## Guidelines

try to generate code by the common code guidelines
 - Keep it simple
 - Minimize duplication
 - Keep files small and focused
 - Any unit or function should try and contain a common level of abstraction  

This is an experimental software, this means:
- Interfaces do not need to be stable, prioritize code clarity and ease of use
- Avoid creating thin shims or wrappers, change the references directly  


## Environment Guidelines

- Use the repo-local `venv` for Python commands, test runs, and workflow scripts when it exists.
- Prefer `. venv/bin/activate && <command>` over the system Python for `pytest`, `python -m ...`, and related tooling.

## Workflow Methodology

- Keep a clear phase split:
  Python generates artifacts into `generated/`,
  CMake builds and packages FMUs and the baseline SSP,
  Python runs simulations through `ssp4sim` and analyzes results.
- Treat Python packaging commands as compatibility tooling, not the canonical workflow.
- Keep run-specific scenario parameter injection in the simulation phase, not in the baseline build/package phase.
- Prefer changes that strengthen this phase boundary over changes that blur it.

## Documentation Guidelines

- Keep docs short, focused, and single-purpose.
- Prefer adding a new focused page over growing a mixed-purpose page.
- Treat `README.md` as a landing page, not a full manual.
- Keep the main onboarding flow in `docs/getting_started.md`.
- Keep reference material in `docs/command_reference.md`, not in onboarding pages.
- Organize docs by audience:
  `docs/user/` for user workflows,
  `docs/dev/` for maintainer and implementation notes,
  `docs/integrations/` for external system integrations.
- Strongly prefer canonical pages over compatibility stubs or redirect files.
- When moving docs, update links to the new destination and remove obsolete references.
- Optimize for the easiest first success:
  show the lowest-friction path before the full rebuild path.
- Scope prerequisites to the workflow that actually needs them.
- Avoid duplication across pages.
- If two pages repeat the same explanation, keep it in one page and link to it.
- Start pages with what the reader can do there and who the page is for.
- Keep filenames stable and descriptive.
- Use `docs/index.md` as the main documentation router.
