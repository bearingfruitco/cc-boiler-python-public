# 📋 Release Notes

## Current Version: v2.4.0

### Latest Release: [Smart Issue Creation & Dependency Tracking](releases/v2.4.0-smart-issue-creation.md)
*Released: January 2025*

Intelligent context capture and dependency management for Python AI-assisted development. Prevents duplicate work and tracks component dependencies.

---

## Release History

### v2.4.x Series - Python Development Intelligence

- **[v2.4.0](releases/v2.4.0-smart-issue-creation.md)** - Smart Issue Creation & Dependency Tracking
  - Capture-to-Issue system (`/cti`) for AI responses → GitHub issues
  - Python dependency management with `@imported-by` annotations
  - Creation guard prevents duplicate components
  - Automatic import updates after refactoring
  - New commands: `/cti`, `/pydeps`, `/pyexists`, `/pysimilar`

### v2.3.x Series - AI Enhancement Features

- **[v2.3.6](releases/v2.3.6-async-architecture.md)** - Async Event-Driven Architecture
  - Event queue system for fire-and-forget operations
  - Lead form event hooks with automatic tracking
  - Async pattern detection and enforcement
  - Required loading states for all async operations
  - New commands: `/prd-async`, `/create-event-handler`, `/validate-async`

- **[v2.3.5](releases/v2.3.5.md)** - Research Management System
  - Smart document updates (no more v1, v2, v3 versions)
  - Automatic organization in `.claude/research/`
  - Context-aware loading with strict limits

- **[v2.3.4](releases/v2.3.4.md)** - CodeRabbit IDE Integration
  - Real-time code review in Cursor/VSCode
  - 95% bug catch rate before commit
  - Dual-AI workflow (Claude generates, CodeRabbit reviews)

- **[v2.3.3](releases/v2.3.3.md)** - Hook System Enhancements
  - PreCompact support for context preservation
  - Suggestion engine for design violations
  - Command logging and analytics

- **[v2.3.2](releases/v2.3.2.md)** - GitHub Apps Integration
  - CodeRabbit and Claude Code apps
  - Repository safety features
  - Package version updates

- **[v2.3.1](releases/v2.3.1.md)** - Workflow Enhancement
  - Smart auto-approval for safe operations
  - No more permission prompt interruptions

### v2.3.0 Series - Grove-Inspired Features

See [CHANGELOG.md](CHANGELOG.md) for complete version history.

---

## Quick Links

- **[Latest Release](releases/v2.4.0-smart-issue-creation.md)** - Full details on newest features
- **[Changelog](CHANGELOG.md)** - Complete version history
- **[Upgrade Guide](guides/upgrading.md)** - Migration instructions
- **[All Releases](releases/)** - Detailed release notes

## Release Schedule

We follow semantic versioning and typically release:
- **Patch versions** (x.x.1) - Bug fixes, weekly as needed
- **Minor versions** (x.1.x) - New features, bi-weekly
- **Major versions** (1.x.x) - Breaking changes, quarterly

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute to the project.
