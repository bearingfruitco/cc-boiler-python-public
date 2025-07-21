# Commit Control Guide - Managing When and How Code Gets Committed

## Current System Behavior

Good news! The system already has **auto-commit disabled** by default. Here's what actually happens:

### What Gets Auto-Saved (Every 60 seconds)
- **Work state** → GitHub Gists (private/secret)
- **Context** → Local checkpoint files
- **Metrics** → Local tracking files

### What Does NOT Get Auto-Committed
- ❌ No automatic `git commit`
- ❌ No automatic `git push`
- ❌ No changes to your main codebase without your approval

## Nikki's Control Options

### 1. **Manual Commit Only (Current Default)**
```json
// .claude/hooks/config.json
"github": {
  "auto_commit": false,  // Already set!
  "commit_threshold": 5,  // Ignored when auto_commit is false
  ...
}
```

### 2. **Disable All Auto-Saves (Nuclear Option)**
If you want to disable even the gist saves:
```bash
# Edit .claude/hooks/config.json
"post-tool-use": [
  {
    "script": "01-state-save.py",
    "enabled": false,  // Change to false
    ...
  }
]
```

### 3. **Custom Commit Workflow**
Create your own commit command:

```bash
# Create custom command: .claude/commands/safe-commit.md
---
name: safe-commit
aliases: ["sc", "commit-safe"]
description: Review changes before committing
---

# Safe Commit Command

Shows all changes and asks for confirmation before committing.

## Usage
```
/safe-commit [message]
/sc "Added new feature"
```

## Implementation
1. Show git diff
2. List all changed files
3. Ask for confirmation
4. Only commit if confirmed
```

### 4. **Task-Based Commits (Recommended)**
Instead of auto-commits, use task checkpoints:

```bash
# After completing a task
/task-checkpoint  # Saves state but doesn't commit

# When ready to commit multiple tasks
/commit-tasks "Completed user auth tasks 1-3"
```

## Recommended Settings for Nikki

Add this to your personal config:

```bash
# Create .claude/team/nikki-config.json
{
  "commit_preferences": {
    "auto_commit": false,
    "require_confirmation": true,
    "default_branch": "feature/nikki-work",
    "commit_style": "conventional",
    "push_after_commit": false
  },
  "save_preferences": {
    "gist_saves": true,
    "gist_visibility": "secret",
    "checkpoint_interval": 300  // 5 minutes
  }
}
```

## Commit Safety Commands

### Check Before Committing
```bash
/git-status      # See what would be committed
/diff-check      # Review all changes
/lint-check      # Ensure code quality
```

### Selective Commits
```bash
/stage-files components/Button.tsx lib/utils.ts
/commit-staged "feat: Add Button component"
```

### Undo Options
```bash
/undo-last       # Undo last file change
/reset-soft      # Undo last commit (keep changes)
/reset-hard      # Nuclear option - lose all changes
```

## Best Practices for Team Commits

1. **Use Feature Branches**
   ```bash
   /fw start 42  # Creates feature/issue-42 branch
   # Work happens here
   /fw complete 42  # Creates PR, no direct commit to main
   ```

2. **Commit Messages**
   - Use conventional commits: `feat:`, `fix:`, `docs:`
   - Reference issues: `feat: Add auth (#42)`
   - Be descriptive: what and why

3. **Review Process**
   - Work on feature branches
   - Create PRs for review
   - Never commit directly to main
   - Use `/pp` (pre-PR) command to validate

## Emergency Controls

If you ever see unwanted commits happening:

1. **Immediate Stop**
   ```bash
   # In terminal
   touch .claude/.no-commits
   ```

2. **Disable Hook**
   ```bash
   chmod -x .claude/hooks/post-tool-use/01-state-save.py
   ```

3. **Report Issue**
   ```bash
   /report-issue "Unwanted auto-commits happening"
   ```

## Summary for Nikki

✅ **You're already protected** - auto-commit is OFF by default
✅ **Gist saves** - These are just backups, not commits
✅ **Full control** - You decide when to commit
✅ **Feature branches** - Work safely without affecting main

The "every 3 tasks" mention in docs was aspirational, not implemented. The system respects your control over commits!

---

💡 **Pro tip**: Use `/checkpoint` frequently to save your work state without committing. This gives you all the benefits of not losing work without the commitment of a git commit.
