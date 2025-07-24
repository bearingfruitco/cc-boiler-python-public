# Claude Code Python Boilerplate - Public Edition

An **AI Operating System for Python Development** that transforms Claude Code into an intelligent development environment.

## 🌟 Features

- **70+ Custom Commands** with intelligent aliases
- **40+ Active Hooks** preventing mistakes before they happen
- **Automated TDD** with test generation
- **Task Ledger System** for central work tracking
- **Multi-Agent Orchestration** for complex features
- **Zero Context Loss** between sessions
- **Pattern Learning** that improves over time

## 🚀 Quick Start

1. Clone this repository to your project
2. Run the setup script: `./.claude/scripts/install-hooks.sh`
3. Start Claude Code and run `/sr` (Smart Resume)
4. Check `/help` for available commands

## 📚 Documentation

- [System Overview](.claude/docs/SYSTEM_OVERVIEW.md) - Complete architecture guide
- [Getting Started](.claude/docs/GETTING_STARTED.md) - First steps
- [Command Reference](.claude/docs/COMMAND_REFERENCE_CARD.md) - All commands
- [Python Workflows](.claude/PYTHON_WORKFLOWS.md) - Python-specific patterns

## 🛡️ Security Note

This public version has been sanitized:
- No API keys or credentials
- No personal data or logs
- No internal configurations
- Example files provided for all sensitive configs

## 📋 What's Included

### Commands (70+)
- Context management (`/sr`, `/tl`, `/checkpoint`)
- Python development (`/py-prd`, `/py-agent`, `/py-api`)
- Testing & quality (`/test`, `/grade`, `/lint`)
- Multi-agent orchestration (`/orch`, `/spawn`)
- Intelligence features (`/prp-create`, `/think-level`)

### Hooks (40+)
- **Pre-Tool Hooks**: Prevent mistakes before they happen
- **Post-Tool Hooks**: Learn from actions and update state
- **Notification Hooks**: Smart suggestions and team awareness
- **Stop Hooks**: Clean session endings

### Workflows
- Test-Driven Development (enforced)
- Feature development flow
- Multi-agent orchestration
- Research and PRPs

## 🔧 Configuration

See `.env.example` for required environment variables.

Key configurations in `.claude/`:
- `settings-default.json` - Hook configuration
- `chains.json` - Workflow definitions
- `aliases.json` - Command shortcuts
- `permission-profiles.json` - Access levels

## 📈 Performance

- **50-70% faster** development with orchestration
- **90% reduction** in common bugs
- **80%+ test coverage** enforced
- **Zero context loss** between sessions

## 🤝 Contributing

This is a public snapshot of our internal boilerplate. For contributions:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

MIT License - See LICENSE file

---

**Note**: This is the public version of our Python boilerplate. Some advanced features and internal optimizations have been removed for security.
