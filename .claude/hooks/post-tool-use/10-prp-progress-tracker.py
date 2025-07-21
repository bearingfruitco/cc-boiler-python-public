#!/usr/bin/env python3
"""
PRP Progress Tracker Hook - Track PRP execution progress
Updates progress tracking when working on PRP-related files
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

def load_prp_state(prp_name: str) -> Dict:
    """Load current PRP state"""
    state_file = Path(f".claude/context/prp_state_{prp_name}.json")
    if state_file.exists():
        return json.loads(state_file.read_text())
    return {
        "name": prp_name,
        "started": datetime.now().isoformat(),
        "tasks": {},
        "validation": {
            "level1": "pending",
            "level2": "pending", 
            "level3": "pending",
            "level4": "pending"
        },
        "progress": 0
    }

def save_prp_state(prp_name: str, state: Dict):
    """Save PRP state"""
    state_file = Path(f".claude/context/prp_state_{prp_name}.json")
    state_file.parent.mkdir(exist_ok=True)
    state_file.write_text(json.dumps(state, indent=2))

def extract_prp_name(file_path: str) -> Optional[str]:
    """Extract PRP name from file path"""
    if "PRPs/active/" in file_path:
        # PRPs/active/feature-name.md
        filename = Path(file_path).stem
        return filename
    elif "/test_" in file_path:
        # tests/test_feature_name.py
        parts = Path(file_path).stem.split("_", 1)
        if len(parts) > 1:
            return parts[1]
    return None

def check_test_generation_needed(state: Dict, task_key: str) -> bool:
    """Check if tests need to be generated for a task"""
    # Check if this is an implementation task that needs tests
    implementation_tasks = ["task_models", "task_api", "task_services", "task_agents"]
    
    if task_key in implementation_tasks:
        # Check if tests task exists and has files
        if "task_tests" not in state["tasks"] or not state["tasks"]["task_tests"]["files"]:
            return True
    return False

def update_task_progress(state: Dict, file_path: str, content: str):
    """Update task progress based on file changes"""
    # Map file patterns to tasks
    task_mapping = {
        "models/": "task_models",
        "api/endpoints/": "task_api", 
        "services/": "task_services",
        "agents/": "task_agents",
        "tests/": "task_tests",
        "db/": "task_database"
    }
    
    for pattern, task_key in task_mapping.items():
        if pattern in file_path:
            if task_key not in state["tasks"]:
                state["tasks"][task_key] = {
                    "status": "in_progress",
                    "files": [],
                    "started": datetime.now().isoformat()
                }
            
            task = state["tasks"][task_key]
            if file_path not in task["files"]:
                task["files"].append(file_path)
            
            # Check if task looks complete
            if "TODO" not in content and "FIXME" not in content:
                task["status"] = "completed"
                task["completed"] = datetime.now().isoformat()
            
            # Check if tests need to be generated
            if check_test_generation_needed(state, task_key):
                print(f"\n🧪 Tests needed for {task_key}. Run: /generate-tests {state['name']}", 
                      file=sys.stderr)
            
            break

def check_validation_gates(state: Dict, file_path: str, tool: str):
    """Check if validation gates are being executed"""
    if tool == "Bash":
        validation_commands = {
            "ruff check": "level1",
            "mypy": "level1",
            "pytest": "level2",
            "docker-compose.*test": "level3",
            "bandit": "level4",
            "safety check": "level4"
        }
        
        for cmd_pattern, level in validation_commands.items():
            if cmd_pattern in file_path:
                state["validation"][level] = "passed"
                break

def calculate_progress(state: Dict) -> int:
    """Calculate overall progress percentage"""
    # Task completion
    total_tasks = len(state["tasks"])
    completed_tasks = sum(1 for t in state["tasks"].values() 
                         if t["status"] == "completed")
    
    # Validation completion
    total_validation = len(state["validation"])
    passed_validation = sum(1 for v in state["validation"].values() 
                           if v == "passed")
    
    if total_tasks == 0:
        return 0
    
    task_weight = 0.7  # 70% weight to tasks
    validation_weight = 0.3  # 30% weight to validation
    
    task_progress = (completed_tasks / max(total_tasks, 1)) * 100 * task_weight
    validation_progress = (passed_validation / total_validation) * 100 * validation_weight
    
    return int(task_progress + validation_progress)

def main():
    """Main hook logic"""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    tool = input_data.get('tool', '')
    file_path = input_data.get('path', '')
    content = input_data.get('content', '')
    
    # Check if this is PRP-related work
    prp_name = extract_prp_name(file_path)
    
    # Also check if we're in a PRP directory
    if not prp_name and "PRPs/active" in os.getcwd():
        # Try to infer from current directory
        cwd_parts = Path(os.getcwd()).parts
        if "PRPs" in cwd_parts and "active" in cwd_parts:
            idx = cwd_parts.index("active")
            if idx + 1 < len(cwd_parts):
                prp_name = cwd_parts[idx + 1]
    
    if prp_name:
        # Load current state
        state = load_prp_state(prp_name)
        
        # Update based on activity
        if tool in ['write_file', 'str_replace', 'create_file']:
            update_task_progress(state, file_path, content)
        elif tool == 'Bash':
            check_validation_gates(state, content, tool)
        
        # Calculate progress
        state["progress"] = calculate_progress(state)
        state["last_updated"] = datetime.now().isoformat()
        
        # Save updated state
        save_prp_state(prp_name, state)
        
        # Log progress
        if state["progress"] > 0:
            print(f"PRP Progress: {prp_name} - {state['progress']}% complete", 
                  file=sys.stderr)
    
    # Always continue
    sys.exit(0)

if __name__ == "__main__":
    main()
