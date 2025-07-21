---
name: work-status
aliases: [ws, status]
description: Show comprehensive work status including task ledger
category: workflow
---

Show comprehensive work status including:
- Current branch and changes
- Task ledger summary
- Active features and progress
- Recent completions
- Blockers and priorities

## Enhanced Output Format:

```markdown
# Work Status

## Current Context
- **Branch**: feature/23-user-auth
- **Working on**: User Authentication
- **Session Duration**: 1h 23m
- **Last Checkpoint**: 15 minutes ago

## 📋 Task Ledger Summary
### Active Tasks (3)
1. **user-authentication** 🔵 In Progress
   - Progress: ████████░░ 80% (8/10 tasks)
   - Issue: #23
   - Time Today: 1h 15m
   
2. **data-pipeline** 🟢 Generated
   - Progress: ░░░░░░░░░░ 0% (0/8 tasks)
   - Issue: Not linked
   - Ready to start

3. **api-refactor** 🔴 Blocked
   - Progress: ███░░░░░░░ 30% (3/10 tasks)
   - Issue: #19
   - Blocked by: #15

### Recently Completed ✅
- **bug-fix-login** - Completed 2 hours ago
- **performance-opt** - Completed yesterday

## Git Status
### Modified Files (3)
- src/auth/login.py (implementing authentication)
- tests/test_auth.py (adding test cases)
- docs/auth.md (updating documentation)

### Uncommitted Changes
```diff
+ def authenticate_user(email: str, password: str):
+     """Authenticate user with email and password."""
+     # Implementation here
```

## Test Status 🧪
- **Current Feature Tests**: 6/8 passing
- **Overall Coverage**: 84%
- **Last Test Run**: 5 minutes ago

## Next Steps
Based on your progress:
1. Complete remaining 2 tasks for user-authentication
2. Run `/pt user-authentication` to see specific tasks
3. Consider starting data-pipeline next (0% complete)

## Blockage Alert 🚨
- **api-refactor** blocked by issue #15
- Consider addressing blocker or switching focus

## Command Suggestions
- `/pt user-authentication` - Continue current feature
- `/tl` - View detailed task ledger
- `/test` - Run tests for current changes
- `/checkpoint` - Save current progress
```

## Data Sources:

The command aggregates information from:
1. `.task-ledger.md` - Central task tracking
2. Git status - Current changes
3. Test results - Latest test runs
4. `.claude/context/state.json` - Session information
5. GitHub API - Issue status

## Options:

```bash
# Basic status
/ws

# Verbose with more details
/ws -v

# Focus on specific feature
/ws user-authentication

# Show only blockers
/ws --blockers
```

## Integration:

This enhanced work status helps with:
- **Daily standups** - Clear view of progress
- **Context switching** - Know exactly where you are
- **Planning** - See what needs attention
- **Handoffs** - Complete picture for next developer
