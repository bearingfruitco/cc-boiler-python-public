# Context Grab

Capture and restore complete working context in a single command.

## Arguments:
- $ACTION: capture|restore|auto
- $DETAIL: minimal|standard|full

## Why This Command:
- Single source of truth for current context
- Automatic context capture at key points
- Quick restoration after compaction
- No need to run multiple commands

## Steps:

### Action: CAPTURE
Creates a comprehensive context snapshot:

```bash
# Create context directory if needed
mkdir -p .claude/context

# Generate timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Capture all context
cat > .claude/context/current.md << EOF
# Working Context - ${TIMESTAMP}

## 🎯 Current Focus
$(git branch --show-current | sed 's/feature\//Issue #/')
$(git log -1 --pretty=format:"Last commit: %s (%cr)")

## 📁 Active Files
### Modified (Uncommitted)
$(git status --porcelain | grep "^ M" | cut -c4-)

### Recently Changed
$(git log --name-only --pretty=format: -n 5 | sort | uniq | grep -v '^$' | head -10)

## 🎨 Design Compliance
$(npm run validate:design --silent 2>&1 | tail -5)

## 📋 Active TODOs
$(grep -r "TODO:" --include="*.tsx" --include="*.ts" . | head -10)

## 🔗 Related Documentation
- Feature Spec: $(find docs -name "*$(git branch --show-current | grep -oE '[0-9]+')*.md" 2>/dev/null | head -1)
- Design Guide: docs/design/design-system.md
- API Routes: $(find app/api -name "*.ts" -mtime -7 | head -5)

## 💡 Quick Commands
- Resume work: \`/context-grab restore\`
- Check TODOs: \`/todo list\`
- Validate design: \`/validate-design\`
- View issues: \`/issue-kanban\`

## 🔄 Work State
$(cat .claude/work-state.json 2>/dev/null || echo "{}")
EOF

echo "✅ Context captured to .claude/context/current.md"
```

### Action: RESTORE
Quickly restore context:

```bash
# Check for context file
if [ ! -f .claude/context/current.md ]; then
  echo "❌ No context found. Run: /context-grab capture"
  exit 1
fi

# Display context
cat .claude/context/current.md

# Also show any checkpoints
echo -e "\n## 📌 Available Checkpoints"
ls -la .claude/checkpoints/*.md 2>/dev/null | tail -5

# Check for work state in gists
ISSUE=$(git branch --show-current | grep -oE '[0-9]+')
if [ ! -z "$ISSUE" ]; then
  echo -e "\n## 🌐 Remote State"
  echo "To restore full state: /compact-prepare resume $ISSUE"
fi
```

### Action: AUTO
Set up automatic context capture:

```bash
# Add git hooks
cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash
/claude-code /context-grab capture minimal
EOF

chmod +x .git/hooks/post-commit

# Add to VS Code tasks
cat > .vscode/tasks.json << 'EOF'
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Capture Context",
      "type": "shell",
      "command": "/claude-code /context-grab capture",
      "runOptions": {
        "runOn": "folderOpen"
      }
    }
  ]
}
EOF
```

## Context Levels:

### MINIMAL
Just the essentials:
```markdown
# Quick Context
Branch: feature/23-auth
Files: 3 modified
TODOs: 5 remaining
Design: ✅ Compliant
Resume: /compact-prepare resume 23
```

### STANDARD (default)
Full working context as shown above

### FULL
Everything including:
- Full git history (last 20 commits)
- All TODO/FIXME comments
- Test coverage report
- Performance metrics
- Dependency tree changes

## Integration with Other Commands:

Update existing commands to use context:

```bash
# In /checkpoint create
/context-grab capture standard
git add .claude/context/current.md
git commit -m "checkpoint: capture context"

# In /compact-prepare
/context-grab capture full
# Include in gist upload

# In /feature-workflow start
/context-grab capture minimal
# Start fresh context for new feature
```

## Smart Context Detection:

```bash
# On Claude Code startup
if [ -f .claude/context/current.md ]; then
  CONTEXT_AGE=$(find .claude/context/current.md -mmin +60 | wc -l)
  if [ $CONTEXT_AGE -gt 0 ]; then
    echo "⚠️  Context is over 1 hour old"
    echo "Run: /context-grab capture"
  else
    echo "✅ Recent context found"
    echo "Run: /context-grab restore"
  fi
fi
```

## Context File Includes:

1. **Current Work**
   - Branch and issue number
   - Modified files
   - Recent commits

2. **Project State**
   - Design validation status
   - Test results
   - Build status

3. **Navigation**
   - Related documentation
   - Active API routes
   - Component locations

4. **Quick Actions**
   - Relevant commands
   - Next steps
   - Resume instructions

## Example Usage:

```bash
# Starting work
/context-grab restore
> Shows complete context
> Ready to continue where you left off

# Before break
/context-grab capture
> Saves current state
> Can resume anytime

# After compaction
/context-grab restore
> Instantly back in context
> No need to remember details

# Automatic mode
/context-grab auto
> Captures on every commit
> Opens with context ready
```

This creates a single, reliable source of context that's always up-to-date!
