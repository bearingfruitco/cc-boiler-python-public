# Getting Started with Python Boilerplate v2.4.2

Welcome to the most intelligent Python development environment! This guide will have you building AI-powered applications in minutes.

## 🚀 10-Minute Quick Start

### 1. Initial Setup (3 minutes)

```bash
# Clone the repository
git clone https://github.com/yourusername/python-boilerplate.git my-project
cd my-project

# Run automatic setup (recommended)
./scripts/setup.sh

# Or manual setup:
poetry install                    # Install dependencies
cp .env.example .env             # Create environment file
chmod +x .claude/hooks/**/*.py   # Make hooks executable
```

### 2. Configure Claude Desktop (2 minutes)

Find your Claude Desktop config:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

Add this configuration:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-filesystem",
        "/absolute/path/to/my-project"
      ]
    }
  }
}
```

**Important**: Use the full absolute path to your project directory!

### 3. Verify Setup (1 minute)

Open Claude Desktop and run:
```bash
/sr              # Should show "Smart Resume Complete"
/help            # Should show command list
/tl              # Should show empty task ledger
```

### 4. Create Your First Feature (4 minutes)

```bash
# Start with smart resume
/sr

# Create a feature specification
/py-prd user-authentication

# Review the generated PRD, then create an issue
/cti "User Authentication System" --tests

# Start working (tests auto-generated!)
/fw start 123    # Use actual issue number

# Work through tasks
/pt user-auth

# Run tests
/test
```

Congratulations! You've just experienced AI-powered development with automatic TDD! 🎉

## 📋 Essential Concepts

### The Task Ledger

Your central command center (`.task-ledger.md`):
- Tracks ALL features and tasks
- Shows real-time progress
- Links to GitHub issues
- Never loses work

```bash
/tl              # View everything
/tl view auth    # Specific feature
/tl update auth  # Update progress
```

### Smart Resume

Never lose context again:
```bash
/sr              # Restores everything instantly
```

This command:
- Loads your last working state
- Shows current task progress
- Suggests next actions
- Reconstructs full context

### Automatic Safety

40+ hooks protect you automatically:
- **Before you code**: Checks for duplicates, validates imports
- **While you code**: Enforces TDD, tracks dependencies
- **After you code**: Updates references, saves state

You don't manage these - they just work!

## 🎯 Common Workflows

### Creating an API Endpoint

```bash
# 1. Define the endpoint
/py-api /users GET POST --auth --pagination

# 2. System automatically:
# - Checks if endpoint exists
# - Generates Pydantic models
# - Creates router with auth
# - Writes comprehensive tests
# - Sets up pagination

# 3. Run tests
/test

# 4. View the generated code
cat src/api/routers/users.py
```

### Building an AI Agent

```bash
# 1. Create the agent
/py-agent EmailAssistant --tools=gmail,calendar

# 2. System creates:
# - Pydantic models for I/O
# - Agent class with tools
# - Memory persistence
# - Async support
# - Full test suite

# 3. Implement logic
# Edit src/agents/email_assistant.py

# 4. Test
/test agents/
```

### Data Pipeline Creation

```bash
# 1. Design pipeline
/py-pipeline CustomerETL --source=api --dest=warehouse

# 2. System generates:
# - Prefect flow structure
# - Error handling
# - Retry logic
# - Monitoring
# - Data validation

# 3. Run pipeline
python -m src.pipelines.customer_etl
```

## 🛠️ Development Patterns

### Pattern 1: TDD Feature Development

```bash
/chain tdd
```

This chain automatically:
1. Creates PRD
2. Generates tests
3. Guides implementation
4. Validates quality
5. Completes feature

### Pattern 2: Multi-Agent Development

For complex features touching multiple domains:

```bash
# 1. Create comprehensive PRD
/py-prd payment-system

# 2. Launch orchestration
/orch payment-system --agents=4

# 3. Monitor progress
/sas

