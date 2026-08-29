---
description: Add or update the crucial points from this session into the knowledge store
argument-hint: ""
disable-model-invocation: true
---

Record the crucial points from the current session and the repository into the store.

Scope is **crucial points only**: development notes, new ideas, and bugs found. Do not write a summary of the whole session.

## Rules for every write

1. Resolve the repository root. Run `git rev-parse --show-toplevel 2>/dev/null || pwd`. Call the result ROOT. The store is `ROOT/.arkiv`.
2. If `ROOT/.arkiv` does not exist, tell the developer to run `/arkiv:init` first. Then stop.
3. Write every document through the ASD-STE100 skill. Invoke the Skill `arkiv:asd-ste100`. Use **strict** mode for `donotforget.md` and `handoff/*`. Use **STE-flavored** mode for all other documents. If the Skill name is not available, read `${CLAUDE_PLUGIN_ROOT}/skills/asd-ste100/SKILL.md` and apply its rules.
4. Do not write the store name or the store path into a tracked file of the repository. The store's own files are exempt.

## Steps

1. Decide which documents to add or update. Use the current chat context and the repository.
2. Show the diff for each planned write. Get confirmation.
3. Prompt before any structural change. A new subfolder is a structural change. A moved document is a structural change.
4. Update in place. Edit the relevant section. Bump `updated`. Do not append a dated `## update:` section. History lives in git, not in the page.
5. Give a new document the full frontmatter schema and the visible date line (see `/arkiv:init`).
6. Regenerate the index. Run `python3 "${CLAUDE_PLUGIN_ROOT}/bin/generate-index.py" "ROOT/.arkiv"`.

## Category rules

On a `dev/` write:
1. Anchor to paths. Reference `path/to/file`. Do not paste code.
2. Capture a reconstructed decision for a non-obvious choice. Record the context, the choice, and the trade-off accepted.

On a `research/` write:
1. Write the math. Do not write a prose gloss of the math.
2. Define every symbol you introduce.
3. Do not anchor to paths. The idea is not in the code yet.
4. Keep `status` current. On promotion, set `status: promoted`. Set `related` to the `dev/` document.

On a `todo.md` write: add the open task. `todo.md` is completion-based.

On a `donotforget.md` write: record the trap as an actionable, future-facing caveat ("do not do Y, it breaks Z"). This differs from a `dev/` decision, which is past-facing ("we chose X over Y because Z").
