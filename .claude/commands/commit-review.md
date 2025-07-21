---
name: commit-review
aliases: ["cr", "safe-commit", "review-commit"]
description: Review all changes before committing with full control
category: git
---

# Commit Review Command

Review all changes and selectively commit with full control.

## Usage

```bash
/commit-review                    # Interactive review of all changes
/cr "feat: Add user auth"        # Review then commit with message
/safe-commit --staged            # Only review staged files
```

## What It Does

1. **Shows Current Status**
   - Current branch
   - Uncommitted changes
   - Files modified

2. **Interactive Review**
   - Display diff for each file
   - Option to stage/unstage files
   - Preview commit before confirming

3. **Safety Checks**
   - Lint check on changed files
   - Design system validation
   - No PII in commit messages
   - Verify tests pass

4. **Commit Options**
   - Commit all changes
   - Commit only staged files
   - Amend last commit
   - Create draft commit message

## Interactive Flow

```
🔍 Commit Review
━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 Branch: feature/user-auth
📝 Files Changed: 5

Modified Files:
  M components/LoginForm.tsx
  M lib/auth/validateUser.ts
  M app/api/auth/route.ts
  ? components/NewButton.tsx
  ? lib/utils/helpers.ts

Review each file? (y/n): y

[Shows diff for each file with options:]
  s - Stage this file
  u - Unstage this file  
  e - Edit file first
  n - Skip to next
  q - Quit review

Ready to commit? (y/n): y
Enter commit message: feat: Add user authentication flow

[Final confirmation showing exactly what will be committed]
```

## Options

- `--staged` - Only review already staged files
- `--quick` - Skip individual file review
- `--amend` - Amend the last commit
- `--no-verify` - Skip pre-commit hooks
- `--push` - Push after successful commit

## Safety Features

1. **Never Auto-Commits**
   - Always requires explicit confirmation
   - Shows exactly what will be committed
   - Can abort at any time

2. **Smart Defaults**
   - Doesn't stage .env files
   - Warns about large files
   - Checks for merge conflicts

3. **Integration with Team Flow**
   - Respects branch protection
   - Updates task tracking
   - Notifies in team channel

## Examples

### Review and Commit Specific Files
```bash
/cr components/*.tsx "refactor: Update all components"
```

### Quick Commit (Still Requires Confirmation)
```bash
/cr --quick "fix: Resolve login bug"
```

### Amend Last Commit
```bash
/cr --amend
```

## Configuration

Customize in `.claude/team/nikki-config.json`:
```json
{
  "commit_review": {
    "auto_stage_tracked": false,
    "show_full_diff": true,
    "require_issue_number": true,
    "sign_commits": true,
    "default_push": false
  }
}
```

## Related Commands

- `/git-status` - Quick status check
- `/checkpoint` - Save work without committing
- `/diff-check` - Review changes only
- `/stage-files` - Stage specific files
