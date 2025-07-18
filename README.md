# Python AI Agent Boilerplate 🐍🤖

A production-ready Python boilerplate for building AI-powered applications with Pydantic agents, FastAPI, data pipelines, and Claude Code automation.

## 🚀 What You Get

### AI Agent Framework
- **Pydantic-based Agents** - Structured inputs/outputs with type safety
- **Multi-Agent Orchestration** - Coordinate specialized agents for complex tasks
- **Intelligent Task Distribution** - Auto-assigns work based on expertise
- **Memory Persistence** - Redis-backed agent memory across sessions
- **Tool Integration** - Agents can use Python libraries and external APIs
- **Async Everything** - Built for performance with asyncio

### 🆕 Intelligent Orchestration
- **Auto-Detection** - Analyzes tasks to recommend multi-agent execution
- **Domain Analysis** - Identifies backend, data, security, testing work
- **Parallel Execution** - 50-70% time savings on complex features
- **Smart Handoffs** - Agents coordinate seamlessly
- **Progress Tracking** - Real-time visibility into parallel work

### Modern Python Stack
- **FastAPI** - High-performance async API framework
- **Typer + Rich** - Beautiful CLI tools with autocomplete
- **Pandas + DuckDB** - Lightning-fast data analysis
- **Prefect** - Modern workflow orchestration
- **Instructor** - Structured LLM outputs with Pydantic

### Development Excellence
- **Poetry** - Dependency management done right
- **Ruff + Black** - Fast, consistent code formatting
- **MyPy** - Full type safety with strict mode
- **Pytest** - Comprehensive testing with 80%+ coverage
- **Pre-commit** - Automated quality checks

### Claude Code Integration
- **70+ Python Commands** - From `/py-agent` to `/py-pipeline`
- **Context Preservation** - Never lose work between sessions
- **PRD-Driven Development** - Requirements → Tests → Implementation
- **Quality Gates** - Automated checks before commit
- **Team Coordination** - Multi-developer awareness

## 📚 Quick Start

### New Project
```bash
# Clone the boilerplate
git clone https://github.com/bearingfruitco/cc-boiler-python-public.git my-project
cd my-project

# Run setup
chmod +x scripts/setup.sh
./scripts/setup.sh

# Install dependencies
poetry install

# Start developing
poetry run agent --help
```

### First Agent
```python
# Create your first agent
from src.agents.base import BaseAgent, AgentRole

class DataAnalystAgent(BaseAgent):
    role = AgentRole.DATA_ANALYST
    name = "Data Expert"
    description = "I analyze data and provide insights"
    
    def analyze(self, data: pd.DataFrame, question: str):
        return self.think(f"Analyze this data: {data.head()} to answer: {question}")
```

### CLI Usage
```bash
# Analyze data
agent analyze data.csv --question "What are the top trends?"

# Run a pipeline
agent pipeline run etl-config.yaml

# Start API server
agent api serve --reload

# Interactive agent chat
agent chat --agent data_analyst
```

## 🤖 Multi-Agent Orchestration

### Automatic Task Analysis
When you generate tasks from a PRD, the system automatically:
- Analyzes domain distribution (backend, data, security, etc.)
- Identifies parallel execution opportunities
- Suggests optimal agent count and strategy
- Estimates time savings

### Example Orchestration
```bash
# Generate PRD and tasks
/py-prd user-authentication
/gt user-authentication

# System suggests orchestration
# "Multi-domain work detected: backend (8), frontend (4), security (3)"
# "Orchestration recommended: /orch user-authentication --agents=4"

# Analyze orchestration plan
agent orchestrate analyze docs/project/features/user-authentication-tasks.md

# Start orchestration
agent orchestrate start user-authentication --strategy=feature_development
```

### Orchestration Strategies
- **feature_development** - Standard feature with backend/frontend/testing
- **bug_investigation** - Root cause analysis with targeted fixes
- **performance_optimization** - Performance analysis and improvements
- **security_audit** - Security review and hardening
- **data_pipeline** - ETL and data processing workflows
- **code_quality** - Refactoring and technical debt reduction

