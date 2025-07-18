# Smart Resume

Intelligently resume work with full context awareness - no memory required!

## Arguments:
- $SPEED: quick|full|auto (default: auto)

## Why This Command:
- Zero memory required - finds your work automatically
- Restores complete context in seconds
- Shows exactly where you left off
- Suggests next actions

## Steps:

### Speed: AUTO (Default)
Automatically determines what you need:

```bash
# 1. Check time since last work
LAST_MODIFIED=$(find .claude/context/current.md -mmin -60 2>/dev/null)

if [ -z "$LAST_MODIFIED" ]; then
  # Context is old, do full resume
  SPEED="full"
else
  # Recent context, quick resume
  SPEED="quick"
fi
```

### Speed: QUICK
For resuming after short breaks (<1 hour):

```bash
# 1. Show Current Location
echo "## 📍 You Are Here"
echo ""

# Get from context file
BRANCH=$(git branch --show-current)
ISSUE=$(echo $BRANCH | grep -oE '[0-9]+' | head -1)
CURRENT_FILE=$(grep "Location:" .claude/context/current.md | head -1 | cut -d' ' -f2)

echo "Branch: $BRANCH"
echo "Issue: #$ISSUE"
echo "File: $CURRENT_FILE"

# 2. Show Last Activity
echo -e "\n## 🕒 Last Activity"
git log -1 --pretty=format:"Commit: %s (%cr)"

# 3. Show Immediate Context
echo -e "\n## 💡 Continue With:"
grep "TODO" $CURRENT_FILE | head -3

# 4. Quick Status
echo -e "\n## ✅ Quick Checks"
echo "Design: $(grep 'Design:' .claude/context/current.md | tail -1)"
echo "Tests: $(npm test --silent 2>&1 | grep -E 'passed|failed' | tail -1)"
```

### Speed: FULL
Complete context restoration:

```bash
# 0. Check for PreCompact Context
PRECOMPACT_FILE=".claude/context/pre-compact-context.json"
if [ -f "$PRECOMPACT_FILE" ]; then
  echo "## 🔄 PreCompact Context Detected!"
  echo "Claude previously saved context before compaction."
  echo ""
  
  # Read critical files from pre-compact context
  CRITICAL_FILES=$(jq -r '.critical_files[]' "$PRECOMPACT_FILE" 2>/dev/null)
  TIMESTAMP=$(jq -r '.timestamp' "$PRECOMPACT_FILE" 2>/dev/null)
  CURRENT_TASK=$(jq -r '.current_task' "$PRECOMPACT_FILE" 2>/dev/null)
  
  echo "📅 Saved at: $TIMESTAMP"
  
  if [ ! -z "$CURRENT_TASK" ] && [ "$CURRENT_TASK" != "null" ]; then
    echo "📋 Active task: $CURRENT_TASK"
  fi
  
  echo ""
  echo "## 📚 Re-reading Critical Files..."
  for file in $CRITICAL_FILES; do
    if [ -f "$file" ]; then
      echo "✓ Re-reading: $file"
      # Force Claude to read the file
      echo "[Please read: $file]"
    fi
  done
  
  echo ""
  echo "✅ Context restoration complete!"
  echo ""
  
  # Clean up after restoration
  mv "$PRECOMPACT_FILE" "$PRECOMPACT_FILE.restored"
fi

# 1. Detect Current State
echo "## 🔍 Analyzing Project State..."

# Check all possible work locations
CURRENT_BRANCH=$(git branch --show-current)
ISSUE_FROM_BRANCH=$(echo $CURRENT_BRANCH | grep -oE '[0-9]+' | head -1)

# Search for work in multiple places
if [ ! -z "$ISSUE_FROM_BRANCH" ]; then
  ISSUE=$ISSUE_FROM_BRANCH
else
  # Check recent commits for issue numbers
  ISSUE=$(git log --oneline -10 | grep -oE '#[0-9]+' | head -1 | tr -d '#')
fi

# 2. Restore From All Sources
echo -e "\n## 📥 Restoring Context..."

# From local context
if [ -f .claude/context/current.md ]; then
  echo "✓ Local context found"
  LOCAL_CONTEXT=$(cat .claude/context/current.md)
fi

# From GitHub
if [ ! -z "$ISSUE" ]; then
  echo "✓ Checking GitHub state for issue #$ISSUE"
  
  # Try gist
  GIST_STATE=$(gh gist list | grep "Work state.*#$ISSUE" | head -1)
  if [ ! -z "$GIST_STATE" ]; then
    GIST_ID=$(echo $GIST_STATE | awk '{print $1}')
    REMOTE_STATE=$(gh gist view $GIST_ID -f work-state-${ISSUE}.json)
    echo "✓ Found saved state in GitHub"
  fi
  
  # Get issue details
  ISSUE_DETAILS=$(gh issue view $ISSUE --json title,body,assignees,labels)
  echo "✓ Retrieved issue details"
fi

# 3. Build Complete Picture
echo -e "\n## 📊 Complete Work Context"
echo ""

# Current work
if [ ! -z "$ISSUE" ]; then
  TITLE=$(echo $ISSUE_DETAILS | jq -r '.title')
  echo "### Issue #$ISSUE: $TITLE"
  echo "Branch: $CURRENT_BRANCH"
else
  echo "### Current Branch: $CURRENT_BRANCH"
  echo "No linked issue detected"
fi

# File status
echo -e "\n### 📁 File Status"
MODIFIED=$(git status --porcelain | wc -l)
echo "Modified files: $MODIFIED"
if [ $MODIFIED -gt 0 ]; then
  git status --porcelain | head -5
fi

# Recent activity
echo -e "\n### 📝 Recent Activity"
git log --oneline -5

# TODOs
echo -e "\n### 📋 Active TODOs"
grep -r "TODO:" --include="*.tsx" --include="*.ts" . 2>/dev/null | grep -v node_modules | head -5

# From saved state
if [ ! -z "$REMOTE_STATE" ]; then
  echo -e "\n### 💾 Saved Progress"
  PROGRESS=$(echo $REMOTE_STATE | jq -r '.progress.percentage')
  CURRENT_TASK=$(echo $REMOTE_STATE | jq -r '.progress.currentTask')
  LOCATION=$(echo $REMOTE_STATE | jq -r '.progress.location.file + ":" + (.progress.location.line|tostring)')
  
  echo "Progress: ${PROGRESS}%"
  echo "Task: $CURRENT_TASK"
  echo "Location: $LOCATION"
fi

# 4. Actionable Next Steps
echo -e "\n## 🎯 Next Actions"

if [ ! -z "$LOCATION" ]; then
  echo "1. Open: $LOCATION"
  echo "   Command: cursor $LOCATION"
fi

if [ ! -z "$CURRENT_TASK" ]; then
  echo -e "\n2. Continue: $CURRENT_TASK"
fi

echo -e "\n3. Validate design compliance:"
echo "   Command: /validate-design"

if [ $MODIFIED -gt 0 ]; then
  echo -e "\n4. Commit your changes:"
  echo "   Command: /feature-workflow validate $ISSUE"
fi

# 5. Smart Suggestions
echo -e "\n## 💡 Smart Suggestions"

# Based on time of day
HOUR=$(date +%H)
if [ $HOUR -lt 10 ]; then
  echo "- Morning! Consider reviewing yesterday's work first"
  echo "  Command: /checkpoint list"
elif [ $HOUR -gt 17 ]; then
  echo "- End of day? Create a checkpoint:"
  echo "  Command: /checkpoint create"
fi

# Based on progress
if [ ! -z "$PROGRESS" ] && [ $PROGRESS -gt 80 ]; then
  echo "- Nearly done! Review before PR:"
  echo "  Command: /feature-workflow complete $ISSUE"
fi

# 6. One-Line Resume
echo -e "\n## ⚡ Quick Resume"
echo "Copy and run:"
if [ ! -z "$LOCATION" ]; then
  echo "cursor $LOCATION && /validate-design"
else
  echo "/context-grab restore && /work-status current"
fi
```

