---
name: branch-status
aliases: [bs, branch-info]
description: Show comprehensive branch status and health
category: branch-management
---

Display complete branch status including:
- Current branch and its state
- Active branches and their purposes
- File conflicts and blocks
- Merge readiness
- Policy compliance

## Usage
```bash
/branch-status
/bs  # alias
```

## What It Shows

### Current Branch Info
- Branch name and purpose
- Base commit and age
- Modified files
- Test status
- Related issue/task

### Active Branches
- All non-merged branches
- Their modification scope
- Conflict detection
- Age warnings

### Branch Health
- Policy compliance
- Stale branch warnings
- Unfinished work alerts
- Merge recommendations

### File Blocks
- Which files are locked to which branches
- Conflict predictions

## Output Example
```
📍 Current Branch: feature/user-auth
📋 Purpose: Implement JWT authentication (Issue #23)
🕐 Age: 2 days
🧪 Tests: ❌ 3 failing
📄 Modified: 5 files

🌿 Active Branches (2):
1. feature/user-auth ← YOU ARE HERE
   - Status: In Progress
   - Files: auth.py, middleware.py, tests/test_auth.py
   - Ready to merge: NO (tests failing)

2. feature/import-fix ⚠️
   - Status: In Progress (5 days old - consider merging!)
   - Files: import_script.py
   - Conflicts with: None
   - Issue: #17

📊 Branch Policy Status:
❌ Max 1 active branch (currently: 2)
✅ Main sync: OK (synced 2 hours ago)
❌ Tests must pass before new branch

🔒 File Blocks:
- import_script.py → locked to feature/import-fix

💡 Recommendations:
1. Fix failing tests on current branch
2. Consider merging old feature/import-fix branch
3. Run /branch-health for detailed analysis
```

## Related Commands
- `/branch-health` - Detailed health analysis
- `/branch-switch` - Smart branch switching
- `/sync-main` - Update from main
- `/feature-status` - Check feature completion
