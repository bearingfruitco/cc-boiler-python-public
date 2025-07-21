#!/usr/bin/env python3
"""
Context Flow Automation Hook
Ensures proper context is maintained and passed between workflow steps
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List

def load_workflow_state() -> Dict:
    """Load current workflow state"""
    state_file = Path(".claude/context/workflow_state.json")
    if state_file.exists():
        return json.loads(state_file.read_text())
    return {
        "current_workflow": None,
        "current_step": None,
        "context_chain": [],
        "related_files": [],
        "validation_gates": []
    }

def save_workflow_state(state: Dict):
    """Save workflow state"""
    state_file = Path(".claude/context/workflow_state.json")
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(state, indent=2))

def detect_workflow_transition(input_data: Dict) -> Optional[str]:
    """Detect workflow transitions based on commands"""
    tool = input_data.get("tool", "")
    args = input_data.get("args", {})
    
    # Workflow detection patterns
    workflows = {
        # Standard workflow
        "py-prd": {"workflow": "standard", "next": ["gt", "generate-tasks"]},
        "generate-tasks": {"workflow": "standard", "next": ["pt", "process-tasks"]},
        "process-tasks": {"workflow": "standard", "next": ["test-runner", "pr-feedback"]},
        
        # PRP workflow
        "prp-create": {"workflow": "prp", "next": ["prp-execute", "prp_runner.py"]},
        "prp-execute": {"workflow": "prp", "next": ["prp_validator.py", "prp-complete"]},
        
        # Orchestration workflow
        "orchestrate-agents": {"workflow": "orchestration", "next": ["orch status", "monitor"]},
        
        # Bug fix workflow
        "bug-track": {"workflow": "bugfix", "next": ["fix", "test-runner", "bt resolve"]},
        
        # Micro task
        "micro-task": {"workflow": "micro", "next": ["implement", "checkpoint"]}
    }
    
    for cmd, info in workflows.items():
        if cmd in tool or cmd in str(args):
            return info
    
    return None

def link_related_files(workflow: str, step: str) -> List[str]:
    """Get files related to current workflow step"""
    file_patterns = {
        "standard": {
            "py-prd": ["docs/project/features/{feature}-PRD.md"],
            "generate-tasks": ["docs/project/features/{feature}-tasks.md"],
            "process-tasks": ["src/**/*.py", "tests/**/*.py"]
        },
        "prp": {
            "prp-create": ["PRPs/active/{feature}.md", "PRPs/templates/*.md"],
            "prp-execute": ["scripts/prp_runner.py", "PRPs/active/{feature}.md"],
            "prp-validate": ["scripts/prp_validator.py", "tests/**/*.py"]
        },
        "orchestration": {
            "orchestrate": [".claude/orchestration/{feature}/*.json"],
            "monitor": [".claude/orchestration/{feature}/progress.json"]
        }
    }
    
    return file_patterns.get(workflow, {}).get(step, [])

def inject_context_hints(workflow_info: Dict, state: Dict) -> str:
    """Generate context hints for the next step"""
    hints = []
    
    # Add workflow continuity hint
    if state["current_workflow"]:
        hints.append(f"Continuing {state['current_workflow']} workflow")
    
    # Add previous step context
    if state["context_chain"]:
        last_context = state["context_chain"][-1]
        hints.append(f"Previous step: {last_context['step']} completed at {last_context['time']}")
    
    # Add related files
    if state["related_files"]:
        hints.append(f"Related files: {', '.join(state['related_files'][:3])}")
    
    # Add next steps
    if workflow_info and "next" in workflow_info:
        hints.append(f"Suggested next: {' or '.join(workflow_info['next'])}")
    
    # Add validation gates
    if state["validation_gates"]:
        pending_gates = [g for g in state["validation_gates"] if not g["completed"]]
        if pending_gates:
            hints.append(f"Pending validations: {', '.join([g['name'] for g in pending_gates])}")
    
    return "\n📍 ".join(["Workflow Context:"] + hints) if hints else ""

def track_validation_gates(workflow: str, step: str) -> List[Dict]:
    """Define validation gates for workflows"""
    gates = {
        "standard": [
            {"name": "tests_pass", "step": "test-runner", "completed": False},
            {"name": "pr_approved", "step": "pr-feedback", "completed": False}
        ],
        "prp": [
            {"name": "level_1_syntax", "step": "prp-validate", "completed": False},
            {"name": "level_2_unit", "step": "prp-validate", "completed": False},
            {"name": "level_3_integration", "step": "prp-validate", "completed": False},
            {"name": "level_4_security", "step": "prp-validate", "completed": False}
        ],
        "orchestration": [
            {"name": "agents_assigned", "step": "orchestrate", "completed": False},
            {"name": "tasks_distributed", "step": "orchestrate", "completed": False},
            {"name": "all_complete", "step": "monitor", "completed": False}
        ]
    }
    
    return gates.get(workflow, [])

def hook_post_tool_use(input_data: Dict, output_data: Dict) -> Dict:
    """
    Post-tool-use hook to maintain workflow context
    Ensures context flows properly between workflow steps
    """
    # Skip if error or not a workflow command
    if output_data.get("error") or not input_data.get("tool"):
        return output_data
    
    # Load current state
    state = load_workflow_state()
    
    # Detect workflow transition
    workflow_info = detect_workflow_transition(input_data)
    
    if workflow_info:
        # Update workflow state
        state["current_workflow"] = workflow_info["workflow"]
        state["current_step"] = input_data.get("tool", "unknown")
        
        # Add to context chain
        state["context_chain"].append({
            "step": state["current_step"],
            "time": datetime.now().isoformat(),
            "input": str(input_data.get("args", {}))[:200],  # Truncate for size
            "success": not output_data.get("error", False)
        })
        
        # Link related files
        feature = input_data.get("args", {}).get("arguments", "").split()[0] if input_data.get("args") else "unknown"
        related = link_related_files(workflow_info["workflow"], state["current_step"])
        state["related_files"] = [f.format(feature=feature) for f in related]
        
        # Track validation gates
        if not state["validation_gates"]:
            state["validation_gates"] = track_validation_gates(workflow_info["workflow"], state["current_step"])
        
        # Update gate completion
        for gate in state["validation_gates"]:
            if gate["step"] == state["current_step"] and not output_data.get("error"):
                gate["completed"] = True
        
        # Inject context hints
        context_hints = inject_context_hints(workflow_info, state)
        if context_hints:
            # Add hints to output
            if isinstance(output_data.get("output"), str):
                output_data["output"] += f"\n\n{context_hints}"
            else:
                output_data["context_hints"] = context_hints
        
        # Auto-suggest next command
        if workflow_info.get("next") and not output_data.get("error"):
            next_commands = workflow_info["next"]
            suggestion = f"\n\n💡 Next step: `/{next_commands[0]}`"
            if isinstance(output_data.get("output"), str):
                output_data["output"] += suggestion
        
        # Save state
        save_workflow_state(state)
        
        # Log workflow progress
        progress = len([g for g in state["validation_gates"] if g["completed"]])
        total = len(state["validation_gates"])
        if total > 0:
            print(f"\n📊 Workflow Progress: {progress}/{total} gates completed ({progress/total*100:.0f}%)")
    
    # Context preservation between PRD/PRP and tasks
    if input_data.get("tool") in ["generate-tasks", "gt"]:
        # Ensure PRD/PRP context is available
        feature = input_data.get("args", {}).get("arguments", "").split()[0]
        prd_path = Path(f"docs/project/features/{feature}-PRD.md")
        prp_path = Path(f"PRPs/active/{feature}.md")
        
        if prd_path.exists() or prp_path.exists():
            doc_path = prp_path if prp_path.exists() else prd_path
            output_data["context_preserved"] = True
            print(f"\n📎 Context linked from: {doc_path}")
    
    # Auto-link orchestration to tasks
    if input_data.get("tool") in ["orchestrate-agents", "orch"]:
        feature = input_data.get("args", {}).get("arguments", "").split()[0]
        tasks_path = Path(f"docs/project/features/{feature}-tasks.md")
        
        if tasks_path.exists() and "--from-prp" not in str(input_data.get("args", {})):
            output_data["tasks_linked"] = True
            print(f"\n🔗 Tasks auto-linked from: {tasks_path}")
    
    return output_data

# Hook registration
sys.exit(0)
if __name__ == "__main__":
    # This allows testing the hook directly
    test_input = {
        "tool": "py-prd",
        "args": {"arguments": "user-auth"}
    }
    test_output = {"output": "PRD created successfully"}
    
    result = hook_post_tool_use(test_input, test_output)
    print(json.dumps(result, indent=2))
