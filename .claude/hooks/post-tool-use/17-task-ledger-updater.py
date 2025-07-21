#!/usr/bin/env python3
"""
Task Ledger Updater - Maintains central task tracking
Updates .task-ledger.md after task-related commands
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def main():
    """Main hook handler following official format."""
    # Read the event from stdin
    event_json = sys.stdin.read()
    
    try:
        event = json.loads(event_json)
    except json.JSONDecodeError:
        print(json.dumps({"status": "error", "message": "Invalid JSON input"}))
        return
    
    # Extract relevant information
    tool_name = event.get('tool', '')
    params = event.get('params', {})
    result = event.get('result', {})
    
    # Check if this is a task-related command by looking at file paths
    if should_update_ledger(tool_name, params, result):
        try:
            update_task_ledger(tool_name, params, result)
        except Exception as e:
            # Log error but don't block operation
            print(json.dumps({
                "status": "success",
                "warning": f"Task ledger update failed: {str(e)}"
            }))
            return
    
    # Always pass through - we're just observing
    print(json.dumps({"status": "success"}))

def should_update_ledger(tool_name: str, params: Dict, result: Dict) -> bool:
    """Check if this tool use should trigger ledger update."""
    # Check for task file creation/modification
    if tool_name in ['str_replace', 'create']:
        path = params.get('path', '')
        # Check if it's a task file
        if 'docs/project/features/' in path and '-tasks.md' in path:
            return True
    
    # Check for command execution output
    if tool_name == 'str_replace' and params.get('path', '').endswith('/cmd_output.txt'):
        # Look for task-related command indicators in the content
        content = params.get('new_str', '')
        task_commands = [
            'generate-tasks', 'process-tasks', 'feature-workflow',
            'task-status', 'verify-task', 'task-checkpoint'
        ]
        for cmd in task_commands:
            if cmd in content:
                return True
    
    return False

def update_task_ledger(tool_name: str, params: Dict, result: Dict):
    """Update the task ledger based on command execution."""
    ledger_path = Path('.task-ledger.md')
    
    # Determine what action to take
    if 'docs/project/features/' in params.get('path', ''):
        # Task file was created/modified
        handle_task_file_change(params.get('path', ''), ledger_path)
    else:
        # Command was executed
        handle_command_execution(params, ledger_path)

def handle_task_file_change(file_path: str, ledger_path: Path):
    """Handle changes to task files."""
    # Extract feature name from path
    match = re.search(r'features/(.+?)-tasks\.md', file_path)
    if not match:
        return
    
    feature_name = match.group(1)
    
    # Check if this is a new task file
    task_file = Path(file_path)
    if task_file.exists():
        add_or_update_ledger_entry(feature_name, task_file, ledger_path)

def handle_command_execution(params: Dict, ledger_path: Path):
    """Handle command execution output."""
    content = params.get('new_str', '')
    
    # Extract command and feature from output
    # Look for patterns like "/generate-tasks user-auth"
    match = re.search(r'/(generate-tasks|process-tasks|feature-workflow)\s+(\S+)', content)
    if match:
        command = match.group(1)
        feature = match.group(2)
        
        if command == 'generate-tasks':
            # Will be handled by file creation
            pass
        elif command == 'process-tasks':
            update_task_progress(feature, ledger_path)
        elif command == 'feature-workflow' and 'start' in content:
            # Extract issue number if present
            issue_match = re.search(r'(\d+)', content)
            if issue_match:
                link_issue_to_feature(feature, issue_match.group(1), ledger_path)

def add_or_update_ledger_entry(feature_name: str, task_file: Path, ledger_path: Path):
    """Add or update a ledger entry for a feature."""
    # Read task file to get task count
    task_content = task_file.read_text()
    task_count = len(re.findall(r'#### Task \d+\.\d+:', task_content))
    completed_count = len(re.findall(r'- \[x\]', task_content))
    
    # Create ledger if it doesn't exist
    if not ledger_path.exists():
        ledger_content = f"# Task Ledger for {Path.cwd().name}\n\n"
        ledger_content += "This file tracks all tasks generated and processed by Claude Code commands.\n\n"
    else:
        ledger_content = ledger_path.read_text()
    
    # Check if feature already exists
    if f"## Task: {feature_name}" in ledger_content:
        # Update existing entry
        update_existing_entry(feature_name, task_count, completed_count, ledger_content, ledger_path)
    else:
        # Add new entry
        add_new_entry(feature_name, task_count, ledger_content, ledger_path)

def add_new_entry(feature_name: str, task_count: int, ledger_content: str, ledger_path: Path):
    """Add a new feature entry to the ledger."""
    new_entry = f"""## Task: {feature_name}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Issue**: Not linked
