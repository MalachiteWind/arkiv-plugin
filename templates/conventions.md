---
title: arkiv conventions
summary: The frontmatter schema and the research status vocabulary (idea, exploring, promoted, parked, discarded) and the dev and research habits
created: __INIT_DATE__
updated: __INIT_DATE__
---

Created: __INIT_DATE__ · Updated: __INIT_DATE__

This document holds the arkiv schema and the arkiv conventions. A fresh agent reads it to learn the frontmatter fields, the research status values, and the per-category habits. This document is a verbatim copy of the plugin template. Do not hand-edit it. To change it, edit the plugin template. Then run `/arkiv:sync`. That command compares this copy against the template and re-copies the template.

## Frontmatter schema

Every document carries this YAML block at the top:

```yaml
---
title: <short title>
summary: <one specific line — feeds INDEX.md>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---
```

The `summary` is the single most important field. The generated `INDEX.md` shows it. The whole progressive-disclosure design depends on a specific `summary`.

- `dev/` documents add `verified: <YYYY-MM-DD or git-ref>`. This field marks when the anchored paths were last confirmed.
- `research/` documents add two fields:
  - `status: idea | exploring | promoted | parked | discarded`
  - `related: [<dev-slug>, ...]`. A `<dev-slug>` is the basename of the target `dev/` document. It carries no `.md` extension. It carries no path. Example: `related: [architecture]` resolves to `dev/architecture.md`.

The body starts with a visible line: `Created: <date> · Updated: <date>`. The developer wants the date readable while navigating. Dates stay in frontmatter. Dates do not go in filenames, so links and git history do not fragment. The `handoff/` directory is the one exception. It uses dated filenames.

## The research status values

A `research/` document declares one status:

- `idea` — a rough idea. The work has not started.
- `exploring` — under active work.
- `promoted` — the idea became code.
- `parked` — set aside. The idea is still valid. `clean` does not prune a parked idea as stale.
- `discarded` — rejected. The record stays for history. `clean` does not prune it as stale.

## Category habits

Force no taxonomy. arkiv uses no `mod-`, `api-`, or `flow-` prefix. arkiv uses two high-value habits per category.

`dev/` records why the code is the way it is:

1. Anchor to paths. Reference `path/to/file`. Do not paste code. Code drifts. The repository is the source of truth for how. arkiv records what and why.
2. Capture a reconstructed decision for a non-obvious choice. Record the context, the choice, and the trade-off accepted. A reconstructed decision is the most drift-critical artifact. It often is the only record of the rationale. It stops a later session from re-deciding a settled question.

`research/` runs ahead of the code. It holds both worked-out theory and rough ideas intended for implementation:

1. Write the math over words. Write the formulation, not a prose gloss of it. Write the math as TeX. Use `$…$` for inline math. Use `$$…$$` for display math. Never put math in a code fence.
2. Define every symbol you introduce, so a fresh agent can parse it.
3. Do not anchor to implementation code. The idea is not in the code yet. This is the deliberate difference from `dev/`. You may still cite evidence. Reference a result, an output, an experiment, or a data file that tests the idea. Evidence keeps the idea verifiable. A negative result has value. Record it and its evidence too.
4. Keep `status` current. The `status` field lets a fresh agent tell a live idea from a parked or dead idea.
5. Link on promotion. When the idea becomes code, set `status: promoted` and set `related` to the `dev/` document that now describes it. This records the moment an idea becomes part of the repository's why.

## Living top-level files

- `todo.md` is completion-based. It holds the open work queue. A finished task is a prune candidate for `clean`.
- `donotforget.md` is persistence-based. A caveat persists until the design removes the hazard. `clean` never auto-prunes a caveat. `clean` always prompts first. A caveat differs from a `dev/` decision. A `dev/` decision is past-facing. It states "the team chose X over Y because Z." A caveat is future-facing. It states "do not do Y. It breaks Z."
