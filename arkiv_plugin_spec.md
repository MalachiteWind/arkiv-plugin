# `.arkiv` — Plugin Specification

A Claude Code **plugin** that maintains a deliberate, command-driven, repo-root knowledge store for a single-developer, long-running codebase. Everything the agent knows about *why the repo is the way it is*, what is being thought about, what is left to do, and what not to break, lives in one place that a fresh agent can read cheaply at the start of any session.

This document is the build spec. Hand it to a builder agent (Claude Code) in the repo where the plugin itself will be developed and git-tracked. The plugin's own source is **separate** from any target repo it operates on.

---

## 1. Purpose (the one goal everything serves)

**Prevent model-drift on a large, evolving repo.** Across many sessions, an agent makes structural choices, forms an understanding of the code, and parks or discards ideas. Without a store, session 7 does not know what session 3 decided, and the developer loses the thread of *why* the code looks the way it does.

`.arkiv` exists so that, at any point, the developer or a fresh agent can open the store and reconstruct: the current state, the open threads, and the *why* behind past choices — without replaying prior chats.

This is the **mental-model / drift** goal. Every command below is judged against it.

Design stance: **deliberate, not automatic.** The store is written only when the developer runs an `arkiv:*` command. Nothing captures sessions in the background.

---

## 2. Name, invisibility, and tracking

- Store directory: **`.arkiv/`** at repo root.
- Command namespace: **`arkiv:*`**.
- **Invisible by default.** On `init`, add `.arkiv/` to `.git/info/exclude` (local, untracked, not named in any versioned file). Single-machine use; the developer rsyncs to other machines if ever needed.
- `arkiv:track [true|false]` toggles the `.git/info/exclude` line. Default `false` (untracked). `true` removes the exclude line so the store *can* be git-tracked; it does not itself commit anything.
- **Invisibility guardrail (hard rule).** The agent must never name the store path or the token `arkiv` in any *tracked* artifact — not in code, code comments, commit messages, or PR text. The excluded folder hides the folder; this rule prevents leakage *out* of it. Because `arkiv` is a distinctive coined token, a pre-commit grep can enforce it (see §8).

---

## 3. Writing standard: ASD-STE100 (the `asd` skill) governs all docs

Every document in `.arkiv/` is written under the `asd-ste100` controlled-language skill. This is non-optional and applies to all categories.

Mode per document type (asd ships both modes; strict where a misread has a cost, STE-flavored where nuance matters):

| Document | asd mode |
|---|---|
| `README.md`, `todo.md`, `research/*`, `dev/*` | **STE-flavored** (structural rules enforced, lexical advisory) |
| `donotforget.md`, `handoff/*` | **strict** (caveats and inter-agent instructions — misreading has a real cost) |

---

## 4. On-disk layout

```
.arkiv/
├── README.md          purpose, how to navigate, upshot for a fresh agent,
│                      BOLD banner: NOT TRACKED / never named in the repo
├── INDEX.md           GENERATED from frontmatter — the cheap dispatcher. Never hand-edited.
├── todo.md            live work queue (completion-based)
├── donotforget.md     persistent pitfalls / caveats (persistence-based) — asd strict
├── research/          ideas + worked theory (runs ahead of the code)
├── dev/               how the repo IS and why (grounded in the code)
└── handoff/           ephemeral session hand-offs — asd strict, pruned by clean
```

`research/` and `dev/` are **free-form on structure** (no forced sub-taxonomy), governed by conventions, not categories — see §6.

---

## 5. Frontmatter schema

Every doc carries YAML frontmatter. `summary` is the single most important field: it is the one-liner the generated `INDEX.md` shows, and the whole progressive-disclosure design depends on it being specific.

Common to all docs:

```yaml
---
title: <short title>
summary: <one specific line — feeds INDEX.md>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---
```

Each doc also shows `created` / `updated` as a visible header line inside the body (the developer wanted the date readable while navigating). Dates live in frontmatter, **not** in filenames, so links and git history do not fragment. Exception: `handoff/` files use dated filenames (the one place a date belongs).

`dev/` adds:

```yaml
verified: <YYYY-MM-DD or git-ref>   # when the anchored paths were last confirmed accurate
```