## 🏗️ Project Structure

```
/python-agent-boilerplate
├── src/
│   ├── agents/          # AI agents with Pydantic models
│   ├── api/            # FastAPI application
│   ├── cli/            # Typer CLI commands
│   ├── pipelines/      # Data pipeline definitions
│   ├── models/         # Pydantic models and schemas
│   ├── tools/          # Agent tools and functions
│   ├── db/             # Database models and queries
│   ├── orchestration/  # Multi-agent coordination
│   └── utils/          # Shared utilities
├── tests/              # Pytest test suite
├── scripts/            # Setup and maintenance scripts
├── docs/               # Documentation
├── .claude/            # Claude Code configuration
│   ├── commands/       # Custom Python commands
│   ├── hooks/          # Automation hooks
│   ├── personas/       # Agent personas and strategies
│   └── agents/         # Agent configurations
├── pyproject.toml      # Poetry configuration
├── Makefile           # Common commands
└── .env.example       # Environment template
```

## 🎯 Core Features

### 1. AI Agents with Structure
```python
from pydantic import BaseModel
from typing import List
import instructor

class AnalysisRequest(BaseModel):
    data_source: str
    questions: List[str]
    output_format: Literal["summary", "detailed", "visualization"]

class AnalysisResponse(BaseModel):
    insights: List[str]
    confidence: float
    visualizations: Optional[List[str]]
    next_steps: List[str]

# Agents always return structured data
response = agent.analyze(AnalysisRequest(
    data_source="sales.csv",
    questions=["What's the trend?", "Any anomalies?"],
    output_format="detailed"
))
# response is guaranteed to be AnalysisResponse type
```

### 2. FastAPI Integration
```python
@app.post("/agent/{agent_type}/execute")
async def execute_agent(
    agent_type: AgentRole,
    request: AgentRequest,
    background_tasks: BackgroundTasks
):
    """Execute any agent via API"""
    if request.async_mode:
        task_id = await queue_agent_task(agent_type, request)
        return {"task_id": task_id, "status": "queued"}
    
    result = await agent_manager.execute(agent_type, request)
    return result
```

### 3. Data Pipeline Framework
```python
from prefect import flow, task

@task(retries=3)
def extract_data(source: str) -> pd.DataFrame:
    """Extract with automatic retries"""
    return pd.read_csv(source)

@task
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform with validation"""
    return df.pipe(clean).pipe(enrich).pipe(validate)

@flow(name="etl-pipeline")
def etl_flow(config: PipelineConfig):
    """Orchestrated pipeline with monitoring"""
    data = extract_data(config.source)
    transformed = transform_data(data)
    load_to_warehouse(transformed, config.destination)
```

### 4. CLI Development
```python
@app.command()
def analyze(
    file: Path = typer.Argument(..., help="Data file to analyze"),
    agent: AgentRole = typer.Option(AgentRole.DATA_ANALYST),
    output: Optional[Path] = typer.Option(None, "--output", "-o"),
    format: OutputFormat = typer.Option(OutputFormat.TABLE),
):
    """Analyze data using AI agents"""
    with console.status(f"[bold green]Loading {file}..."):
        data = load_data(file)
    
    response = agent.analyze(data)
    
    if format == OutputFormat.TABLE:
        console.print(format_as_table(response))
    elif format == OutputFormat.JSON:
        output.write_text(response.model_dump_json(indent=2))
```

## 🔧 Essential Commands

### Setup & Configuration

#### MCP Configuration
This project uses Model Context Protocol (MCP) servers. To set up:

1. Copy the example configuration:
   ```bash
   cp .mcp-example.json .mcp.json
   ```

2. Add your API keys to `.mcp.json`:
   - `GITHUB_PERSONAL_ACCESS_TOKEN` - For GitHub integration
   - `OPENAI_API_KEY` - For AI features (if using OpenAI)
   - Other service-specific keys as needed

