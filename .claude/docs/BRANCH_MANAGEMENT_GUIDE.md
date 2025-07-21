# Branch Management & Feature Protection System

## 🎯 Overview

This system prevents Claude Code from:
- Recreating completed features
- Working on wrong branches
- Creating conflicting branches
- Losing track of what's built

## 🛡️ Core Components

### 1. Feature State Registry (`.claude/feature-state.json`)
Tracks what features are complete, in-progress, or planned.

### 2. Branch Registry (`.claude/branch-registry.json`)
Monitors active branches, file locks, and merge readiness.

### 3. Protection Hooks
- **20-feature-state-guardian.py**: Prevents modifying completed features
- **21-branch-controller.py**: Enforces branch discipline

### 4. Branch Commands
- `/branch-status` (`/bs`): See all branch activity
- `/feature-status` (`/fs`): Check feature completion
- `/sync-main`: Update from main safely
- `/branch-switch` (`/bsw`): Smart branch switching

## 🚀 Quick Start

### Check Current State
```bash
/bs  # Branch status - see what's active
/fs  # Feature status - see what's built
```

### Start New Work Safely
```bash
/sync-main  # Ensure you have latest
/fw start 123  # Start feature (checks for conflicts)
```

### Switch Branches Intelligently
```bash
/bsw feature/other  # Saves context, switches smartly
```

## 📋 Protection Scenarios

### Scenario 1: Preventing Feature Recreation
```
❌ You try to modify auth.py on a feature branch
✅ System detects auth is already complete on main
📝 Warns you and suggests proper enhancement approach
```

### Scenario 2: Branch Limit Enforcement
```
❌ You try to create a new branch with unfinished work
✅ System blocks and shows what needs completion
📝 Forces you to finish or stash current work
```

### Scenario 3: File Conflict Prevention
```
❌ You try to modify a file being changed on another branch
✅ System warns about the conflict before it happens
📝 Suggests switching to the right branch
```

## 🔧 Configuration

### Branch Rules (`.claude/branch-registry.json`)
```json
{
  "branch_rules": {
    "max_active_branches": 1,        // One branch at a time
    "require_main_sync": true,       // Must sync before new branches
    "require_tests_before_new": true,// Tests must pass
    "prevent_conflicting_branches": true
  }
}
```

### Feature Protection (`.claude/hooks/config.json`)
```json
{
  "feature_protection": {
    "enabled": true,
    "strict_mode": true,
    "track_working_implementations": true,
    "warn_on_branch_mismatch": true
  }
}
```

## 💡 Best Practices

### 1. Always Check Status First
```bash
/bs  # Before creating branches
/fs [feature]  # Before modifying features
```

### 2. Keep Branches Focused
- One issue per branch
- Merge frequently
- Don't let branches age

### 3. Mark Features Complete
When a feature is done and tested:
```bash
/feature-complete [name]  # Marks as protected
```

### 4. Use Smart Switching
```bash
/bsw [branch]  # Don't use raw git checkout
```

## 🚨 Common Warnings and Solutions

### "Feature Already Complete"
**Cause**: Trying to recreate working code
**Solution**: 
1. Check feature status: `/fs [feature]`
2. Create enhancement branch from main
3. Or continue on existing enhancement branch

### "Branch Limit Exceeded"
**Cause**: Too many active branches
**Solution**:
1. Check branch status: `/bs`
2. Complete current work: `/fw complete`
3. Or stash: `/branch stash`

### "File Conflict Detected"
**Cause**: File being modified on another branch
**Solution**:
1. Switch to correct branch: `/bsw [branch]`
2. Or wait for other branch to merge
3. Or work on different files

## 🔄 Workflow Integration

### Starting Features
```bash
/fw start 123
# ✅ Checks feature state
# ✅ Ensures clean branches
# ✅ Syncs from main
# ✅ Creates protected branch
```

### Daily Work
```bash
/sr  # Smart resume loads branch context
/bs  # Check branch health
/pt  # Process tasks (knows your branch)
```

### Completing Work
```bash
/test  # Run tests
/fw complete  # Marks done, updates registries
/branch-merge  # Safe merge with protection
```

## 📊 Monitoring

### Branch Health Indicators
- 🟢 **Healthy**: < 3 days old, tests passing
- 🟡 **Warning**: 3-7 days old, needs attention  
- 🔴 **Critical**: > 7 days old, merge or close

### Feature State Indicators
- ✅ **Completed**: Protected, don't recreate
- 🔧 **In Progress**: Active development
- 📋 **Planned**: Not started yet

## 🆘 Troubleshooting

### Override Protection (Use Carefully!)
```bash
/truth-override  # Temporarily disable protections
# Make changes
/truth-restore  # Re-enable protections
```

### Fix Branch Registry
```bash
/branch-repair  # Scan and fix inconsistencies
```

### Reset Feature State
```bash
/feature-reset [name]  # Remove protection
```

## 🎯 Summary

This system ensures:
1. **No Lost Work**: Everything is tracked
2. **No Recreated Features**: Completed = protected
3. **No Conflicts**: Prevented before they happen
4. **Clear Context**: Always know branch purpose

The key is using the commands instead of raw git operations!
