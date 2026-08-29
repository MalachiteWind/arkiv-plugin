---
description: Compact the current session into an ephemeral hand-off for the next session
argument-hint: ""
disable-model-invocation: true
---

Compact the current session into a hand-off document. The current chat is too context-heavy. The next session needs a cheap resume point.

## Steps

1. Resolve the repository root. Run `git rev-parse --show-toplevel 2>/dev/null || pwd`. Call the result ROOT. The store is `ROOT/.arkiv`.
2. If `ROOT/.arkiv` does not exist, tell the developer to run `/arkiv:init` first. Then stop.
3. Compute the date. Run `date +%Y-%m-%d`.
4. Choose a short slug for the session topic.
5. Write `ROOT/.arkiv/handoff/<YYYY-MM-DD>-<slug>.md`. Capture only what the next session needs to resume.
6. Write the document through the ASD-STE100 skill in **strict** mode. Invoke the Skill `arkiv:asd-ste100`. If the Skill name is not available, read `${CLAUDE_PLUGIN_ROOT}/skills/asd-ste100/SKILL.md` and apply its rules.
7. Give the document the common frontmatter schema and the visible date line (see `/arkiv:init`).
8. Regenerate the index. Run `python3 "${CLAUDE_PLUGIN_ROOT}/bin/generate-index.py" "ROOT/.arkiv"`.

## Note

A hand-off is ephemeral. It is not permanent knowledge. `/arkiv:clean` prunes an old hand-off. Put durable knowledge in `dev/`, `research/`, `todo.md`, or `donotforget.md` with `/arkiv:update` instead.
