# Context Refresh

Refresh context after Claude Code compaction or when resuming work.

## Arguments:
- $SCOPE: all|project|issues|validation|changes

## Why This Command:
After context compaction or starting a new session, quickly restore awareness of:
- Current project state
- Active issues and branches
- Recent changes
- Design system compliance
- Next priorities

## Steps:

### Scope: ALL (Default)
1. **Project Overview**
   ```markdown
   # Context Refresh: [Project Name]
   
   ## Project Type: AI Documentation Generator
   ## Design Rules: 4 sizes, 2 weights, 4px grid
   ## Current Phase: [Active Development]
   ```

2. **Active Work Status**
   ```bash
   # Current branch
   BRANCH=$(git branch --show-current)
   
   # Uncommitted changes
   CHANGES=$(git status --porcelain | wc -l)
   
   # Recent commits
   RECENT=$(git log --oneline -5)
   ```

3. **Issue Status** (via MCP)
   ```typescript
   const myIssues = await github.listIssues({
     assignee: '@me',
     state: 'open'
   });
   
   const inProgress = myIssues.filter(i => 
     i.labels.includes('in-progress')
   );
   ```

4. **Design Compliance**
   ```bash
   # Quick validation check
   npm run validate:design --summary
   ```

5. **Generate Summary**
   ```markdown
   ## 📍 You Are Here
   
   Branch: feature/23-auth-components
   Changes: 3 files modified (uncommitted)
   
   ## 🎯 Current Focus
   Issue #23: Add authentication components
   - Status: In Progress
   - Design: ✅ Compliant
   - TODO: Add error states, write tests
   
   ## 📋 Other Active Issues
   - #24: Dashboard layout (Ready)
   - #25: User settings (Blocked on #23)
   
   ## 💡 Suggested Next Actions
   1. Commit current changes: `/feature-workflow validate 23`
   2. Complete error states for LoginForm
   3. Run tests before PR
   ```

### Scope: PROJECT
Show only project configuration and rules:
```markdown
## Project Configuration
- Type: [Project Type]
- Stack: Next.js 15, React 19, TypeScript
- Design System: ✅ Active (4/2/4 rules)
- Validation: Automated

## Key Commands Available
- /generate-docs - Create documentation
- /create-component - Generate components
- /validate-design - Check compliance
```

### Scope: ISSUES
Show only GitHub issues status:
```markdown
## Issue Overview
### In Progress (1)
- #23 Auth components [75% complete]

### Ready to Start (2)
- #24 Dashboard layout
- #26 Search feature

### Blocked (1)
- #25 User settings (waiting on #23)
```

### Scope: VALIDATION
Show only design system status:
```markdown
## Design System Status
- Last check: 10 minutes ago
- Status: ✅ Compliant
- Components checked: 15
- Violations found: 0

## Coverage
- UI Components: 15/15 ✅
- Forms: 8/8 ✅
- Layouts: 5/5 ✅
- Features: 3/5 🚧
```

### Scope: CHANGES
Show only recent changes:
```markdown
## Recent Changes
### Uncommitted (3 files)
- M components/auth/LoginForm.tsx
- M components/auth/RegisterForm.tsx
- A components/auth/AuthLayout.tsx

### Recent Commits
- feat: add login form base structure
- fix: correct button spacing
- docs: update component list
```

## Integration with Workflow:

```bash
# After context compaction
/context-refresh all

# Starting work for the day
/context-refresh all

# Before creating PR
/context-refresh validation

# Checking what to work on
/context-refresh issues
```

## Output Format:
Always ends with:
1. Current location (branch/issue)
2. Immediate next step
3. Available commands for that context
