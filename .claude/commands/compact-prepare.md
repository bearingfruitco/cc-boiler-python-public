# Enhanced Compact Prepare with GitHub Persistence

Save work state to GitHub for long-term persistence and seamless resumption.

## Arguments:
- $ACTION: prepare|resume|status|list
- $STORAGE: local|github|both (default: github)

## Why This Enhancement:
- Persist state across days/weeks
- Resume from any machine
- Track all features in progress
- Team visibility into work status

## Steps:

### Action: PREPARE
1. **Capture Complete State** (same as before)
   ```typescript
   const currentState = {
     timestamp: new Date().toISOString(),
     issue: extractIssueNumber(),
     branch: getCurrentBranch(),
     worktree: getWorktreePath(),
     
     // Detailed progress
     currentFile: getCurrentEditingFile(),
     currentLine: getCurrentLine(),
     currentTask: getCurrentTaskDetails(),
     
     // Task checklist
     completedTasks: getCompletedTasks(),
     remainingTasks: getRemainingTasks(),
     progressPercentage: calculateProgress(),
     
     // Code context
     uncommittedChanges: getUncommittedFiles(),
     lastCommit: getLastCommit(),
     codeSnippet: getCodeContext()
   };
   ```

2. **Save to GitHub** (PRIMARY METHOD)
   
   **Option A: GitHub Gist** (Recommended)
   ```bash
   # Create a JSON file with state
   cat > work-state-${ISSUE_NUMBER}.json << EOF
   {
     "issue": ${ISSUE_NUMBER},
     "title": "${ISSUE_TITLE}",
     "branch": "${BRANCH_NAME}",
     "lastUpdated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
     "progress": {
       "percentage": 70,
       "currentTask": "Adding error states to LoginForm",
       "location": {
         "file": "components/auth/LoginForm.tsx",
         "line": 145,
         "function": "handleSubmit"
       }
     },
     "tasks": {
       "completed": [
         "Created LoginForm base structure",
         "Added validation schemas",
         "Implemented form submission"
       ],
       "current": "Adding network error handling at line 145",
       "remaining": [
         "Add loading states",
         "Create integration tests",
         "Update documentation"
       ]
     },
     "nextSteps": "Add try-catch block for API call at line 145",
     "codeContext": "const handleSubmit = async (formData: LoginData) => {\\n  setLoading(true);\\n  // TODO: Add network error handling here\\n  const response = await apiClient.post('/auth/login', formData);"
   }
   EOF
   
   # Create/update gist
   gh gist create work-state-${ISSUE_NUMBER}.json \
     --desc "Work state for issue #${ISSUE_NUMBER}" \
     --public=false
   
   # Or update existing
   gh gist edit ${GIST_ID} work-state-${ISSUE_NUMBER}.json
   ```

   **Option B: Issue Comment** (Alternative)
   ```bash
   # Post state as issue comment
   gh issue comment ${ISSUE_NUMBER} --body "## 🔄 Work State Checkpoint
   
   **Last Updated**: $(date -u +%Y-%m-%dT%H:%M:%SZ)
   **Progress**: 70% complete
   **Branch**: \`${BRANCH_NAME}\`
   
   ### Current Status
   Working on: Adding network error handling
   - File: \`components/auth/LoginForm.tsx\`
   - Line: 145
   - Function: \`handleSubmit()\`
   
   ### Completed ✅
   - Created LoginForm base structure
   - Added validation schemas
   - Implemented form submission
   - Added TypeScript types
   - Created unit tests for validation
   
   ### In Progress 🚧
   - Adding error states to LoginForm
     - ✓ Basic error display
     - → Network error handling (line 145)
     - ⬜ Field-specific errors
   
   ### Remaining 📋
   - Add loading states
   - Create integration tests
   - Update documentation
   - Add Storybook examples
   
   ### Resume Instructions
   \`\`\`bash
   # 1. Setup worktree
   /worktree create ${BRANCH_NAME}
   
   # 2. Resume work
   /compact-prepare resume ${ISSUE_NUMBER}
   \`\`\`
   
   ### Code Context
   \`\`\`typescript
   // Next: Add try-catch at line 145
   const handleSubmit = async (formData: LoginData) => {
     setLoading(true);
     // TODO: Add network error handling here
     const response = await apiClient.post('/auth/login', formData);
   \`\`\`
   "
   ```

   **Option C: Dedicated Branch** (Most Robust)
   ```bash
   # Create a state branch
   git checkout -b state/${ISSUE_NUMBER}-checkpoint
   
   # Save state files
   mkdir -p .claude/state
   echo "$STATE_JSON" > .claude/state/issue-${ISSUE_NUMBER}.json
   echo "$CONTINUATION_SCRIPT" > .claude/state/continuation-${ISSUE_NUMBER}.md
   
   # Commit and push
   git add .claude/state/
   git commit -m "checkpoint: Save state for issue #${ISSUE_NUMBER}"
   git push origin state/${ISSUE_NUMBER}-checkpoint
   
   # Return to working branch
   git checkout ${BRANCH_NAME}
   ```

