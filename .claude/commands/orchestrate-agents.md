---
name: orchestrate-agents
aliases: [orch, orchestrate]
description: Orchestrate multiple specialized AI agents for parallel development
category: development
---

Orchestrate sub-agents with specialized personas to work on tasks in parallel: $ARGUMENTS

Parse arguments:
- Feature name or task file path
- --strategy=feature|security|performance|data|deployment|auto (default: auto)
- --agents=auto|2-8 (default: auto-detect based on tasks)
- --personas=backend,data,qa (override auto-selection)

## 🤖 Intelligent Multi-Agent Orchestration

### 1. Available Personas (Python-Specific)

Reading from: `.claude/personas/personas.json`

**Core Development Personas:**
- **backend**: FastAPI, SQLAlchemy, authentication, server logic
- **frontend**: CLI interfaces, Rich terminal UI, Typer commands
- **data_engineer**: Prefect pipelines, ETL, BigQuery, data quality
- **agent**: Pydantic agents, LLM integration, instructor library

**Specialized Personas:**
- **analyzer**: Root cause analysis, debugging, profiling
- **refactorer**: Code quality, pattern extraction, technical debt
- **devops**: Docker, Kubernetes, CI/CD, deployment
- **security**: Auth, encryption, compliance, vulnerability assessment
- **performance**: Optimization, caching, async patterns
- **qa**: Pytest, fixtures, coverage, test automation

### 2. Orchestration Strategies

**Auto-Detection Based on Domains:**
```python
def detect_strategy(task_domains):
    """Auto-detect best orchestration strategy"""
    if 'bug' in task_domains or 'error' in task_domains:
        return 'bug_investigation'
    elif 'performance' in task_domains:
        return 'performance_optimization'
    elif 'security' in task_domains:
        return 'security_audit'
    elif 'refactor' in task_domains:
        return 'code_quality'
    elif 'deploy' in task_domains:
        return 'deployment'
    elif 'data' in task_domains and 'pipeline' in task_domains:
        return 'data_pipeline'
    else:
        return 'feature_development'
```

### 3. Task Assignment Algorithm

```python
# Intelligent task distribution based on:
# 1. Domain keywords in task description
# 2. File patterns (src/api/* → backend)
# 3. Dependencies between tasks
# 4. Agent expertise matching

task_assignment = {
    "backend_agent": {
        "tasks": ["1.1", "1.2", "2.1"],  # API and database tasks
        "focus": "FastAPI endpoints and data models",
        "outputs": ["src/api/routers/", "src/models/"]
    },
    "data_agent": {
        "tasks": ["1.3", "3.1", "3.2"],  # Pipeline tasks
        "focus": "Prefect flows and data transformations",
        "outputs": ["src/pipelines/", "src/etl/"]
    },
    "qa_agent": {
        "tasks": ["4.1", "4.2", "4.3"],  # Testing tasks
        "focus": "Pytest fixtures and test coverage",
        "outputs": ["tests/", "fixtures/"]
    }
}
```

### 4. Coordination Protocol

#### Phase-Based Execution
```yaml
Phase 1 - Foundation (Parallel):
  - backend_agent: Database schema, API structure
  - data_agent: Pipeline architecture
  - devops_agent: Container setup

Phase 2 - Implementation (Parallel):
  - backend_agent: Core logic
  - frontend_agent: CLI commands
  - agent_developer: AI agents

Phase 3 - Integration:
  - integrator: Connect components
  - qa_agent: Integration tests

Phase 4 - Quality:
  - security_agent: Security audit
  - performance_agent: Optimization
  - qa_agent: Final testing
```

#### Communication Channels
```json
{
  "communication": {
    "shared_context": ".claude/orchestration/context.json",
    "progress_tracking": ".claude/orchestration/progress/",
    "handoff_contracts": ".claude/orchestration/handoffs/",
    "message_queue": ".claude/orchestration/messages.json"
  }
}
```

### 5. Sub-Agent Instructions Template

```markdown
## You are {AGENT_TYPE} for feature: {FEATURE_NAME}

### Your Specialized Role:
- Expertise: {EXPERTISE_LIST}
- Focus Area: {FOCUS_DESCRIPTION}
- Tools Available: {TOOLS_LIST}

### Assigned Tasks:
{TASK_LIST}

### File Ownership:
You have exclusive write access to:
{FILE_PATTERNS}

### Dependencies:
- Wait for: {BLOCKING_TASKS}
- Enables: {DOWNSTREAM_TASKS}

### Output Contracts:
{OUTPUT_SPECIFICATIONS}

### Progress Protocol:
1. Update progress after each task: `.claude/orchestration/progress/{agent_id}.json`
2. Check messages regularly: `.claude/orchestration/messages.json`
3. Signal handoffs with clear contracts
4. Use `/agent-checkpoint` to save state
```

