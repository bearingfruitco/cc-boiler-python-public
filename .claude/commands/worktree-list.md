---
name: worktree-list
aliases: [wt-list, wtl]
description: List all active git worktrees
category: orchestration
---

# Worktree List

Display all active git worktrees in the project.

## Usage

```bash
# List all worktrees
/worktree-list

# List with details
/wt-list --detailed

# Show as tree
/wtl --tree
```

## Output Format

```
🌳 Git Worktrees:

main (current)
├── /Users/you/project
└── Branch: main

auth-feature
├── /Users/you/project/../worktrees/auth-feature
└── Branch: feature/auth-feature

payment-feature
├── /Users/you/project/../worktrees/payment-feature
└── Branch: feature/payment-feature
```

## Integration Points

- Reads git worktree list
- Checks for Claude configuration in each
- Shows task from worktree config
- Indicates merge readiness

## Options

- `--detailed` - Include task info and status
- `--tree` - Tree view format
- `--json` - JSON output
- `--paths-only` - Just show paths
