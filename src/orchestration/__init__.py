"""Multi-Agent Orchestration System

This module provides intelligent orchestration of multiple AI agents working
in parallel on complex tasks. It analyzes task domains and automatically
assigns work to specialized agents.
"""

from enum import Enum
from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field
import re
from collections import defaultdict
from pathlib import Path

from src.agents.base import AgentRole


class OrchestrationStrategy(str, Enum):
    """Available orchestration strategies"""
    
    FEATURE_DEVELOPMENT = "feature_development"
    BUG_INVESTIGATION = "bug_investigation"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    SECURITY_AUDIT = "security_audit"
    CODE_QUALITY = "code_quality"
    DEPLOYMENT = "deployment"
    DATA_PIPELINE = "data_pipeline"


class TaskDomain(str, Enum):
    """Task domains for classification"""
    
    BACKEND = "backend"
    FRONTEND = "frontend"
    DATA = "data"
    AGENT = "agent"
    SECURITY = "security"
    TESTING = "testing"
    PERFORMANCE = "performance"
    DEVOPS = "devops"
    REFACTOR = "refactor"


class Task(BaseModel):
    """Individual task representation"""
    
    id: str = Field(description="Task identifier (e.g., 1.1)")
    description: str = Field(description="Task description")
    domains: List[TaskDomain] = Field(description="Associated domains")
    complexity: str = Field(description="Low, Medium, or High")
    estimated_time: int = Field(description="Estimated time in minutes")
    dependencies: List[str] = Field(default_factory=list)
    enables: List[str] = Field(default_factory=list)


class AgentAssignment(BaseModel):
    """Assignment of tasks to a specific agent"""
    
    agent_role: AgentRole
    agent_id: str
    tasks: List[str] = Field(description="Task IDs assigned")
    focus: str = Field(description="Agent's focus area")
    outputs: List[str] = Field(description="Expected output paths")
    status: str = Field(default="waiting")
    current_task: Optional[str] = None
    completed_tasks: List[str] = Field(default_factory=list)


class OrchestrationPlan(BaseModel):
    """Complete orchestration plan for a feature"""
    
    feature_name: str
    strategy: OrchestrationStrategy
    total_tasks: int
    agent_assignments: Dict[str, AgentAssignment]
    phases: List[Dict[str, List[str]]] = Field(description="Execution phases")
    estimated_sequential_time: int = Field(description="Time if done sequentially (min)")
    estimated_parallel_time: int = Field(description="Time with orchestration (min)")
    time_savings_percent: float
    critical_path: List[str] = Field(description="Tasks on critical path")