### 6. Real-Time Progress Dashboard

```
╔══════════════════════════════════════════════════════════╗
║ ORCHESTRATION STATUS: user-authentication-system         ║
╠══════════════════════════════════════════════════════════╣
║ Strategy: feature_development | Agents: 5 | Time Saved: 65% ║
╠══════════════════════════════════════════════════════════╣
║ BACKEND_AGENT     [████████░░] 80%  Task: JWT implementation ║
║ DATA_AGENT        [██████░░░░] 60%  Task: User schema       ║
║ FRONTEND_AGENT    [████░░░░░░] 40%  Task: CLI commands      ║
║ QA_AGENT          [██░░░░░░░░] 20%  Task: Test fixtures     ║
║ SECURITY_AGENT    [░░░░░░░░░░] 0%   Status: Waiting         ║
╠══════════════════════════════════════════════════════════╣
║ Critical Path: 1.1 → 2.1 → 3.1 → 4.1 → 5.1                ║
║ Parallel Savings: 3.5 hours → 1.2 hours                   ║
╠══════════════════════════════════════════════════════════╣
║ Recent Messages:                                          ║
║ • [BACKEND → DATA]: User model ready at src/models/user.py ║
║ • [DATA → QA]: Pipeline needs test data fixtures          ║
║ • [FRONTEND → ALL]: CLI structure established             ║
╚══════════════════════════════════════════════════════════╝
```

### 7. Conflict Prevention System

```python
# File ownership mapping prevents conflicts
FILE_OWNERSHIP = {
    "src/api/**": "backend_agent",
    "src/cli/**": "frontend_agent",
    "src/agents/**": "agent_developer",
    "src/pipelines/**": "data_agent",
    "tests/**": "qa_agent",
    "docker/**": "devops_agent",
    ".github/**": "devops_agent"
}

# Automatic conflict detection
if agent_wants_to_edit(file) and not owns_file(agent, file):
    raise OwnershipError(f"{agent} cannot edit {file}, owned by {owner}")
```

### 8. Smart Handoff Contracts

```json
{
  "handoff": {
    "from": "backend_agent",
    "to": "frontend_agent",
    "timestamp": "2024-01-10T10:30:00Z",
    "deliverables": {
      "api_endpoints": {
        "POST /api/auth/login": {
          "request": "LoginRequest",
          "response": "TokenResponse",
          "errors": ["InvalidCredentials", "RateLimited"]
        }
      },
      "models": {
        "LoginRequest": "src/models/auth.py:LoginRequest",
        "TokenResponse": "src/models/auth.py:TokenResponse"
      }
    },
    "notes": "Auth endpoints ready for CLI integration"
  }
}
```

### 9. Benefits & Metrics

**Performance Gains:**
- Sequential execution: 4-6 hours
- Parallel orchestration: 1.5-2 hours
- Time saved: 60-70%

**Quality Improvements:**
- Specialized expertise per domain
- No context switching overhead
- Clear ownership prevents conflicts
- Better test coverage from dedicated QA

**Developer Experience:**
- Set and forget - agents coordinate themselves
- Clear progress visibility
- Automatic conflict resolution
- Natural documentation from handoffs

### 10. Usage Examples

```bash
# Auto-detect strategy and agent count
/orch user-authentication

# Specific strategy
/orch payment-processing --strategy=security_audit

# Manual agent selection
/orch data-pipeline --agents=3 --personas=data_engineer,backend,qa

# View orchestration status
/orch status

# Abort orchestration
/orch abort user-authentication

# PRP-driven orchestration (NEW)
/orch payment-integration --from-prp
```

### PRP-Driven Orchestration

When a PRP exists for a feature, orchestration can leverage its detailed task breakdown:

```bash
# Execute orchestration from PRP
/orch [feature] --from-prp
```

This will:
1. **Parse PRP task breakdown** - Extract structured tasks from PRP
2. **Auto-assign to specialized agents** - Use PRP's domain hints
3. **Use validation gates as sync points** - Coordinate at validation levels
4. **Track progress against PRP criteria** - Measure success metrics

Example PRP task integration:
```yaml
# From PRP task breakdown
Task 1 - Data Models:
  domain: backend
  agent: backend_specialist
  validation: level_2_unit_tests
  
Task 2 - API Endpoints:
  domain: api
  agent: api_developer
  depends_on: task_1
  validation: level_3_integration
```

## Orchestration Lifecycle:

1. **Analysis**: Scan tasks for domains and complexity
2. **Strategy**: Select or auto-detect orchestration strategy  
3. **Assignment**: Distribute tasks to specialized agents
4. **Execution**: Agents work in parallel with clear boundaries
5. **Coordination**: Automatic handoffs at phase boundaries
6. **Integration**: Combine outputs and validate
7. **Completion**: Final review and merge

The system automatically handles all coordination, leaving you free to focus on the bigger picture!