#!/bin/bash
# Remove commits with secrets and force push

echo "🔒 Removing commits with secrets..."

cd /Users/shawnsmith/dev/bfc/boilerplate-python

# The commit before the problematic one
SAFE_COMMIT="519a5ff8"  # feat: v2.4.0 - Smart Issue Creation & Dependency Tracking

echo "📍 Resetting to safe commit: $SAFE_COMMIT"
git reset --hard $SAFE_COMMIT

# Now cherry-pick the good commits after the bad ones
echo "🍒 Cherry-picking good commits..."

# Get all commits after the safe one
COMMITS_TO_CHERRY_PICK=$(git log --reverse --pretty=format:"%H" $SAFE_COMMIT..origin/main | grep -v "abd21c76" | grep -v "829918f" | grep -v "825aab9" | grep -v "acfa4b0f")

for commit in $COMMITS_TO_CHERRY_PICK; do
    echo "Cherry-picking: $commit"
    git cherry-pick $commit || {
        echo "⚠️  Conflict in $commit, resolving..."
        git cherry-pick --continue
    }
done

# Re-apply our latest changes
echo "📝 Re-applying latest changes..."
git add -A
git commit -m "Major update: Remove TypeScript boilerplate remnants and focus on Python-specific features

- Removed all TypeScript/JavaScript related files and configs
- Cleaned up commands to be Python-specific only
- Updated hooks for Python development workflow
- Streamlined documentation to focus on Python agent development
- Added new Python-specific commands and workflows
- Updated README with latest features including UltraThink integration
- Removed design system enforcement (not applicable to Python CLI/API development)
- Enhanced orchestration and parallel agent features"

echo "✅ Clean history created!"
echo ""
echo "📤 To push to bearingfruitco repository:"
echo "   git push --force public main"
echo ""
echo "⚠️  This will overwrite the remote history!"
