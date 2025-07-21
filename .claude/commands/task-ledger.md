---
name: task-ledger
aliases: [tl, ledger]
description: View and manage the central task ledger
category: workflow
---

Manage the central task ledger (.task-ledger.md) that tracks all tasks across the project.

## Arguments:
- $ACTION: view|update|link|generate|clean
- $FEATURE: (optional) specific feature name

## Actions:

### VIEW (default)
Show current task ledger status:
```bash
/tl view
# or just
/tl
```

Output:
```markdown
# Task Ledger Summary

## Active Tasks (3)
1. **user-authentication** - In Progress (5/12 tasks, 42%)
   - Issue: #23
   - Branch: feature/23-user-auth
   - Last updated: 2 hours ago

2. **data-pipeline** - Generated (0/8 tasks)
   - Issue: Not linked
   - Branch: Not created
   - Created: Yesterday

3. **api-refactor** - Blocked (3/15 tasks, 20%)
   - Issue: #19
   - Blocked by: #15
   - Last updated: 3 days ago

## Completed This Week (2)
- ✅ **bug-fix-login** - 5/5 tasks (100%)
- ✅ **performance-optimization** - 8/8 tasks (100%)

## Statistics
- Total Active Tasks: 35
- Completed Tasks: 16 (45.7%)
- Blocked Tasks: 15
- Time This Week: 12h 30m
```

### UPDATE
Update task progress for a specific feature:
```bash
/tl update user-authentication
```

This will:
1. Read the current task file
2. Count completed tasks (marked with [x])
3. Update progress in ledger
4. Update status if all complete

### LINK
Link a feature to a GitHub issue:
```bash
/tl link data-pipeline 25
```

Updates the ledger entry with:
- Issue number
- Suggested branch name
- Issue title and description

### GENERATE
Generate task ledger from existing task files:
```bash
/tl generate
```

Scans `docs/project/features/*.md` and creates/updates ledger entries.
Useful for:
- Migrating existing projects
- Recovering from ledger corruption
- Initial setup

### CLEAN
Remove completed tasks older than X days:
```bash
/tl clean 30
```

Archives completed tasks to `.task-ledger-archive.md`.

## Integration with Other Commands:

The task ledger integrates with:
- `/gt` - Automatically adds entries when generating tasks
- `/pt` - Updates progress as tasks are completed
- `/fw start` - Links issues when starting features
- `/ws` - Includes ledger summary in work status
- `/sr` - Shows pending tasks on resume

## Ledger File Format:

The `.task-ledger.md` file uses this structure:
```markdown
# Task Ledger for [project]

This file tracks all tasks generated and processed by Claude Code commands.

## Task: [feature-name]
**Generated**: [timestamp]
**Issue**: #[number] - [title]
**Status**: Generated | In Progress | Completed | Blocked
**Branch**: feature/[branch-name]
**Progress**: [completed]/[total] tasks completed ([percentage]%)
**Time Spent**: [optional time tracking]
**Blocked By**: [optional blocker reference]

### Description
[Brief description of the feature]

### Task File
See detailed tasks in: `docs/project/features/[feature]-tasks.md`

### Recent Updates
- [timestamp]: Started implementation
- [timestamp]: Completed phase 1
- [timestamp]: Blocked on API design

### Validation Checklist
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] No regressions
- [ ] Code review completed

---
```

## Quick Commands:

```bash
# View all tasks
/tl

# View specific feature
/tl view user-auth

# Update progress
/tl update user-auth

# Link to issue
/tl link user-auth 23

# Generate from existing
/tl generate

# Clean old tasks
/tl clean 30
```

## Visual Indicators:

The ledger uses visual indicators for quick scanning:
- 🟢 **Generated** - Ready to start
- 🔵 **In Progress** - Active development
- ✅ **Completed** - All tasks done
- 🔴 **Blocked** - Waiting on something
- 🟡 **Partial** - Some progress made

## Benefits:

1. **Never lose track** of any generated tasks
2. **See progress** across all features at a glance
3. **Identify blockers** quickly
4. **Plan sprints** with accurate task counts
5. **Track velocity** over time
