# Feature Workflow Command

Orchestrates issue-based development with design validation, complementing GitHub MCP.

## Arguments:
- $ACTION: start|validate|complete
- $ISSUE_NUMBER: GitHub issue number

## Why This Command:
GitHub MCP handles Git operations, but doesn't:
- Enforce design system rules
- Manage worktrees
- Create issue-based workflows
- Auto-generate compliant code

## Steps:

### Action: START
1. **Use MCP to Get Issue**
   ```typescript
   // MCP handles this
   const issue = await github.getIssue(ISSUE_NUMBER);
   ```

2. **Create Worktree** (Not in MCP)
   ```bash
   # Extract requirements from issue
   BRANCH_NAME="feature/${ISSUE_NUMBER}-${SLUG}"
   WORKTREE_PATH="../$(basename $(pwd))-worktrees/$BRANCH_NAME"
   
   # Create isolated workspace
   git worktree add -b $BRANCH_NAME $WORKTREE_PATH origin/main
   ```

3. **Generate Implementation Plan**
   ```markdown
   # Feature Plan: ${issue.title}
   
   ## Requirements from Issue:
   ${parseRequirements(issue.body)}
   
   ## Components to Create:
   ${identifyComponents(issue.body)}
   
   ## Design System Checklist:
   - [ ] Typography: 4 sizes, 2 weights
   - [ ] Spacing: 4px grid
   - [ ] Touch targets: 44px+
   - [ ] Mobile-first
   ```

4. **Scaffold Initial Files**
   Based on issue requirements, create:
   - Component stubs with design system
   - Test file templates
   - Documentation updates

### Action: VALIDATE
1. **Pre-Commit Validation**
   ```bash
   # Run design system check
   npm run validate:design || {
     echo "❌ Fix violations before committing"
     exit 1
   }
   ```

2. **Generate Commit Message**
   ```typescript
   // Smart commit with issue linking
   const files = await git.status();
   const message = generateCommitMessage(files, ISSUE_NUMBER);
   // e.g., "feat: add auth components (#23)"
   ```

3. **Use MCP for Commit**
   ```typescript
   // Let MCP handle the actual commit
   await github.commit(message);
   ```

### Action: COMPLETE
1. **Final Validation**
   ```bash
   # Comprehensive checks
   npm run validate:design
   npm test
   npm run build
   ```

2. **Generate PR Body**
   ```markdown
   Closes #${ISSUE_NUMBER}
   
   ## Design System Compliance ✅
   - Typography: 4 sizes, 2 weights only
   - Spacing: 4px grid (validated)
   - Colors: 60/30/10 distribution
   - Touch targets: 44px+ confirmed
   
   ## Changes
   ${generateChangeLog()}
   ```

3. **Use MCP for PR**
   ```typescript
   // MCP creates the PR
   await github.createPullRequest({
     title: `feat: ${issue.title} (#${ISSUE_NUMBER})`,
     body: prBody,
     base: 'main'
   });
   ```

4. **Cleanup Worktree**
   ```bash
   # After merge (not in MCP)
   git worktree remove $WORKTREE_PATH
   ```

## What This Command Adds Beyond MCP:

1. **Design Validation** - Enforced at every step
2. **Worktree Management** - Isolated feature development
3. **Smart Scaffolding** - Generate compliant components
4. **Issue Parsing** - Extract requirements automatically
5. **Workflow Automation** - Orchestrate MCP commands

## Integration Example:

```bash
# Start feature (our command + MCP)
/feature-workflow start 23
# - Creates worktree
# - Generates plan
# - Uses MCP to update issue

# During development
/create-component ui AuthForm
/validate-design

# Complete feature (our command + MCP)
/feature-workflow complete 23
# - Validates design system
# - Uses MCP to create PR
# - Cleans up worktree
```
