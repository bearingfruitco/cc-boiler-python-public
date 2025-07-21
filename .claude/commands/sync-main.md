---
name: sync-main
aliases: [sync-from-main, update-main]
description: Safely sync current branch with latest main
category: branch-management
---

Safely update your branch with the latest changes from main:
- Pulls latest main
- Shows what changed
- Merges or rebases safely
- Updates branch registry

## Usage
```bash
/sync-main
/sync-main --rebase  # Use rebase instead of merge
/sync-main --check   # Just check, don't sync
```

## What It Does

### 1. Pre-flight Checks
- Ensures clean working directory
- Stashes uncommitted changes
- Checks for conflicts

### 2. Updates Main
```bash
git checkout main
git pull origin main
```

### 3. Updates Current Branch
```bash
git checkout [your-branch]
git merge main  # or rebase
```

### 4. Registry Updates
- Updates last sync time
- Refreshes feature states
- Clears stale blocks

## Safety Features

### Automatic Stashing
If you have uncommitted changes:
```
📦 Stashing uncommitted changes...
✅ Stashed as: sync-main-backup-2025-07-21
```

### Conflict Detection
```
⚠️ Potential conflicts detected in:
- src/auth/login.py
- tests/test_auth.py

Continue with sync? (y/n)
```

### Rollback Option
```
❌ Merge failed!

Rollback options:
1. Abort merge: git merge --abort
2. Restore stash: git stash pop
3. Get help: /help merge-conflict
```

## Output Example
```
🔄 Syncing with main branch...

📍 Current: feature/user-dashboard
📦 Stashing 3 uncommitted files...

Updating main:
✅ Pulled 5 new commits
📝 Changes:
  - auth/middleware.py (enhanced)
  - models/user.py (new fields)
  - tests/test_auth.py (more tests)

Merging into feature/user-dashboard:
✅ Merge successful (no conflicts)

📊 Summary:
- Added: 120 lines
- Modified: 5 files
- Deleted: 0 files
- Your branch is now up-to-date!

💡 Next steps:
1. Run tests: /test
2. Continue work: /pt
3. Check status: /branch-status
```

## Best Practices

### When to Sync
- Before creating new branches
- After main has significant updates
- Before submitting PR
- When conflicts are suspected

### Sync Strategies
- **Merge**: Preserves branch history (default)
- **Rebase**: Cleaner history, rewrites commits
- **Check only**: See changes without applying

## Related Commands
- `/branch-status` - Check sync status
- `/branch-health` - See if sync needed
- `/conflict-resolve` - Help with conflicts
