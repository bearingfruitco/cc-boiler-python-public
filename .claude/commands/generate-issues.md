# Generate GitHub Issues from PRD (Enhanced)

Converts your PROJECT_PRD.md or feature PRDs into GitHub issues in the CORRECT repository.

## Usage

```bash
/generate-issues PROJECT     # From PROJECT_PRD.md
/gi PROJECT                  # Short alias

/generate-issues [feature]   # From feature PRD
/gi user-dashboard          # Example
```

## Repository Safety Check

Before creating any issues, the command now:

1. **Verifies Repository Configuration**:
   ```
   Checking repository configuration...
   Current repo: YOUR_USERNAME/YOUR_REPO_NAME ✓
   
   ⚠️  ERROR if still pointing to boilerplate:
   Cannot create issues in boilerplate repository!
   Run /init-project first to configure YOUR repository.
   ```

2. **Confirms Target Repository**:
   ```
   Will create issues in: YOUR_USERNAME/YOUR_REPO_NAME
   
   Is this correct? (y/n): y
   ```

3. **Checks GitHub App Permissions**:
   ```
   Checking GitHub permissions...
   ✓ Write access to issues
   ✓ Write access to pull requests
   ```

## What It Does

### For PROJECT-level:
1. Reads `docs/project/PROJECT_PRD.md`
2. Verifies target repository
3. Extracts each major feature
4. Creates GitHub issues in YOUR repo
5. Updates `docs/project/ISSUE_MAP.md`

### For feature-level:
1. Reads `docs/project/features/[feature]-PRD.md`
2. Creates sub-issues for complex features
3. Links to parent issue
4. Updates issue map

## Example Flow

```bash
# After /init-project creates PROJECT_PRD.md:
/gi PROJECT

# Output:
Repository Check:
  Target: shawnsmith/tofu-quiz-app ✓
  Apps: CodeRabbit ✓, Claude Code ✓

Creating issues from PROJECT_PRD.md...
✓ Issue #1: User Authentication System
  → https://github.com/shawnsmith/tofu-quiz-app/issues/1
✓ Issue #2: Quiz Creation & Management  
  → https://github.com/shawnsmith/tofu-quiz-app/issues/2
✓ Issue #3: Quiz Taking Flow
  → https://github.com/shawnsmith/tofu-quiz-app/issues/3

Created 3 issues in shawnsmith/tofu-quiz-app
Updated: docs/project/ISSUE_MAP.md
```

## Enhanced Issue Template

Each issue now includes:

```markdown
## 🎯 Feature: [Feature Name]

### 📋 Description
[From PRD description]

### ✅ Acceptance Criteria
- [ ] Criterion 1 from PRD
- [ ] Criterion 2 from PRD
- [ ] Criterion 3 from PRD

### 🔗 References
- PRD: `docs/project/PROJECT_PRD.md#feature-name`
- Related: #[other-issue-numbers]

### 🤖 AI Review Configuration
- CodeRabbit: Enabled ✓
- Claude Code: Enabled ✓

### 📏 Sizing
Estimated: [S/M/L/XL based on PRD complexity]

---
*Generated from PRD by Claude Code Boilerplate*
```

## ISSUE_MAP.md Enhanced Format

```markdown
# Issue Map

**Repository**: shawnsmith/tofu-quiz-app
**Generated**: 2024-12-30 10:00 AM
**GitHub Apps**: CodeRabbit ✓, Claude Code ✓

## PROJECT_PRD.md → GitHub Issues

| Feature | Issue | Status | Branch | PR | AI Reviews |
|---------|-------|--------|--------|----|-----------| 
| User Authentication | [#1](https://github.com/shawnsmith/tofu-quiz-app/issues/1) | Open | - | - | Pending |
| Quiz Creation | [#2](https://github.com/shawnsmith/tofu-quiz-app/issues/2) | Open | - | - | Pending |
| Quiz Taking | [#3](https://github.com/shawnsmith/tofu-quiz-app/issues/3) | Open | - | - | Pending |

## Feature PRDs → Sub-Issues

| Parent | Feature PRD | Sub-Issues | Status |
|--------|------------|------------|--------|
| #1 | user-auth-PRD.md | #4, #5, #6 | In Progress |

Last updated: [timestamp]
```

## Configuration Check

Reads from `.claude/project-config.json`:
```json
{
  "repository": {
    "owner": "shawnsmith",
    "name": "tofu-quiz-app",
    "branch": "main"
  }
}
```

If this file is missing or still shows boilerplate:
```
❌ ERROR: Repository not configured!
   
   Please run /init-project first to set up your repository.
   
   Current config shows: bearingfruitco/claude-code-boilerplate
   This would create issues in the WRONG repository!
```

## Integration with Workflow

```bash
/init-project        # Sets up YOUR repo (required first!)
/gi PROJECT          # Creates issues in YOUR repo
/fw start 1          # Works with YOUR repo's issue #1
/prd user-auth       # Creates feature PRD
/gt user-auth        # Generates tasks
/pt user-auth        # Processes tasks
/fw complete 1       # Creates PR in YOUR repo
```

## Batch Operations

New capability for multiple features:
```bash
/gi PROJECT --batch  # Creates all issues at once

# Or selectively:
/gi PROJECT --only "auth,quiz"  # Just these features
```

## Safety Features

1. **Never creates issues in boilerplate repo**
2. **Always shows target repo before creating**
3. **Validates GitHub App permissions**
4. **Creates backup in `docs/project/issues-backup.json`**
5. **Dry run mode**: `/gi PROJECT --dry-run`

This ensures your issues always go to the right place!
