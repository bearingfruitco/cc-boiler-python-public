# PRP: AI Agent Development

## Metadata
- **Created**: [DATE]
- **Author**: [AUTHOR]
- **Confidence**: [1-10]
- **Complexity**: [Low/Medium/High]
- **Type**: AI-Agent

## Goal
[Clear description of the AI agent to be built]

## Why
- **Business Value**: [How this agent helps users/system]
- **Technical Need**: [Problems this agent solves]
- **Priority**: [Critical/High/Medium/Low]

## What
[Agent behavior and capabilities]

### Success Criteria
- [ ] Agent follows BaseAgent interface
- [ ] Structured input/output with Pydantic models
- [ ] Memory persistence via Redis
- [ ] Tool integration working
- [ ] 90%+ test coverage
- [ ] Response time < 2 seconds

## All Needed Context

### Documentation & References
```yaml
# Agent Framework
- file: src/agents/base.py
  why: BaseAgent class to extend
  pattern: Class structure and required methods

- file: src/agents/data_analyst.py
  why: Example agent implementation
  pattern: How to structure agent logic

# Pydantic Models
- url: https://docs.pydantic.dev/latest/concepts/models/
  why: Model validation patterns
  sections: ["validation", "serialization"]

# Tool Integration
- file: src/tools/__init__.py
  why: Available tools registry
  critical: Tool registration pattern

# Memory System
- docfile: PRPs/ai_docs/redis_memory_pattern.md
  why: Agent memory persistence approach
```

### Current Agent Structure
```python
from src.agents.base import BaseAgent, AgentRole

class ExampleAgent(BaseAgent):
    role = AgentRole.DATA_ANALYST
    name = "Example"
    description = "I do X"
    tools = ["pandas", "matplotlib"]
    
    def process(self, request: RequestModel) -> ResponseModel:
        # Implementation
        pass
```

### Known Gotchas & Critical Patterns
```python
# CRITICAL: All agents must be async
async def process(self, request: RequestModel) -> ResponseModel:
    # Use async context manager for tools
    async with self.get_tool("pandas") as pd:
        result = await self.think(prompt)

# PATTERN: Memory persistence
async def remember(self, key: str, value: Any):
    await self.memory.set(f"{self.agent_id}:{key}", value)

# GOTCHA: Tool initialization happens in __init__
def __init__(self):
    super().__init__()
    self._initialize_tools()  # Don't skip this!

# WARNING: Rate limiting on LLM calls
# Use semaphore: self._llm_semaphore (max 10 concurrent)
```

## Implementation Blueprint

### Task Breakdown
```yaml
Task 1 - Define Agent Models:
  CREATE src/models/{agent_name}_models.py:
    - Request model with validation
    - Response model with structure
    - Configuration model if needed
    
  TESTS tests/models/test_{agent_name}_models.py:
    - Validation edge cases
    - Serialization tests

Task 2 - Implement Agent:
  CREATE src/agents/{agent_name}_agent.py:
    - Extend BaseAgent
    - Define role and metadata
    - Implement process method
    - Add tool initialization
    
  UPDATE src/agents/__init__.py:
    - Export new agent
    - Add to agent registry

Task 3 - Tool Integration:
  CREATE/UPDATE src/tools/{agent_name}_tools.py:
    - Custom tools if needed
    - Tool wrappers for external libs
    
  REGISTER in tool registry:
    - Add to AVAILABLE_TOOLS

Task 4 - Memory & State:
  IMPLEMENT memory patterns:
    - Short-term memory for context
    - Long-term memory for learning
    - State persistence between calls

Task 5 - CLI Integration:
  UPDATE src/cli/main.py:
    - Add agent-specific commands
    - Interactive mode support
    
  CREATE src/cli/commands/{agent_name}.py:
    - Specialized CLI commands

Task 6 - Testing:
  CREATE tests/agents/test_{agent_name}_agent.py:
    - Unit tests with mocked LLM
    - Integration tests
    - Tool usage tests
    - Memory persistence tests
    
  CREATE tests/integration/test_{agent_name}_flow.py:
    - End-to-end workflow tests
    - Performance benchmarks
```

### Implementation Patterns

