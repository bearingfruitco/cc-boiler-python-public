# Documentation Structure

This directory contains all documentation for the Python Boilerplate project.

## Organization

```
docs/
├── architecture/      # System architecture and design
├── guides/           # How-to guides and tutorials
├── development/      # Development-specific documentation
├── workflow/         # Workflow documentation
├── examples/         # Code examples and patterns
├── project/          # Project templates and PRDs
├── updates/          # Change logs and update summaries
├── troubleshooting/  # Common issues and solutions
├── claude/           # Claude-specific documentation
├── archive/          # Deprecated documentation
└── README.md         # This file
```

## Key Documents

### Getting Started
- [SYSTEM_OVERVIEW.md](./SYSTEM_OVERVIEW.md) - High-level system overview
- [FEATURE_MATRIX.md](./FEATURE_MATRIX.md) - Feature comparison matrix
- [guides/COMMAND_DECISION_GUIDE.md](./guides/COMMAND_DECISION_GUIDE.md) - When to use which command

### Security & Compliance
- [SECURITY_GUIDE.md](./SECURITY_GUIDE.md) - Security best practices
- [RELEASES.md](./RELEASES.md) - Release history

### Claude Code Integration
- [claude/](./claude/) - Claude-specific documentation
- [.claude/docs/](./../.claude/docs/) - System documentation for Claude Code

## Quick Links

- **For new users**: Start with [SYSTEM_OVERVIEW.md](./SYSTEM_OVERVIEW.md)
- **For commands**: See [guides/COMMAND_DECISION_GUIDE.md](./guides/COMMAND_DECISION_GUIDE.md)
- **For workflows**: Check [workflow/](./workflow/)
- **For examples**: Browse [examples/](./examples/)

## Documentation Standards

1. All documentation should be in Markdown format
2. Use clear, descriptive filenames
3. Include a table of contents for long documents
4. Update the appropriate index when adding new docs
5. Move deprecated docs to `archive/` rather than deleting
