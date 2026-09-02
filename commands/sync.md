---
description: Re-copy the conventions template into arkiv when the plugin template changed
argument-hint: ""
disable-model-invocation: true
---

Compare `conventions.md` in arkiv against the plugin template. Re-copy the template when the two files differ.

`init` copies the template one time. `init` refuses an existing arkiv. `clean` and `update` must not edit the copy. So a template change never reaches an existing arkiv. This command closes that gap.

This command takes no argument.

## Rules for every write

1. This command is the only sanctioned writer of `ROOT/.arkiv/conventions.md` after `init`. `clean` and `update` still must not touch that file.
2. Do not write this document through the ASD-STE100 skill. The document is a verbatim copy of the plugin template. This rule matches the conventions step of `init`.
3. Do not write the token `arkiv` or the arkiv path into a tracked file of the repository. arkiv's own files are exempt. `/arkiv:track true` lets git track arkiv, so this command writes the copy in that state too.

## Steps

1. Resolve the repository root. Run `git rev-parse --show-toplevel 2>/dev/null || pwd`. Call the result ROOT. arkiv is `ROOT/.arkiv`.
2. If `ROOT/.arkiv` does not exist, tell the developer to run `/arkiv:init` first. Then stop.
3. Resolve TEMPLATE as `${CLAUDE_PLUGIN_ROOT}/templates/conventions.md`. Report an unreachable template. Then stop. Do this in each of these two conditions. Change no file.
   - `${CLAUDE_PLUGIN_ROOT}` is unresolved.
   - You cannot read TEMPLATE. An absent TEMPLATE matches this condition.
4. Resolve COPY as `ROOT/.arkiv/conventions.md`. Act on the state of COPY:
   - **COPY is absent**: this arkiv predates the conventions document. Write COPY from TEMPLATE. Replace every `__INIT_DATE__` token with today's date. Report the new file. Then go to the index step.
   - **COPY exists and you cannot read it**: report the error. Then stop. Change no file.
   - **COPY exists and you can read it**: go to the comparison step.
5. **The comparison step.** Compare TEMPLATE and COPY. Apply the normalization rule below. That rule holds NORMALIZED in memory, so this step writes no file.
6. If the comparison finds no difference, report that the conventions agree with the plugin template. Then stop. Change no file.
7. If the comparison finds a difference, do these two actions in order:
   1. Print the difference. State that TEMPLATE is the left side. State that COPY is the right side.
   2. Ask the developer to confirm the re-copy. Name the content that the overwrite discards.
8. Act on the answer. On a confirmation, write COPY from TEMPLATE. Apply the date rule below. Change no other byte. Then go to the index step. Without a confirmation, change no file. Then stop. Do not go to the index step.
9. **The index step.** Regenerate the index. Run `python3 "${CLAUDE_PLUGIN_ROOT}/bin/generate-index.py" "ROOT/.arkiv"`. The `summary` field of COPY feeds `INDEX.md`, so a template change can change the index. If the generator fails, report the failure. Also state that COPY is already written.
10. Report the result.

## The normalization rule

TEMPLATE holds the token `__INIT_DATE__` on exactly three lines:

```
created: __INIT_DATE__
updated: __INIT_DATE__
Created: __INIT_DATE__ · Updated: __INIT_DATE__
```

The separator on the third line is a middle dot. It is not a hyphen. Keep the middle dot exact.

`init` replaces each token with a date. `init` copies every other byte without a change. So a date is the only legitimate difference between the two files.

Build NORMALIZED from COPY. Apply three substitutions. Each pattern must match a complete line. Set TEMPLATE and COPY as shell variables first. Run this command under bash. A process substitution needs bash. It builds NORMALIZED and compares it in one action:

```bash
diff "$TEMPLATE" <(sed -E \
  -e 's/^created: [0-9]{4}-[0-9]{2}-[0-9]{2}$/created: __INIT_DATE__/' \
  -e 's/^updated: [0-9]{4}-[0-9]{2}-[0-9]{2}$/updated: __INIT_DATE__/' \
  -e 's/^Created: [0-9]{4}-[0-9]{2}-[0-9]{2} · Updated: [0-9]{4}-[0-9]{2}-[0-9]{2}$/Created: __INIT_DATE__ · Updated: __INIT_DATE__/' \
  "$COPY")
```

**Use `sed -E`.** The patterns use `{4}` and `{2}`. That interval syntax is an extended regular expression. Plain `sed` reads a basic regular expression, and it treats `{` as a literal character. Under plain `sed`, no substitution runs. Then an arkiv that agrees with the template reports a difference. Another tool is acceptable when it applies the same three patterns as an extended regular expression.

**Write no file.** The command above holds NORMALIZED in a process substitution. Do not write NORMALIZED into the repository.

**Normalize by substitution. Never normalize by deletion.** A rule that deletes a date line from both files hides a defect. Under a deletion rule, a missing `created:` line compares as equal. A malformed date value compares as equal. A second body line that starts with `Created: ` compares as equal. Substitution keeps each of those defects visible.

A line that does not match its exact expected form gets no substitution. That line stays in the comparison. A missing line, a duplicated line, and an extra line each change the line count, so the comparison shows each one.

**The patterns match any line of the file. They do not read the frontmatter block alone.** So the template body must never hold a literal `YYYY-MM-DD` date on a line that starts with `created: `, `updated: `, or `Created: `. The schema example in the body uses the placeholder `<YYYY-MM-DD>`, and a placeholder matches no pattern. A literal date in the body would mask a real difference on that line.

## The date rule for a re-copy

Read OLD_CREATED from the `created:` field of COPY. Use the first `created:` line inside the frontmatter block. The body of the document holds a `created: <YYYY-MM-DD>` line in the schema example. Do not read that line. Write COPY from TEMPLATE. Replace the three tokens by this rule:

- `created: __INIT_DATE__` becomes `created: <OLD_CREATED>`.
- `updated: __INIT_DATE__` becomes `updated: <today>`.
- `Created: __INIT_DATE__ · Updated: __INIT_DATE__` becomes `Created: <OLD_CREATED> · Updated: <today>`.

`created:` keeps the original date. That date records when this arkiv was built. `updated:` gets today's date.

COPY can hold no `created:` field. The value of `created:` can also be an invalid date. The frontmatter block can also hold more than one `created:` line. In each of those three conditions, use today's date for OLD_CREATED. Report this substitution to the developer.

## Note

This command does not classify the difference. A comparison proves that the two files differ. A comparison cannot show which file changed. A changed template and a hand-edited copy look the same.

So this command always prints the difference. This command always asks before it overwrites. The developer reads the difference and decides.
