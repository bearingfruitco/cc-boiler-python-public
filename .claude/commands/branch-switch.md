---
name: branch-switch
aliases: [bsw, switch-branch]
description: Smart context-aware branch switching
category: branch-management
---

Switch branches intelligently with:
- Automatic stashing
- Context preservation
- State loading
- Conflict warnings

## Usage
```bash
/branch-switch [branch-name]
/bsw main  # Switch to main
/branch-switch feature/auth --no-stash  # Don't auto-stash
```

## Smart Features

### 1. Uncommitted Changes Handling
```
📋 Uncommitted changes detected:
- src/auth/login.py (modified)
- tests/test_auth.py (new)

Options:
1. Stash changes (recommended)
2. Commit changes
3. Discard changes
4. Cancel switch

Your choice (1-4): _
```

### 2. Context Preservation
Before switching, saves:
- Current work state
- Open files/issues
- Test status
- Modified files list

### 3. Context Loading
After switching, loads:
- Branch purpose
- Related issue
- Previous state
- Next suggested action

### 4. Conflict Prevention
```
⚠️ Warning: Target branch modifies same files!

Conflicting files:
- src/models/user.py (both branches modify)

Continue anyway? (y/n): _
```

## Full Workflow Example
```
$ /branch-switch feature/import-fix

🔄 Switching from: feature/auth → feature/import-fix

📦 Saving current context...
✅ Context saved: .claude/branch-context/feature-auth.json

📋 You have uncommitted changes. Stashing...
✅ Stashed as: branch-switch-auth-2025-07-21

🌿 Switching branches...
✅ Now on: feature/import-fix

📥 Loading branch context...
📋 Branch Purpose: Add missing LeadProsper fields (Issue #17)
📅 Last worked: 3 days ago
🧪 Tests: ✅ Passing
📄 Working on: scripts/import_to_leads.py

💡 Suggested next action:
→ Continue where you left off: /pt import-fields
→ Or check current status: /task-status

📝 Previous work summary:
- Added 45 of 112 missing fields
- Validation logic updated
- Need to add remaining demographic fields
```

## Options

### `--no-stash`
Don't automatically stash changes

### `--force`
Switch even with conflicts

### `--status`
Just show what would happen

## Context Files

Each branch gets a context file:
```
.claude/branch-context/feature-auth.json
```

Contains:
- Branch purpose
- Modified files
- Work history
- Test status
- Related issues

## Related Commands
- `/branch-status` - Check before switching
- `/branch-stash` - Manual stashing
- `/branch-restore` - Restore context
