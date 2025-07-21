# Claude Code Hooks for Multi-Agent Collaboration

## Overview

This hooks system enables seamless collaboration between multiple developers using separate Claude Code agents on the same codebase. It provides:

- **Automatic GitHub synchronization** to prevent conflicts
- **Design system enforcement** that blocks violations before they're written
- **Work state persistence** to GitHub gists for handoffs
- **Team awareness** showing who's working on what
- **Knowledge sharing** to build collective intelligence

## Installation

```bash
cd /path/to/your/project
./.claude/scripts/install-hooks.sh
```

Follow the prompts to set your username (shawn/nikki).

## Hook Types

### 1. Pre-Tool-Use Hooks (Before File Operations)

#### 01-collab-sync.py
- **Purpose**: Sync with GitHub before any file operation
- **Actions**: 
  - Auto-pulls latest changes
  - Detects conflicts with remote
  - Warns if files were recently modified by others

#### 02-design-check.py
- **Purpose**: Enforce design system rules
- **Actions**:
  - Blocks forbidden font sizes (only text-size-[1-4])
  - Blocks forbidden font weights (only font-regular/semibold)
  - Blocks non-4px grid spacing
  - Offers auto-fix suggestions

#### 03-conflict-check.py
- **Purpose**: Check for team conflicts
- **Actions**:
  - Tracks who's editing what files
  - Warns about potential conflicts
  - Registers your file activity

#### 04-actually-works.py (NEW)
- **Purpose**: Enforce the "Actually Works" protocol
- **Actions**:
  - Detects untested claims ("should work", "fixed")
  - Requires actual testing before claiming success
  - Shows 30-second reality checklist

#### 05-code-quality.py (NEW)
- **Purpose**: Enforce code quality standards
- **Actions**:
  - Warns about console.logs in production
  - Tracks TODO comments
  - Blocks 'any' types in TypeScript
  - Checks complexity and suggests refactoring

### 2. Post-Tool-Use Hooks (After File Operations)

#### 01-state-save.py
- **Purpose**: Auto-save work state to GitHub
- **Actions**:
  - Saves to GitHub gist every 60 seconds
  - Updates PR descriptions with state
  - Enables seamless handoffs

#### 02-metrics.py
- **Purpose**: Track design compliance
- **Actions**:
  - Counts violations by type
  - Tracks compliance rate
  - Generates insights

#### 03-pattern-learning.py (NEW)
- **Purpose**: Learn from successful code patterns
- **Actions**:
  - Extracts reusable patterns from code
  - Builds library of successful solutions
  - Suggests similar patterns when coding
  - Tracks most-used patterns

### 3. Notification Hooks (When Input Needed)

#### team-aware.py
- **Purpose**: Show team activity
- **Actions**:
  - Shows who's working on what
  - Suggests coordination commands
  - Warns about conflicts

#### smart-suggest.py
- **Purpose**: Context-aware suggestions
- **Actions**:
  - Suggests relevant commands
  - Time-based recommendations
  - Work-stage awareness

### 4. Stop Hooks (Session End)

#### save-state.py
- **Purpose**: Final state save
- **Actions**:
  - Session summary
  - GitHub gist backup
  - Daily activity log

#### knowledge-share.py
- **Purpose**: Extract learnings
- **Actions**:
  - Captures reusable patterns
  - Updates team knowledge base
  - Creates GitHub discussions

## Usage

### For Shawn

1. Set your user in team config:
```json
{
  "current_user": "shawn"
}
```

2. Start working normally - hooks run automatically
3. See Nikki's work: `/team-status`
4. Sync before major changes: `/collab-sync nikki`

### For Nikki

1. Clone the repo with hooks already installed
2. Change team config to your name:
```bash
echo '{"current_user": "nikki"}' > .claude/team/config.json
```

3. Work normally - you'll see Shawn's activity
4. Handoffs happen automatically via GitHub

## Commands Enhanced by Hooks

### Existing Commands Get Smarter

- `/cc` - Now validates design system before creating
- `/vd` - Uses metrics from all sessions
- `/checkpoint` - Auto-saves to GitHub
- `/compact-prepare` - Includes team state

### New Team Commands

```bash
/team-status          # See all team activity
/collab-sync [user]   # Sync with specific person
/handoff prepare      # Prepare work for handoff
/handoff receive      # Receive handoff package
```

## Typical Workflow

### Morning Start
```bash
# Shawn starts work
/sr                    # Hooks show Nikki worked last night
/collab-sync nikki     # Pull her changes
/work-status           # See what needs doing
```

### During Development
```
# Create component - design hook validates
/cc ui Button

# If violation detected:
> "DESIGN VIOLATION: text-sm detected. Use text-size-4"
> Auto-fix available. Accept? (y/n)

# Team awareness:
> "📝 NOTE: nikki edited this file 23m ago"
```

### Before Break
```
# Auto-saves every 60 seconds
# But can force save:
/checkpoint create lunch

# State saved to GitHub gist
# Nikki can pick up exactly where you left off
```

### Handoff Process
```
# Automatic via hooks:
- Work state saved to gist
- PR description updated
- Team registry updated
- Knowledge base updated

# Nikki sees:
/sr
> "Shawn last worked on auth-component (2h ago)"
> "70% complete, next: Add error states"
> Resume with: /compact-prepare resume 23
```

## Configuration

### Hook Config (.claude/hooks/config.json)
```json
{
  "team": {
    "members": ["shawn", "nikki"],
    "sync_interval": 300,          // Sync every 5 minutes
    "auto_pull": true,
    "conflict_strategy": "prompt"
  },
  "github": {
    "gist_visibility": "secret",    // Keep work private
    "use_worktrees": true
  },
  "design_system": {
    "enforce": true,
    "auto_fix": true
  }
}
```

### Disable Specific Hooks
Edit `.claude/settings.json` and set `enabled: false` for any hook.

## Troubleshooting

### Hooks Not Running
1. Restart Claude Code
2. Check Python 3 is installed
3. Verify `.claude/settings.json` has hooks section

### Sync Conflicts
```bash
# Manual sync
git pull --rebase origin $(git branch --show-current)

# Reset team registry
echo '{"active_work": {}}' > .claude/team/registry.json
```

### Design Violations Not Caught
- Check file extension is .tsx or .jsx
- Verify hook is enabled in settings
- Run test: `python3 .claude/scripts/test-hooks.py`

## Uninstalling

```bash
./.claude/scripts/uninstall-hooks.sh
```

This removes hook configuration but preserves hook files.

## Benefits

1. **No More Conflicts**: Auto-sync prevents overwrites
2. **Consistent Design**: Violations blocked before commit
3. **Perfect Handoffs**: State transfers seamlessly
4. **Shared Learning**: Patterns propagate to both users
5. **Async Collaboration**: Work different hours smoothly
6. **GitHub Backup**: Everything saved and versioned

## Advanced Features

### Custom Hooks
Add your own hooks:
1. Create script in appropriate hook directory
2. Add to `.claude/settings.json`
3. Follow input/output format

### Hook Chaining
Hooks run in filename order:
- 01-first.py
- 02-second.py
- 03-third.py

### Conditional Hooks
Use matchers to run hooks only for certain files:
```json
{
  "matcher": {"path_pattern": "*.tsx"},
  "commands": ["python3 .claude/hooks/my-hook.py"]
}
```

## Summary

This hook system transforms two separate Claude Code instances into a coordinated development team. Work is automatically synchronized, design rules are enforced, and knowledge is shared - all without manual intervention.

Happy collaborative coding! 🚀
