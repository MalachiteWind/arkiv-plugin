---
description: Create the repo-root arkiv and propose a small starting skeleton
argument-hint: "[<existing_docs_path>]"
disable-model-invocation: true
---

Create the repo-root arkiv. arkiv prevents model-drift across sessions.

`$1` is an optional path to existing notes. Import them when it is present.

`init` runs one time for the life of a repository. Every later session starts from what `init` writes. So `init` must be correct. Speed and cost are less important.

## Rules for every write

1. Resolve the repository root. Run `git rev-parse --show-toplevel 2>/dev/null || pwd`. Call the result ROOT. arkiv is `ROOT/.arkiv`.
2. Write every document through the ASD-STE100 skill. Invoke the Skill `arkiv:asd-ste100`. Use **strict** mode for `donotforget.md` and `handoff/*`. Use **STE-flavored** mode for all other documents. If the Skill name is not available, read `${CLAUDE_PLUGIN_ROOT}/skills/asd-ste100/SKILL.md` and apply its rules.
3. Do not write the token `arkiv` or the arkiv path into a tracked file of the repository. arkiv's own files are exempt.
4. Read `${CLAUDE_PLUGIN_ROOT}/templates/conventions.md`. It defines the frontmatter schema, the research status values, and the category habits. Apply it to every document you write.

## Steps

1. Check for a git repository. Run `git rev-parse --show-toplevel`. If it fails, tell the developer that the exclude step needs a git repository. On request, create arkiv and skip the hide step.
2. Check for an existing arkiv. If `ROOT/.arkiv` exists, **STOP**. `init` writes from scratch. `init` destroys an untracked arkiv. Name the correct command for the developer's goal:
   - To record new content, run `/arkiv:update`.
   - To update `conventions.md` from a changed plugin template, run `/arkiv:sync`. `update` must never edit that file.
3. Create the directories: `ROOT/.arkiv/research/`, `ROOT/.arkiv/dev/`, and `ROOT/.arkiv/handoff/`.
4. Create the files: `ROOT/.arkiv/README.md`, `ROOT/.arkiv/todo.md`, and `ROOT/.arkiv/donotforget.md`.
5. Hide arkiv. Resolve the exclude file with `git rev-parse --git-path info/exclude`. Add the single line `.arkiv/` to that file. Add the line only when the line is absent.
6. Gather the evidence. Do these actions in this order. Do not read the docs first.
   1. Read the code in full. The code is the source of truth for how the project works. Find the entry points first. An entry point is a file that starts a program, a command, or a service. A main module is a file that an entry point imports, directly or through another file.
   2. Read the git history. Run `git log --oneline`. Read the full message of each commit that changed a main module. A commit message is often the only record of a reason.
   3. Read `README`, `CLAUDE.md`, and every other document. Complete action 1 and action 2 first. Do not compare a document claim against the evidence before action 1 and action 2 are complete. You can see a document early during orientation. That early view does not change the order of these actions. Treat each claim in a document as unverified.
   4. Report the evidence in the proposal. Name every part that you did not read. Never present a partial read as a full read. A repository can be too large for a full read. In that condition, read every entry point and every main module. That read completes action 1. Report the gap in the proposal.
   5. A repository can have no git history. In that condition, read the code. Skip the two history actions. Report the missing git evidence in the proposal.
7. Reconcile the evidence. Prefer the code and the git history over a document claim. Put each document claim that the evidence does not support into one of three lists:
   1. Unconfirmed. The evidence gives no support for the claim. The evidence gives no support against the claim. A claim is unconfirmed only after a partial read, or after a read of a repository with no git history. Call this list the unconfirmed claims.
   2. Outdated. The current code contradicts the claim. The git history shows the claim as true before. Record what changed. Record the commit that changed it. Call this list the outdated claims.
   3. Contradicted. The current code contradicts the claim. The git history never shows the claim as true. Call this list the contradicted claims.

   A full read shows what the code does not have. After a full read, a missing feature contradicts a claim for that feature. Put a claim for a missing feature in the contradicted list. Call this action the missing-feature rule.

   The missing-feature rule applies to a claim about specific behavior. `Serves on port 8080.` states specific behavior. The missing-feature rule does not apply to a claim about the project purpose. `A calculator.` states a purpose. An unbuilt project can state its purpose correctly. Keep a purpose claim out of the contradicted list. The missing-feature rule does not apply to a research note.
