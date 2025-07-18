# Work Status Command

Find and display your current work context without remembering issue numbers.

## Arguments:
- $ACTION: current|list|find|last
- $QUERY: Optional search term (e.g., "auth", "dashboard")

## Why This Command:
- No need to remember issue numbers
- Shows all active work
- Finds work by description
- Always know where you left off

## Steps:

### Action: CURRENT (default)
1. **Check Current Branch**
   ```bash
   # Extract issue number from current branch
   BRANCH=$(git branch --show-current)
   ISSUE_NUMBER=$(echo $BRANCH | grep -oE '[0-9]+' | head -1)
   
   if [ -z "$ISSUE_NUMBER" ]; then
     echo "❌ Not on a feature branch"
     echo "Run: /work-status list"
     exit 1
   fi
   ```

2. **Show Current Status**
   ```markdown
   ## 📍 Current Work Context
   
   Branch: feature/23-auth-components
   Issue: #23 - Add authentication components
   Progress: 70% complete
   
   ### Last Checkpoint
   - File: LoginForm.tsx:145
   - Task: Adding error handling
   - TODOs: 3 remaining
   
   ### Resume Command:
   ```
   /compact-prepare resume 23
   ```
   ```

### Action: LIST
1. **Show All Active Work**
   ```bash
   # Get all saved work states from GitHub
   echo "## 🗂️ All Active Work"
   echo ""
   
   # Check local branches first
   echo "### Local Branches:"
   git branch | grep -E "feature/|fix/" | while read branch; do
     ISSUE=$(echo $branch | grep -oE '[0-9]+')
     if [ ! -z "$ISSUE" ]; then
       TITLE=$(gh issue view $ISSUE --json title -q .title 2>/dev/null || echo "Unknown")
       echo "- Issue #$ISSUE: $TITLE"
       echo "  Branch: $branch"
     fi
   done
   
   # Check GitHub for saved states
   echo -e "\n### Saved Work States:"
   gh gist list --limit 20 | grep "Work state" | while read line; do
     GIST_ID=$(echo $line | awk '{print $1}')
     DESC=$(echo $line | cut -d' ' -f3-)
     ISSUE=$(echo $DESC | grep -oE '#[0-9]+' | tr -d '#')
     
     # Get last updated
     CONTENT=$(gh gist view $GIST_ID -f work-state-${ISSUE}.json 2>/dev/null)
     if [ ! -z "$CONTENT" ]; then
       UPDATED=$(echo $CONTENT | jq -r '.lastUpdated' 2>/dev/null || echo "Unknown")
       PROGRESS=$(echo $CONTENT | jq -r '.progress.percentage' 2>/dev/null || echo "?")
       TITLE=$(echo $CONTENT | jq -r '.title' 2>/dev/null || echo "Unknown")
       
       echo "- Issue #$ISSUE: $TITLE"
       echo "  Progress: ${PROGRESS}%"
       echo "  Updated: $UPDATED"
       echo "  Resume: /compact-prepare resume $ISSUE"
       echo ""
     fi
   done
   ```

2. **Display Results**
   ```markdown
   ## 🗂️ All Active Work
   
   ### Recent Work (Last 7 days)
   - Issue #23: Add authentication components
     Progress: 70%
     Updated: 2 hours ago
     Resume: `/compact-prepare resume 23`
   
   - Issue #24: Create dashboard layout
     Progress: 30%
     Updated: yesterday
     Resume: `/compact-prepare resume 24`
   
   - Issue #25: Fix mobile responsiveness
     Progress: 90%
     Updated: 3 days ago
     Resume: `/compact-prepare resume 25`
   
   ### Quick Actions
   - Resume last: `/work-status last`
   - Find by name: `/work-status find auth`
   ```

