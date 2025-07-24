#!/usr/bin/env python3
"""
Thinking Level Integration Hook
Automatically sets appropriate thinking level based on command/context
"""

import json
import sys
import os
from pathlib import Path

def get_current_thinking_level():
    """Get the current thinking level from state."""
    state_file = Path('.claude/context/workflow_state.json')
    if state_file.exists():
        with open(state_file, 'r') as f:
            state = json.load(f)
            return state.get('thinking_level', 'standard')
    return 'standard'

def set_thinking_level(level, scope='task'):
    """Set the thinking level in state."""
    state_file = Path('.claude/context/workflow_state.json')
    state = {}
    if state_file.exists():
        with open(state_file, 'r') as f:
            state = json.load(f)
    
    state['thinking_level'] = level
    state['thinking_scope'] = scope
    
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)

def should_escalate_thinking(tool_name, parameters):
    """Determine if thinking level should be escalated."""
    # Commands that trigger deep thinking
    deep_triggers = [
        'think-through',
        'prp-create',
        'py-prd',
        'security-check',
        'performance-monitor'
    ]
    
    # Keywords that trigger deep thinking
    deep_keywords = [
        'architecture',
        'design',
        'security',
        'performance',
        'optimize',
        'debug'
    ]
    
    # Check command
    if tool_name == 'Task':
        command = parameters.get('command', '')
        for trigger in deep_triggers:
            if trigger in command:
                return 'deep'
    
    # Check for keywords in parameters
    param_str = json.dumps(parameters).lower()
    for keyword in deep_keywords:
        if keyword in param_str:
            return 'deep'
    
    # Ultra thinking for critical issues
    ultra_keywords = ['security breach', 'data loss', 'critical bug', 'production issue']
    for keyword in ultra_keywords:
        if keyword in param_str:
            return 'ultra'
    
    return None

def main():
    """Main hook logic."""
    try:
        # Read input
        input_data = json.loads(sys.stdin.read())
        tool_name = input_data.get('tool_name', '')
        parameters = input_data.get('tool_input', {})
        
        # Check if thinking level should be escalated
        suggested_level = should_escalate_thinking(tool_name, parameters)
        current_level = get_current_thinking_level()
        
        if suggested_level and suggested_level != current_level:
            # Log the escalation
            level_weights = {'standard': 1, 'deep': 2, 'ultra': 3}
            if level_weights.get(suggested_level, 0) > level_weights.get(current_level, 0):
                set_thinking_level(suggested_level, 'task')
                print(f"🧠 Thinking level escalated to '{suggested_level}' for this task")
        
    except Exception as e:
        # Don't block on errors
        if os.environ.get('DEBUG_HOOKS'):
            print(f"Thinking integration error: {e}", file=sys.stderr)
        pass
    
    sys.exit(0)

if __name__ == "__main__":
    main()
