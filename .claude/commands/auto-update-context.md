Automatically update CLAUDE.md based on current codebase analysis.

Analyze the project and update:
1. New components and their purposes
2. Updated API endpoints
3. New business logic rules discovered
4. Database schema changes
5. New patterns detected
6. Dependencies added
7. File structure changes

Process:
1. Scan all files modified in last 7 days
2. Extract patterns and conventions
3. Identify new features
4. Update relevant sections in CLAUDE.md
5. Show diff for review
6. Create backup of current CLAUDE.md

Important: Show changes for approval before applying.

Example usage:
```
/project:auto-update-context
```

The command will:
- Analyze your codebase for changes
- Generate updates to CLAUDE.md
- Show you a diff of proposed changes
- Apply changes only after your approval