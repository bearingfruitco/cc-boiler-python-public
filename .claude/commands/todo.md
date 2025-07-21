# TODO Tracking System

Comprehensive TODO tracking integrated with GitHub for persistent progress monitoring.

## Arguments:
- $ACTION: add|update|list|sync|report
- $SCOPE: current|issue|project|all
- $ISSUE_NUMBER: Issue number (optional)

## Why This Command:
- Track TODOs across compactions
- Maintain progress visibility
- Integrate with GitHub issues
- Never lose track of tasks

## TODO Storage Locations

### 1. **In-Code TODOs**
```typescript
// TODO: Add error handling for network failures
// TODO: [#23] Implement retry logic
// FIXME: Handle edge case when user is offline
// NOTE: This will need refactoring after auth update
```

### 2. **GitHub Issue Checklist**
```markdown
## Implementation Tasks
- [x] Create LoginForm component
- [x] Add form validation
- [ ] Add error handling <!-- TODO: Network errors -->
- [ ] Add loading states
- [ ] Write unit tests
  - [x] Validation tests
  - [ ] Submission tests <!-- TODO: Mock API calls -->
- [ ] Update documentation
```

### 3. **Dedicated TODO Gist**
```json
{
  "lastUpdated": "2024-01-15T14:30:00Z",
  "issues": {
    "23": {
      "title": "Add authentication components",
      "todos": [
        {
          "id": "todo-001",
          "task": "Add network error handling",
          "location": "components/auth/LoginForm.tsx:145",
          "priority": "high",
          "status": "in-progress",
          "created": "2024-01-15T10:00:00Z",
          "context": "Need try-catch around API call"
        },
        {
          "id": "todo-002",
          "task": "Add loading spinner",
          "location": "components/auth/LoginForm.tsx:78",
          "priority": "medium",
          "status": "pending",
          "created": "2024-01-15T11:00:00Z"
        }
      ],
      "progress": {
        "completed": 7,
        "total": 10,
        "percentage": 70
      }
    }
  }
}
```

## Steps:

### Action: ADD
1. **Add TODO to Multiple Locations**
   ```bash
   # Add to code
   echo "// TODO: [#${ISSUE_NUMBER}] ${TODO_TEXT}" >> ${FILE}
   
   # Add to GitHub issue
   gh issue comment ${ISSUE_NUMBER} --body "## 📝 New TODO
   - [ ] ${TODO_TEXT}
   Location: \`${FILE}:${LINE}\`
   Priority: ${PRIORITY}
   Added: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
   
   # Add to TODO gist
   TODO_ENTRY="{
     \"id\": \"todo-$(date +%s)\",
     \"task\": \"${TODO_TEXT}\",
     \"location\": \"${FILE}:${LINE}\",
     \"priority\": \"${PRIORITY}\",
     \"status\": \"pending\"
   }"
   
   # Update gist
   gh gist edit ${TODO_GIST_ID} --add-file todos-issue-${ISSUE_NUMBER}.json
   ```

### Action: UPDATE
1. **Mark TODO as Complete**
   ```bash
   # Update in issue
   gh issue comment ${ISSUE_NUMBER} --body "## ✅ Completed TODO
   - [x] ${TODO_TEXT}
   Completed: $(date -u +%Y-%m-%dT%H:%M:%SZ)
   Commit: ${COMMIT_SHA}"
   
   # Update in gist
   # Mark status as "completed"
   ```

2. **Update Progress**
   ```markdown
   ## 📊 Progress Update - Issue #23
   
   ### Overall: 75% Complete (↑ from 70%)
   
   #### Just Completed:
   - ✅ Add network error handling
   
   #### Currently Working On:
   - 🚧 Add loading states
   
   #### Remaining TODOs (3):
   1. Field-specific error display
   2. Integration tests
   3. Documentation update
   
   ### Time Estimate: 2 hours remaining
   ```