## Smart Detection Features:

### 1. **Multi-Source Context**
Checks in order:
1. Current branch name
2. Recent commits
3. Local context file
4. GitHub gists
5. Issue comments
6. Modified files
7. Recent research documents (NEW!)
8. Feature-related research (NEW!)

### 2. **Intelligent Suggestions**
Based on:
- Time of day
- Progress percentage
- File modifications
- Last activity time
- Current task

### 3. **Zero Configuration**
No need to specify:
- Issue numbers
- Branch names
- File locations
- Task status

## Integration with Other Commands:

```bash
# After compaction
/smart-resume
> Detects you need full context
> Restores from all sources

# Start of day
/smart-resume
> Shows overnight changes
> Suggests review first

# After short break
/smart-resume quick
> Just shows current location
> Ready to continue

# Lost and confused
/smart-resume full
> Searches everywhere
> Rebuilds complete context
```

## Example Output:

```
## 🔍 Analyzing Project State...
✓ Local context found
✓ Checking GitHub state for issue #23
✓ Found saved state in GitHub
✓ Retrieved issue details
✓ Found 2 related research documents (NEW!)

## 📊 Complete Work Context

### Issue #23: Add authentication components
Branch: feature/23-auth-components

### 📄 Related Research (NEW!)
- `auth-analysis-2025-01-15.md` - JWT vs Session comparison
- `auth-planning-2025-01-14.md` - Implementation approach

### 📁 File Status
Modified files: 2
 M components/auth/LoginForm.tsx
 M components/auth/RegisterForm.tsx

### 💾 Saved Progress
Progress: 70%
Task: Adding network error handling
Location: components/auth/LoginForm.tsx:145

## 🎯 Next Actions
1. Open: components/auth/LoginForm.tsx:145
   Command: cursor components/auth/LoginForm.tsx:145

2. Continue: Adding network error handling

3. Validate design compliance:
   Command: /validate-design

## ⚡ Quick Resume
Copy and run:
cursor components/auth/LoginForm.tsx:145 && /validate-design

## 🆕 New Safety Features Active
- ✅ Truth Enforcement - Protecting established values
- ✅ Deletion Guard - Warning before removals
- ✅ Hydration Safety - Catching SSR errors
- ✅ Import Validation - Fixing path issues

## 📋 Quick Commands
- `/facts` - See protected values
- `/exists [name]` - Check before creating
- `/chain safe-commit` - Validate before commit
- `/help new` - See all new features
```

This makes resuming work effortless - just run `/smart-resume` and you're back in context!
