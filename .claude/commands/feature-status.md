---
name: feature-status
aliases: [fs, feature-info]
description: Check feature completion status and implementation details
category: branch-management
---

Check the status of a specific feature:
- Is it complete or in progress?
- What branch has the latest version?
- What's the working implementation?
- Are there enhancements in progress?

## Usage
```bash
/feature-status [feature-name]
/fs auth  # Check auth feature status
```

## What It Shows

### Feature Information
- Completion status
- Implementation description
- Key components/functions
- Test coverage
- Files involved

### Branch Information
- Which branch has the feature
- Any enhancement branches
- Modification history

### Implementation Details
- Working patterns
- Key functions/classes
- Performance metrics
- Known issues

## Output Example
```
📦 Feature: user-authentication
✅ Status: Completed (2025-07-15)
🌿 Stable Branch: main

📝 Working Implementation:
- Description: JWT-based auth with Redis sessions
- Key Components:
  • login() - Handle user login
  • logout() - Clear sessions
  • validate_token() - JWT validation
  • AuthMiddleware - Request authentication
- Test Coverage: 95%
- Performance: <50ms average

📄 Files:
- src/auth/login.py
- src/auth/middleware.py
- src/auth/validators.py
- tests/test_auth.py

🔧 Enhancement in Progress:
- Issue: #45 - Add 2FA support
- Branch: feature/auth-2fa
- Developer: team member
- Adding: Two-factor authentication

⚠️ Protection Status:
- Do not recreate: YES
- Files are protected on main

💡 To enhance this feature:
1. Create branch from main: git checkout -b feature/enhance-auth
2. Or continue on: feature/auth-2fa
```

## Integration with Workflow

The feature status integrates with:
- `/fw start` - Checks feature status before starting
- `/py-prd` - References completed features
- Branch protection hooks - Prevents recreation

## Related Commands
- `/branch-status` - Overall branch health
- `/truth` - See protected features
- `/feature-list` - List all tracked features
