# Issue Kanban View

Provides a kanban-style view of GitHub issues with design system status.

## Arguments:
- $VIEW: board|sprint|my-work|validation-status

## Why This Command:
GitHub MCP can list issues, but doesn't provide:
- Kanban board visualization
- Design system compliance status
- Sprint/iteration planning
- Work-in-progress limits

## Steps:

### View: BOARD
1. **Fetch Issues via MCP**
   ```typescript
   const allIssues = await github.listIssues({
     state: 'open',
     labels: ['feature', 'bug', 'enhancement']
   });
   ```

2. **Categorize by Status**
   ```typescript
   const board = {
     backlog: [],
     ready: [],
     inProgress: [],
     review: [],
     blocked: []
   };
   
   // Sort by labels and PR status
   for (const issue of allIssues) {
     if (issue.labels.includes('blocked')) {
       board.blocked.push(issue);
     } else if (issue.pull_request) {
       board.review.push(issue);
     } else if (issue.labels.includes('in-progress')) {
       board.inProgress.push(issue);
     } else if (issue.labels.includes('ready')) {
       board.ready.push(issue);
     } else {
       board.backlog.push(issue);
     }
   }
   ```

3. **Check Design Status for Each**
   ```typescript
   // For each in-progress issue, check worktree
   for (const issue of board.inProgress) {
     const worktreePath = findWorktree(issue.number);
     if (worktreePath) {
       const validationStatus = await runValidation(worktreePath);
       issue.designStatus = validationStatus;
     }
   }
   ```

4. **Generate Kanban View**
   ```markdown
   # 📋 Project Kanban Board
   
   ## 📝 Backlog (5)
   - #25 Add user settings page
   - #26 Implement search feature
   - #27 Create analytics dashboard
   
   ## 🎯 Ready (3)
   - #23 Add authentication flow
   - #24 Create dashboard layout
   
   ## 🚧 In Progress (2) [WIP Limit: 3]
   - #21 Fix button styles ✅ Design Valid
   - #22 Add form validation ❌ 3 violations
   
   ## 👀 In Review (1)
   - #20 Add navigation component (PR #89)
   
   ## 🚫 Blocked (1)
   - #19 Payment integration (waiting for API keys)
   ```

### View: SPRINT
1. **Get Current Sprint Issues**
   ```typescript
   // Use milestone as sprint
   const sprint = await github.listIssues({
     milestone: 'Sprint 23',
     state: 'all'
   });
   ```

2. **Calculate Sprint Metrics**
   ```markdown
   # Sprint 23 Overview
   
   ## Progress: ████████░░ 80%
   - Completed: 8/10 issues
   - In Progress: 2 issues
   - Design Compliance: 100%
   
   ## Burndown
   Day 1: ██████████ 10 issues
   Day 3: ████████░░ 8 issues  
   Day 5: ██████░░░░ 6 issues
   Day 7: ████░░░░░░ 4 issues
   Day 9: ██░░░░░░░░ 2 issues
   ```

### View: MY-WORK
1. **Get Assigned Issues**
   ```typescript
   const myIssues = await github.listIssues({
     assignee: '@me',
     state: 'open'
   });
   ```

2. **Check Local Worktrees**
   ```bash
   # Match issues to worktrees
   git worktree list | grep -E "[0-9]+"
   ```

3. **Generate Personal Dashboard**
   ```markdown
   # My Work Dashboard
   
   ## 🔴 Due Today (1)
   - #23 Auth flow - ⚠️ 2 design violations
     Worktree: `feature/23-auth`
     Next: Run `/validate-design --fix`
   
   ## 🟡 Due This Week (2)
   - #24 Dashboard layout - ✅ Ready to start
   - #25 User settings - 🚫 Blocked on #23
   
   ## 🟢 Upcoming (3)
   - #26 Search feature
   - #27 Analytics
   - #28 Reports
   
   ## 📊 Your Stats This Week
   - Completed: 3 issues
   - PRs Merged: 2
   - Design Violations Fixed: 12
   - Code Coverage: 87%
   ```

### View: VALIDATION-STATUS
1. **Scan All Active Branches**
   ```bash
   # Check each worktree
   for worktree in $(git worktree list --porcelain | grep "worktree" | cut -d' ' -f2); do
     cd $worktree
     npm run validate:design --json > validation.json
   done
   ```

2. **Generate Compliance Report**
   ```markdown
   # Design System Compliance Report
   
   ## ✅ Fully Compliant (3)
   - #20 Navigation component
   - #21 Button fixes
   - #18 Card updates
   
   ## ⚠️ Minor Violations (2)
   - #23 Auth flow
     - 2 typography violations (text-sm used)
     - 1 spacing violation (p-5 used)
   - #24 Dashboard
     - 3 color distribution warnings
   
   ## ❌ Major Violations (1)
   - #22 Form validation
     - 8 typography violations
     - 5 spacing violations
     - Touch targets too small (h-10)
   
   ## 📈 Trend
   Week 1: 45% compliant
   Week 2: 67% compliant
   Week 3: 89% compliant ↗️
   ```

## Integration with Other Commands:

```bash
# Check board before starting work
/issue-kanban board

# See your assignments
/issue-kanban my-work

# Start highest priority
/feature-workflow start 23

# Check sprint progress
/issue-kanban sprint

# Validate all active work
/issue-kanban validation-status
```

## Why This Matters:

1. **Visibility** - See all work at a glance
2. **Prioritization** - Clear what to work on next
3. **Compliance Tracking** - Design system status visible
4. **WIP Limits** - Prevent overcommitment
5. **Progress Tracking** - Sprint burndown and velocity

This command bridges the gap between GitHub MCP (raw issue data) and project management needs (visualization and workflow).
