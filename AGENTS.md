# AGENTS

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
