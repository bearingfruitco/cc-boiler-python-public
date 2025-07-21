#!/usr/bin/env python3
"""
Branch Controller - Enforces branch management rules and prevents conflicts
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

def load_branch_registry():
    """Load branch registry."""
    registry_file = Path('.claude/branch-registry.json')
    if registry_file.exists():
        with open(registry_file, 'r') as f:
            return json.load(f)
    return {
        'main_branch': {'name': 'main', 'last_pulled': '2025-01-01T00:00:00Z'},
        'active_branches': [],
        'branch_rules': {},
        'blocked_files': {}
    }

def save_branch_registry(registry):
    """Save branch registry."""
    registry_file = Path('.claude/branch-registry.json')
    registry['last_updated'] = datetime.now().isoformat()
    with open(registry_file, 'w') as f:
        json.dump(registry, f, indent=2)

def get_current_branch():
    """Get current git branch."""
    try:
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except:
        return 'unknown'

def is_branch_creation(tool_name, command):
    """Check if operation creates a new branch."""
    if tool_name == 'bash':
        return 'git checkout -b' in command or ('git branch' in command and not '--show-current' in command)
    return False

def is_file_modification(tool_name):
    """Check if operation modifies files."""
    return tool_name in ['str_replace_editor', 'create_file']

def has_uncommitted_changes():
    """Check for uncommitted changes."""
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True
        )
        return bool(result.stdout.strip())
    except:
        return False

def get_modified_files():
    """Get list of modified files in working directory."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-only'],
            capture_output=True,
            text=True
        )
        files = result.stdout.strip().split('\n')
        return [f for f in files if f]
    except:
        return []

def check_active_branch_limit(registry):
    """Check if we're within active branch limits."""
    rules = registry.get('branch_rules', {})
    max_active = rules.get('max_active_branches', 1)
    
    active_count = len([b for b in registry['active_branches'] 
                       if b['status'] == 'in_progress'])
    
    return active_count < max_active, active_count

def check_main_sync_requirement(registry):
    """Check if main branch sync is required."""
    rules = registry.get('branch_rules', {})
    if not rules.get('require_main_sync', True):
        return True
    
    last_pulled = datetime.fromisoformat(registry['main_branch']['last_pulled'])
    sync_interval = timedelta(hours=rules.get('sync_interval_hours', 24))
    
    return datetime.now() - last_pulled <= sync_interval

def find_unfinished_work(registry):
    """Find unfinished work on current branch."""
    current_branch = get_current_branch()
    
    for branch in registry['active_branches']:
        if branch['name'] == current_branch and branch['status'] == 'in_progress':
            if not branch.get('tests_passing', False):
                return branch
    
    return None

def check_file_conflicts(new_branch_name, registry):
    """Check for potential file conflicts."""
    # Get files modified in working directory
    modified_files = get_modified_files()
    conflicts = []
    
    for branch in registry['active_branches']:
        if branch['status'] == 'in_progress' and branch['name'] != new_branch_name:
            overlapping = set(modified_files) & set(branch.get('files_modified', []))
            if overlapping:
                conflicts.append({
                    'branch': branch['name'],
                    'files': list(overlapping),
                    'issue': branch.get('issue', 'Unknown')
                })
    
    return conflicts

def format_branch_limit_error(active_count, active_branches):
    """Format error for too many active branches."""
    branch_list = "\n".join([
        f"  • {b['name']} (Issue: {b.get('issue', 'None')}, Status: {b['status']})"
        for b in active_branches if b['status'] == 'in_progress'
    ])
    
    return f"""
🚫 BRANCH LIMIT EXCEEDED!

You already have {active_count} active branch(es):

{branch_list}

📋 Branch Policy: Maximum 1 active feature branch at a time

💡 To create a new branch, first:
1. Complete current work: /fw complete [issue]
2. Or stash work: /branch stash
3. Or close branch: /branch close

Run: /branch-status to see all branches
"""

def format_sync_required_error():
    """Format error for outdated main branch."""
    return """
🔄 MAIN BRANCH SYNC REQUIRED!

Your main branch is over 24 hours old. You must sync before creating new branches.

💡 To sync:
1. Save current work: /checkpoint
2. Sync main: /sync-main
3. Then create your new branch

This prevents conflicts and ensures you're building on latest code!
"""

