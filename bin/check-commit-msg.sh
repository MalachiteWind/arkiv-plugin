#!/bin/sh
# Invisibility guard for the commit MESSAGE.
#
# A pre-commit hook cannot see the commit message. This companion runs as a
# commit-msg hook, which git calls with the path to the message file.
#
# Wire it in the TARGET repo:
#   ln -sf "<plugin>/bin/check-commit-msg.sh" .git/hooks/commit-msg
#   chmod +x .git/hooks/commit-msg
#
# Exit status: 0 = clean, 1 = the store token was found in the message.

set -u

TOKEN='arkiv'

if [ "$#" -lt 1 ] || [ ! -f "$1" ]; then
    echo "invisibility guard: error: no commit message file given; commit blocked." >&2
    exit 1
fi

if grep -F -i -q -e "$TOKEN" "$1"; then
    echo "invisibility guard: the store token appears in the commit message. Remove it." >&2
    exit 1
fi
exit 0
