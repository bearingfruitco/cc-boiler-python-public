# Claude Code Context Structure

## Overview
This document defines how context should be structured and maintained across all Claude Code commands.

## Context File Location
```
.claude/
  context/
    current.md       # Active working context
    history/         # Historical contexts
    templates/       # Context templates
```

## Context Sections

### 1. Identity Block (Always First)
```markdown
# Working Context
Project: [Project Name]
Type: [Project Type]
Last Updated: [Timestamp]
```

### 2. Current Work Block
```markdown
## 🎯 Current Focus
Issue: #[Number] - [Title]
Branch: [Branch Name]
Progress: [Percentage]%
Location: [File:Line]
```

### 3. File State Block
```markdown
## 📁 Active Files
### Modified (Uncommitted)
- [List of files]

### Recently Edited
- [Last 10 files with timestamps]
```

### 4. TODO Block
```markdown
## 📋 Active TODOs
### Current File
- [ ] TODO at line X: Description

### Project Wide
- [ ] High Priority TODOs
```

### 5. Design Compliance Block
```markdown
## 🎨 Design System Status
Last Check: [Timestamp]
Status: [✅ Compliant | ❌ Violations]
Details: [Summary]
```

### 6. Quick Commands Block
```markdown
## 💡 Quick Commands
Based on current context:
- Next: `[Most relevant command]`
- Check: `/validate-design`
- Resume: `/context-grab restore`
```

### 7. References Block
```markdown
## 🔗 References
- Feature Spec: [Path or Issue Link]
- Design Guide: docs/design/design-system.md
- Related PRs: [Links]
- Documentation: [Relevant docs]
```

## Context Update Rules

### When to Update Context

1. **Automatic Updates**
   - On every command completion
   - On file saves (VS Code integration)
   - On git commits
   - Every 30 minutes during active work

2. **Command-Specific Updates**
   - `/create-component` - Add to Active Files
   - `/validate-design` - Update Design Compliance
   - `/todo add` - Update TODO Block
   - `/checkpoint` - Full context capture
   - `/feature-workflow` - Update Current Work

### What to Include

1. **Always Include**
   - Timestamp
   - Command that updated
   - Current branch/issue
   - File being edited

2. **Conditionally Include**
   - Error states
   - Validation results
   - Test results
   - Performance metrics

## Context Templates

### New Feature Template
```markdown
# Working Context - New Feature
Project: [Name]
Feature: #[Issue] - [Title]
Started: [Timestamp]

## 🎯 Current Focus
Setting up feature structure

## 📋 Feature Checklist
- [ ] Create branch
- [ ] Setup components
- [ ] Add tests
- [ ] Update docs
```

### Bug Fix Template
```markdown
# Working Context - Bug Fix
Project: [Name]
Bug: #[Issue] - [Title]
Started: [Timestamp]

## 🐛 Bug Details
Reproduction: [Steps]
Expected: [Behavior]
Actual: [Behavior]

## 🔍 Investigation
- [ ] Reproduce locally
- [ ] Identify root cause
- [ ] Write test
- [ ] Implement fix
```

## Integration Examples

### In create-component command:
```bash
# After creating component
echo "## Component Created
- Name: $COMPONENT_NAME
- Path: $COMPONENT_PATH
- Type: $COMPONENT_TYPE
- Design: ✅ Compliant
" >> .claude/context/current.md
```

### In validate-design command:
```bash
# After validation
echo "## Design Validation
- Time: $(date '+%H:%M')
- Result: $VALIDATION_RESULT
- Components: $COMPONENTS_CHECKED
- Violations: $VIOLATIONS_FOUND
" >> .claude/context/current.md
```

### In feature-workflow command:
```bash
# When starting feature
echo "## Feature Started
- Issue: #$ISSUE_NUMBER
- Title: $ISSUE_TITLE
- Branch: $BRANCH_NAME
- Worktree: $WORKTREE_PATH
" >> .claude/context/current.md
```

## Context Queries

Commands should be able to query context:

```bash
# Get current issue
current_issue() {
  grep "Issue: #" .claude/context/current.md | head -1 | grep -oE '[0-9]+'
}

# Get current file
current_file() {
  grep "Location:" .claude/context/current.md | head -1 | cut -d: -f2
}

# Get progress
current_progress() {
  grep "Progress:" .claude/context/current.md | head -1 | grep -oE '[0-9]+'
}
```

## Benefits

1. **Single Source of Truth** - One file to check
2. **Chronological History** - See work progression
3. **Quick Restoration** - Everything in one place
4. **Command Integration** - All commands contribute
5. **Human Readable** - Easy to scan and understand