`research/` adds:

```yaml
status: idea | exploring | promoted | parked | discarded
related: [<dev-slug>, ...]          # linkage to the dev doc(s) that implement this idea
```

---

## 6. Category conventions

### `dev/` — how the repo *is* (grounded)

Answers "why is the code like this." Two conventions the agent must satisfy on every write (this is the "Option C" choice: no forced `mod-`/`api-`/`flow-` taxonomy, only the two high-value habits):

1. **Reconstructed decisions.** When the agent encounters a non-obvious choice (why this library, why this boundary, why this flow bypasses the usual path) and no formal decision record exists, it writes one: context, choice, trade-off accepted. Often this is the *only* written record of the rationale, and it is the single most drift-critical artifact — it is the "why session 3 did this" that keeps session 7 (and the developer) from re-litigating a settled question.
2. **Anchor, do not paste.** Reference `path/to/file.ts`, never embed code. Code drifts; the repo is the source of truth for *how*. The store describes *what* and *why*.

### `research/` — ideas and theory (runs ahead of the code)

Answers "what are we thinking about doing, and on what basis." Holds both worked-out theory/formulations and rough ideas intended for implementation. Conventions:

- **Math over words** — write the formulation, not a prose gloss of it.
- **Notation defined** — every symbol introduced is declared, so a fresh agent can parse it.
- **No path-anchoring requirement** — ideas are not in the code yet, so there is nothing to anchor to. (This is the deliberate difference from `dev/`.)
- **Lifecycle via `status`** — every research doc carries a `status` (see §5). This lets a fresh agent tell a live idea from a parked or dead one, and lets `clean` avoid pruning parked ideas as if stale.
- **Linkage on promotion** — when an idea becomes code, set its `status: promoted` and populate `related:` with the `dev/` decision doc that now describes it. This captures the moment an idea becomes part of the repo's "why."

### `todo.md` vs `donotforget.md` (top-level living files)

- **`todo.md` — completion-based.** The live work queue: open tasks, next steps, unfinished threads. Items are added/checked by `update` and **pruned when done** by `clean`.
- **`donotforget.md` — persistence-based.** Persistent traps and caveats ("looks reasonable but breaks X"). Entries are **not** "done"; they persist until the hazard is genuinely designed out. `clean` must **never auto-prune** a caveat — always prompt.
- **Distinct from `dev/` decisions:** a decision doc says "we chose X over Y because Z" (rationale, past-facing). `donotforget` says "do not do Y, it breaks Z" (actionable trap, future-facing). Related but not the same.

---

## 7. Commands

All commands resolve the repo root as `git rev-parse --show-toplevel 2>/dev/null || pwd`. All writes go through asd (§3). After any command that adds/removes/renames a doc, regenerate `INDEX.md` (§8).

### `arkiv:init [<existing_docs_path>]`

**No arg (default):**
1. Resolve root; create `.arkiv/` with the layout in §4.
2. Add `.arkiv/` to `.git/info/exclude`.
3. Scan `README`, `CLAUDE.md`, and key code to **propose** a starting skeleton — do not blast a large doc set. Five deep pages beat fifty shallow ones.
4. **If a store already exists: STOP.** Tell the developer to use `arkiv:update`. `init` writes from scratch and is destructive on an untracked store.

**With `<existing_docs_path>`:** additionally ingest an existing set of notes to help populate `.arkiv/` — effectively `init` + a first `update` + a first `clean` in one pass (import, then dedupe and normalize what was imported into the schema and conventions above).

### `arkiv:update`

From the current chat context **and** the repo, decide which docs to add or update. Scope is **crucial points only** — development notes, new ideas, bugs found — **not** a summary of the whole session.

- Show diffs before writing. **Prompt before any structural change** (new subfolder, moving a doc).
- **Update in place.** Never append dated `## update:` sections to living docs; edit the relevant section and bump `updated`. History lives in git / the operation log, not in the page.
- On a `dev/` write: anchor to paths, and capture a reconstructed decision when a non-obvious choice is present.
- On a `research/` write: set/maintain `status`; on promotion set `status: promoted` and the `related:` link to the `dev/` doc.
- Regenerate `INDEX.md`.

### `arkiv:read [<path>]`