# 4. Integrate results
/orch integrate
```

### Pattern 3: Quick Fixes

```bash
# 1. Create micro task
/mt "fix login timeout bug"

# 2. Make fix
# Edit code...

# 3. Verify
/test --related

# 4. Safe commit
/sc
```

## 🔧 Environment Configuration

### Required Environment Variables

Create `.env` file:
```bash
# AI Models (at least one required)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Database
DATABASE_URL=postgresql://localhost/myapp

# Redis (for agent memory)
REDIS_URL=redis://localhost:6379

# Optional but recommended
GITHUB_TOKEN=ghp_...        # For issue creation
SENTRY_DSN=https://...     # Error tracking
```

### Python Setup

The project uses Poetry for dependency management:

```bash
# Install all dependencies
poetry install

# Add new dependency
poetry add fastapi

# Add dev dependency
poetry add --group dev pytest-mock

# Update dependencies
poetry update
```

### Git Configuration

The system includes git hooks for safety:

```bash
# Install git hooks
./scripts/install-git-hooks.sh

# Hooks will:
# - Run tests before commit
# - Check code quality
# - Validate types
# - Update task ledger
```

## 🐛 Troubleshooting

### "Command not found"

```bash
# Ensure you're in Claude Desktop with MCP configured
/sr              # This should work

# If not, check:
# 1. MCP server is running (check Claude Desktop logs)
# 2. Path in config is absolute
# 3. Hooks have execute permission
```

### "Context not loading"

```bash
# Force full context rebuild
/sr full

# Or load specific profile
/cp load last
```

### "Tests failing"

```bash
# Run with details
/test --verbose

# Check specific test
/test tests/test_auth.py::test_login

# Use AI debugging
/think-level deep
/debug "login test failing with 401"
```

### "Too many tokens"

```bash
# Compress context
/compress --target=50

# Or focus on specific area
/compress --focus="api implementation"
```

## 📚 Learning Resources

### Interactive Tutorials

```bash
# General onboarding
/onboard

# Workflow guidance
/workflow-guide

# Command help
/help [command]
```

### Example Projects

Check the `examples/` directory:
- `examples/simple-api/` - Basic FastAPI app
- `examples/ai-agent/` - Pydantic AI agent
- `examples/etl-pipeline/` - Prefect pipeline

### Best Practices

1. **Always start with `/sr`** - Context is crucial
2. **Trust the hooks** - They prevent 90% of errors
3. **Use chains** - Faster than individual commands
4. **Check dependencies** - `/pydeps check` before refactoring
5. **Leverage orchestration** - `/orch` for complex features

## 🎓 Next Steps

### Week 1 Goals
- [ ] Complete first feature with TDD
- [ ] Try multi-agent orchestration
- [ ] Create custom chain
- [ ] Explore PRPs for research

### Week 2 Goals
- [ ] Master task ledger workflow
- [ ] Use thinking levels effectively
- [ ] Contribute pattern to system
- [ ] Optimize token usage

### Month 1 Goals
- [ ] Build complete application
- [ ] Create custom personas
- [ ] Extend hook system
- [ ] Share learnings with team

## 🆘 Getting Help

### In-System Help
```bash
/help            # General help
/help new        # What's new
/help [command]  # Specific command
/workflow-guide  # Personalized guidance
```

### Community Resources
- GitHub Issues: Report bugs or request features
- Discussions: Share patterns and tips
- Wiki: Advanced techniques and examples

### Direct Support
- Check `.claude/docs/` for detailed guides
- Review `.claude/examples/` for patterns
- Read hook source code for deep understanding

## 🎉 You're Ready!

You now have everything needed to build intelligent Python applications with AI assistance. Remember:

1. **The system protects you** - Trust the hooks
2. **Context is maintained** - Use `/sr` liberally  
3. **Quality is automatic** - TDD is enforced
4. **Help is available** - `/help` anywhere

Start building something amazing! The AI is ready to help. 🚀

---

*Pro tip: Keep this guide open in another window during your first week. The commands will become muscle memory quickly!*
