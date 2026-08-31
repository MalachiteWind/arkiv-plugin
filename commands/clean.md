---
description: Find stale, outdated, or duplicated arkiv content and propose a cleanup
argument-hint: ""
disable-model-invocation: true
---

Find stale, outdated, or duplicated content in arkiv. Propose a cleanup plan. Act on confirmation.

## Steps

1. Resolve the repository root. Run `git rev-parse --show-toplevel 2>/dev/null || pwd`. Call the result ROOT. arkiv is `ROOT/.arkiv`.
2. If `ROOT/.arkiv` does not exist, tell the developer to run `/arkiv:init` first. Then stop.
3. Read arkiv. Apply the category rules below.
4. Show the cleanup plan. Get confirmation before you change any file.
5. Regenerate the index after any confirmed change. Run `python3 "${CLAUDE_PLUGIN_ROOT}/bin/generate-index.py" "ROOT/.arkiv"`. An in-place edit changes an indexed field, so regenerate even when no file is added, removed, or renamed.

## Category rules

`todo.md`: prune a completed item.

`handoff/`: prune an old hand-off. A hand-off is ephemeral.

`dev/`: flag a document as a defect when its anchored path changed, or when `verified` predates the file it points at. A stale `dev/` document is a defect to fix.

`research/`: a `parked` or `discarded` idea is **not** stale. Do not prune it as outdated.

`donotforget.md`: never auto-prune a caveat. Always prompt. A caveat persists until the hazard is designed out.

`conventions.md`: never prune it. Never edit it. It is a verbatim copy of the plugin template. To change it, edit the plugin template and run `/arkiv:init` in a fresh arkiv, or copy the template again.

## Writing

Write any edit through the ASD-STE100 skill. Invoke the Skill `arkiv:asd-ste100`. Use **strict** mode for `donotforget.md` and `handoff/*`. Use **STE-flavored** mode for all other documents.
