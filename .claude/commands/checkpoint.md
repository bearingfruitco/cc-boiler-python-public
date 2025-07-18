# Checkpoint

Create a development checkpoint with full context for easy resumption.

## Arguments:
- $ACTION: create|restore|list
- $NAME: Checkpoint name (optional, auto-generated if not provided)

## Why This Command:
When switching contexts or ending a session, capture:
- Current work state
- Design validation status
- Next steps planned
- Any blocking issues

## Steps:

### Action: CREATE
1. **Capture Current State**
   ```typescript
   const checkpoint = {
     timestamp: new Date().toISOString(),
     branch: getCurrentBranch(),
     issue: extractIssueNumber(),
     uncommittedFiles: getUncommittedFiles(),
     validationStatus: await runValidation(),
     lastCommit: getLastCommit()
   };
   ```

2. **Document Work Status**
   ```markdown
   ## Checkpoint: auth-feature-2024-01-15-14:30
   
   ### Current Task
   Working on: Issue #23 - Authentication Components
   Branch: feature/23-auth-components
   
   ### Progress
   ✅ Completed:
   - LoginForm base component
   - RegisterForm base component
   - Form validation schemas
   
   🚧 In Progress:
   - Adding error states to LoginForm
   - Writing unit tests
   
   📋 TODO:
   - Complete error states
   - Add loading states
   - Write integration tests
   - Update documentation
   
   ### Design Status
   - Validation: ✅ Passing
   - Components: 2/3 complete
   - Test Coverage: 45%
   
   ### Blockers
   None
   
   ### Next Steps
   1. Finish error states (30 min)
   2. Run validation
   3. Create PR
   ```

3. **Save Checkpoint**
   ```bash
   # Create checkpoint file
   mkdir -p .claude/checkpoints
   echo "$CHECKPOINT_DATA" > .claude/checkpoints/${NAME}.md
   
   # Optionally commit if clean
   if [ -z "$(git status --porcelain)" ]; then
     git add .claude/checkpoints/${NAME}.md
     git commit -m "checkpoint: ${NAME}"
   fi
   ```

### Action: RESTORE
1. **Load Checkpoint**
   ```bash
   cat .claude/checkpoints/${NAME}.md
   ```

2. **Restore Context**
   ```markdown
   ## Restored Checkpoint: ${NAME}
   
   You were working on: Issue #23
   Branch: feature/23-auth-components
   
   ## Quick Status Check
   - Current branch matches: ✅
   - Uncommitted changes: 2 files
   - Design validation: ✅ Still passing
   
   ## Resume Instructions
   1. Review uncommitted changes
   2. Continue with: "Adding error states to LoginForm"
   3. Next milestone: Create PR
   
   ## Commands to Run
   - `/validate-design` - Ensure still compliant
   - `/create-component ui ErrorMessage` - If needed
   - `/feature-workflow complete 23` - When ready
   ```

### Action: LIST
Show available checkpoints:
```markdown
## Available Checkpoints

### Recent (Last 7 days)
1. **auth-feature-2024-01-15-14:30**
   - Issue #23: Authentication
   - Status: In progress
   - Branch: feature/23-auth-components

2. **dashboard-start-2024-01-14-09:00**
   - Issue #24: Dashboard
   - Status: Planning
   - Branch: main

### Older
3. **fix-buttons-2024-01-10-16:45**
   - Issue #21: Button fixes
   - Status: Completed ✅
   - Branch: (deleted)
```

## Auto-Checkpoint Triggers:

The command can suggest creating checkpoints when:
- Switching branches
- Before large refactors
- End of work session
- Before context might be lost

## Integration:

```bash
# End of day
/checkpoint create end-of-day-auth
"Created checkpoint: end-of-day-auth"

# Next morning
/context-refresh all
"You have a checkpoint from yesterday. Run: /checkpoint restore end-of-day-auth"

# Restore and continue
/checkpoint restore end-of-day-auth
```

## Checkpoint Contents Include:
- Current branch and issue
- File changes summary
- Design validation status
- Work completed/remaining
- Blockers or dependencies
- Specific next steps
- Relevant commands to run

This helps maintain continuity across:
- Context compactions
- Session breaks
- Task switching
- Team handoffs
