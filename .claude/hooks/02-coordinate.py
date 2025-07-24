#!/usr/bin/env python3
"""
Sub-Agent Coordination Hook - Manages parallel agent execution
Tracks progress, handles handoffs, and prevents conflicts
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def load_orchestration_state():
    """Load current orchestration state"""
    state_file = Path('.claude/orchestration/state.json')
    if state_file.exists():
        with open(state_file) as f:
            return json.load(f)
    return None

def update_agent_progress(agent_id, completed_task, next_task=None):
    """Update progress for a specific agent"""
    progress_dir = Path('.claude/orchestration/progress')
    progress_dir.mkdir(parents=True, exist_ok=True)
    
    progress_file = progress_dir / f'{agent_id}.json'
    
    progress = {
        'agent_id': agent_id,
        'last_update': datetime.now().isoformat(),
        'completed_task': completed_task,
        'next_task': next_task,
        'status': 'active' if next_task else 'waiting'
    }
    
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)
    
    return progress

def check_dependencies(task_id, orchestration_state):
    """Check if dependencies for a task are met"""
    if not orchestration_state:
        return True
        
    task_deps = orchestration_state.get('dependencies', {}).get(task_id, [])
    if not task_deps:
        return True
    
    # Check if all dependencies are completed
    completed_tasks = []
    progress_dir = Path('.claude/orchestration/progress')
    
    if progress_dir.exists():
        for progress_file in progress_dir.glob('*.json'):
            with open(progress_file) as f:
                agent_progress = json.load(f)
                if agent_progress.get('completed_task'):
                    completed_tasks.append(agent_progress['completed_task'])
    
    return all(dep in completed_tasks for dep in task_deps)

def send_handoff_message(from_agent, to_agent, message, artifacts=None):
    """Send a handoff message between agents"""
    messages_file = Path('.claude/orchestration/messages.json')
    
    messages = []
    if messages_file.exists():
        with open(messages_file) as f:
            messages = json.load(f)
    
    handoff = {
        'timestamp': datetime.now().isoformat(),
        'from': from_agent,
        'to': to_agent,
        'message': message,
        'artifacts': artifacts or {},
        'read': False
    }
    
    messages.append(handoff)
    
    with open(messages_file, 'w') as f:
        json.dump(messages, f, indent=2)
    
    return handoff

def generate_status_report():
    """Generate a status report of all agents"""
    orchestration_state = load_orchestration_state()
    if not orchestration_state:
        return "No active orchestration"
    
    report = f"=== ORCHESTRATION STATUS ===\n"
    report += f"Feature: {orchestration_state.get('feature', 'Unknown')}\n"
    report += f"Started: {orchestration_state.get('started_at', 'Unknown')}\n\n"
    
    # Check each agent's progress
    agents = orchestration_state.get('agents', {})
    progress_dir = Path('.claude/orchestration/progress')
    
    for agent_id, agent_info in agents.items():
        total_tasks = len(agent_info.get('tasks', []))
        completed = 0
        current_task = None
        
        # Load agent progress
        progress_file = progress_dir / f'{agent_id}.json'
        if progress_file.exists():
            with open(progress_file) as f:
                progress = json.load(f)
                # Count completed tasks
                for task in agent_info.get('tasks', []):
                    if task == progress.get('completed_task'):
                        completed += 1
                current_task = progress.get('next_task', 'Waiting')
        
        # Calculate percentage
        percentage = int((completed / total_tasks) * 100) if total_tasks > 0 else 0
        
        # Create progress bar
        bar_length = 20
        filled = int(bar_length * percentage / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        report += f"{agent_id.upper():<15} [{bar}] {percentage:3d}% - {current_task or 'Idle'}\n"
    
    # Add recent messages
    messages_file = Path('.claude/orchestration/messages.json')
    if messages_file.exists():
        with open(messages_file) as f:
            messages = json.load(f)
            recent = messages[-5:] if len(messages) > 5 else messages
            
            if recent:
                report += "\nRecent Handoffs:\n"
                for msg in recent:
                    report += f"  [{msg['from']} → {msg['to']}]: {msg['message'][:50]}...\n"
    
    return report

def handle_task_completion(agent_id, task_id, artifacts):
    """Handle when an agent completes a task"""
    orchestration_state = load_orchestration_state()
    if not orchestration_state:
        return
    
    # Update progress
    agent_info = orchestration_state['agents'].get(agent_id, {})
    remaining_tasks = [t for t in agent_info.get('tasks', []) if t != task_id]
    next_task = remaining_tasks[0] if remaining_tasks else None
    
    update_agent_progress(agent_id, task_id, next_task)
    
    # Check for handoffs
    handoffs = orchestration_state.get('handoffs', {}).get(task_id, [])
    for handoff in handoffs:
        target_agent = handoff['to_agent']
        send_handoff_message(
            agent_id,
            target_agent,
            f"Task {task_id} complete. {handoff.get('message', '')}",
            artifacts
        )
    
    # Generate status report
    return generate_status_report()

def prevent_conflicts(agent_id, file_path):
    """Check if an agent is allowed to modify a file"""
    orchestration_state = load_orchestration_state()
    if not orchestration_state:
        return True
    
    ownership = orchestration_state.get('file_ownership', {})
    
    # Check ownership rules
    for pattern, owner in ownership.items():
        if pattern.endswith('*'):
            # Wildcard pattern
            prefix = pattern[:-1]
            if file_path.startswith(prefix):
                return owner == agent_id
        elif file_path == pattern:
            return owner == agent_id
    
    # No ownership rules = allowed
    return True

def main():
    """Main hook logic"""
    input_data = json.loads(sys.stdin.read())
    
    # This hook is called when a sub-agent completes
    agent_id = input_data.get('agent_id')
    event_type = input_data.get('event_type', 'task_complete')
    
    if event_type == 'task_complete':
        task_id = input_data.get('task_id')
        artifacts = input_data.get('artifacts', {})
        
        report = handle_task_completion(agent_id, task_id, artifacts)
        
        print(json.dumps({
            "decision": "continue",
            "message": report,
            "next_task": input_data.get('next_task')
        }))
    
    elif event_type == 'file_check':
        file_path = input_data.get('file_path')
        allowed = prevent_conflicts(agent_id, file_path)
        
        if not allowed:
            print(json.dumps({
                "decision": "block",
                "message": f"Agent {agent_id} not authorized to modify {file_path}"
            }))
        else:
            sys.exit(0)
    
    elif event_type == 'status_request':
        report = generate_status_report()
        print(json.dumps({
            "decision": "info",
            "message": report
        }))
    
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
