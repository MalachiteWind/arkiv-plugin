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
4. Load more, silently, until you can answer three questions: the project purpose, the high-level working, and the open work. Escalate tiers by the rule below. Read a `dev/` document body when its INDEX line matches purpose or working. Do not print this load.

## Progressive disclosure

Load one tier at a time. Escalate one tier only when the cheaper tier does not answer.

1. Tier 1: the INDEX one-liners. This is the dispatcher. Read it first.
2. Tier 2: a matched document's `summary` frontmatter. Read it when the INDEX shows a match.
3. Tier 3: the full document body. Read it when the `summary` does not answer.

## Output — a concise summary, not an outline

After the silent load, write a short, high-level summary of the project. Write it through the ASD-STE100 skill. Invoke the Skill `arkiv:asd-ste100` in **STE-flavored** mode. If the Skill name is not available, read `${CLAUDE_PLUGIN_ROOT}/skills/asd-ste100/SKILL.md` and apply its rules.

arkiv normally serves another repository. In that case, summarize **that project**, not the plugin. Reconstruct the summary from arkiv. Cover three parts:

1. **Purpose** — what the project is, and why it exists.
2. **Working** — how the project operates, at a high level.
3. **Open work** — the open items from `todo.md`, and any active hand-off in `handoff/`. State "none" when a part is empty.

Keep the summary short. Do not print an outline or a table of arkiv contents. Do not list every document. State that the developer can ask for more detail by name, or pass a path as `$1`.

## With `$1` (a path)

Do the default load first. Then read `$1` in full on top.
