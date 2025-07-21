#!/bin/bash

echo "=== Checking local vs GitHub differences ==="
echo

# Count local files
echo "📁 LOCAL .claude/commands:"
ls -la .claude/commands/ | grep -E "\.md$" | wc -l
echo

echo "📁 LOCAL .claude/hooks:"
find .claude/hooks -name "*.py" -type f | wc -l
echo

# Check current branch
echo "📌 Current branch:"
git branch --show-current
echo

# Check if there are unpushed commits
echo "📤 Unpushed commits:"
git log origin/main..HEAD --oneline
echo

# Check untracked files
echo "❓ Untracked files in .claude:"
git status .claude --porcelain | grep "^??"
echo

# Check modified files
echo "📝 Modified files in .claude:"
git status .claude --porcelain | grep "^ M"
echo

# Show what would be pushed
echo "🚀 Files that would be added if you run 'git add .claude':"
git add --dry-run .claude 2>&1 | head -20
