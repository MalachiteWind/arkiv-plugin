---
description: List the arkiv commands and a one-line purpose for each
argument-hint: ""
disable-model-invocation: true
---

List the arkiv commands. This is a read-only command. Do not write any document. Do not invoke a skill.

## Steps

1. Read the command files at `${CLAUDE_PLUGIN_ROOT}/commands/*.md`.
2. For each file, read the `description` field from the YAML frontmatter.
3. Print one line for each command. Use this format:

   `/arkiv:<name> — <description>`

   The `<name>` is the file name without the `.md` extension. The `<description>` is the frontmatter `description` value, verbatim.
4. Print the commands in this order: `init`, `read`, `update`, `handoff`, `clean`, `sync`, `track`, `help`. Print a command that this list does not name at the end.

## Rules

- Print the `description` value verbatim. Do not paraphrase it.
- Do not print the command body.
- Do not read arkiv. This command describes the plugin commands, not arkiv content.
