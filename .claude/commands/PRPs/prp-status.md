---
name: prp-status
aliases: [prp-track, prp-progress]
description: Track PRP execution progress
category: PRPs
---

# PRP Status: $ARGUMENTS

## Check PRP Progress

### 1. Locate PRP
```bash
# Active PRPs
ls PRPs/active/ | grep $ARGUMENTS

# Completed PRPs
ls PRPs/completed/ | grep $ARGUMENTS
```

### 2. Execution Logs
```bash
# Latest execution
ls -lt PRPs/execution_logs/$ARGUMENTS* | head -1

# All executions
ls PRPs/execution_logs/$ARGUMENTS*
```

### 3. Progress Tracking
- Task completion percentage
- Validation levels passed
- Current blockers
- Time elapsed

### 4. Validation Status
```yaml
Level 1 - Syntax: ✅ Passed
Level 2 - Unit Tests: ✅ Passed
Level 3 - Integration: 🔄 In Progress
Level 4 - Security: ⏸️ Pending
```

### 5. Dependencies Impact
```bash
/pydeps check $ARGUMENTS
```

### 6. Related Issues
```bash
# GitHub issues
gh issue list --search "$ARGUMENTS"

# Captured responses
ls .claude/captures/ | grep $ARGUMENTS
```

## Output Format
```
╔══════════════════════════════════════════════════════════╗
║ PRP STATUS: $ARGUMENTS                                   ║
╠══════════════════════════════════════════════════════════╣
║ State: Active                                            ║
║ Progress: 65%                                            ║
║ Started: 2024-01-15 10:30                               ║
║ Confidence: 8/10                                         ║
╠══════════════════════════════════════════════════════════╣
║ Tasks:                                                   ║
║ [✅] Create models                                       ║
║ [✅] Implement service layer                             ║
║ [🔄] Add API endpoints                                   ║
║ [⏸️] Write tests                                         ║
║ [⏸️] Security validation                                 ║
╠══════════════════════════════════════════════════════════╣
║ Validation:                                              ║
║ Level 1: ✅ | Level 2: ✅ | Level 3: 🔄 | Level 4: ⏸️  ║
╚══════════════════════════════════════════════════════════╝
```
