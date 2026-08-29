---
description: Load the knowledge store cheaply for fresh-agent orientation
argument-hint: "[<path>]"
disable-model-invocation: true
---

Load the store for orientation. This is a read-only command. Do not write any document.

`$1` is an optional path to read in full on top of the default load.

## Steps

1. Resolve the repository root. Run `git rev-parse --show-toplevel 2>/dev/null || pwd`. Call the result ROOT. The store is `ROOT/.arkiv`.
2. If `ROOT/.arkiv` does not exist, tell the developer to run `/arkiv:init` first. Then stop.
3. Read these files in this fixed order:
   1. `ROOT/.arkiv/README.md`
   2. `ROOT/.arkiv/INDEX.md`
   3. every file in `ROOT/.arkiv/handoff/`
4. Load the rest selectively. Match the task against the INDEX one-liners.

## Progressive disclosure

Load one tier at a time. Escalate one tier only when the cheaper tier does not answer.

1. Tier 1: the INDEX one-liners. This is the dispatcher. Read it first.
2. Tier 2: a matched document's `summary` frontmatter. Read it when the INDEX shows a match.
3. Tier 3: the full document body. Read it when the `summary` does not answer.

## With `$1` (a path)

Do the default load first. Then read `$1` in full on top.