3. **Create State Summary**
   ```markdown
   ## 📍 State Saved Successfully
   
   ### Storage Locations:
   - GitHub Gist: https://gist.github.com/[id]
   - Issue Comment: #${ISSUE_NUMBER} (latest comment)
   - State Branch: state/${ISSUE_NUMBER}-checkpoint
   
   ### Quick Resume:
   ```bash
   /compact-prepare resume ${ISSUE_NUMBER}
   ```
   
   ### Manual Resume:
   1. Check issue #${ISSUE_NUMBER} for latest state
   2. Create worktree: `/worktree create ${BRANCH_NAME}`
   3. Open file: `components/auth/LoginForm.tsx:145`
   4. Continue with error handling implementation
   ```

### Action: RESUME
1. **Fetch State from GitHub**
   ```bash
   # Option A: From Gist
   STATE=$(gh gist view work-state-${ISSUE_NUMBER}.json)
   
   # Option B: From Issue Comment
   STATE=$(gh issue view ${ISSUE_NUMBER} --comments | grep -A 100 "Work State Checkpoint" | head -n 100)
   
   # Option C: From State Branch
   git fetch origin state/${ISSUE_NUMBER}-checkpoint
   git show origin/state/${ISSUE_NUMBER}-checkpoint:.claude/state/issue-${ISSUE_NUMBER}.json
   ```

2. **Parse and Display State**
   ```typescript
   const state = JSON.parse(stateJson);
   
   console.log(`
   ## 🔄 Resuming Issue #${state.issue}: ${state.title}
   
   Last updated: ${state.lastUpdated}
   Progress: ${state.progress.percentage}%
   
   ### You were here:
   - File: ${state.progress.location.file}
   - Line: ${state.progress.location.line}
   - Task: ${state.progress.currentTask}
   
   ### Next Step:
   ${state.nextSteps}
   
   ### Code Context:
   \`\`\`typescript
   ${state.codeContext}
   \`\`\`
   `);
   ```

3. **Setup Working Environment**
   ```bash
   # Ensure worktree exists
   if ! git worktree list | grep -q "${BRANCH_NAME}"; then
     echo "Creating worktree..."
     /worktree create ${BRANCH_NAME}
   fi
   
   # Switch to worktree
   cd ../$(basename $(pwd))-worktrees/${BRANCH_NAME}
   
   # Open in editor at exact location
   cursor ${state.progress.location.file}:${state.progress.location.line}
   ```

### Action: LIST
Show all saved states:
```bash
# List all work states
echo "## 📋 All Saved Work States"
echo ""

# From Gists
echo "### GitHub Gists:"
gh gist list | grep "Work state for issue"

# From Issues
echo -e "\n### Active Issues with States:"
gh issue list --assignee @me --state open --json number,title,updatedAt \
  --jq '.[] | "- #\(.number): \(.title) (updated: \(.updatedAt))"'

# From State Branches
echo -e "\n### State Branches:"
git branch -r | grep "state/.*-checkpoint"
```

### Action: STATUS
Check current work state:
```markdown
## 📊 Work State Status

### Current Context
- Branch: feature/23-auth-components
- Issue: #23
- Context Usage: 87%

### Saved States
- ✅ GitHub Gist: Updated 5 min ago
- ✅ Issue Comment: Posted 5 min ago
- ⚠️ State Branch: 1 hour old

### Resume Commands
- From anywhere: `/compact-prepare resume 23`
- List all states: `/compact-prepare list`
```

## Configuration Options

Add to `.claude/config.json`:
```json
{
  "compactPrepare": {
    "storage": "github",
    "githubOptions": {
      "useGists": true,
      "useIssueComments": true,
      "useStateBranch": false
    },
    "autoSave": {
      "enabled": true,
      "threshold": 0.85,
      "interval": 300000
    }
  }
}
```

## Benefits of GitHub Storage:

1. **Persistent** - Survives across days/weeks/months
2. **Accessible** - Resume from any machine
3. **Visible** - Team can see progress
4. **Versioned** - History of checkpoints
5. **Integrated** - Part of issue/PR workflow

## Example Long-Term Workflow:

```bash
# Monday: Start feature
/feature-workflow start 23
/create-component ui LoginForm

# System auto-saves to GitHub
> "State saved to GitHub. Issue #23 updated."

# Friday: Prepare for weekend
/compact-prepare prepare
> "State saved to Gist and Issue #23"

# Next Monday: Resume
/compact-prepare resume 23
> "Restored: LoginForm.tsx:145 - Add error handling"
> "70% complete. Continue where you left off."

# Or check all work
/compact-prepare list
> "Active work states:"
> "- #23: Auth Components (70%)"
> "- #24: Dashboard Layout (30%)"
> "- #25: User Settings (not started)"
```

This ensures your work state is never lost and you can always pick up exactly where you left off, even after weeks away!
