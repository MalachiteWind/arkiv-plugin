#!/bin/sh
# Invisibility guard for a target repository.
#
# The store name is a coined token. It must never leak into the developer's
# tracked artifacts (code, comments, tracked filenames). This script blocks a
# commit when the token appears in tracked content or in a tracked filename.
#
# The store's own files are exempt. They legitimately name the store, and they
# are exempt whether or not the store is tracked.
#
# Wire it as a pre-commit hook in the TARGET repo:
#   ln -sf "<plugin>/bin/check-invisibility.sh" .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# Scope limit: a pre-commit hook cannot read the commit message or PR text.
# Use bin/check-commit-msg.sh for the message. PR-body text needs a separate
# CI or review control.
#
# Exit status: 0 = clean, 1 = the token was found or a git command failed.

set -u

TOKEN='arkiv'
STORE_EXCLUDE=':(exclude).arkiv/**'
violation=0

# 1. Staged content (the index is what the commit will contain).
content=$(git grep -n -I -F -i -e "$TOKEN" --cached -- "$STORE_EXCLUDE" 2>/dev/null)
rc=$?
if [ "$rc" -gt 1 ]; then
    echo "invisibility guard: error: 'git grep' failed (exit $rc); commit blocked." >&2
    exit 1
fi
if [ "$rc" -eq 0 ]; then
    echo "invisibility guard: the store token appears in tracked content:" >&2
    echo "$content" >&2
    violation=1
fi

# 2. Tracked filenames (git grep searches content, not paths).
names=$(git ls-files -- "$STORE_EXCLUDE" 2>/dev/null | grep -F -i -e "$TOKEN")
rc=$?
if [ "$rc" -gt 1 ]; then
    echo "invisibility guard: error: 'git ls-files' failed; commit blocked." >&2
    exit 1
fi
if [ -n "$names" ]; then
    echo "invisibility guard: the store token appears in tracked filenames:" >&2
    echo "$names" >&2
    violation=1
fi

if [ "$violation" -ne 0 ]; then
    echo "" >&2
    echo "The store name must not appear in tracked artifacts. Remove it, then commit." >&2
    exit 1
fi
exit 0
