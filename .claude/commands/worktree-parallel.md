---
name: worktree-parallel
aliases: [wt, worktree, wt-parallel]
description: Execute tasks in isolated git worktrees for true parallel agent execution
category: orchestration
---

# Worktree Parallel Execution

Execute multiple tasks in completely isolated git worktrees, preventing file conflicts and enabling true parallel development.

## Usage

```bash
# Basic usage - creates worktrees for each feature
/worktree-parallel auth-feature payment-feature ui-refactor

# With task assignment
/wt --tasks "implement auth" "add payment processing" "refactor dashboard"

# Integrated with existing orchestration
/wt-orchestrate "build three features" --from-prd

# From task ledger
/wt --from-task-ledger auth-tasks payment-tasks
```

## Options

- `--tasks` - Specify task for each worktree
- `--from-prd` - Generate worktrees from PRD tasks
- `--from-task-ledger` - Use tasks from task ledger
- `--no-merge` - Don't auto-merge when complete
- `--base` - Base branch (default: main)
- `--monitor` - Open monitoring in new terminal tabs

## How It Works

1. **Setup Phase**
   ```bash
   # For each task, creates:
   git worktree add -b feature/[name] ../worktrees/[name] main
   ```

2. **Execution Phase**
   - Each worktree gets own Claude Code instance
   - Agents work in complete isolation
   - No file conflicts possible

3. **Merge Phase**
   - Reviews changes in each worktree
   - Creates PRs or merges to base
   - Cleans up worktrees

## Integration with Existing System

### With Orchestration
```bash
# Old way (shared filesystem)
/orchestrate-agents "implement auth, payment, and UI"

# New way (isolated filesystems)  
/wt-orchestrate "implement auth, payment, and UI"
```

### With PRD Workflow
```bash
# Generate PRD
/prd "multi-feature system"

# Generate tasks
/gt multi-feature

# Execute in parallel worktrees
/wt --from-tasks
```

### With Task Ledger
```bash
# View task ledger
/tl view

# Create worktrees from specific features
/wt --from-task-ledger auth-feature payment-feature
```

## Example Workflow

```bash
# 1. Create PRD for multiple features
/prd "user management system with auth, profile, and settings"

# 2. Generate tasks
/gt user-management

# 3. Execute in parallel worktrees
/wt auth profile settings \
    --tasks "implement authentication" \
            "create profile management" \
            "build settings page"

# 4. Monitor progress
/wt-status

# 5. Review and merge
/wt-review auth
/wt-merge auth --run-tests
```

## Worktree Management Commands

```bash
/wt-list          # List active worktrees
/wt-status        # Show status of all worktrees  
/wt-review [name] # Review changes in worktree
/wt-merge [name]  # Merge worktree to base
/wt-clean         # Remove completed worktrees
/wt-switch [name] # Switch to worktree directory
/wt-monitor       # Open monitoring dashboard
```

## Integration with Existing Hooks

All existing hooks run normally in each worktree:
- Design validation per worktree
- TDD enforcement per worktree  
- Import validation per worktree
- Python dependency tracking per worktree
- Metrics tracked separately
- Task ledger updates per worktree

## Automatic Safety Features

1. **Branch Protection**: Won't create if branch exists
2. **Conflict Detection**: Pre-checks for merge conflicts
3. **State Preservation**: Each worktree maintains own `.claude/context`
4. **Validation Gates**: Must pass all checks before merge
5. **Hook Compatibility**: All Python hooks run in each worktree

## Benefits Over Standard Parallel

1. **True Isolation**: No file conflicts
2. **Independent Branches**: Each feature on own branch
3. **Parallel Testing**: Run tests simultaneously
4. **Easy Rollback**: Just remove worktree
5. **Clean History**: Separate commit streams

## Best Practices

1. **One Feature Per Worktree**: Keep changes focused
2. **Clear Naming**: Use descriptive worktree names
3. **Regular Syncing**: Pull main changes into worktrees
4. **Clean Up**: Remove worktrees after merging
5. **Monitor Progress**: Use `/wt-status` regularly

## Notes

- Requires git 2.5+
- Disk space: Each worktree is full checkout
- Memory: Each Claude instance separate
- Best for 2-5 parallel tasks
- Integrates with existing Task Ledger system
