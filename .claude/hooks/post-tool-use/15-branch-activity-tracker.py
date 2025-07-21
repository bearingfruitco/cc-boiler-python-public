#!/usr/bin/env python3
"""
Branch Activity Tracker - Automatically tracks file modifications per branch
Updates branch registry and feature states
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

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
        return None

def load_branch_registry():
    """Load branch registry."""
    registry_file = Path('.claude/branch-registry.json')
    if registry_file.exists():
        with open(registry_file, 'r') as f:
            return json.load(f)
    return {
        'main_branch': {'name': 'main'},
        'active_branches': [],
        'blocked_files': {}
    }

def save_branch_registry(registry):
    """Save branch registry."""
    registry_file = Path('.claude/branch-registry.json')
    registry['last_updated'] = datetime.now().isoformat()
    with open(registry_file, 'w') as f:
        json.dump(registry, f, indent=2)

def find_or_create_branch_entry(registry, branch_name):
    """Find or create branch entry in registry."""
    for branch in registry['active_branches']:
        if branch['name'] == branch_name:
            return branch
    
    # Create new entry
    new_branch = {
        'name': branch_name,
        'status': 'in_progress',
        'created': datetime.now().isoformat(),
        'files_modified': [],
        'last_activity': datetime.now().isoformat()
    }
    registry['active_branches'].append(new_branch)
    return new_branch

def update_file_tracking(registry, branch_name, file_path):
    """Update file tracking for branch."""
    branch = find_or_create_branch_entry(registry, branch_name)
    
    # Update modified files list
    if file_path not in branch['files_modified']:
        branch['files_modified'].append(file_path)
    
    # Update last activity
    branch['last_activity'] = datetime.now().isoformat()
    
    # Update file blocks
    if file_path not in registry['blocked_files']:
        registry['blocked_files'][file_path] = {
            'blocked_by': branch_name,
            'since': datetime.now().isoformat(),
            'reason': 'Active modifications'
        }

def update_feature_state(file_path, branch_name):
    """Update feature state if file belongs to tracked feature."""
    state_file = Path('.claude/feature-state.json')
    if not state_file.exists():
        return
    
    with open(state_file, 'r') as f:
        feature_state = json.load(f)
    
    # Check if file belongs to any feature
    for feature_name, feature_data in feature_state['features'].items():
        if file_path in feature_data.get('files', []):
            # Update in-progress enhancement if applicable
            if branch_name != 'main' and feature_data.get('status') == 'completed':
                feature_data['in_progress_enhancements'] = {
                    'branch': branch_name,
                    'last_updated': datetime.now().isoformat()
                }
    
    # Save updated state
    feature_state['last_updated'] = datetime.now().isoformat()
    with open(state_file, 'w') as f:
        json.dump(feature_state, f, indent=2)

def main():
    """Main hook logic."""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Only track file modifications
    if input_data['tool'] not in ['str_replace_editor', 'create_file']:
        sys.exit(0)
        return
    
    # Get current branch
    current_branch = get_current_branch()
    if not current_branch:
        sys.exit(0)
        return
    
    # Get file path
    file_path = input_data.get('path', '')
    if not file_path:
        sys.exit(0)
        return
    
    # Skip if successful
    if input_data.get('exit_code', 0) != 0:
        sys.exit(0)
        return
    
    # Update branch registry
    registry = load_branch_registry()
    update_file_tracking(registry, current_branch, file_path)
    save_branch_registry(registry)
    
    # Update feature state
    update_feature_state(file_path, current_branch)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
