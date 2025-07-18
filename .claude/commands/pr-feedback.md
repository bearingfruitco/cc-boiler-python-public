# PR Feedback

Lightweight PR status check that complements CodeRabbit IDE extension.

## Arguments:
- $PR_NUMBER: PR number to check (optional, defaults to current branch)

## Why This Command:
- Quick PR status check
- See CodeRabbit's final review summary
- Check approval status
- Complement real-time IDE feedback

## Usage:

```bash
/pr-feedback

# Get current PR status
BRANCH=$(git branch --show-current)
PR_NUMBER=$(gh pr list --head "$BRANCH" --json number -q '.[0].number')

if [ -z "$PR_NUMBER" ]; then
  echo "❌ No PR found for branch: $BRANCH"
  echo "💡 Create one with: gh pr create"
  exit 1
fi

echo "📋 PR #$PR_NUMBER Status Check"
echo "================================"

# 1. Basic PR Info
PR_DATA=$(gh pr view $PR_NUMBER --json state,mergeable,reviews,checks)
STATE=$(echo $PR_DATA | jq -r '.state')
MERGEABLE=$(echo $PR_DATA | jq -r '.mergeable')

echo "State: $STATE"
echo "Mergeable: $MERGEABLE"
echo ""

# 2. CodeRabbit Summary (if available)
echo "🐰 CodeRabbit Summary:"
RABBIT_SUMMARY=$(gh pr view $PR_NUMBER --comments | grep -A 5 "coderabbitai" | grep -E "Summary|Overall|found" | head -3)

if [ ! -z "$RABBIT_SUMMARY" ]; then
  echo "$RABBIT_SUMMARY"
else
  echo "No CodeRabbit review found (using IDE extension?)"
fi

# 3. Quick Checks Status
echo -e "\n✅ Checks:"
gh pr checks $PR_NUMBER --interval 0 | head -5

# 4. Approval Status
echo -e "\n👥 Reviews:"
REVIEWS=$(echo $PR_DATA | jq -r '.reviews[] | "\(.author.login): \(.state)"' | head -3)
echo "${REVIEWS:-No reviews yet}"

# 5. Next Action
echo -e "\n💡 Next Steps:"
if [ "$MERGEABLE" = "true" ] && [ "$STATE" = "open" ]; then
  echo "Ready to merge! Run: gh pr merge $PR_NUMBER"
elif [ "$STATE" = "open" ]; then
  echo "Address remaining issues in Cursor with CodeRabbit IDE"
else
  echo "PR is $STATE"
fi
```

## Simplified Workflow:

1. **During Development** - CodeRabbit IDE catches issues in real-time
2. **Before Push** - Issues already fixed via IDE extension
3. **After Push** - Run `/pr-feedback` for final status check
4. **If Issues** - Fix in Cursor with CodeRabbit's help

## Integration with CodeRabbit IDE:

Since you have the IDE extension:
- Most issues caught before commit
- PR reviews are cleaner
- This command becomes a final check
- No duplicate feedback

## Quick Commands:

```bash
# Check status
/pr-feedback

# Create PR if needed
gh pr create --fill

# Merge when ready
gh pr merge --auto --squash
```