**No arg (default — the fresh-agent load):** read in this fixed order for cheap orientation:
1. `README.md`
2. `INDEX.md`
3. any active `handoff/*`

then load selectively by INDEX match. Follow the progressive-disclosure tiers (§8): INDEX one-liners → a doc's `summary` → full body, escalating one tier only when the cheaper tier does not answer.

**With `<path>`:** do the default load **and then** fully read the specified path on top.

### `arkiv:clean`

Read the store for stale, outdated, or duplicated content; propose a cleanup plan; act on confirmation. Category-aware rules:

- **`todo.md`** — prune completed items.
- **`handoff/`** — prune old hand-offs (ephemeral by definition).
- **`dev/`** — flag docs whose anchored path changed or whose `verified` predates the file it points at (stale = a defect to fix).
- **`research/`** — a `parked` or `discarded` idea is **not** stale; never prune it as outdated.
- **`donotforget.md`** — never auto-prune a caveat; always prompt.

### `arkiv:handoff`

The current chat is too context-heavy and needs a new session. Compact it into `handoff/<YYYY-MM-DD>-<slug>.md` in **asd strict**, capturing only what the next session needs to resume. Ephemeral — not permanent knowledge; `clean` prunes old ones.

### `arkiv:track [true|false]`

Toggle the `.git/info/exclude` line for `.arkiv/`. Default `false` (untracked/invisible). `true` removes the exclude line so the store may be tracked; does not commit.

---

## 8. Generated index + progressive disclosure

**`INDEX.md` is generated, never hand-edited.** A stdlib-only script (`bin/generate-index.py`, no third-party deps) reads each doc's frontmatter and emits a table grouped by category (top-level files, `research/`, `dev/`, active `handoff/`). Columns: title, path, `updated`, and the `summary` one-liner (plus `status` for `research/`). The source of truth is each doc's frontmatter; the index is a runtime artifact regenerated on demand.

**Progressive-disclosure tiers (the read side — this is what keeps a large store cheap):**

| Tier | Load | When |
|---|---|---|
| 1 | `INDEX.md` one-liners | always — the dispatcher |
| 2 | a matched doc's `summary` frontmatter | when the index shows a match |
| 3 | the full doc body | when the summary does not answer |

Escalate one tier only. The reason `summary` must be specific is that it is the entire signal available before paying to load a doc.

**Invisibility grep-check (pre-commit).** Provide a hook/script that greps the *tracked* tree for the token `arkiv` and fails the commit if found, enforcing the §2 guardrail. Because the token is distinctive, this produces no false positives.

---

## 9. Plugin packaging

Build as a Claude Code plugin so the `arkiv:*` slash commands run against a real filesystem at repo root:

```
<plugin-repo>/
├── .claude-plugin/
│   └── plugin.json         name, description, version
├── commands/               one file per arkiv:* command
├── bin/
│   └── generate-index.py   stdlib-only index generator
└── (dependency) asd-ste100 skill — https://github.com/danyuchn/asd-ste100-skill
```

The plugin must be installed and exercised in Claude Code to verify real behavior — that `init` writes and adds the exclude line, that `read`'s load order holds, that `clean`'s category rules fire correctly. This is why it is built and iterated locally in its own tracked repo, not in the web interface.

---

## 10. Locked decisions (quick reference)

- Store: `.arkiv/`; commands `arkiv:*`; packaged as a plugin.
- Goal: mental-model / drift prevention on a large, long-running repo.
- Deliberate/command-driven; single machine; invisible via `.git/info/exclude`; `track` is opt-out.
- asd-ste100 governs **all** writing — STE-flavored for prose, strict for `donotforget.md` and `handoff/`.
- Dates in frontmatter (+ visible header line), off filenames except `handoff/`.
- `dev/` = grounded (reconstructed decisions + anchor-don't-paste); `research/` = ahead-of-code (math-over-words, notation-defined, `status` lifecycle, `related` linkage to `dev/`).
- `todo.md` completion-based; `donotforget.md` persistence-based (never auto-pruned).
- Generated `INDEX.md` dispatcher + 3-tier progressive disclosure.
- Invisibility enforced by a pre-commit grep on the token `arkiv`.