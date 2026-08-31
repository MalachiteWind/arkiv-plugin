---
description: Create the repo-root arkiv and propose a small starting skeleton
argument-hint: "[<existing_docs_path>]"
disable-model-invocation: true
---

Create the repo-root arkiv. arkiv prevents model-drift across sessions.

`$1` is an optional path to existing notes. Import them when it is present.

## Rules for every write

1. Resolve the repository root. Run `git rev-parse --show-toplevel 2>/dev/null || pwd`. Call the result ROOT. arkiv is `ROOT/.arkiv`.
2. Write every document through the ASD-STE100 skill. Invoke the Skill `arkiv:asd-ste100`. Use **strict** mode for `donotforget.md` and `handoff/*`. Use **STE-flavored** mode for all other documents. If the Skill name is not available, read `${CLAUDE_PLUGIN_ROOT}/skills/asd-ste100/SKILL.md` and apply its rules.
3. Do not write the token `arkiv` or the arkiv path into a tracked file of the repository. arkiv's own files are exempt.
4. Read `${CLAUDE_PLUGIN_ROOT}/templates/conventions.md`. It defines the frontmatter schema, the research status values, and the category habits. Apply it to every document you write.

## Steps

1. Check for a git repository. Run `git rev-parse --show-toplevel`. If it fails, tell the developer that the exclude step needs a git repository. On request, create arkiv and skip step 5.
2. Check for an existing arkiv. If `ROOT/.arkiv` exists, **STOP**. Tell the developer to run `/arkiv:update`. `init` writes from scratch. `init` destroys an untracked arkiv.
3. Create the directories: `ROOT/.arkiv/research/`, `ROOT/.arkiv/dev/`, and `ROOT/.arkiv/handoff/`.
4. Create the files: `ROOT/.arkiv/README.md`, `ROOT/.arkiv/todo.md`, and `ROOT/.arkiv/donotforget.md`.
5. Hide arkiv. Resolve the exclude file with `git rev-parse --git-path info/exclude`. Add the single line `.arkiv/` to that file. Add the line only when the line is absent.
6. Propose a skeleton. Read `README`, `CLAUDE.md`, and the key code. Propose a small set of documents. Five deep pages are better than fifty shallow pages. Show the proposal. Get confirmation before you write.
7. Write `README.md`. Start it with a bold banner: **NOT TRACKED — never named in the repo**. State the arkiv purpose. State how to navigate arkiv. State the upshot for a fresh agent. Point to `conventions.md` for the schema and the conventions.
8. Write `conventions.md`. Copy `${CLAUDE_PLUGIN_ROOT}/templates/conventions.md` to `ROOT/.arkiv/conventions.md` without change. Then replace every `__INIT_DATE__` token with today's date. Do not change any other text. Do not write this document through the skill. It is a verbatim copy.
9. Give every document the frontmatter schema from `conventions.md` and a visible date line in the body.
10. Regenerate the index. Run `python3 "${CLAUDE_PLUGIN_ROOT}/bin/generate-index.py" "ROOT/.arkiv"`.
11. Print the guard-wiring command. Do not run it:
    ```
    HOOKS="$(git rev-parse --git-path hooks)"
    ln -sf "${CLAUDE_PLUGIN_ROOT}/bin/check-invisibility.sh" "$HOOKS/pre-commit"
    ln -sf "${CLAUDE_PLUGIN_ROOT}/bin/check-commit-msg.sh" "$HOOKS/commit-msg"
    chmod +x "$HOOKS/pre-commit" "$HOOKS/commit-msg"
    ```

## With `$1` (existing notes path)

After step 10, import the notes. Do one `update` pass. Fold the notes into the schema in `conventions.md`. Then do one `clean` pass. Remove duplicates. Normalize the result.

## Conventions

The frontmatter schema, the research status values, and the category habits live in `${CLAUDE_PLUGIN_ROOT}/templates/conventions.md`. That template is the single source of truth for the schema and the conventions. Read it. Apply it to every document you write. Step 8 copies it verbatim into `ROOT/.arkiv/conventions.md`, so a fresh agent finds the same rules in the arkiv.
