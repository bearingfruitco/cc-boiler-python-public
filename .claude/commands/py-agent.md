---
name: py-agent
aliases: [pya, agent-create]
description: Create a new Pydantic AI agent with structured I/O
category: python
---

Create a new Pydantic-based AI agent with:
- Structured input/output models using Pydantic
- Memory management with Redis backend
- Tool integration capabilities
- Async support
- Type safety throughout

## Usage
```bash
/py-agent <AgentName> [options]
```

## Options
- `--role`: Agent role (data_analyst, api_developer, etc.)
- `--tools`: Comma-separated list of tools the agent can use
- `--memory`: Enable memory persistence (default: true)
- `--async`: Generate async methods (default: true)

## Examples
```bash
# Create a financial analyst agent
/py-agent FinancialAnalyst --role=data_analyst --tools=pandas,yfinance,plotly

# Create an API developer agent
/py-agent APIBuilder --role=api_developer --tools=fastapi,pydantic,httpx

# Create a test engineer agent
/py-agent TestEngineer --role=test_engineer --tools=pytest,hypothesis,faker
```

## What Gets Created

1. **Agent Class** (`src/agents/{name}.py`):
   - Inherits from BaseAgent
   - Specialized prompts and behaviors
   - Tool integration methods
   - Custom response models

2. **Pydantic Models** (`src/models/{name}_models.py`):
   - Request/Response models
   - Validation rules
   - Type hints

3. **Tests** (`tests/agents/test_{name}.py`):
   - Unit tests for agent behavior
   - Mock LLM responses
   - Tool usage tests

4. **CLI Command** (updates `src/cli/main.py`):
   - New command for the agent
   - Integration with existing CLI

## Template Structure
```python
from typing import List, Optional
from pydantic import BaseModel, Field
from src.agents.base import BaseAgent, AgentRole

class {AgentName}Request(BaseModel):
    """Request model for {AgentName}"""
    # Define request fields

class {AgentName}Response(BaseModel):
    """Response model for {AgentName}"""
    # Define response fields

class {AgentName}Agent(BaseAgent):
    """Agent specialized in {description}"""
    
    role: AgentRole = AgentRole.{ROLE}
    name: str = "{AgentName}"
    description: str = "{description}"
    tools: List[str] = {tools}
    
    def process(self, request: {AgentName}Request) -> {AgentName}Response:
        """Main processing method"""
        return self.think(
            prompt=self._build_prompt(request),
            response_model={AgentName}Response
        )
```