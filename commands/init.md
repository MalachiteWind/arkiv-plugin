---
description: Create the repo-root knowledge store and propose a small starting skeleton
argument-hint: "[<existing_docs_path>]"
disable-model-invocation: true
---

Create the repo-root knowledge store. The store prevents model-drift across sessions.

`$1` is an optional path to existing notes. Import them when it is present.

## Rules for every write

1. Resolve the repository root. Run `git rev-parse --show-toplevel 2>/dev/null || pwd`. Call the result ROOT. The store is `ROOT/.arkiv`.
2. Write every document through the ASD-STE100 skill. Invoke the Skill `arkiv:asd-ste100`. Use **strict** mode for `donotforget.md` and `handoff/*`. Use **STE-flavored** mode for all other documents. If the Skill name is not available, read `${CLAUDE_PLUGIN_ROOT}/skills/asd-ste100/SKILL.md` and apply its rules.
3. Do not write the store name or the store path into a tracked file of the repository. The store's own files are exempt.

## Steps

1. Check for a git repository. Run `git rev-parse --show-toplevel`. If it fails, tell the developer that the exclude step needs a git repository. On request, create the store and skip step 5.
2. Check for an existing store. If `ROOT/.arkiv` exists, **STOP**. Tell the developer to run `/arkiv:update`. `init` writes from scratch. `init` destroys an untracked store.
3. Create the directories: `ROOT/.arkiv/research/`, `ROOT/.arkiv/dev/`, and `ROOT/.arkiv/handoff/`.
4. Create the files: `ROOT/.arkiv/README.md`, `ROOT/.arkiv/todo.md`, and `ROOT/.arkiv/donotforget.md`.
5. Hide the store. Resolve the exclude file with `git rev-parse --git-path info/exclude`. Add the single line `.arkiv/` to that file. Add the line only when the line is absent.
6. Propose a skeleton. Read `README`, `CLAUDE.md`, and the key code. Propose a small set of documents. Five deep pages are better than fifty shallow pages. Show the proposal. Get confirmation before you write.
7. Write `README.md`. Start it with a bold banner: **NOT TRACKED — never named in the repo**. State the store purpose. State how to navigate the store. State the upshot for a fresh agent.
8. Give every document the frontmatter schema below and a visible date line in the body.
9. Regenerate the index. Run `python3 "${CLAUDE_PLUGIN_ROOT}/bin/generate-index.py" "ROOT/.arkiv"`.
10. Print the guard-wiring command. Do not run it:
    ```
    HOOKS="$(git rev-parse --git-path hooks)"
    ln -sf "${CLAUDE_PLUGIN_ROOT}/bin/check-invisibility.sh" "$HOOKS/pre-commit"
    ln -sf "${CLAUDE_PLUGIN_ROOT}/bin/check-commit-msg.sh" "$HOOKS/commit-msg"
    chmod +x "$HOOKS/pre-commit" "$HOOKS/commit-msg"
    ```

## With `$1` (existing notes path)

After step 9, import the notes. Do one `update` pass. Fold the notes into the schema below. Then do one `clean` pass. Remove duplicates. Normalize the result.

## Frontmatter schema

Give every document this YAML block at the top:

```yaml
---
title: <short title>
summary: <one specific line — feeds INDEX.md>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---
```

- `dev/` documents add `verified: <YYYY-MM-DD or git-ref>`.
- `research/` documents add `status: idea | exploring | promoted | parked | discarded` and `related: [<dev-slug>, ...]`.
- The body starts with a visible line: `Created: <date> · Updated: <date>`.
- Dates stay in frontmatter. Dates do not go in filenames. Exception: `handoff/` uses dated filenames.

## Category conventions

`dev/` (grounded — why the code is like this):
1. Anchor to paths. Reference `path/to/file`. Do not paste code.
2. Capture a reconstructed decision for a non-obvious choice. Record the context, the choice, and the trade-off accepted.

`research/` (ahead of the code):
1. Write the math. Do not write a prose gloss of the math.
2. Define every symbol you introduce.
3. Do not anchor to paths. The idea is not in the code yet.
4. Keep `status` current. On promotion, set `status: promoted`. Set `related` to the `dev/` document.

`todo.md` is completion-based. Add open tasks. `clean` prunes a finished task.

`donotforget.md` is persistence-based. A caveat persists until the hazard is designed out. `clean` never auto-prunes a caveat.
