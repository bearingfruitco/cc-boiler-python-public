---
name: context-profile
aliases: [cp, profile]
description: Manage and switch between context profiles including permission profiles
category: workflow
---

Manage context profiles including permission profiles, work contexts, and saved states.

## Usage
```bash
/context-profile [action] [profile_name]
/cp [action] [profile_name]
```

## Actions

### load
Load a context profile (including permission profile):
```bash
/cp load exploration     # Switch to exploration mode
/cp load development     # Standard development mode
/cp load testing         # Testing mode with broader permissions
/cp load ci_pipeline     # CI/CD mode
```

### save
Save current context as a profile:
```bash
/cp save my-feature      # Save current state
/cp save debug-session   # Save debug context
```

### list
Show available profiles:
```bash
/cp list
# Shows: exploration, development, testing, ci_pipeline, + custom profiles
```

### current
Show current profile:
```bash
/cp current
# Shows: Current profile: development (standard permissions)
```

## Integration with Permission Profiles

When loading a profile, it automatically:
1. Sets the corresponding permission profile
2. Loads saved context state
3. Restores working directory
4. Applies profile-specific settings

## Permission Profile Details

### exploration
- Read-only access to codebase
- No file modifications allowed
- Safe for browsing unfamiliar code

### development (default)
- Standard development permissions
- Auto-approves test/cache writes
- Requires approval for sensitive operations

### testing
- Broader file access for test runs
- Auto-approves all test-related operations
- Still blocks dangerous commands

### ci_pipeline
- Maximum automation
- Auto-approves most operations
- Only blocks catastrophic commands

### multi_agent
- Optimized for orchestration
- Allows parallel file operations
- Maintains safety for production files

## Examples

### Switch to exploration mode
```bash
/cp load exploration
# Now in read-only mode
```

### Save feature context
```bash
/cp save auth-feature
# Saves current state, permissions, and context
```

### Check current mode
```bash
/cp current
# Current profile: development
# Permission level: standard
# Context size: 45,230 tokens
```

## State Persistence

Profiles are saved in:
- `.claude/profiles/[name].json` - Profile configuration
- `.claude/profiles/[name]-state.json` - Context state
- `.claude/permission-profiles.json` - Permission rules

This integrates with Smart Resume (`/sr`) for seamless context switching.
