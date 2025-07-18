---
name: git-status
aliases: ["gs", "status", "changes"]
description: Check git status and changes without committing
category: git
---

# Git Status Command

Check current git status and review changes without any risk of auto-commit.

## Usage

```bash
/git-status              # Show current status
/gs                      # Quick status
/status --detailed       # Show file diffs
```

## What It Shows

1. **Current Branch**: Where you are
2. **Uncommitted Changes**: What's modified
3. **Untracked Files**: New files not in git
4. **Staged Files**: Ready to commit
5. **Behind/Ahead**: Sync status with remote

## Output Example

```
📍 Current Branch: feature/user-auth
🔄 Status: 3 commits ahead of origin/main

📝 Changes:
  Modified (not staged):
    M components/LoginForm.tsx
    M lib/auth/validateUser.ts
  
  Staged for commit:
    A components/SignupForm.tsx
  
  Untracked:
    ? .env.local
    ? notes.md

💡 Use /cr to review and commit changes
   Use /checkpoint to save work without committing
```

## Options

- `--detailed` - Show diff for each file
- `--summary` - Just count of changes
- `--ignored` - Include ignored files

## Related Commands

- `/cr` - Review and commit changes
- `/checkpoint` - Save work state
- `/diff-check` - See detailed diffs
