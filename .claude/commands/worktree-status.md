---
name: worktree-status
aliases: [wt-status, wts]
description: Show status of all active worktrees
category: orchestration
---

# Worktree Status

Display comprehensive status of all active git worktrees.

## Usage

```bash
# Show all worktrees status
/worktree-status

# Show specific worktree
/wt-status auth-feature

# Show with details
/wts --detailed

# Monitor mode (refreshes every 5s)
/wts --monitor
```

## What It Shows

1. **Worktree Information**
   - Name and path
   - Current branch
   - Task description
   - Creation time

2. **Progress Tracking**
   - Task completion status
   - Test results
   - Validation status
   - Last activity

3. **Git Status**
   - Changed files
   - Commits ahead/behind
   - Merge readiness

## Integration with Task Ledger

The status command reads from each worktree's task ledger to show:
- Tasks completed
- Tasks in progress
- Blocked tasks
- Overall progress percentage

## Output Example

```
🌳 Active Worktrees (3)

📁 auth-feature
   Branch: feature/auth-feature
   Task: Implement authentication system
   Progress: 7/10 tasks (70%)
   Status: 🟢 Tests passing
   Changes: 15 files (+523/-45)
   Last activity: 2 minutes ago

📁 payment-feature  
   Branch: feature/payment-feature
   Task: Add payment processing
   Progress: 3/8 tasks (37%)
   Status: 🟡 In progress
   Changes: 8 files (+234/-12)
   Last activity: 5 minutes ago

📁 ui-refactor
   Branch: feature/ui-refactor
   Task: Refactor dashboard UI
   Progress: 10/10 tasks (100%)
   Status: ✅ Ready to merge
   Changes: 22 files (+892/-445)
   Last activity: 15 minutes ago
```

## Options

- `--detailed` - Show file changes and commit history
- `--monitor` - Auto-refresh every 5 seconds
- `--json` - Output in JSON format
- `--brief` - One-line summary per worktree
