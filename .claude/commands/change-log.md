# Change Log

Track and document all significant changes to the codebase.

## Arguments:
- $ACTION: add|view|sync|report
- $TYPE: feature|fix|refactor|docs|breaking
- $SCOPE: component|api|design|config

## Why This Command:
- Document all changes
- Update affected docs automatically
- Maintain project history
- Sync with git commits

## Steps:

### Action: ADD
Document a change:

```bash
# Automatically triggered after commits
/change-log add feature "Added user authentication"

# Creates entry
{
  "id": "change-001",
  "timestamp": "2024-01-15T14:30:00Z",
  "type": "feature",
  "scope": "auth",
  "description": "Added user authentication",
  "commit": "abc123",
  "files": [
    "components/auth/LoginForm.tsx",
    "app/api/auth/route.ts"
  ],
  "breaking": false,
  "docs_updated": [],
  "todos": []
}

# Analyzes impact
echo "## 📝 Change Recorded"
echo ""
echo "### Impact Analysis"
echo "- Components affected: 2"
echo "- API routes: 1 new"
echo "- Breaking change: No"
echo ""
echo "### Documentation to Update"
echo "- [ ] API docs: Add auth endpoints"
echo "- [ ] Component docs: LoginForm usage"
echo "- [ ] README: Add auth setup"
echo ""
echo "### Auto-Updates"
echo "✅ Updated PROJECT_CONTEXT.md"
echo "✅ Added to CHANGELOG.md"
echo "⚠️  PRD needs manual update for auth feature"
```

### Automatic Documentation Updates

#### 1. PROJECT_CONTEXT.md
```markdown
# Working Context
Project: MyApp
Last Updated: 2024-01-15 14:30
++Latest Change: Added user authentication

## Recent Changes
- 2024-01-15: Added user authentication (feature)
- 2024-01-14: Fixed button spacing (fix)
- 2024-01-13: Refactored API client (refactor)
```

#### 2. Component Registry
```typescript
// Auto-updated components.json
{
  "components": {
    "auth/LoginForm": {
      "created": "2024-01-15",
      "lastModified": "2024-01-15",
      "type": "feature",
      "dependencies": ["Button", "Input", "Card"],
      "tests": true,
      "docs": false  // Flagged for update
    }
  }
}
```

#### 3. API Documentation
```yaml
# Auto-updated openapi.yaml
paths:
  /api/auth/login:
    post:
      summary: User login
      tags: [Authentication]
      added: "2024-01-15"
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginRequest'
```

### Git Integration

#### Pre-Commit Hook
```bash
#!/bin/bash
# .husky/pre-commit

# Get staged files
STAGED=$(git diff --cached --name-only)

# Detect change type
if echo "$STAGED" | grep -q "components/"; then
  SCOPE="component"
elif echo "$STAGED" | grep -q "app/api/"; then
  SCOPE="api"
fi

# Prompt for change description
echo "Describe this change:"
read DESCRIPTION

# Record change
/change-log add auto "$DESCRIPTION" --scope=$SCOPE
```

#### Post-Commit Hook
```bash
#!/bin/bash
# .husky/post-commit

# Get commit info
COMMIT=$(git rev-parse HEAD)
MESSAGE=$(git log -1 --pretty=%B)

# Update change log
/change-log sync $COMMIT "$MESSAGE"

# Check for needed updates
/change-log check-docs
```

### Viewing Changes

```bash
/change-log view

## 📋 Recent Changes

### Today (3 changes)
- 14:30 - ✨ Added user authentication [abc123]
  Files: 2 | Docs: ⚠️ Needs update
  
- 11:45 - 🐛 Fixed button spacing in LoginForm [def456]
  Files: 1 | Docs: ✅ Updated
  
- 09:20 - ♻️ Refactored API client for better errors [ghi789]
  Files: 3 | Docs: ✅ Updated

### This Week (12 changes)
[... more entries ...]

### Pending Documentation
- auth/LoginForm.tsx - Usage guide needed
- api/auth/route.ts - Endpoint docs needed
- README.md - Add auth setup section
```

### Documentation Sync

```bash
/change-log sync-docs

## 🔄 Syncing Documentation

### Checking for updates needed...
- components/auth/LoginForm.tsx → docs/components/auth.md
  Status: ⚠️ Missing documentation
  Action: Creating template...
  
- app/api/auth/route.ts → docs/api/auth.md
  Status: ⚠️ Outdated
  Action: Updating endpoints...

### Updating Project Docs
- README.md: Adding auth section
- CHANGELOG.md: Adding today's changes
- PROJECT_CONTEXT.md: Updating latest changes

### Results
✅ Created 1 new doc
✅ Updated 3 existing docs
⚠️ 2 docs need manual review

Run `/generate-docs` to complete documentation
```

### Smart PRD Updates

```typescript
// When significant changes detected
if (isBreakingChange || isNewFeature) {
  console.log(`
  ## ⚠️ PRD Update Needed
  
  Detected: ${changeType}
  Feature: ${description}
  
  ### Suggested PRD Updates:
  1. Add to "Features" section:
     - ${featureDescription}
  
  2. Update "Technical Requirements":
     - Authentication: Supabase Auth
     - Session management: JWT
  
  3. Update "User Stories":
     - As a user, I can log in
     - As a user, I can reset password
  
  Create PR for PRD? (Y/n)
  `);
}
```

### Change Report

```bash
/change-log report weekly

## 📊 Weekly Change Report

### Summary
- Total Changes: 47
- Features: 12 (26%)
- Fixes: 23 (49%)
- Refactors: 8 (17%)
- Docs: 4 (8%)

### Major Features
1. User Authentication System
2. Dashboard Analytics
3. File Upload Support

### Breaking Changes
None this week ✅

### Documentation Status
- Updated: 34/47 (72%)
- Pending: 13 items
- Auto-updated: 28 items

### Git Statistics
- Commits: 89
- Lines added: +2,847
- Lines removed: -1,235
- Files changed: 134

### Recommendations
1. Update PRD for auth feature
2. Document new API endpoints
3. Add migration guide for users
```

## Configuration

```json
{
  "changeLog": {
    "autoTrack": true,
    "updateDocs": true,
    "requireDescription": true,
    "syncWithGit": true,
    "notifyOn": ["breaking", "feature"],
    "documentationPaths": {
      "components": "docs/components",
      "api": "docs/api",
      "guides": "docs/guides"
    }
  }
}
```

## Integration with Other Commands

```bash
# After creating component
/cc ui AuthButton
> "Change logged: New component AuthButton"
> "Docs template created: docs/components/ui.md"

# After feature complete
/fw complete 23
> "Change logged: Feature #23 - Authentication"
> "PRD update suggested - review needed"
> "4 documentation files updated"

# Regular commits
git commit -m "feat: add password reset"
> "Change logged automatically"
> "Documentation sync pending"
```

This ensures all changes are tracked and documentation stays current!