### Action: LIST
1. **Show Current TODOs**
   ```markdown
   ## 📋 Active TODOs
   
   ### Current File (LoginForm.tsx)
   - [ ] Line 145: Add try-catch for API errors [HIGH]
   - [ ] Line 78: Add loading spinner [MEDIUM]
   - [ ] Line 203: Improve error message UX [LOW]
   
   ### Current Issue (#23)
   Total: 10 tasks (7 complete, 3 remaining)
   
   #### High Priority:
   1. Network error handling (in progress)
   
   #### Medium Priority:
   2. Loading states
   3. Integration tests
   
   #### Low Priority:
   4. Documentation
   ```

### Action: SYNC
1. **Sync All TODO Sources**
   ```typescript
   // Scan codebase for TODOs
   const codeTodos = await scanForTodos(['TODO:', 'FIXME:', 'HACK:']);
   
   // Get issue checklists
   const issueTodos = await getIssueChecklists();
   
   // Get gist TODOs
   const gistTodos = await getGistTodos();
   
   // Merge and deduplicate
   const allTodos = mergeTodos(codeTodos, issueTodos, gistTodos);
   
   // Update master list
   await updateMasterTodoList(allTodos);
   ```

### Action: REPORT
1. **Generate TODO Report**
   ```markdown
   # TODO Report - Generated 2024-01-15
   
   ## Summary
   - Total TODOs: 47
   - Completed Today: 5
   - Added Today: 3
   - Net Progress: -2
   
   ## By Issue
   ### Issue #23: Authentication (70% complete)
   - ✅ Completed: 7
   - 🚧 In Progress: 1
   - ⬜ Remaining: 2
   
   ### Issue #24: Dashboard (30% complete)
   - ✅ Completed: 3
   - 🚧 In Progress: 0
   - ⬜ Remaining: 7
   
   ## By Priority
   - 🔴 High: 5 TODOs
   - 🟡 Medium: 12 TODOs
   - 🟢 Low: 8 TODOs
   
   ## Stale TODOs (>7 days old)
   1. [#18] Refactor API client (14 days)
   2. [#20] Add performance monitoring (10 days)
   ```

## About the Resume Command

When I showed `/compact-prepare resume 23`, the `23` is the GitHub issue number. Here's what it means:

```bash
# Resume work on issue #23
/compact-prepare resume 23

# This fetches the saved state for issue #23 and shows:
# - What file you were editing
# - What line you were on
# - What task you were doing
# - Your TODO list for that issue
```

## Integration with Compact-Prepare

The TODO system integrates with compact-prepare:

```typescript
// When preparing for compaction
const todoState = {
  currentTodos: getCurrentFileTodos(),
  issueTodos: getIssueTodos(issueNumber),
  progress: calculateProgress()
};

// Save with other state
state.todos = todoState;

// When resuming
console.log(`
## 📋 TODO Status
Current: ${state.todos.currentTodos.length} TODOs in file
Issue #${issueNumber}: ${state.todos.progress}% complete

Next TODO: ${state.todos.currentTodos[0].text}
Location: ${state.todos.currentTodos[0].location}
`);
```

## Complete Workflow Example

```bash
# Start feature
/feature-workflow start 23

# Add TODOs as you work
/todo-tracking add "Implement retry logic" high

# Check progress
/todo-tracking list current
> "3 TODOs in current file"

# Before compaction
/compact-prepare prepare
> "Saving 3 active TODOs to GitHub"

# After compaction
/compact-prepare resume 23
> "Restored: 3 TODOs (1 in progress)"

# Complete a TODO
/todo-tracking update complete todo-001
> "Marked complete. Progress: 75%"

# Get daily report
/todo-tracking report
> "Today: +5 completed, -3 added"
```

## GitHub Integration Benefits

1. **Persistent** - TODOs survive across sessions
2. **Visible** - Team sees all TODOs on issues
3. **Searchable** - Find TODOs across project
4. **Trackable** - Progress over time
5. **Integrated** - Part of issue workflow

This ensures you never lose track of what needs to be done, even across compactions and long breaks!