def format_unfinished_work_error(unfinished):
    """Format error for unfinished work."""
    return f"""
⚠️ UNFINISHED WORK DETECTED!

You have incomplete tasks on branch: {unfinished['name']}

Issue: {unfinished.get('issue', 'Unknown')}
Tests Passing: {'✅ Yes' if unfinished.get('tests_passing') else '❌ No'}
Files Modified: {len(unfinished.get('files_modified', []))}

💡 Options:
1. Run tests: /test
2. Complete feature: /fw complete {unfinished.get('issue', '')}
3. Or explicitly stash: /branch stash --reason "Starting urgent fix"

This prevents abandoned work and maintains code quality!
"""

def format_conflict_error(conflicts):
    """Format error for file conflicts."""
    conflict_details = "\n".join([
        f"  • Branch: {c['branch']} (Issue: {c['issue']})\n    Files: {', '.join(c['files'])}"
        for c in conflicts
    ])
    
    return f"""
⚠️ FILE CONFLICT DETECTED!

These files are being modified on other branches:

{conflict_details}

🚫 Cannot create conflicting branches!

💡 Options:
1. Work on different files
2. Wait for other branch to merge
3. Collaborate on existing branch: git checkout {conflicts[0]['branch']}

This prevents merge conflicts before they happen!
"""

def format_file_blocked_error(file_path, block_info):
    """Format error for blocked file access."""
    return f"""
⚠️ FILE ACCESS BLOCKED!

This file is being modified on another branch:

📄 File: {file_path}
🔒 Blocked by: {block_info['blocked_by']}
📝 Reason: {block_info.get('reason', 'Active modifications')}

💡 To modify this file:
1. Switch to the branch: git checkout {block_info['blocked_by']}
2. Or wait for that branch to merge

This prevents conflicting changes to the same file!
"""

def extract_branch_name(command):
    """Extract branch name from git command."""
    if 'git checkout -b' in command:
        parts = command.split('git checkout -b')[1].strip().split()
        if parts:
            return parts[0]
    elif 'git branch' in command:
        parts = command.split('git branch')[1].strip().split()
        if parts:
            return parts[0]
    return None

def main():
    """Main hook logic."""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    tool_name = input_data['tool']
    
    # Handle branch creation
    if tool_name == 'bash':
        command = input_data.get('command', '')
        
        if is_branch_creation(tool_name, command):
            registry = load_branch_registry()
            
            # Check active branch limit
            within_limit, active_count = check_active_branch_limit(registry)
            if not within_limit:
                active_branches = [b for b in registry['active_branches'] 
                                 if b['status'] == 'in_progress']
                error = format_branch_limit_error(active_count, active_branches)
                print(error, file=sys.stderr)
                sys.exit(1)
            
            # Check main sync requirement
            if not check_main_sync_requirement(registry):
                error = format_sync_required_error()
                print(error, file=sys.stderr)
                sys.exit(1)
            
            # Check for unfinished work
            if registry['branch_rules'].get('require_tests_before_new', True):
                unfinished = find_unfinished_work(registry)
                if unfinished:
                    error = format_unfinished_work_error(unfinished)
                    print(error, file=sys.stderr)
                    sys.exit(1)
            
            # Check for conflicts
            if registry['branch_rules'].get('prevent_conflicting_branches', True):
                branch_name = extract_branch_name(command)
                if branch_name:
                    conflicts = check_file_conflicts(branch_name, registry)
                    if conflicts:
                        error = format_conflict_error(conflicts)
                        print(error, file=sys.stderr)
                        sys.exit(1)
    
    # Handle file modifications
    elif is_file_modification(tool_name):
        file_path = input_data.get('path', '')
        if file_path:
            registry = load_branch_registry()
            
            # Check if file is blocked
            if file_path in registry.get('blocked_files', {}):
                block_info = registry['blocked_files'][file_path]
                current_branch = get_current_branch()
                
                if current_branch != block_info['blocked_by']:
                    error = format_file_blocked_error(file_path, block_info)
                    print(error, file=sys.stderr)
                    sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