**Status**: Generated
**Branch**: Not created
**Progress**: 0/{task_count} tasks completed

### Description
Feature implementation tasks generated from PRD/Issue.

### Task File
See detailed tasks in: `docs/project/features/{feature_name}-tasks.md`

### Validation Checklist
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] No regressions
- [ ] Code review completed

---

"""
    
    ledger_path.write_text(ledger_content + new_entry)

def update_existing_entry(feature_name: str, task_count: int, completed_count: int, ledger_content: str, ledger_path: Path):
    """Update an existing ledger entry."""
    # Calculate progress
    progress_pct = int((completed_count / task_count * 100)) if task_count > 0 else 0
    
    # Determine status
    if completed_count == 0:
        status = "Generated"
    elif completed_count == task_count:
        status = "Completed"
    elif progress_pct > 0:
        status = "In Progress"
    else:
        status = "Generated"
    
    # Update progress line
    progress_pattern = rf'(## Task: {feature_name}.*?\*\*Progress\*\*: )[^\n]+'
    new_progress = rf'\g<1>{completed_count}/{task_count} tasks completed ({progress_pct}%)'
    ledger_content = re.sub(progress_pattern, new_progress, ledger_content, flags=re.DOTALL)
    
    # Update status
    status_pattern = rf'(## Task: {feature_name}.*?\*\*Status\*\*: )[^\n]+'
    new_status = rf'\g<1>{status}'
    ledger_content = re.sub(status_pattern, new_status, ledger_content, flags=re.DOTALL)
    
    ledger_path.write_text(ledger_content)

def update_task_progress(feature_name: str, ledger_path: Path):
    """Update task progress when process-tasks is run."""
    if not ledger_path.exists():
        return
    
    # Check the actual task file for progress
    task_file = Path(f'docs/project/features/{feature_name}-tasks.md')
    if task_file.exists():
        task_content = task_file.read_text()
        task_count = len(re.findall(r'#### Task \d+\.\d+:', task_content))
        completed_count = len(re.findall(r'- \[x\]', task_content))
        
        ledger_content = ledger_path.read_text()
        update_existing_entry(feature_name, task_count, completed_count, ledger_content, ledger_path)

def link_issue_to_feature(feature_name: str, issue_number: str, ledger_path: Path):
    """Link a GitHub issue to a feature in the ledger."""
    if not ledger_path.exists():
        return
    
    ledger_content = ledger_path.read_text()
    
    # Update issue line
    issue_pattern = rf'(## Task: {feature_name}.*?\*\*Issue\*\*: )[^\n]+'
    new_issue = rf'\g<1>#{issue_number}'
    ledger_content = re.sub(issue_pattern, new_issue, ledger_content, flags=re.DOTALL)
    
    # Update branch line
    branch_pattern = rf'(## Task: {feature_name}.*?\*\*Branch\*\*: )[^\n]+'
    new_branch = rf'\g<1>feature/{issue_number}-{feature_name}'
    ledger_content = re.sub(branch_pattern, new_branch, ledger_content, flags=re.DOTALL)
    
    ledger_path.write_text(ledger_content)

if __name__ == "__main__":
    main()
