# New Chat Context - Python Boilerplate v2.4.2

## 🆕 What's New in v2.4.2

### Claude Code Integration Features
- **Permission Profiles**: Dynamic safety levels (exploration → ci_pipeline)
- **Screenshot Capture**: Automatic browser screenshots on test failures
- **Auto-staging**: Git stages files after successful tests/edits
- **Thinking Levels**: Control reasoning depth with `/think-level`
- **Enhanced Compression**: Focus-aware context compression

### New Commands
```bash
/think-level deep       # Enhanced reasoning for complex problems
/compress --focus="api design"  # Targeted context compression
```

## 🆕 What's New in v2.4.1

### Automatic Test-Driven Development
- **Zero-Friction TDD**: Tests generate automatically at key moments
- **Smart Triggers**: Tests appear when:
  - Starting work: `/fw start 123` (from issue)
  - Processing tasks: `/pt feature` (checks/creates)
  - Creating issues: `/cti --tests` (instant tests)
- **Enforcement Options**: Block code without tests (configurable)
- **Visibility**: Test status shown throughout workflow
- **No Manual Steps**: Just start working, tests appear

## 🆕 What's New in v2.4.0

### Smart Issue Creation & Dependency Tracking
- **Capture-to-Issue**: Convert AI responses directly to GitHub issues with `/cti`
- **Python Dependency Management**: Track module dependencies with `/pydeps`
- **Creation Guard**: Prevent duplicate modules/classes/functions
- **Response Capture**: Auto-capture valuable AI analyses for later use

### New Python Commands
```bash
# Capture AI response to issue
/cti "User Auth API" --type=api --framework=fastapi

# Check dependencies
/pydeps check UserModel
/pydeps breaking auth_module
/pydeps circular

# Check existence
/pyexists UserModel class
/pysimilar AuthService
```

## 🆕 What's New in v2.3.6

### Async Event-Driven Architecture
- **Event Queue System**: Fire-and-forget pattern for non-critical operations
- **No More Blocking**: Analytics and tracking run asynchronously
- **Parallel Processing**: Automatic detection of operations that can run in parallel
- **Required Loading States**: Every async operation must show user feedback
- **Smart Form Events**: Built-in tracking hooks for lead generation
- **Timeout Protection**: All external calls have automatic timeout handling

### New Commands
- `/create-event-handler` - Create async event handler with retry logic
- `/prd-async` - Add async requirements section to any PRD
- `/validate-async` - Check code for async anti-patterns
- `/test-async-flow` - Test event chains end-to-end

## 🚀 Quick Start

You're working with a Python AI-assisted development system focused on building AI agents, FastAPI applications, and data pipelines with Prefect.

### First Commands
```bash
/sr                    # Smart Resume - restores full context
/help new              # See latest features
/cp load [profile]     # Load focused context
```

## 🌟 Python-Specific Features

### AI Agent Development
```bash
/py-agent DataAnalyst --role=data_analyst --tools=pandas,plotly
/py-api /analyze POST --agent=data_analyst --auth
/py-pipeline ETL --source=bigquery --agents=data_analyst
```

### Dependency Tracking (v2.4.0)
```python
"""
User authentication module.

@module: auth
@imports-from: database, utils.security
@imported-by: api.endpoints, services.user
@breaking-changes: 2024-01-15 - Removed legacy_auth
"""
```

### Smart Issue Creation (v2.4.0)
```bash
# After AI provides implementation plan:
/cti "Authentication System" --type=api --framework=fastapi --tests

# Automatically:
# - Extracts Python components (classes, functions, models)
# - Detects duplicate issues (80% threshold)
# - Links to PRDs and parent issues
# - Creates actionable GitHub issue
```

### Creation Guard (v2.4.0)
Before creating any Python component, the system checks:
- Exact name matches across all modules
- Similar names (80%+ similarity)
- Where component is already imported
- Suggests import statements

## 🎯 Core Python Workflow

```
IDEA → /py-prd → /cti --tests → /fw start → /pt → /grade
```

1. **Define** Python feature specification
2. **Capture** to issue (tests auto-generated!)
3. **Start** work (tests already waiting)
4. **Process** tasks (TDD enforced)
5. **Grade** implementation quality

🆕 No more manual test generation - it's automatic!

## 📋 Essential Python Commands

### Development
```bash
/py-prd [feature]      # Python-specific PRD
/py-agent [name]       # Create Pydantic AI agent
/py-api [endpoint]     # FastAPI endpoint + models
/py-pipeline [name]    # Prefect data pipeline
/pyexists [name]       # Check before creating
```

### Issue & Dependency Management
```bash
/cti [title]           # Capture to GitHub issue
/pydeps check [module] # What imports this?
/pydeps scan           # Full dependency scan
/pydeps breaking       # Detect breaking changes
/pydeps circular       # Find circular imports
```

### Quality & Testing
```bash
/lint                  # Run ruff linter
/test                  # Run pytest suite
/type-check            # Run mypy
/coverage              # Check test coverage
```

## 🛡️ Automatic Python Protections

The system automatically:
- **Prevents** duplicate module/class creation
- **Tracks** all import dependencies
- **Warns** about breaking changes
- **Captures** AI implementation plans
- **Detects** circular imports
- **Updates** imports after refactoring
- **Enforces** type safety with mypy
- **Validates** with ruff linting

## 🏗️ Python Project Structure

```
src/
├── agents/        # AI agents with Pydantic models
├── api/           # FastAPI routers and endpoints
├── models/        # Pydantic data models
├── pipelines/     # Prefect flows and tasks
├── services/      # Business logic
├── db/            # Database operations
└── utils/         # Helper functions

tests/
├── unit/          # Unit tests
├── integration/   # Integration tests
└── e2e/           # End-to-end tests
```

## 🔧 Configuration

### Python Dependencies (config.json)
```json
{
  "dependencies": {
    "auto_track": true,
    "scan_on_save": true,
    "alert_threshold": 3,
    "frameworks": {
      "fastapi": ["routers", "dependencies", "models"],
      "pydantic": ["models", "validators"],
      "prefect": ["flows", "tasks", "blocks"]
    }
  }
}
```

### Capture Settings
```json
{
  "capture_to_issue": {
    "similarity_threshold": 0.8,
    "include_tests": true,
    "python_specific": {
      "extract_imports": true,
      "extract_type_hints": true,
      "track_async": true
    }
  }
}
```

## 📋 Task Ledger (NEW!)

Central task tracking across all features:
```bash
/tl                # View all tasks and progress
/tl view [feature] # See specific feature tasks
/tl update [feat]  # Update task progress
/tl link [f] [#]   # Link feature to GitHub issue
```

The `.task-ledger.md` file tracks:
- All generated tasks across features
- Progress on each feature (X/Y tasks)
- Links to GitHub issues
- Status: Generated, In Progress, Completed, Blocked

## 🚦 Getting Help

```bash
/help              # Context-aware help
/help python       # Python-specific help
/help [command]    # Specific command help
```

## 💭 Philosophy

This system combines the power of AI-assisted development with Python's ecosystem:
- **Pydantic** for structured data and AI agents
- **FastAPI** for high-performance APIs
- **Prefect** for orchestrated data pipelines
- **Type Safety** throughout with mypy
- **Dependency Tracking** to prevent breaks
- **Task Ledger** for never losing work

Ready to build? Try `/py-prd` for a new feature or `/sr` to resume!
