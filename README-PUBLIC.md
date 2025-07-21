# Python AI Agent Boilerplate 🚀

> **AI-Powered Python Development System** - Build production-ready AI agents, FastAPI applications, and data pipelines with 70+ Claude Code commands, multi-agent orchestration, and zero context loss between sessions.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.5+-red.svg)](https://pydantic-docs.helpmanual.io/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🎯 What Is This?

A production-ready Python boilerplate that transforms Claude Code into a powerful development assistant with:

- **70+ Custom Commands** - Specialized Python development commands
- **Multi-Agent Orchestration** - Parallel development with AI personas
- **Zero Context Loss** - Perfect session continuity
- **PRD-Driven Workflow** - From idea to implementation
- **Automated Safety** - 27+ hooks preventing common mistakes
- **Type-Safe Everything** - Pydantic models throughout

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/bearingfruitco/cc-boiler-python-public.git my-ai-project
cd my-ai-project

# Install dependencies
poetry install

# Copy environment files
cp .env.example .env
cp .mcp-example.json .mcp.json

# Run setup
./scripts/setup-hooks.sh
```

### 2. Configure Claude Desktop

Add to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/path/to/my-ai-project"]
    }
  }
}
```

### 3. Start Building

In Claude Desktop:
```bash
/sr                    # Smart Resume - loads all context
/workflow-guide        # Get personalized workflow recommendation
/py-prd user-auth      # Create a Python PRD for user authentication
```

## 📚 Core Features

### 🤖 AI Agent Development

Create Pydantic-based AI agents with structured I/O:

```bash
/py-agent DataAnalyst --role=analyst --tools=pandas,plotly
```

Generates:
- Pydantic request/response models
- Agent class with tool integration
- Async support and error handling
- Complete test suite

### 🚄 FastAPI Development

Build type-safe APIs instantly:

```bash
/py-api /users GET POST --auth --pagination
```

Creates:
- FastAPI router with endpoints
- Pydantic models for validation
- Authentication middleware
- OpenAPI documentation

### 📊 Data Pipeline Creation

Orchestrate data workflows with Prefect:

```bash
/py-pipeline ETLPipeline --source=bigquery --destination=postgres
```

Includes:
- Prefect flow definition
- Error handling and retries
- Monitoring and logging
- Data quality checks

### 🔍 Dependency Management

Track and prevent breaking changes:

```bash
/pydeps check UserModel        # What depends on this?
/pydeps breaking auth_module   # Will changes break anything?
/pyexists UserService         # Check before creating
```

## 🛠️ Available Workflows

### 1. Standard Workflow (1-2 days)
```
/sr → /py-prd → /gt → /pt → /test → /grade
```
Best for single-domain features with clear requirements.

### 2. PRP Workflow (3-5 days)
```
/sr → /prp-create → execute → validate → complete
```
For complex integrations requiring research and external APIs.

### 3. Orchestration Workflow (50-70% faster)
```
/sr → /py-prd → /orch → monitor → integrate
```
Parallel development with multiple AI agents.

### 4. Micro Task Workflow (< 2 hours)
```
/sr → /mt → implement → checkpoint
```
Quick fixes and small improvements.

## 🎨 Command Reference

### Essential Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `/smart-resume` | `/sr` | Restore full project context |
| `/py-prd` | `/prd` | Create Python-specific PRD |
| `/generate-tasks` | `/gt` | Generate tasks from PRD |
| `/process-tasks` | `/pt` | Work through tasks |
| `/orchestrate-agents` | `/orch` | Launch multi-agent mode |
| `/help` | `/h` | Context-aware help |

### Python-Specific Commands

| Command | Description |
|---------|-------------|
| `/py-agent` | Create Pydantic AI agent |
| `/py-api` | Generate FastAPI endpoint |
| `/py-pipeline` | Build Prefect pipeline |
| `/pyexists` | Check if component exists |
| `/pydeps` | Analyze dependencies |
| `/pysimilar` | Find similar code patterns |

### Testing & Quality

| Command | Description |
|---------|-------------|
| `/test` | Run pytest suite |
| `/lint` | Run Ruff linter |
| `/type-check` | Run MyPy |
| `/coverage` | Check test coverage |
| `/grade` | Grade implementation quality |

## 🛡️ Safety Features

### Pre-Execution Hooks
- **Duplicate Prevention** - Checks before creating
- **Import Validation** - Prevents circular imports
- **Style Enforcement** - Auto-formats with Black/Ruff
- **Dangerous Command Blocking** - No `rm -rf /`
- **PII Protection** - Blocks sensitive data in logs

### Post-Execution Hooks
- **State Persistence** - GitHub backup every 60s
- **Dependency Updates** - Auto-fixes imports
- **Pattern Learning** - Captures successful patterns
- **Test Generation** - Creates tests automatically

## 🏗️ Project Structure

```
my-ai-project/
├── .claude/           # Claude Code configuration
│   ├── commands/      # 70+ command definitions
│   ├── hooks/         # Pre/post execution hooks
│   └── personas/      # AI agent personalities
├── src/
│   ├── agents/        # Pydantic AI agents
│   ├── api/           # FastAPI routers
│   ├── models/        # Data models
│   ├── pipelines/     # Prefect workflows
│   └── utils/         # Helpers
├── tests/             # Comprehensive test suite
├── docs/              # Documentation
└── PRPs/              # Product Requirement Prompts
```

## 🔧 Configuration

### Required Environment Variables

```bash
# .env
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
DATABASE_URL=postgresql://localhost/myapp
REDIS_URL=redis://localhost:6379
```

### Python Dependencies

Core stack managed with Poetry:
- **Python 3.11+** - Modern Python features
- **Pydantic 2.5+** - Data validation
- **FastAPI** - High-performance APIs
- **Prefect** - Workflow orchestration
- **Instructor** - Structured LLM outputs

## 📊 Success Metrics

- **50-70% faster** development with orchestration
- **80% less boilerplate** to write
- **90% duplicate prevention** success rate
- **One-pass implementation** with PRPs

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built with ❤️ by the Bearing Fruit team. Special thanks to the Claude Code community for feedback and testing.

---

**Ready to build?** Start with `/sr` in Claude Desktop and let the AI guide you! 🚀
