# arkiv

arkiv is a Claude Code plugin. It maintains arkiv: a deliberate, command-driven knowledge base at the repository root. arkiv serves a single developer on a long-running codebase.

## Why

A large repository changes across many sessions. In each session, an agent makes structural choices, forms an understanding of the code, and parks or discards ideas. Without arkiv, session 7 does not know what session 3 decided. The developer loses the thread of why the code looks the way it does.

arkiv fixes this. At any point, the developer or a fresh agent opens arkiv. They reconstruct the current state, the open threads, and the reason behind past choices. They do not replay prior chats. This is the one goal. Every command serves it.

arkiv is deliberate, not automatic. The plugin writes arkiv only when the developer runs a command. Nothing records sessions in the background.

## Layout

arkiv lives in the `.arkiv/` directory at the repository root.

```
.arkiv/
├── README.md          purpose, navigation, and the upshot for a fresh agent
├── INDEX.md           generated dispatcher — never hand-edited
├── todo.md            live work queue (completion-based)
├── donotforget.md     persistent traps and caveats (persistence-based)
├── research/          ideas and worked theory (ahead of the code)
├── dev/               how the repo is, and why (grounded in the code)
└── handoff/           ephemeral session hand-offs (pruned by clean)
```

Every document carries YAML frontmatter. The `summary` line feeds the generated `INDEX.md`. A reader loads arkiv in three tiers:

1. the `INDEX.md` one-liners
2. a matched document's `summary` frontmatter
3. the full document body

The reader escalates one tier only when the cheaper tier does not answer. This method keeps a large arkiv cheap to read.

## Writing standard

Every document follows the ASD-STE100 controlled-language standard. The plugin bundles the skill at `skills/asd-ste100`. You do not install the skill separately. The plugin uses strict mode for `donotforget.md` and the `handoff/` files, where a misread has a real cost. The plugin uses STE-flavored mode for the other documents.

## Commands

| Command | Purpose |
|---|---|
| `/arkiv:init [<optional_docs_path>]` | Create arkiv. Propose a small skeleton. `Optional`: Import existing notes when you give a path. |
| `/arkiv:update` | Record the crucial points from a chat session and the repository. |
| `/arkiv:read [<optional_path>]` | Summarize the project from arkiv for orientation. `Optional`: Read a given path in full for extra context. |
| `/arkiv:clean` | Find stale, outdated, or duplicated content. Propose a cleanup to arkiv. |
| `/arkiv:handoff` | Compact current session into an ephemeral hand-off for the next session. |
| `/arkiv:track [true\|false]` | Toggle whether git can track arkiv. Default: `false`. |

## Install

Install the plugin from its marketplace. The `arkiv:*` commands then run against the repository root.

**From GitHub:**

1. Add the marketplace. Run:

> ```bash
> claude plugin marketplace add MalachiteWind/arkiv-plugin
>  ```

2. Install the plugin. Run: 
> ```bash
> claude plugin install arkiv@arkiv-plugin
> ```
3. Start a new Claude Code session.

**From a local path:**

1. Add the marketplace. Run:

>```bash
>claude plugin marketplace add <repo_path>/arkiv-plugin
>```
2. Install the plugin. Run:
>```
>claude plugin install arkiv@arkiv-plugin
>```
3. Start a new Claude Code session.

The plugin bundles the ASD-STE100 skill, so you do not install that skill separately.

The install scope controls where the plugin is active. `--scope user` activates the plugin in all your projects. `--scope project` activates the plugin for this repository through shared settings. `--scope local` activates the plugin for this repository for you only. The default scope is user.

## Invisibility

arkiv is invisible by default. `init` adds `.arkiv/` to `.git/info/exclude`. Git does not track arkiv. This setting is local. It is not named in any versioned file.

arkiv is a coined token. The agent never writes that token, or the arkiv path, into a tracked file. This rule stops the token from reaching code, comments, commit messages, or PR text.

`/arkiv:track true` removes the exclude line, so git can track arkiv. `/arkiv:track false` restores the exclude line. `/arkiv:track` with no argument reports the current state.

## The invisibility guard (optional)

The plugin ships two guard scripts. The plugin does not install them. Add them to the target repository as git hooks when you want them:

```sh
HOOKS="$(git rev-parse --git-path hooks)"
ln -sf "<plugin>/bin/check-invisibility.sh" "$HOOKS/pre-commit"
ln -sf "<plugin>/bin/check-commit-msg.sh" "$HOOKS/commit-msg"
chmod +x "$HOOKS/pre-commit" "$HOOKS/commit-msg"
```

`check-invisibility.sh` runs before a commit. It blocks the commit when the forbidden token `arkiv` appears in tracked content or in a tracked filename. `check-commit-msg.sh` blocks a commit when the message names the token. The guard exempts arkiv's own `.arkiv/` files, so a tracked arkiv does not trip the guard. A pre-commit hook cannot read PR text, so PR-body enforcement needs a separate CI or review control.

## The index generator (automatic per commands)

`bin/generate-index.py` reads each document's frontmatter and writes `INDEX.md`. It uses the Python standard library only. The commands run it after any arkiv write. You can also run it directly:

```sh
python3 bin/generate-index.py path/to/.arkiv
```
