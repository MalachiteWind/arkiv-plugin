---
description: Orient a fresh agent with a concise, arkiv-backed summary of the project
argument-hint: "[<path>]"
disable-model-invocation: true
---

Load arkiv for orientation. This is a read-only command. Do not write any document.

`$1` is an optional path to read in full on top of the default load.

## Steps

1. Resolve the repository root. Run `git rev-parse --show-toplevel 2>/dev/null || pwd`. Call the result ROOT. arkiv is `ROOT/.arkiv`.
2. If `ROOT/.arkiv` does not exist, tell the developer to run `/arkiv:init` first. Then stop.
3. Load these files silently in this fixed order. Do not print them:
   1. `ROOT/.arkiv/README.md`
   2. `ROOT/.arkiv/INDEX.md`
   3. every file in `ROOT/.arkiv/handoff/`
   4. `ROOT/.arkiv/todo.md`
4. Answer three questions from this load: the project purpose, the high-level working, and the open work. Use the INDEX one-liners as the default source. Escalate a tier only by the rule below. Read a `dev/` document `summary` when an INDEX line matches a question. Read a `dev/` document body only when that `summary` does not answer the question. Do not read a body for extra confidence. Do not print this load.
5. Check the conventions for drift. See the drift check below. Print its warning after the summary.

## Progressive disclosure

Load one tier at a time. Escalate one tier only when the cheaper tier does not answer.

1. Tier 1: the INDEX one-liners. This is the dispatcher. Read it first.
2. Tier 2: a matched document's `summary` frontmatter. Read it when the INDEX shows a match.
3. Tier 3: the full document body. Read it when the `summary` does not answer.

## The drift check

`conventions.md` in arkiv is a copy of the plugin template. A template change does not reach the copy. This check reports that condition. This check never repairs it.

1. Resolve TEMPLATE as `${CLAUDE_PLUGIN_ROOT}/templates/conventions.md`. Resolve COPY as `ROOT/.arkiv/conventions.md`.
2. Skip this check in silence in each of these four conditions:
   - `${CLAUDE_PLUGIN_ROOT}` is unresolved.
   - You cannot read TEMPLATE.
   - COPY is absent.
   - You cannot read COPY.
3. Compare TEMPLATE and COPY. Set TEMPLATE and COPY as shell variables first. Run this command under bash. A process substitution needs bash:

   ```bash
   diff "$TEMPLATE" <(sed -E \
     -e 's/^created: [0-9]{4}-[0-9]{2}-[0-9]{2}$/created: __INIT_DATE__/' \
     -e 's/^updated: [0-9]{4}-[0-9]{2}-[0-9]{2}$/updated: __INIT_DATE__/' \
     -e 's/^Created: [0-9]{4}-[0-9]{2}-[0-9]{2} · Updated: [0-9]{4}-[0-9]{2}-[0-9]{2}$/Created: __INIT_DATE__ · Updated: __INIT_DATE__/' \
     "$COPY")
   ```

   Use `sed -E`. The interval syntax `{4}` is an extended regular expression. Plain `sed` runs no substitution, and then an arkiv that agrees with the template reports a difference. The separator on the third pattern is a middle dot. It is not a hyphen. The patterns match any line of the file. They do not read the frontmatter block alone. The process substitution holds the normalized copy in memory, so this command writes no file.
4. If the comparison finds a difference, print exactly this one line. Print it last, after the summary:

   `! conventions.md does not match the plugin template. Run /arkiv:sync to re-copy.`
5. If the comparison finds no difference, print nothing.

This command must never fail because the plugin path is unavailable. This command stays read-only. Do not print the comparison. Do not write any file.

## Output — a concise summary, not an outline

After the silent load, write a short, high-level summary of the project. Write plain prose. Use active voice. Write one idea per sentence. Do not invoke the `arkiv:asd-ste100` skill for this summary. The summary is transient terminal output. The summary is not a stored arkiv document. The skill governs the write commands only.

arkiv normally serves another repository. In that case, summarize **that project**, not the plugin. Reconstruct the summary from arkiv. Cover three parts:

1. **Purpose** — what the project is, and why it exists.
2. **Working** — how the project operates, at a high level.
3. **Open work** — the open items from `todo.md`, and any active hand-off in `handoff/`. State "none" when a part is empty.

Keep the summary short. Do not print an outline or a table of arkiv contents. Do not list every document. State that the developer can ask for more detail by name, or pass a path as `$1`.

## With `$1` (a path)

Do the default load first. Then read `$1` in full on top.