class TaskAnalyzer:
    """Analyzes tasks to determine orchestration strategy"""
    
    # Domain keyword patterns for Python projects
    DOMAIN_PATTERNS = {
        TaskDomain.BACKEND: r'\b(api|endpoint|database|server|auth|route|middleware|validation|schema|fastapi|sqlalchemy|redis)\b',
        TaskDomain.FRONTEND: r'\b(cli|terminal|ui|ux|typer|rich|prompt|interactive|display|format)\b',
        TaskDomain.DATA: r'\b(pipeline|etl|transform|extract|load|bigquery|pandas|duckdb|prefect|airflow|data quality)\b',
        TaskDomain.AGENT: r'\b(agent|llm|ai|pydantic|instructor|memory|orchestration|gpt|claude)\b',
        TaskDomain.SECURITY: r'\b(encrypt|pii|phi|audit|compliance|vulnerability|auth|owasp|jwt|hash|secret)\b',
        TaskDomain.TESTING: r'\b(test|spec|pytest|coverage|mock|fixture|unit|integration|e2e)\b',
        TaskDomain.PERFORMANCE: r'\b(optimize|slow|cache|bottleneck|profile|performance|latency|async|concurrent)\b',
        TaskDomain.DEVOPS: r'\b(deploy|docker|kubernetes|ci|cd|pipeline|monitor|helm|terraform)\b',
        TaskDomain.REFACTOR: r'\b(refactor|cleanup|technical debt|simplify|extract|pattern|design)\b'
    }
    
    def analyze_task_domains(self, task_description: str) -> List[TaskDomain]:
        """Identify domains present in a task description"""
        domains = []
        
        for domain, pattern in self.DOMAIN_PATTERNS.items():
            if re.search(pattern, task_description, re.IGNORECASE):
                domains.append(domain)
        
        return domains or [TaskDomain.BACKEND]  # Default to backend
    
    def extract_tasks_from_markdown(self, content: str) -> List[Task]:
        """Extract tasks from markdown task list"""
        tasks = []
        
        # Pattern to match task format
        task_pattern = r'####?\s*Task\s*(\d+\.\d+):\s*(.+?)\s*\[domains:\s*(.+?)\]'
        complexity_pattern = r'\*\*Complexity\*\*:\s*(\w+)\s*\((\d+)\s*min\)'
        dependencies_pattern = r'\*\*Dependencies\*\*:\s*(.+)'
        enables_pattern = r'\*\*Enables\*\*:\s*(.+)'
        
        # Find all tasks
        for match in re.finditer(task_pattern, content, re.MULTILINE):
            task_id = match.group(1)
            description = match.group(2).strip()
            domains_str = match.group(3)
            
            # Parse domains
            domains = []
            for domain_name in domains_str.split(','):
                domain_name = domain_name.strip()
                try:
                    domains.append(TaskDomain(domain_name))
                except ValueError:
                    pass
            
            # Extract complexity and time
            complexity = "Medium"
            estimated_time = 15
            
            complexity_match = re.search(complexity_pattern, content[match.end():match.end()+200])
            if complexity_match:
                complexity = complexity_match.group(1)
                estimated_time = int(complexity_match.group(2))
            
            # Extract dependencies
            dependencies = []
            deps_match = re.search(dependencies_pattern, content[match.end():match.end()+200])
            if deps_match and deps_match.group(1).strip().lower() != 'none':
                dependencies = [d.strip() for d in deps_match.group(1).split(',')]
            
            # Extract enables
            enables = []
            enables_match = re.search(enables_pattern, content[match.end():match.end()+200])
            if enables_match:
                enables = [e.strip() for e in enables_match.group(1).split(',')]
            
            tasks.append(Task(
                id=task_id,
                description=description,
                domains=domains,
                complexity=complexity,
                estimated_time=estimated_time,
                dependencies=dependencies,
                enables=enables
            ))
        
        return tasks
    
    def determine_strategy(self, tasks: List[Task]) -> OrchestrationStrategy:
        """Determine best orchestration strategy based on tasks"""
        # Count domain occurrences
        domain_counts = defaultdict(int)
        for task in tasks:
            for domain in task.domains:
                domain_counts[domain] += 1
        
        # Strategy selection logic
        if domain_counts[TaskDomain.SECURITY] > 2:
            return OrchestrationStrategy.SECURITY_AUDIT
        elif domain_counts[TaskDomain.PERFORMANCE] > 2:
            return OrchestrationStrategy.PERFORMANCE_OPTIMIZATION
        elif domain_counts[TaskDomain.REFACTOR] > 3:
            return OrchestrationStrategy.CODE_QUALITY
        elif domain_counts[TaskDomain.DEVOPS] > 2:
            return OrchestrationStrategy.DEPLOYMENT
        elif domain_counts[TaskDomain.DATA] > 3:
            return OrchestrationStrategy.DATA_PIPELINE
        elif any(domain in ['bug', 'error', 'fix'] for task in tasks for domain in task.description.lower().split()):
            return OrchestrationStrategy.BUG_INVESTIGATION
        else:
            return OrchestrationStrategy.FEATURE_DEVELOPMENT