### Action: FIND
1. **Search by Description**
   ```bash
   # Search for work by keyword
   QUERY="$1"
   
   echo "## 🔍 Searching for: $QUERY"
   echo ""
   
   # Search issue titles
   gh issue list --assignee @me --state open --search "$QUERY" \
     --json number,title,labels | jq -r '.[] | "- Issue #\(.number): \(.title)"'
   
   # Search saved states
   gh gist list | grep -i "$QUERY" | while read line; do
     # Extract and display matching work
   done
   ```

2. **Show Matches**
   ```markdown
   ## 🔍 Search Results for "auth"
   
   Found 2 matches:
   
   1. Issue #23: Add authentication components
      Progress: 70%
      Resume: `/compact-prepare resume 23`
   
   2. Issue #31: Fix auth token refresh
      Progress: 20%
      Resume: `/compact-prepare resume 31`
   ```

### Action: LAST
1. **Find Most Recent Work**
   ```bash
   # Get the most recently updated work
   LATEST=$(gh gist list --limit 10 | grep "Work state" | head -1)
   
   if [ -z "$LATEST" ]; then
     # Fallback to current branch
     BRANCH=$(git branch --show-current)
     ISSUE=$(echo $BRANCH | grep -oE '[0-9]+')
   else
     GIST_ID=$(echo $LATEST | awk '{print $1}')
     ISSUE=$(gh gist view $GIST_ID -f *.json | jq -r '.issue')
   fi
   
   echo "## 🕒 Most Recent Work"
   echo ""
   echo "Issue #$ISSUE"
   echo "Resume with: /compact-prepare resume $ISSUE"
   ```

## Master Status Gist

Create a master status gist that tracks all work:

```json
{
  "lastUpdated": "2024-01-15T14:30:00Z",
  "currentWork": {
    "issue": 23,
    "title": "Add authentication components",
    "branch": "feature/23-auth-components"
  },
  "activeIssues": [
    {
      "issue": 23,
      "title": "Add authentication components",
      "progress": 70,
      "lastWorked": "2024-01-15T14:30:00Z"
    },
    {
      "issue": 24,
      "title": "Create dashboard layout",
      "progress": 30,
      "lastWorked": "2024-01-14T16:45:00Z"
    }
  ]
}
```

## Simplified Workflow

```bash
# Starting fresh - don't know where you were
/work-status list
> Shows all your active work with progress
> Pick one to resume

# Or find by keyword
/work-status find dashboard
> "Found: Issue #24 - Create dashboard layout"
> "Resume: /compact-prepare resume 24"

# Or just get the last thing you worked on
/work-status last
> "Last worked on: Issue #23"
> "Resume: /compact-prepare resume 23"

# Once you know the issue number
/compact-prepare resume 23
> Restores complete context
```

## Auto-Detection Integration

When you run Claude Code, it can automatically detect:

```bash
# On startup
/work-status current
> "You're on Issue #23: Auth Components"
> "70% complete, 3 TODOs remaining"

# If not on a feature branch
> "No active issue detected"
> "Run: /work-status list"
```

## Visual Status in Terminal

Add to your `.zshrc` or `.bashrc`:
```bash
# Show current issue in prompt
git_issue() {
  BRANCH=$(git branch --show-current 2>/dev/null)
  if [ ! -z "$BRANCH" ]; then
    ISSUE=$(echo $BRANCH | grep -oE '[0-9]+' | head -1)
    if [ ! -z "$ISSUE" ]; then
      echo " [#$ISSUE]"
    fi
  fi
}

# Add to prompt
PS1='...$GIT_ISSUE...'
```

Now your terminal shows:
```
~/projects/myapp (feature/23-auth) [#23] $
```

## Benefits:

1. **No Memory Required** - System finds your work
2. **Multiple Entry Points** - List, search, or last
3. **Always Visible** - In terminal prompt
4. **Quick Resume** - One command to restore context
5. **Team Friendly** - Others can see active work

This way, you never need to remember issue numbers - just run `/work-status` and the system shows you everything!
