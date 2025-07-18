# Generate GitHub Issues from PRD

Converts your PROJECT_PRD.md or feature PRDs into GitHub issues.

## Usage

```bash
/generate-issues PROJECT     # From PROJECT_PRD.md
/gi PROJECT                  # Short alias

/generate-issues [feature]   # From feature PRD
/gi user-dashboard          # Example
```

## What It Does

### For PROJECT-level:
1. Reads `docs/project/PROJECT_PRD.md`
2. Extracts each major feature from Core Features section
3. Creates a GitHub issue for each feature
4. Links issues in `docs/project/ISSUE_MAP.md`

### For feature-level:
1. Reads `docs/project/features/[feature]-PRD.md`
2. Creates sub-issues for complex features
3. Updates issue map

## Example Flow

```bash
# After /init-project creates PROJECT_PRD.md:
/gi PROJECT

# Output:
Creating issues from PROJECT_PRD.md...
✓ Issue #1: User Authentication System
✓ Issue #2: Quiz Creation & Management
✓ Issue #3: Quiz Taking Flow
✓ Issue #4: Score Tracking & Progress
✓ Issue #5: User Dashboard

Created 5 issues. See docs/project/ISSUE_MAP.md
```

## Issue Template

Each issue includes:
- Clear title from PRD
- Description from PRD section
- Acceptance criteria
- Labels: `feature`, `mvp`
- Milestone if applicable

## ISSUE_MAP.md Format

```markdown
# Issue Map

## PROJECT_PRD.md → GitHub Issues

| Feature | Issue | Status | Branch |
|---------|-------|--------|--------|
| User Authentication | #1 | Open | - |
| Quiz Creation | #2 | Open | - |
| Quiz Taking | #3 | Open | - |
| Score Tracking | #4 | Open | - |
| User Dashboard | #5 | Open | - |

Last updated: [timestamp]
```

## Integration with Workflow

```bash
/init-project        # Creates PROJECT_PRD.md
/gi PROJECT          # Creates GitHub issues
/fw start 1          # Start working on issue #1
/prd user-auth       # Create detailed feature PRD
/gt user-auth        # Generate tasks
/pt user-auth        # Process tasks
/fw complete 1       # Create PR that closes #1
```

This maintains the complete chain from vision → issues → features → tasks → code → PR!
