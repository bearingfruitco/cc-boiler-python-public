#!/usr/bin/env python3
"""
Feature State Guardian - Prevents recreation of completed features
Ensures branch awareness and protects working implementations
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def load_feature_state():
    """Load feature state registry."""
    state_file = Path('.claude/feature-state.json')
    if state_file.exists():
        with open(state_file, 'r') as f:
            return json.load(f)
    return {'features': {}, 'branches': {}, 'protected_files': {}}

def load_workflow_state():
    """Load current workflow state."""
    state_file = Path('.claude/context/workflow_state.json')
    if state_file.exists():
        try:
            with open(state_file, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}

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

def find_feature_for_file(file_path, feature_state):
    """Find which feature owns a file."""
    for feature_name, feature_data in feature_state['features'].items():
        if file_path in feature_data.get('files', []):
            return feature_name, feature_data
    return None, None

def check_branch_context(file_path, current_branch, feature_data):
    """Check if we're on the right branch for this file."""
    if feature_data.get('status') == 'completed' and feature_data.get('do_not_recreate'):
        # Check if there's in-progress enhancement
        if 'in_progress_enhancements' in feature_data:
            enhancement = feature_data['in_progress_enhancements']
            if current_branch != enhancement.get('branch'):
                return False, 'wrong_branch', enhancement
        elif current_branch != 'main':
            # Modifying completed feature from non-main branch
            return False, 'completed_feature', None
    
    # Check if file is blocked by another branch
    protected_files = feature_state.get('protected_files', {})
    if file_path in protected_files:
        protection = protected_files[file_path]
        if current_branch != protection.get('branch'):
            return False, 'file_blocked', protection
    
    return True, None, None

def format_warning(warning_type, feature_name, feature_data, file_path, current_branch, extra_data=None):
    """Format appropriate warning message."""
    
    if warning_type == 'completed_feature':
        return f"""
⚠️ FEATURE STATE PROTECTION TRIGGERED!

You're about to modify a COMPLETED feature that's already working!

📍 Feature: {feature_name}
📄 File: {file_path}
✅ Status: {feature_data['status']} (completed {feature_data.get('completed_date', 'unknown')})
🌿 Current Branch: {current_branch}
⚠️ Main Branch Has: {feature_data['working_implementation']['description']}

🛡️ Protection Reasons:
1. This feature is marked as complete and working
2. You're on a different branch that might not have latest code
3. Changes could overwrite the working implementation

💡 Recommended Actions:
1. Switch to main: `git checkout main && git pull`
2. Create new branch FROM main: `git checkout -b feature/enhance-{feature_name}`
3. Use: /feature-status {feature_name} to check details

To override (with caution): Use /truth-override
"""
    
    elif warning_type == 'wrong_branch':
        enhancement = extra_data
        return f"""
⚠️ WRONG BRANCH FOR THIS ENHANCEMENT!

You're trying to modify {feature_name} from the wrong branch!

📍 Feature: {feature_name}
🎯 Enhancement Issue: {enhancement.get('issue', 'Unknown')}
✅ Correct Branch: {enhancement['branch']}
❌ Current Branch: {current_branch}
📝 Enhancement Goal: {enhancement.get('adding', 'Unknown')}

💡 To fix:
1. Stash current changes: `git stash`
2. Switch to correct branch: `git checkout {enhancement['branch']}`
3. Apply changes: `git stash pop`

This prevents duplicate work and merge conflicts!
"""
    
    elif warning_type == 'file_blocked':
        protection = extra_data
        return f"""
⚠️ FILE IS BLOCKED BY ANOTHER BRANCH!

This file is being modified on a different branch!

📄 File: {file_path}
🔒 Blocked by: {protection['branch']}
📝 Reason: {protection.get('reason', 'Active modifications')}
❌ Current Branch: {current_branch}

💡 Options:
1. Switch to the branch: `git checkout {protection['branch']}`
2. Wait for that branch to merge
3. Work on different files

This prevents merge conflicts before they happen!
"""

def main():
    """Main hook logic."""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Only check on file modifications
    if input_data['tool'] not in ['str_replace_editor', 'create_file']:
        sys.exit(0)
        return
    
    # Get file path
    path = input_data.get('path', '')
    if not path:
        sys.exit(0)
        return
    
    # Skip non-Python files unless they're critical configs
    if not (path.endswith('.py') or path.endswith('.json') or path.endswith('.yaml')):
        sys.exit(0)
        return
    
    # Load states
    feature_state = load_feature_state()
    current_branch = get_current_branch()
    
    # Update feature state with current branch
    feature_state['current_branch'] = current_branch
    
    # Find if this file belongs to a feature
    feature_name, feature_data = find_feature_for_file(path, feature_state)
    
    if feature_data:
        # Check branch context
        allowed, warning_type, extra_data = check_branch_context(
            path, current_branch, feature_data
        )
        
        if not allowed:
            warning = format_warning(
                warning_type, feature_name, feature_data, 
                path, current_branch, extra_data
            )
            print(warning, file=sys.stderr)
            
            # Check for override
            workflow_state = load_workflow_state()
            if not workflow_state.get('truth_override_active'):
                sys.exit(1)  # Block the operation
    
    sys.exit(0)

if __name__ == "__main__":
    main()
