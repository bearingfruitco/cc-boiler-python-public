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

Save as: docs/project/features/$ARGUMENTS-PRD.md