# Resume Command

One-command work resumption - automatically finds and restores your work context.

## Arguments:
- $QUERY: Optional search term (e.g., "auth", "dashboard") or issue number
- If no argument: resumes last worked issue

## Why This Command:
- Single command to get back to work
- No need to remember issue numbers
- Combines work-status + compact-prepare
- The fastest way to resume

## Steps:

### No Arguments: Resume Last Work
```bash
# Called as: /resume
```

1. **Find Last Work**
   ```bash
   # Check current branch first
   BRANCH=$(git branch --show-current)
   ISSUE=$(echo $BRANCH | grep -oE '[0-9]+' | head -1)
   
   if [ -z "$ISSUE" ]; then
     # Get from master status gist
     LAST_ISSUE=$(gh gist view work-status-master.json | jq -r '.lastWorked.issue')
     
     if [ -z "$LAST_ISSUE" ]; then
       # Fallback to most recent gist
       LATEST=$(gh gist list --limit 10 | grep "Work state" | head -1)
       GIST_ID=$(echo $LATEST | awk '{print $1}')
       ISSUE=$(echo $LATEST | grep -oE '#[0-9]+' | tr -d '#')
     fi
   fi
   ```

2. **Show What's Being Resumed**
   ```markdown
   ## 🔄 Resuming Last Work
   
   Found: Issue #23 - Add authentication components
   Last worked: 2 hours ago
   Progress: 70%
   
   Loading work state...
   ```

3. **Execute Resume**
   ```bash
   # Call compact-prepare resume
   /compact-prepare resume $ISSUE
   ```

### With Search Query: Find and Resume
```bash
# Called as: /resume auth
# Or: /resume dashboard
```

1. **Search for Matching Work**
   ```bash
   QUERY="$1"
   
   # If it's a number, treat as issue number
   if [[ "$QUERY" =~ ^[0-9]+$ ]]; then
     ISSUE=$QUERY
   else
     # Search in issues
     FOUND=$(gh issue list --assignee @me --state open --search "$QUERY" \
       --json number,title --limit 1)
     
     if [ -z "$FOUND" ]; then
       # Search in gist descriptions
       FOUND=$(gh gist list | grep -i "$QUERY" | head -1)
       ISSUE=$(echo $FOUND | grep -oE '#[0-9]+' | tr -d '#')
     else
       ISSUE=$(echo $FOUND | jq -r '.[0].number')
     fi
   fi
   ```

2. **Confirm Match**
   ```markdown
   ## 🔍 Search: "auth"
   
   Found: Issue #23 - Add authentication components
   Progress: 70%
   
   Resuming...
   ```

3. **Execute Resume**
   ```bash
   /compact-prepare resume $ISSUE
   ```

### Smart Workspace Handling
```bash
# Check if worktree exists
WORKTREE_EXISTS=$(git worktree list | grep -c "feature/$ISSUE")

if [ "$WORKTREE_EXISTS" -eq 0 ]; then
  echo "📁 Creating worktree for issue #$ISSUE..."
  /worktree create feature-$ISSUE
else
  echo "📁 Worktree exists, switching..."
  /worktree switch feature-$ISSUE
fi
```

### Complete Resume Output
```markdown
## ✅ Resumed: Issue #23 - Authentication Components

### You Were Here:
- File: `components/auth/LoginForm.tsx`
- Line: 145
- Task: Adding network error handling

### Progress: 70% Complete
✅ Completed (7/10):
- Created login form
- Added validation
- TypeScript types
- Unit test setup

🚧 Current Task:
- Network error handling (line 145)

📋 Remaining (3):
- Loading states
- Integration tests
- Documentation

### Next Steps:
1. Continue at LoginForm.tsx:145
2. Add try-catch for network errors
3. Run `/validate-design` when done

### Quick Commands:
- See TODOs: `/todo-tracking list`
- Check design: `/validate-design`
- Save progress: `/compact-prepare prepare`
```

## Error Handling

### No Work Found
```markdown
## ❌ No Active Work Found

Try one of these:
- `/work-status list` - See all work
- `/issue-kanban board` - View project
- `/feature-workflow start [issue]` - Start new work
```

### Multiple Matches
```markdown
## 🤔 Multiple Matches for "auth"

1. Issue #23: Add authentication components (70%)
2. Issue #31: Fix auth token refresh (20%)
3. Issue #45: Auth documentation (0%)

Please be more specific or use issue number:
- `/resume 23`
- `/resume "authentication components"`
```

## Integration with Terminal

Add to `.zshrc` for even faster access:
```bash
# Quick resume alias
alias r="claude /resume"
alias rl="claude /resume"  # resume last
alias rf="claude /resume"  # with search
```

Now just type:
```bash
$ r
# Resumes last work

$ r auth
# Resumes auth feature

$ r 23
# Resumes issue #23
```

## Complete Workflow Examples

### Monday Morning
```bash
$ /resume
> "Resuming Issue #23: Auth (70%)"
> "You were at: LoginForm.tsx:145"
> "Continue adding error handling"
```

### After Lunch
```bash
$ /resume
> "Still on Issue #23"
> "No state changes needed"
> "Continue at LoginForm.tsx:145"
```

### Switching Features
```bash
$ /resume dashboard
> "Found Issue #24: Dashboard Layout"
> "Creating worktree..."
> "Progress: 30%"
> "Start at: Dashboard.tsx:78"
```

### Can't Remember Anything
```bash
$ /resume
> "No recent work in current branch"
> "Last work: Issue #23 (2 days ago)"
> "Resuming..."
```

## Why This Is The Perfect Command

1. **One Command** - Don't need to remember two commands
2. **Smart Search** - Finds work by number, keyword, or recency
3. **Context Aware** - Checks current branch first
4. **Workspace Ready** - Creates/switches worktrees automatically
5. **Complete State** - Shows everything you need to continue

This is now your primary command for getting back to work!
