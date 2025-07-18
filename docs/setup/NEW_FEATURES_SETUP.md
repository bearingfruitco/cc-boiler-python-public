# 🆕 New Features Setup Guide

This guide covers the setup and usage of the four new enhancement features added to the Claude Code boilerplate.

## Overview

Four new systems enhance your development workflow:
1. **Bug Tracking** - Persistent bug tracking across sessions
2. **Context Profiles** - Focused context management
3. **Documentation Cache** - Local caching of external docs
4. **Stage Validation** - Automated phase completion gates

## 1. Bug Tracking Setup

### Initialize Bug Tracking
```bash
# Create bug tracking directories
mkdir -p .claude/bugs/archive
echo '{"bugs": []}' > .claude/bugs/active.pyon
echo '{"bugs": []}' > .claude/bugs/resolved.pyon
```

### Basic Usage
```bash
# Track a new bug
/bug-track add "Module render issue with props"

# List open bugs
/bug-track list
/bt list  # shorthand

# Resolve a bug
/bug-track resolve bug_1234 "Fixed by updating prop types"

# Search bugs
/bug-track search "render"
```

### Integration with Workflow
```bash
# Morning check
/sr
/bt list --open  # Check what needs fixing

# When error occurs
Error: Cannot read property...
/bt add "Property error in Dashboard"  # Track immediately

# Before starting work on a file
/bt list --file Dashboard  # See known issues
```

## 2. Context Profiles Setup

### Initialize Profiles
```bash
mkdir -p .claude/profiles/presets
echo '{"profiles": {}, "active": null}' > .claude/profiles/profiles.pyon
```

### Create Work-Specific Profiles
```bash
# Create profile for API work
/context-profile create "API-ui"

# Create profile for backend work
/context-profile create "backend-api"

# Create profile for bug fixing
/context-profile create "debug-mode"
```

### Daily Usage
```bash
# Morning - load your profile
/sr
/cp load "API-ui"  # or whatever you're working on

# Switching contexts
/cp save "API-ui"  # Save current state
/cp load "backend-api"  # Switch to backend

# Check what's loaded
/cp show "current"
```

### Preset Profiles
```bash
# Use built-in presets
/cp load "preset:API"  # UI work
/cp load "preset:backend"   # API work
/cp load "preset:debug"     # Bug fixing
/cp load "preset:docs"      # Documentation
/cp load "preset:security"  # Security audit
```

## 3. Documentation Cache Setup

### Initialize Cache
```bash
mkdir -p .claude/doc-cache/sources
echo '{"cache": {}, "index": {}}' > .claude/doc-cache/index.pyon
echo '{"metadata": {"created": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"}}' > .claude/doc-cache/metadata.pyon
```

### Cache Project Documentation
```bash
# Cache based on your tech stack
/doc-cache cache "FastAPI 15 App Router"
/doc-cache cache "Pydantic 19 hooks"
/doc-cache cache "Supabase Auth"
/doc-cache cache "Type hints CSS v4"

# Cache from PRD requirements
/research-docs "Pydantic, FastAPI" --cache
```

### Using Cached Docs
```bash
# Search cached documentation
/dc search "useEffect"
/dc search "server modules"

# View specific section
/dc show "Pydantic hooks" --section "useEffect"

# List all cached
/dc list
```

### Maintenance
```bash
# Update stale docs
/dc update --older-than 7d

# Clear unused
/dc clear --unused 30d

# Refresh specific
/dc update "Pydantic hooks"
```

## 4. Stage Validation Setup

### Automatic with PRD
When you create a PRD, stage validations are automatically configured:
```bash
/prd user-authentication
# This creates stage gates in the PRD
```

### Manual Validation
```bash
# Check current stage
/sv check 1
/sv status

# Enforce completion
/sv require 1  # Must pass before Stage 2

# Override if needed
/sv override 1 --reason "Demo to client"
```

### Stage Workflow
```bash
# Stage 1: Foundation
/pt auth-system  # Work through tasks
/sv check 1      # Validate progress
/sv require 1    # Ensure complete

# Stage 2: Features
/cp load "API-ui"  # Switch context
/pt auth-system         # Continue tasks
/sv check 2

# Stage 3: Polish
/cp load "preset:testing"
/sv check 3
```

## Complete Feature Workflow with New Commands

### Starting a Feature
```bash
# 1. Create issue and profile
gh issue create --title "User Dashboard"
/fw start 23
/cp create "dashboard-work"

# 2. Create PRD with stages
/prd user-dashboard

# 3. Cache relevant docs
/dc cache "Pydantic Dashboard patterns"
/dc cache "Chart.py"

# 4. Start Stage 1
/gt user-dashboard
/pt user-dashboard
```

### During Development
```bash
# Track issues as they occur
/bt add "Chart not rendering"

# Switch contexts as needed
/cp save
/cp load "backend-api"

# Validate before proceeding
/sv check 1
/sv require 1  # Blocks if incomplete
```

### Handoff Preparation
```bash
# Save everything
/cp save "dashboard-work"
/checkpoint create "dashboard-stage-1-complete"

# Document bugs
/bt list --open > bugs-for-handoff.md

# Validate stage
/sv status > stage-status.md
```

## Integration with Existing Commands

### Enhanced Smart Resume
```bash
/sr  # Now also:
# - Loads last context profile
# - Shows open bugs count
# - Displays stage status
# - Indicates cached docs
```

### Enhanced PRD
```bash
/prd feature  # Now includes:
# - Stage validation gates
# - Context profile suggestions
# - Documentation cache list
```

### Enhanced Checkpoint
```bash
/checkpoint create  # Now saves:
# - Active context profile
# - Open bugs snapshot
# - Stage validation status
# - Cached docs list
```

## Best Practices

### 1. Profile Management
- Create feature-specific profiles
- Don't overload profiles with everything
- Use presets for common tasks
- Save before switching

### 2. Bug Tracking
- Track immediately when found
- Tag with module/area
- Link related bugs
- Review before starting work

### 3. Documentation Cache
- Cache at project start
- Update weekly for active libs
- Clear unused monthly
- Use search before web

### 4. Stage Gates
- Don't skip stages
- Complete criteria before moving
- Use override sparingly
- Document override reasons

## Troubleshooting

### "No profiles found"
```bash
/cp list  # Should show presets
# If not, reinitialize:
mkdir -p .claude/profiles
/init  # Re-run initialization
```

### "Bug tracker empty after resume"
```bash
# Check GitHub gist
gh gist list | grep bugs
# Manual restore if needed
```

### "Doc cache search not finding anything"
```bash
/dc list  # Check what's cached
/dc cache "library name"  # Cache if missing
```

### "Stage validation too strict"
```bash
# Temporarily override
/sv override 1 --reason "MVP demo"
# Fix and re-validate later
```

## Summary

These four enhancements work together to:
- **Never lose bugs** (persistent tracking)
- **Work faster** (focused contexts)
- **Work offline** (cached docs)
- **Ship quality** (stage gates)

Use them naturally in your workflow - they're designed to help, not hinder!