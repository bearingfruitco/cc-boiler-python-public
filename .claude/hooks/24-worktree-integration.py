#!/usr/bin/env python3
"""
Worktree Integration Hook
Ensures worktree operations integrate with existing Claude Code systems
"""

import json
import sys
import os
from pathlib import Path
import subprocess

def check_worktree_context():
    """Check if we're in a worktree and load its context"""
    try:
        # Check if we're in a git worktree
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True
        )
        
        current_root = Path(result.stdout.strip())
        
        # Check for worktree config
        worktree_config = current_root / ".claude" / "worktree-config.json"
        
        if worktree_config.exists():
            with open(worktree_config) as f:
                config = json.load(f)
                return config.get('worktree', {})
                
    except:
        pass
        
    return None

def enhance_command_for_worktree(command: str, worktree_info: dict) -> str:
    """Enhance commands with worktree context"""
    
    # Add worktree context to relevant commands
    context_commands = [
        'smart-resume',
        'task-ledger',
        'generate-tasks',
        'orchestrate-agents'
    ]
    
    if any(cmd in command for cmd in context_commands):
        # Add worktree context
        task = worktree_info.get('task', '')
        name = worktree_info.get('name', '')
        
        if task:
            command += f" --context 'Working in worktree {name}: {task}'"
            
    return command

def update_task_ledger_for_worktree(worktree_info: dict):
    """Update task ledger with worktree information"""
    ledger_path = Path(".task-ledger.md")
    
    if ledger_path.exists():
        content = ledger_path.read_text()
        
        # Add worktree marker if not present
        worktree_marker = f"[Worktree: {worktree_info['name']}]"
        if worktree_marker not in content:
            # Find the feature section and add marker
            lines = content.split('\n')
            new_lines = []
            
            for line in lines:
                new_lines.append(line)
                if line.startswith('## ') and worktree_info['name'] in line:
                    new_lines.append(f"\n{worktree_marker}")
                    
            ledger_path.write_text('\n'.join(new_lines))

def main():
    """Main hook logic"""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Check if we're in a worktree
    worktree_info = check_worktree_context()
    
    if worktree_info:
        # Enhance command with worktree context
        if 'command' in input_data:
            input_data['command'] = enhance_command_for_worktree(
                input_data['command'], 
                worktree_info
            )
            
        # Update task ledger
        update_task_ledger_for_worktree(worktree_info)
        
        # Add worktree info to context
        input_data['worktree'] = worktree_info
        
    # Pass through
    print(json.dumps(input_data))
    sys.exit(0)

if __name__ == "__main__":
    main()
