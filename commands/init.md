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

## Steps

1. Check for a git repository. Run `git rev-parse --show-toplevel`. If it fails, tell the developer that the exclude step needs a git repository. On request, create arkiv and skip step 5.
2. Check for an existing arkiv. If `ROOT/.arkiv` exists, **STOP**. Tell the developer to run `/arkiv:update`. `init` writes from scratch. `init` destroys an untracked arkiv.
3. Create the directories: `ROOT/.arkiv/research/`, `ROOT/.arkiv/dev/`, and `ROOT/.arkiv/handoff/`.
4. Create the files: `ROOT/.arkiv/README.md`, `ROOT/.arkiv/todo.md`, and `ROOT/.arkiv/donotforget.md`.
5. Hide arkiv. Resolve the exclude file with `git rev-parse --git-path info/exclude`. Add the single line `.arkiv/` to that file. Add the line only when the line is absent.
6. Propose a skeleton. Read `README`, `CLAUDE.md`, and the key code. Propose a small set of documents. Five deep pages are better than fifty shallow pages. Show the proposal. Get confirmation before you write.
7. Write `README.md`. Start it with a bold banner: **NOT TRACKED — never named in the repo**. State the arkiv purpose. State how to navigate arkiv. State the upshot for a fresh agent.
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
- `research/` documents add `status: idea | exploring | promoted | parked | discarded` and `related: [<dev-slug>, ...]`. A `<dev-slug>` is the basename of the target `dev/` document. It carries no `.md` extension. It carries no path. Example: `related: [architecture]` resolves to `dev/architecture.md`.
- The body starts with a visible line: `Created: <date> · Updated: <date>`.
- Dates stay in frontmatter. Dates do not go in filenames. Exception: `handoff/` uses dated filenames.

## Category conventions

Two habits govern `dev/` and `research/`. Force no taxonomy. arkiv uses no `mod-`, `api-`, or `flow-` prefix. arkiv uses only the two high-value habits per category.

`dev/` (grounded — why the code is like this):
1. Anchor to paths. Reference `path/to/file`. Do not paste code. Code drifts. The repository is the source of truth for *how*. arkiv records *what* and *why*.
2. Capture a reconstructed decision for a non-obvious choice. Record the context, the choice, and the trade-off accepted. A reconstructed decision is the most drift-critical artifact. It is often the only record of the rationale. It stops a later session from re-deciding a settled question.

`research/` (ahead of the code):
1. Write the math. Do not write a prose gloss of the math. Write math as TeX. Use `$…$` for inline math. Use `$$…$$` for display math. Never put math in a code fence.
2. Define every symbol you introduce.
3. Do not anchor to implementation code. The idea is not in the code yet. You may still cite evidence. Reference a result, an output, an experiment, or a data file that tests the idea. Evidence keeps the idea verifiable. A negative result has value. Record it and its evidence too.
4. Keep `status` current. The `status` field lets a fresh agent tell a live idea from a parked or dead idea. It also stops `clean` from a prune of a parked idea as stale. On promotion, set `status: promoted`. Set `related` to the `dev/` document. This records the moment an idea becomes part of the repository's "why".

`todo.md` is completion-based. Add open tasks. `clean` prunes a finished task.

`donotforget.md` is persistence-based. A caveat persists until the design removes the hazard. A caveat differs from a `dev/` decision. A `donotforget` caveat is future-facing. It states "do not do Y. It breaks Z." A `dev/` decision is past-facing. It states "the team chose X over Y because Z." `clean` never auto-prunes a caveat. `clean` always prompts first.
