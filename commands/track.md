---
description: Toggle whether git can track the store (default is untracked and invisible)
argument-hint: "[true|false]"
disable-model-invocation: true
---

Toggle whether git can track the store. The default state is `false` (untracked and invisible).

`$1` is `true`, `false`, or absent.

## Steps

1. Resolve the repository root. Run `git rev-parse --show-toplevel`. If it fails, tell the developer that this command needs a git repository. Then stop.
2. Resolve the exclude file. Run `git rev-parse --git-path info/exclude`. Call the result EXCLUDE. This path is correct in a linked worktree.
3. Act on `$1`:
   - **Absent**: report the current state. State whether the line `.arkiv/` is present in EXCLUDE. State that the default is `false` (untracked). Do not change any file. This avoids a surprise state flip.
   - **`false`**: ensure the line `.arkiv/` is present in EXCLUDE. Add the line only when it is absent. The store stays untracked.
   - **`true`**: remove the line `.arkiv/` from EXCLUDE. The store can now be tracked. This command does not commit anything.
4. Report the resulting state.

## Note

`true` lets git track the store. It does not add or commit the store. The invisibility guard (`bin/check-invisibility.sh`) exempts `.arkiv/**`, so a tracked store does not trip the guard.
