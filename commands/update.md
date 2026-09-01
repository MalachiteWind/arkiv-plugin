---
description: Add or update the crucial points from this session into arkiv
argument-hint: ""
disable-model-invocation: true
---

Record the crucial points from the current session and the repository into arkiv.

Scope is **crucial points only**: development notes, new ideas, and bugs found. Do not write a summary of the whole session.

## Rules for every write

1. Resolve the repository root. Run `git rev-parse --show-toplevel 2>/dev/null || pwd`. Call the result ROOT. arkiv is `ROOT/.arkiv`.
2. If `ROOT/.arkiv` does not exist, tell the developer to run `/arkiv:init` first. Then stop.
3. Write every document through the ASD-STE100 skill. Invoke the Skill `arkiv:asd-ste100`. Use **strict** mode for `donotforget.md` and `handoff/*`. Use **STE-flavored** mode for all other documents. If the Skill name is not available, read `${CLAUDE_PLUGIN_ROOT}/skills/asd-ste100/SKILL.md` and apply its rules.
4. Do not write the token `arkiv` or the arkiv path into a tracked file of the repository. arkiv's own files are exempt.
5. Read `ROOT/.arkiv/conventions.md` for the frontmatter schema, the research status values, and the category habits. Apply it to every document you write. Never edit `conventions.md`. It is a verbatim copy of the plugin template.

## Steps

1. Inspect the git state. Run `git log --oneline -n 20`. Run `git status --short`. Use the log to find work that is complete. Use the status to find work that is not committed yet. A repository can have no commit. In that condition, `git log` fails. Skip `git log`. Run `git status --short`. It works without a commit. Report the missing log evidence in the proposal.
2. Decide which documents to add or update. Use the current chat context, the repository, and the git state from step 1. Do not propose a task that the log shows as done. Work in the status output is not committed. A task about that work stays open.
3. Show the diff for each planned write. Get confirmation.
4. Prompt before any structural change. A new subfolder is a structural change. A moved document is a structural change.
5. Update in place. Edit the relevant section. Bump `updated`. Do not append a dated `## update:` section. arkiv records the current state. arkiv is not a changelog.
6. Give a new document the full frontmatter schema and the visible date line (see `conventions.md`). A `research/` document uses one status value from `conventions.md`: `idea`, `exploring`, `promoted`, `parked`, or `discarded`.
7. Regenerate the index. Run `python3 "${CLAUDE_PLUGIN_ROOT}/bin/generate-index.py" "ROOT/.arkiv"`.

## Category rules

The frontmatter schema, the research status values, and the `dev/` and `research/` habits live in `ROOT/.arkiv/conventions.md`. Read it. Apply it to every document you write. It is the single source of truth for the schema and the conventions.

Two category actions are specific to `update`:

- On a `todo.md` write: add the open task. `todo.md` is completion-based. Step 1 inspects the git state. Do not add a task that the git history shows as done.
- On a `donotforget.md` write: record the trap as an actionable, future-facing caveat. See the caveat-versus-decision rule in `conventions.md`.