```python
# Pattern 1: Agent Structure
from typing import List, Optional
from pydantic import BaseModel, Field
from src.agents.base import BaseAgent, AgentRole
import instructor

class AnalysisRequest(BaseModel):
    """Request model for analysis"""
    data_source: str = Field(..., description="Data to analyze")
    questions: List[str] = Field(..., description="Questions to answer")
    output_format: Literal["summary", "detailed"] = "summary"
    
class AnalysisResponse(BaseModel):
    """Structured response from agent"""
    insights: List[str] = Field(..., description="Key insights found")
    confidence: float = Field(..., ge=0, le=1)
    recommendations: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AnalystAgent(BaseAgent):
    """Agent specialized in data analysis"""
    
    role = AgentRole.DATA_ANALYST
    name = "Data Analyst"
    description = "I analyze data and provide insights"
    tools = ["pandas", "numpy", "matplotlib"]
    
    async def process(self, request: AnalysisRequest) -> AnalysisResponse:
        """Main processing method"""
        # Load data
        data = await self._load_data(request.data_source)
        
        # Check memory for similar analyses
        cached = await self._check_cache(request)
        if cached and not request.force_new:
            return cached
        
        # Build analysis prompt
        prompt = self._build_prompt(data, request.questions)
        
        # Get structured response
        response = await self.think(
            prompt=prompt,
            response_model=AnalysisResponse,
            temperature=0.7
        )
        
        # Cache result
        await self._cache_result(request, response)
        
        return response

# Pattern 2: Tool Usage
async def _analyze_with_pandas(self, data_path: str):
    """Use pandas through tool system"""
    async with self.get_tool("pandas") as pd:
        df = pd.read_csv(data_path)
        
        # Analysis logic
        summary = {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "missing": df.isnull().sum().to_dict(),
            "dtypes": df.dtypes.to_dict()
        }
        
    return summary

# Pattern 3: Memory Management  
async def _remember_analysis(self, key: str, result: Any):
    """Store analysis in memory"""
    await self.memory.short_term.append({
        "timestamp": datetime.now(),
        "key": key,
        "result": result
    })
    
    # Long-term storage for important results
    if result.confidence > 0.8:
        await self.memory.long_term.set(
            f"analysis:{key}",
            result.model_dump(),
            expire=86400  # 24 hours
        )
```

## Validation Loops

### Level 1: Syntax & Style
```bash
# Automatic via hooks
ruff check src/agents/ --fix
black src/agents/
mypy src/agents/ --strict
```

### Level 2: Unit Tests
```bash
# Test agent logic
pytest tests/agents/test_{agent_name}_agent.py -v

# Test models
pytest tests/models/test_{agent_name}_models.py -v

# Coverage check
pytest tests/ --cov=src/agents/{agent_name} --cov-report=term-missing
# Required: >90% coverage
```

### Level 3: Integration Tests
```bash
# Test with real tools
pytest tests/integration/test_{agent_name}_integration.py -v

# Test CLI integration
python -m src.cli.main {agent_name} test-command

# Test memory persistence
docker-compose up -d redis
pytest tests/integration/test_{agent_name}_memory.py -v
```

### Level 4: Performance & Security
```bash
# Load testing
python tests/load/test_{agent_name}_load.py
# Requirement: <2s response time @ 100 concurrent

# Memory profiling
mprof run python tests/agents/profile_{agent_name}.py
mprof plot

# Security check
bandit -r src/agents/{agent_name}_agent.py
# No high severity issues allowed
```

## Deployment Checklist
- [ ] Agent registered in registry
- [ ] CLI commands working
- [ ] Documentation updated
- [ ] Example usage in README
- [ ] Performance benchmarks met
- [ ] Memory limits configured
- [ ] Rate limiting in place

## Anti-Patterns to Avoid
- ❌ Don't bypass BaseAgent interface
- ❌ Don't use synchronous I/O in agents
- ❌ Don't store secrets in agent memory
- ❌ Don't skip tool initialization
- ❌ Don't ignore rate limits
- ❌ Don't use unstructured LLM outputs
- ❌ Don't forget error handling

## Confidence Score: [X]/10

### Scoring Rationale:
- BaseAgent patterns followed: [X]/2
- Tool integration complete: [X]/2
- Memory system utilized: [X]/2
- Test coverage adequate: [X]/2
- Performance validated: [X]/2
