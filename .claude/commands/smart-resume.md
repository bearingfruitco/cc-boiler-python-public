---
name: smart-resume
aliases: [sr, resume]
description: Intelligently resume work with task ledger integration
category: workflow
---

Intelligently resume work with full context awareness - no memory required!

## Arguments:
- $SPEED: quick|full|auto (default: auto)

## Why This Command:
- Zero memory required - finds your work automatically
- **NEW**: Shows task progress from central ledger
- Restores complete context in seconds
- Shows exactly where you left off
- Suggests next actions based on task status

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

# 2. Show Task Progress (NEW!)
echo -e "\n## 📋 Task Progress"
# Extract from task ledger
FEATURE=$(echo $BRANCH | sed 's/feature\///' | sed 's/[0-9]*-//')
grep -A 5 "## Task: $FEATURE" .task-ledger.md 2>/dev/null || echo "No tasks tracked yet"

# 3. Show Last Activity
echo -e "\n## 🕒 Last Activity"
tail -5 .claude/context/session.log | sed 's/^/  /'

# 4. Next Actions from ledger
echo -e "\n## 🎯 Suggested Next Steps"
# Check incomplete tasks
if [ -f ".task-ledger.md" ]; then
  INCOMPLETE=$(grep -A 20 "## Task: $FEATURE" .task-ledger.md | grep -c "\[ \]")
  if [ $INCOMPLETE -gt 0 ]; then
    echo "1. Continue with $INCOMPLETE remaining tasks: /pt $FEATURE"
  fi
fi
```

### Speed: FULL
Complete context reconstruction:

```bash
# 1. Project Overview
echo "## 🏗️ Project State"
echo ""

# Active features from task ledger
echo "### Active Features (from Task Ledger)"
grep -E "^## Task:|Progress:" .task-ledger.md | sed 's/## Task:/\n- /' | sed 's/.*Progress:/  Progress:/'

# 2. Git Status
echo -e "\n### Git State"
git status --short

# 3. Recent Commands
echo -e "\n### Recent Commands"
grep "Command:" .claude/logs/actions-*.jsonl | tail -10 | cut -d'"' -f4

# 4. Test Status
echo -e "\n### Test Results"
if [ -f ".pytest_cache/v/cache/lastfailed" ]; then
  echo "⚠️ Tests failing - check with: pytest --lf"
else
  echo "✅ All tests passing"
fi

# 5. Task Ledger Summary (NEW!)
echo -e "\n## 📊 Task Summary"
if [ -f ".task-ledger.md" ]; then
  # Count tasks by status
  GENERATED=$(grep -c "Status**: Generated" .task-ledger.md)
  IN_PROGRESS=$(grep -c "Status**: In Progress" .task-ledger.md)
  COMPLETED=$(grep -c "Status**: Completed" .task-ledger.md)
  BLOCKED=$(grep -c "Status**: Blocked" .task-ledger.md)
  
  echo "- 🟢 Generated: $GENERATED features ready to start"
  echo "- 🔵 In Progress: $IN_PROGRESS features being worked on"
  echo "- ✅ Completed: $COMPLETED features done"
  echo "- 🔴 Blocked: $BLOCKED features need attention"
fi

# 6. Intelligent Recommendations
echo -e "\n## 🤖 AI Recommendations"

# Check various states and suggest
if [ $IN_PROGRESS -gt 0 ]; then
  echo "1. You have active work - run: /tl view"
  echo "2. Continue current feature: /pt [feature-name]"
fi

if [ $BLOCKED -gt 0 ]; then
  echo "3. ⚠️ Address blocked features: /tl view --blocked"
fi

if [ $GENERATED -gt 0 ]; then
  echo "4. Start new feature: /fw start [issue-number]"
fi
```

## Enhanced Features:

### Task Ledger Integration
- Shows progress on current feature
- Displays overall task statistics
- Highlights blocked work
- Suggests most logical next step

### Context Restoration
```bash
# Restore full context
/cp load last

# Show work status
/ws

# View task details
/tl view
```

### Smart Suggestions
Based on task ledger state:
- If tasks in progress → suggest `/pt`
- If all complete → suggest `/fw complete`
- If blocked → suggest resolution
- If nothing active → suggest new feature

## Example Output:

```markdown
## 📍 You Are Here
Branch: feature/23-user-auth
Issue: #23
File: src/auth/login.py

## 📋 Task Progress
**user-authentication** - In Progress (7/10 tasks, 70%)
- Last updated: 45 minutes ago
- Time spent today: 2h 15m

## 🕒 Last Activity
- 14:23: Modified src/auth/login.py
- 14:25: Ran tests - 8/10 passing
- 14:30: Updated documentation

## 🎯 Suggested Next Steps
1. Continue with 3 remaining tasks: /pt user-authentication
2. Fix 2 failing tests: pytest tests/test_auth.py::test_token_validation -v
3. After completion: /fw complete 23

## 💡 Pro Tip
You're 70% done! The remaining tasks are:
- Implement token refresh
- Add rate limiting
- Update API documentation
```

## Benefits:

1. **Never ask "where was I?"** - Always know exactly
2. **Task awareness** - See progress without searching
3. **Smart suggestions** - AI knows what's next
4. **Zero memory needed** - Everything reconstructed
5. **Team friendly** - Anyone can pick up where you left
