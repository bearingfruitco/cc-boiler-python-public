---
name: generate-tasks
aliases: [gt, tasks]
description: Generate detailed task list from PRD with domain analysis and ledger tracking
category: development
---

Generate a detailed task list from PRD: $ARGUMENTS

Read the PRD and create a comprehensive task breakdown with:
- Domain tagging for each task
- Complexity estimates
- Dependency mapping
- Orchestration analysis
- **NEW**: Update central task ledger

## Format

```markdown
# Task List for $ARGUMENTS

## 🤖 Orchestration Analysis

### Domain Distribution:
- Backend: X tasks
- Frontend: X tasks
- Data: X tasks
- Security: X tasks
- Testing: X tasks
- Performance: X tasks

### Parallel Work Opportunities:
1. **Phase 1**: Tasks X.X, X.X can run in parallel (different domains)
2. **Phase 2**: Frontend work can start once APIs are defined
3. **Phase 3**: Testing can begin per component as completed

### Orchestration Recommendation:
[✅/❌] **Multi-agent orchestration [recommended/not recommended]**
- X domains with significant work
- X parallel opportunities identified
- Estimated X% time savings

**Suggested command** (if recommended):
```bash
/orch $ARGUMENTS --agents=X --strategy=feature_development
```

## Task Breakdown

### Phase 1: Foundation
#### Task 1.1: Create database schema [domains: data, backend]
**Complexity**: Medium (15 min)
**Dependencies**: None
**Enables**: Tasks 1.2, 2.1

Design and implement the database schema with all required fields.

**Acceptance Criteria**:
- [ ] Schema includes all PRD-specified fields
- [ ] Proper indexes defined
- [ ] Migration file created
- [ ] Schema documented

#### Task 1.2: Set up API structure [domains: backend, security]
**Complexity**: Low (10 min)
**Dependencies**: None
**Enables**: Tasks 2.1, 2.2

Create FastAPI router structure and basic endpoints.

**Acceptance Criteria**:
- [ ] Router module created
- [ ] Endpoint stubs defined
- [ ] Authentication middleware configured
- [ ] OpenAPI documentation generated

### Phase 2: Core Implementation
#### Task 2.1: Implement data models [domains: backend, data]
**Complexity**: Medium (15 min)
**Dependencies**: Task 1.1
**Enables**: Tasks 2.2, 3.1

Create Pydantic models for request/response validation.

**Acceptance Criteria**:
- [ ] Request models with validation
- [ ] Response models defined
- [ ] Error models created
- [ ] Models have examples

[Continue with all tasks...]

### Phase 3: Agent Development
#### Task 3.1: Create specialized agent [domains: agent, backend]
**Complexity**: High (25 min)
**Dependencies**: Tasks 2.1, 2.2
**Enables**: Tasks 3.2, 4.1

Implement Pydantic agent for feature-specific logic.

**Acceptance Criteria**:
- [ ] Agent inherits from BaseAgent
- [ ] Structured input/output models
- [ ] Tool integration configured
- [ ] Memory persistence enabled

### Phase 4: Testing & Quality
#### Task 4.1: Write unit tests [domains: testing, backend]
**Complexity**: Medium (20 min)
**Dependencies**: Tasks 2.1, 2.2
**Enables**: Task 5.1

Create comprehensive test suite with pytest.

**Acceptance Criteria**:
- [ ] Unit tests for all functions
- [ ] Fixtures for test data
- [ ] Mocks for external services
- [ ] Coverage > 80%

### Phase 5: Integration & Deployment
#### Task 5.1: Create deployment config [domains: devops, security]
**Complexity**: Medium (15 min)
**Dependencies**: All previous phases
**Enables**: Production deployment

Set up Docker and deployment configuration.

**Acceptance Criteria**:
- [ ] Dockerfile created
- [ ] Environment variables configured
- [ ] Security scanning passed
- [ ] Health checks implemented

## Summary Statistics
- **Total Tasks**: X
- **Total Estimated Time**: X hours
- **Parallel Execution Time**: X hours (with orchestration)
- **Critical Path**: Tasks X.X → X.X → X.X
- **Recommended Team Size**: X agents
```

## Post-Generation Actions:

1. Save as `docs/project/features/$ARGUMENTS-tasks.md`
2. **Update task ledger** at `.task-ledger.md` with:
   - Feature name
   - Task count
   - Current status (Generated)
   - Link to detailed task file

## Task Ledger Entry Format:
```markdown
## Task: $ARGUMENTS
**Generated**: [timestamp]
**Issue**: [If linked to issue]
**Status**: Generated
**Branch**: [If created]
**Progress**: 0/X tasks completed

### Description
[Brief description from PRD]

### Task File
See detailed tasks in: `docs/project/features/$ARGUMENTS-tasks.md`

### Validation Checklist
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] No regressions
- [ ] Code review completed

---
```

## Rules for Task Generation:
1. Each task must include domain tags in square brackets
2. Complexity must be one of: Low (5-10 min), Medium (10-20 min), High (20-30 min)
3. Clearly mark dependencies and what each task enables
4. Group tasks by domain when possible for parallel execution
5. Include specific acceptance criteria for each task
6. Consider Python-specific concerns (async, typing, testing)

## Domain Tags to Use:
- **backend**: API, server, authentication, middleware
- **frontend**: CLI, UI, prompts, display
- **data**: Database, pipelines, ETL, analytics
- **agent**: AI agents, LLM integration, orchestration
- **security**: Auth, encryption, validation, compliance
- **testing**: Unit tests, integration, fixtures
- **performance**: Optimization, caching, profiling
- **devops**: Deployment, CI/CD, monitoring
- **refactor**: Code quality, patterns, cleanup
