Create a task-based checkpoint for feature: $ARGUMENTS

Save current state including:
1. Which tasks are complete in $ARGUMENTS-tasks.md
2. Current task being worked on
3. Any blockers or issues encountered
4. Code changes made so far
5. Next steps planned

Format:
## Checkpoint: $ARGUMENTS - $(date)
### Progress: X of Y tasks complete
### Current Task: X.Y
### Changes Made:
- List of files changed
- Key implementations

### Issues/Blockers:
- Any problems encountered

### Next Session:
- Start with task X.Y
- Consider: [any notes]

Save to .claude/checkpoints/tasks/$ARGUMENTS-$(timestamp).md