8. Propose a skeleton. Propose a small set of documents. Five deep pages are better than fifty shallow pages. Show the proposal. Show the evidence report from the gather step. Show the three claim lists from the reconcile step. Get confirmation before you write.
9. Write `README.md`. Give it the frontmatter schema first. Then start the body with a bold banner: **NOT TRACKED — never named in the repo**. Put the visible date line after the banner. State the arkiv purpose. State how to navigate arkiv. State the upshot for a fresh agent. Point to `conventions.md` for the schema and the conventions.
10. **The conventions step.** Write `conventions.md`. Copy `${CLAUDE_PLUGIN_ROOT}/templates/conventions.md` to `ROOT/.arkiv/conventions.md` without change. Then replace every `__INIT_DATE__` token with today's date. Do not change any other text. Do not write this document through the skill. It is a verbatim copy.
11. Write the confirmed skeleton documents into `ROOT/.arkiv/dev/` and `ROOT/.arkiv/research/`.
12. Give every document that you write the frontmatter schema from `conventions.md` and a visible date line in the body.
13. Write the reconcile results into `ROOT/.arkiv/todo.md`. Write one open task for each claim. Use the form that matches the claim list:
    - Unconfirmed: `- [ ] Reconcile <document>: <claim>. The code and the git history do not confirm it.`
    - Outdated: `- [ ] Reconcile <document>: <claim>. Commit <hash> changed this behavior to <current behavior>.`
    - Contradicted: `- [ ] Reconcile <document>: <claim>. The code does <current behavior>. The git history holds no record of the claim.`

    Write no task when the three lists are empty.
14. Regenerate the index. Run `python3 "${CLAUDE_PLUGIN_ROOT}/bin/generate-index.py" "ROOT/.arkiv"`. This action is the first index regeneration.
15. Print the guard-wiring command. Do not run it:
    ```
    HOOKS="$(git rev-parse --git-path hooks)"
    ln -sf "${CLAUDE_PLUGIN_ROOT}/bin/check-invisibility.sh" "$HOOKS/pre-commit"
    ln -sf "${CLAUDE_PLUGIN_ROOT}/bin/check-commit-msg.sh" "$HOOKS/commit-msg"
    chmod +x "$HOOKS/pre-commit" "$HOOKS/commit-msg"
    ```

## With `$1` (existing notes path)

The notes are an untrusted source. Do not import a note without a check.

Import the notes after the first index regeneration. These rules govern the full import. They govern the update pass and the clean pass.

1. Check each note against the code and the git history from the gather step. Check a note claim by claim. A note can hold one true claim and one false claim.
2. Never delete a note. Assign a status instead. Import every note. Use these three status rules for a research idea:
   - The code or the git history contradicts the idea. The idea takes `status: discarded`. Record the contradiction and its evidence in the body.
   - The code does not hold the idea yet. The idea takes `status: idea` or `status: exploring`.
   - The code holds the idea now. The idea takes `status: promoted`. Set `related` to the matching `dev/` document.

   A note can hold claims that need different status values. Split that note into one document for each status value. Keep every claim.
3. A note that is not a research idea takes no status. Keep its content. Record each contradicted claim as an open task in `todo.md`.
4. A research note that the code does not hold yet is not stale. `conventions.md` states that research is ahead of the code. Mark a research note only when the code or the git history contradicts it.
5. Keep the high-value content. Do not compress a note into a one-line summary. The "crucial points only" scope of `update` does not apply to an import.
6. Keep legible TeX math as TeX. Use `$…$` for inline math. Use `$$…$$` for display math. Never put math in a code fence.
7. Show each status that you assigned. Show each claim that you marked. Get confirmation before you write the import.
8. Do one update pass. Apply the schema in `conventions.md` to the notes. Then do one clean pass. Consolidate a duplicate idea into one place. Keep the information. Normalize the result.
9. Regenerate the index after the import.

## Conventions

The frontmatter schema, the research status values, and the category habits live in `${CLAUDE_PLUGIN_ROOT}/templates/conventions.md`. That template is the single source of truth for the schema and the conventions. Read it. Apply it to every document you write. The conventions step copies it verbatim into `ROOT/.arkiv/conventions.md`, so a fresh agent finds the same rules in the arkiv.
