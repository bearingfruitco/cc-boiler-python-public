---
name: py-prd
aliases: [pyprd, prd-python]
description: Create a Python-specific PRD with orchestration analysis
category: python
---

Create a Product Requirements Document for Python feature: $ARGUMENTS

## PRD Structure with Orchestration Analysis

### 1. Feature Overview
- Name, description, business value
- Technical approach (API, CLI, Pipeline, Agent)

### 2. Domain Analysis
Automatically analyze which domains this feature touches:
- **Backend**: API endpoints, server logic
- **Data**: Pipelines, ETL, transformations  
- **Agent**: AI agents, LLM integration
- **CLI**: Terminal interface, commands
- **Testing**: Test requirements
- **Security**: Auth, encryption needs
- **Performance**: Optimization requirements

### 3. Orchestration Recommendation
Based on domain analysis:
```yaml
Orchestration Analysis:
  Domains Involved: [backend, data, testing]
  Complexity Score: 18 (high)
  Recommended Strategy: feature_development
  Suggested Agents: 4
  Time Savings: ~65%
  
Command: /orch {feature_name} --strategy=feature_development
```

### 4. Technical Requirements
- Python-specific considerations
- Async requirements
- Type safety needs
- Testing strategy

### 5. Implementation Phases
Tag each phase with responsible domains:
- Phase 1: Foundation [backend, data]
- Phase 2: Core Logic [backend, agent]
- Phase 3: Interface [cli, frontend]
- Phase 4: Quality [testing, security]

### 6. Sub-Specifications (For Complex Features)
If complexity score > 15, generate focused sub-specs:

#### API Specification
```yaml
# .claude/specs/$ARGUMENTS/api-spec.md
endpoints:
  - path: /api/v1/$FEATURE
    methods: [GET, POST]
    auth: required
    rate_limit: 100/hour
    request_schema: Pydantic model
    response_schema: Pydantic model
    error_codes: [400, 401, 403, 404, 500]
```

#### Database Specification  
```yaml
# .claude/specs/$ARGUMENTS/db-spec.md
migrations:
  - create_table: feature_name
    columns:
      - id: UUID primary key
      - created_at: timestamp
    indexes: [created_at]
    constraints: []
```

#### Test Specification
```yaml
# .claude/specs/$ARGUMENTS/test-spec.md
test_scenarios:
  unit_tests:
    - happy_path: Expected behavior
    - edge_cases: Boundary conditions
    - error_cases: Exception handling
  integration_tests:
    - api_flow: End-to-end API test
    - data_flow: Pipeline test
```

Save as: docs/project/features/$ARGUMENTS-PRD.md

## Enhanced PRP Mode

To create a research-heavy PRP instead of standard PRD:
```bash
/py-prd $ARGUMENTS --prp
```

This will:
1. Run deep research phase
2. Cache documentation
3. Include gotchas and anti-patterns
4. Add 4-level validation
5. Enable automation via prp_runner.py
6. **NEW**: Generate all sub-specs automatically

### PRP Benefits
- **One-pass success**: 78% success rate
- **Time savings**: 55% faster implementation
- **Automation ready**: Execute with prp_runner.py
- **Validation gates**: 4-level quality checks
- **Sub-specs**: Detailed technical specifications

### When to Use PRP Mode
- Complex features with multiple components
- Features requiring external API integration
- When you want automated execution
- For repeatable patterns
- CI/CD pipeline integration

## Integration with Task Generation

After PRD creation:
1. Sub-specs are used by `/generate-tasks` for detailed task creation
2. Each sub-spec generates specific implementation tasks
3. Tasks are linked back to both PRD and sub-specs
4. Validation checks against specifications