3. The `.mcp.json` file is gitignored for security - never commit it!

### Claude Code Commands
```bash
# Agent Development
/py-agent <name>          # Create new Pydantic agent
/py-tool <name>           # Create agent tool/function
/py-memory                # Set up Redis memory backend

# API Development  
/py-api <endpoint>        # Create FastAPI endpoint
/py-schema <model>        # Generate Pydantic model
/py-auth                  # Add authentication

# Data Pipelines
/py-pipeline <name>       # Create Prefect pipeline
/py-etl                   # Generate ETL template
/py-transform             # Create data transformer

# Testing & Quality
/py-test <module>         # Generate comprehensive tests
/py-fixture               # Create pytest fixtures
/py-mock                  # Generate mocks

# CLI Development
/py-cli <command>         # Create Typer command
/py-interactive           # Build interactive CLI

# Orchestration (NEW)
/py-prd <feature>         # Create PRD with orchestration analysis
/orch <feature>           # Start multi-agent orchestration
```

### Development Workflow
```bash
# Start new feature
make dev               # Set up development environment
poetry run agent chat  # Test with interactive agent

# Run quality checks
make lint             # Ruff + MyPy
make test             # Pytest with coverage
make security         # Security scanning

# Deploy
make build            # Build distribution
make docker           # Build container
make deploy           # Deploy to cloud
```

## 🚦 Getting Started

1. **Choose Your First Project**
   - Data Analysis Agent
   - API with AI endpoints  
   - CLI tool for automation
   - Data pipeline system

2. **Set Up Environment**
   ```bash
   cp .env.example .env
   # Add your API keys
   poetry install
   poetry shell
   ```

3. **Create Your First Agent**
   ```bash
   /py-agent FinancialAnalyst --tools=pandas,yfinance
   ```

4. **Run Tests**
   ```bash
   make test
   ```

## 🌟 Example Projects

### 1. Financial Data Analyzer
```bash
agent analyze portfolio.csv \
  --question "What's my risk exposure?" \
  --agent financial_analyst \
  --output report.pdf
```

### 2. API Gateway with AI
```bash
# Start API server
agent api serve

# Call from anywhere
curl -X POST http://localhost:8000/agent/data_analyst/execute \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Analyze sales trends", "context": {"file": "sales.csv"}}'
```

### 3. Automated Data Pipeline
```yaml
# pipeline.yaml
name: daily-etl
schedule: "0 9 * * *"
steps:
  - extract:
      source: bigquery
      query: "SELECT * FROM analytics.events WHERE date = CURRENT_DATE()"
  - transform:
      agent: data_analyst
      prompt: "Clean and enrich this data"
  - load:
      destination: warehouse
      table: processed_events
```

## 📈 Why This Stack?

- **Type Safety** - Catch errors before runtime with Pydantic + MyPy
- **Performance** - Async everywhere, DuckDB for analytics
- **Developer Experience** - Rich CLI output, helpful error messages
- **Production Ready** - Structured logging, monitoring, error handling
- **AI-First** - Built for LLM integration from the ground up
- **Intelligent Orchestration** - Automatic work distribution for speed

## 🤝 Contributing

This boilerplate evolves with use. Contribute:
- New agent types
- Pipeline patterns
- CLI enhancements
- Tool integrations
- Orchestration strategies

## 📚 Documentation

- [Agent Development Guide](docs/agents/README.md)
- [API Reference](docs/api/README.md)
- [Pipeline Patterns](docs/pipelines/README.md)
- [Testing Strategy](docs/testing/README.md)
- [Deployment Guide](docs/deployment/README.md)
- [Orchestration Guide](docs/orchestration/README.md)

---

Built for Python developers who want:
- 🚀 AI agents that actually work
- 📊 Fast data processing pipelines
- 🛠️ Beautiful CLI tools
- 🔒 Type-safe everything
- ⚡ Async performance
- 🤖 Intelligent multi-agent orchestration

Ready to build? Start with `poetry install` and `/py-agent --help` 🐍