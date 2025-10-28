#!/bin/bash
git log --reverse --format="%h|%s" | grep "Auto-commit" | while IFS='|' read hash msg; do
    echo "=== $hash ==="
    git diff-tree --no-commit-id --name-only -r $hash
    echo
done
