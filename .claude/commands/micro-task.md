# Micro Task - Quick Task Creation

## Command: micro-task
**Aliases:** `mt`, `quick-task`, `tiny`

## Description
Creates micro-tasks (< 5 minutes) for immediate execution. Complements the PRD task system by handling small, atomic changes that don't need full task tracking.

## Usage
```bash
/micro-task "Add loading spinner to submit button"
/mt "Fix typo in header" --no-test
/quick-task "Update color to blue-600" --component Button
```

## Options
- `--component [name]` - Specify component for focused work
- `--no-test` - Skip testing for trivial changes
- `--chain` - Chain multiple micro-tasks
- `--convert` - Convert to full task if grows beyond 5 min

## Task Hierarchy

```
PRD Level (Strategic)
└── Generated Tasks (5-15 min)
    └── Micro Tasks (< 5 min)  ← You are here
```

## When to Use Micro Tasks

### Perfect For:
- Typo fixes
- Color/style adjustments
- Adding simple props
- Updating text content
- Adding console.logs for debugging
- Simple validation rules
- Minor refactors

### Use Regular Tasks For:
- New components
- API changes
- Business logic
- Database modifications
- Complex debugging
- Feature additions

## Examples

### Simple UI Fix
```bash
/mt "Change button text from 'Submit' to 'Save Changes'"
# Direct 1-line change, auto-verified
```

### Quick Style Update
```bash
/micro-task "Add hover state to card component" --component Card
# Adds transition, updates className
```

### Debugging Addition
```bash
/mt "Add console.log to track form submission values"
# Temporary addition for debugging
```

### Chained Micro Tasks
```bash
/micro-task "Fix button alignment" --chain
/mt "Update padding to p-4" --chain
/mt "Center text with text-center" --chain
# Executes all three in sequence
```

## Auto-Conversion

If a micro-task exceeds 5 minutes:
1. Automatically converts to regular task
2. Updates task tracking
3. Notifies about scope creep
4. Suggests breaking into smaller pieces

## Integration with Task System

```bash
# Current task context
/ts
> Feature: User Profile
> Current: Task 3 of 8 - "Add form validation"

# Add quick fix without disrupting flow
/mt "Fix email regex pattern"
> Micro-task completed in 2 min
> Continuing with Task 3...
```

## Best Practices

1. **Keep it atomic** - One change per micro-task
2. **Be specific** - "Change color" → "Change button color to blue-600"
3. **Skip ceremony** - No PRD needed for typos
4. **Trust the hooks** - Design validation still applies
5. **Document later** - Micro-tasks auto-document in session

## Micro Task Rules

- Max 5 minutes execution time
- Single file changes preferred
- No architectural decisions
- No database migrations
- No breaking changes
- Auto-tested unless --no-test

## Tracking

Micro-tasks are:
- Logged in session history
- Included in checkpoint saves
- Summarized in handoff docs
- Not tracked as formal tasks

This keeps your main task flow clean while handling the inevitable small fixes that arise during development.