class Orchestrator:
    """Main orchestration engine"""
    
    def __init__(self):
        self.analyzer = TaskAnalyzer()
        self.strategy_agents = {
            OrchestrationStrategy.FEATURE_DEVELOPMENT: [
                AgentRole.ARCHITECT,
                AgentRole.BACKEND,
                AgentRole.FRONTEND,
                AgentRole.DATA_ENGINEER,
                AgentRole.QA
            ],
            OrchestrationStrategy.BUG_INVESTIGATION: [
                AgentRole.ANALYZER,
                AgentRole.BACKEND,
                AgentRole.QA
            ],
            OrchestrationStrategy.PERFORMANCE_OPTIMIZATION: [
                AgentRole.PERFORMANCE,
                AgentRole.ANALYZER,
                AgentRole.BACKEND,
                AgentRole.DATA_ENGINEER
            ],
            OrchestrationStrategy.SECURITY_AUDIT: [
                AgentRole.SECURITY,
                AgentRole.ANALYZER,
                AgentRole.BACKEND
            ],
            OrchestrationStrategy.CODE_QUALITY: [
                AgentRole.REFACTORER,
                AgentRole.ARCHITECT,
                AgentRole.QA
            ],
            OrchestrationStrategy.DEPLOYMENT: [
                AgentRole.DEVOPS,
                AgentRole.SECURITY,
                AgentRole.QA
            ],
            OrchestrationStrategy.DATA_PIPELINE: [
                AgentRole.DATA_ENGINEER,
                AgentRole.BACKEND,
                AgentRole.PERFORMANCE,
                AgentRole.QA
            ]
        }
    
    def create_orchestration_plan(
        self,
        feature_name: str,
        tasks: List[Task],
        strategy: Optional[OrchestrationStrategy] = None
    ) -> OrchestrationPlan:
        """Create a complete orchestration plan"""
        # Auto-detect strategy if not provided
        if not strategy:
            strategy = self.analyzer.determine_strategy(tasks)
        
        # Get agents for strategy
        agent_roles = self.strategy_agents[strategy]
        
        # Assign tasks to agents based on domains
        assignments = self._assign_tasks_to_agents(tasks, agent_roles)
        
        # Calculate execution phases
        phases = self._calculate_execution_phases(tasks, assignments)
        
        # Calculate time estimates
        sequential_time = sum(task.estimated_time for task in tasks)
        parallel_time = self._calculate_parallel_time(phases, tasks)
        
        # Find critical path
        critical_path = self._find_critical_path(tasks)
        
        return OrchestrationPlan(
            feature_name=feature_name,
            strategy=strategy,
            total_tasks=len(tasks),
            agent_assignments=assignments,
            phases=phases,
            estimated_sequential_time=sequential_time,
            estimated_parallel_time=parallel_time,
            time_savings_percent=round((1 - parallel_time / sequential_time) * 100, 1),
            critical_path=critical_path
        )
    
    def _assign_tasks_to_agents(
        self,
        tasks: List[Task],
        agent_roles: List[AgentRole]
    ) -> Dict[str, AgentAssignment]:
        """Assign tasks to agents based on domain expertise"""
        # Domain to agent mapping
        domain_agent_map = {
            TaskDomain.BACKEND: AgentRole.BACKEND,
            TaskDomain.FRONTEND: AgentRole.FRONTEND,
            TaskDomain.DATA: AgentRole.DATA_ENGINEER,
            TaskDomain.AGENT: AgentRole.DATA_ANALYST,
            TaskDomain.SECURITY: AgentRole.SECURITY,
            TaskDomain.TESTING: AgentRole.QA,
            TaskDomain.PERFORMANCE: AgentRole.PERFORMANCE,
            TaskDomain.DEVOPS: AgentRole.DEVOPS,
            TaskDomain.REFACTOR: AgentRole.REFACTORER
        }
        
        assignments = {}
        
        # Initialize assignments for each agent
        for role in agent_roles:
            agent_id = f"{role.value}_agent"
            assignments[agent_id] = AgentAssignment(
                agent_role=role,
                agent_id=agent_id,
                tasks=[],
                focus=f"Specialized in {role.value}",
                outputs=[]
            )
        
        # Assign tasks
        for task in tasks:
            # Find best agent for task
            assigned = False
            for domain in task.domains:
                preferred_agent = domain_agent_map.get(domain)
                if preferred_agent and preferred_agent in agent_roles:
                    agent_id = f"{preferred_agent.value}_agent"
                    assignments[agent_id].tasks.append(task.id)
                    assigned = True
                    break
            
            # Fallback to first available agent
            if not assigned and agent_roles:
                agent_id = f"{agent_roles[0].value}_agent"
                assignments[agent_id].tasks.append(task.id)
        
        return assignments
    
    def _calculate_execution_phases(
        self,
        tasks: List[Task],
        assignments: Dict[str, AgentAssignment]
    ) -> List[Dict[str, List[str]]]:
        """Calculate parallel execution phases"""
        # Build task dependency graph
        task_map = {task.id: task for task in tasks}
        phases = []
        completed = set()
        
        while len(completed) < len(tasks):
            # Find tasks that can be executed in this phase
            phase_tasks = {}
            
            for task in tasks:
                if task.id in completed:
                    continue
                
                # Check if dependencies are met
                if all(dep in completed for dep in task.dependencies):
                    # Find which agent owns this task
                    for agent_id, assignment in assignments.items():
                        if task.id in assignment.tasks:
                            if agent_id not in phase_tasks:
                                phase_tasks[agent_id] = []
                            phase_tasks[agent_id].append(task.id)
                            break
            
            if phase_tasks:
                phases.append(phase_tasks)
                for agent_tasks in phase_tasks.values():
                    completed.update(agent_tasks)
            else:
                # Prevent infinite loop
                break
        
        return phases
    
    def _calculate_parallel_time(
        self,
        phases: List[Dict[str, List[str]]],
        tasks: List[Task]
    ) -> int:
        """Calculate total time with parallel execution"""
        task_map = {task.id: task for task in tasks}
        total_time = 0
        
        for phase in phases:
            # Time for each phase is the max time of any agent
            phase_time = 0
            for agent_id, task_ids in phase.items():
                agent_time = sum(task_map[tid].estimated_time for tid in task_ids)
                phase_time = max(phase_time, agent_time)
            total_time += phase_time
        
        return total_time
    
    def _find_critical_path(self, tasks: List[Task]) -> List[str]:
        """Find the critical path through task dependencies"""
        # Simple implementation - find longest dependency chain
        task_map = {task.id: task for task in tasks}
        
        def find_path_length(task_id: str, memo: Dict[str, int]) -> int:
            if task_id in memo:
                return memo[task_id]
            
            task = task_map.get(task_id)
            if not task:
                return 0
            
            max_dep_length = 0
            for dep in task.dependencies:
                max_dep_length = max(max_dep_length, find_path_length(dep, memo))
            
            memo[task_id] = task.estimated_time + max_dep_length
            return memo[task_id]
        
        # Calculate path lengths for all tasks
        memo = {}
        for task in tasks:
            find_path_length(task.id, memo)
        
        # Reconstruct critical path
        # This is simplified - proper implementation would trace back
        critical_tasks = sorted(tasks, key=lambda t: memo.get(t.id, 0), reverse=True)
        return [t.id for t in critical_tasks[:5]]  # Top 5 critical tasks