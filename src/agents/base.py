"""Base Agent Framework for Python AI Agents

This module provides the foundation for all Pydantic-based AI agents in the system.
Agents have structured inputs/outputs, memory persistence, and tool integration.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Type, TypeVar

import instructor
from openai import AsyncOpenAI, OpenAI
from pydantic import BaseModel, Field, field_validator
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

# Type variable for generic agent responses
T = TypeVar("T", bound=BaseModel)


class AgentRole(str, Enum):
    """Available agent roles in the system"""
    
    DATA_ANALYST = "data_analyst"
    PIPELINE_BUILDER = "pipeline_builder"
    API_DEVELOPER = "api_developer"
    TEST_ENGINEER = "test_engineer"
    SECURITY_AUDITOR = "security_auditor"
    DOCUMENTATION_WRITER = "documentation_writer"
    CODE_REVIEWER = "code_reviewer"
    DEVOPS_ENGINEER = "devops_engineer"


class AgentMemory(BaseModel):
    """Persistent memory structure for agents"""
    
    short_term: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Recent interactions and context"
    )
    long_term: Dict[str, Any] = Field(
        default_factory=dict,
        description="Persistent knowledge and patterns"
    )
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Current working context"
    )
    
    def add_interaction(self, role: str, content: str) -> None:
        """Add an interaction to short-term memory"""
        self.short_term.append({
            "role": role,
            "content": content,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        })
        
        # Keep only last 20 interactions
        if len(self.short_term) > 20:
            self.short_term = self.short_term[-20:]
    
    def update_context(self, **kwargs: Any) -> None:
        """Update the current context"""
        self.context.update(kwargs)
    
    def store_knowledge(self, key: str, value: Any) -> None:
        """Store knowledge in long-term memory"""
        self.long_term[key] = value


class AgentConfig(BaseModel):
    """Configuration for an agent"""
    
    model: str = Field(default="gpt-4-turbo-preview", description="LLM model to use")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_retries: int = Field(default=3, ge=1, le=10)
    timeout: int = Field(default=60, ge=10, le=300)
    tools_enabled: bool = Field(default=True)
    memory_enabled: bool = Field(default=True)
    streaming: bool = Field(default=False)


class BaseAgent(BaseModel):
    """Base class for all AI agents"""
    
    role: AgentRole
    name: str
    description: str
    memory: AgentMemory = Field(default_factory=AgentMemory)
    config: AgentConfig = Field(default_factory=AgentConfig)
    tools: List[str] = Field(default_factory=list)
    
    # Clients are excluded from Pydantic serialization
    _client: Optional[OpenAI] = None
    _async_client: Optional[AsyncOpenAI] = None
    _instructor_client: Optional[Any] = None
    _async_instructor_client: Optional[Any] = None
    
    model_config = {
        "arbitrary_types_allowed": True,
        "extra": "ignore"
    }
    
    def __init__(self, **data: Any) -> None:
        """Initialize the agent with clients"""
        super().__init__(**data)
        self._setup_clients()
    
    def _setup_clients(self) -> None:
        """Set up OpenAI and Instructor clients"""
        self._client = OpenAI()
        self._async_client = AsyncOpenAI()
        self._instructor_client = instructor.from_openai(self._client)
        self._async_instructor_client = instructor.from_openai(self._async_client)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def think(
        self,
        prompt: str,
        response_model: Type[T],
        context: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> T:
        """Process a prompt and return structured output"""
        # Build messages
        messages = self._build_messages(prompt, context)
        
        # Add to memory if enabled
        if self.config.memory_enabled:
            self.memory.add_interaction("user", prompt)
        
        # Get structured response
        response = self._instructor_client.chat.completions.create(
            model=self.config.model,
            response_model=response_model,
            messages=messages,
            temperature=self.config.temperature,
            **kwargs
        )
        
        # Store in memory
        if self.config.memory_enabled and hasattr(response, "model_dump"):
            self.memory.add_interaction("assistant", str(response.model_dump()))
        
        return response
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def think_async(
        self,
        prompt: str,
        response_model: Type[T],
        context: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> T:
        """Async version of think"""
        messages = self._build_messages(prompt, context)
        
        if self.config.memory_enabled:
            self.memory.add_interaction("user", prompt)
        
        response = await self._async_instructor_client.chat.completions.create(
            model=self.config.model,
            response_model=response_model,
            messages=messages,
            temperature=self.config.temperature,
            **kwargs
        )
        
        if self.config.memory_enabled and hasattr(response, "model_dump"):
            self.memory.add_interaction("assistant", str(response.model_dump()))
        
        return response
    
    def _build_messages(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, str]]:
        """Build messages for the LLM"""
        system_prompt = self._build_system_prompt()
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add memory context if enabled
        if self.config.memory_enabled and self.memory.short_term:
            for interaction in self.memory.short_term[-5:]:  # Last 5 interactions
                messages.append({
                    "role": interaction["role"],
                    "content": interaction["content"]
                })
        
        # Add user prompt with context
        user_content = prompt
        if context:
            user_content = f"Context: {context}\n\n{prompt}"
        
        messages.append({"role": "user", "content": user_content})
        
        return messages
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for the agent"""
        prompt = f"""You are {self.name}, a specialized AI agent with the role of {self.role.value}.

{self.description}

Your capabilities:
- Structured thinking and analysis
- Access to tools: {', '.join(self.tools) if self.tools else 'No special tools'}
- Memory of our conversation
- Ability to learn from interactions

Current context: {self.memory.context}

Always:
1. Provide clear, structured responses
2. Include your reasoning process
3. Suggest concrete next steps
4. Acknowledge any limitations
5. Learn from feedback and adapt"""
        
        return prompt
    
    def use_tool(self, tool_name: str, *args: Any, **kwargs: Any) -> Any:
        """Use a tool if available"""
        if not self.config.tools_enabled:
            raise ValueError("Tools are disabled for this agent")
        
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not available. Available tools: {self.tools}")
        
        # Tool implementation would go here
        logger.info(f"Using tool: {tool_name}")
        # This is where you'd integrate actual tool usage
        
    def reset_memory(self) -> None:
        """Reset the agent's memory"""
        self.memory = AgentMemory()
        logger.info(f"Memory reset for agent: {self.name}")
    
    def save_memory(self, path: str) -> None:
        """Save memory to disk"""
        import json
        with open(path, "w") as f:
            json.dump(self.memory.model_dump(), f, indent=2)
        logger.info(f"Memory saved to: {path}")
    
    def load_memory(self, path: str) -> None:
        """Load memory from disk"""
        import json
        with open(path, "r") as f:
            data = json.load(f)
            self.memory = AgentMemory(**data)
        logger.info(f"Memory loaded from: {path}")
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', role={self.role.value})"


class AgentResponse(BaseModel):
    """Standard response format for agents"""
    
    content: str = Field(description="Main response content")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in the response")
    reasoning: str = Field(description="Explanation of reasoning process")
    next_steps: List[str] = Field(default_factory=list, description="Suggested next actions")
    artifacts: Dict[str, Any] = Field(default_factory=dict, description="Additional data/files")
    
    @field_validator("confidence")
    def validate_confidence(cls, v: float) -> float:
        """Ensure confidence is between 0 and 1"""
        return max(0.0, min(1.0, v))


class AgentError(BaseModel):
    """Error response from an agent"""
    
    error: str
    error_type: str
    suggestion: Optional[str] = None
    retry_after: Optional[int] = None