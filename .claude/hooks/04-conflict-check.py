#!/usr/bin/env python3
"""
Conflict Check Hook - Check for potential conflicts with team members
Warns about files being edited by others or potential merge issues
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def get_team_registry():
    """Load team work registry"""
    registry_path = Path(__file__).parent.parent.parent / 'team' / 'registry.json'
    if registry_path.exists():
        with open(registry_path) as f:
            return json.load(f)
    return {"active_work": {}, "worktrees": {}}

def update_team_registry(registry):
    """Save team work registry"""
    registry_path = Path(__file__).parent.parent.parent / 'team' / 'registry.json'
    registry['last_updated'] = datetime.now().isoformat()
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)

def get_current_user():
    """Get current user from team config"""
    config_path = Path(__file__).parent.parent.parent / 'team' / 'config.json'
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f).get('current_user', 'unknown')
    return 'unknown'

def check_file_locks(file_path, registry):
    """Check if file is locked by another team member"""
    current_user = get_current_user()
    active_work = registry.get('active_work', {})
    
    for user, work_info in active_work.items():
        if user != current_user:
            # Check if this user is actively editing this file
            active_files = work_info.get('active_files', [])
            if file_path in active_files:
                time_ago = calculate_time_ago(work_info.get('last_activity'))
                return {
                    'locked': True,
                    'by': user,
                    'since': time_ago,
                    'branch': work_info.get('branch', 'unknown')
                }
    
    return {'locked': False}

def calculate_time_ago(timestamp):
    """Calculate human-readable time ago"""
    if not timestamp:
        return 'unknown time'
    
    try:
        then = datetime.fromisoformat(timestamp)
        now = datetime.now()
        delta = now - then
        
        if delta.seconds < 60:
            return 'just now'
        elif delta.seconds < 3600:
            minutes = delta.seconds // 60
            return f'{minutes} minute{"s" if minutes > 1 else ""} ago'
        elif delta.days < 1:
            hours = delta.seconds // 3600
            return f'{hours} hour{"s" if hours > 1 else ""} ago'
        else:
            return f'{delta.days} day{"s" if delta.days > 1 else ""} ago'
    except:
        return 'unknown time'

def register_file_activity(file_path):
    """Register that we're working on this file"""
    registry = get_team_registry()
    current_user = get_current_user()
    
    if current_user not in registry['active_work']:
        registry['active_work'][current_user] = {
            'active_files': [],
            'last_activity': datetime.now().isoformat(),
            'branch': get_current_branch()
        }
    
    user_work = registry['active_work'][current_user]
    if file_path not in user_work['active_files']:
        user_work['active_files'].append(file_path)
    
    user_work['last_activity'] = datetime.now().isoformat()
    
    # Clean up old entries (older than 1 hour)
    user_work['active_files'] = [
        f for f in user_work['active_files']
        if f == file_path or not is_stale_activity(user_work['last_activity'])
    ]
    
    update_team_registry(registry)

def is_stale_activity(timestamp):
    """Check if activity is older than 1 hour"""
    try:
        then = datetime.fromisoformat(timestamp)
        now = datetime.now()
        return (now - then).seconds > 3600
    except:
        return True

def get_current_branch():
    """Get current git branch"""
    try:
        result = subprocess.run(
            "git branch --show-current",
            shell=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except:
        return 'unknown'

def check_related_files(file_path):
    """Check for related files that might cause conflicts"""
    related_patterns = {
        '.tsx': ['.test.tsx', '.stories.tsx', '.css', '.module.css'],
        '.ts': ['.test.ts', '.d.ts'],
        'package.json': ['package-lock.json', 'yarn.lock', 'pnpm-lock.yaml']
    }
    
    warnings = []
    base_path = Path(file_path)
    
    for ext, related_exts in related_patterns.items():
        if file_path.endswith(ext):
            for related_ext in related_exts:
                related_file = str(base_path).replace(ext, related_ext)
                lock_info = check_file_locks(related_file, get_team_registry())
                if lock_info['locked']:
                    warnings.append({
                        'file': related_file,
                        'locked_by': lock_info['by'],
                        'since': lock_info['since']
                    })
    
    return warnings

def main():
    """Main hook logic"""
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    # Only process file operations
    if input_data['tool'] not in ['write_file', 'edit_file', 'str_replace']:
        sys.exit(0)
        return
    
    file_path = input_data.get('path', '')
    registry = get_team_registry()
    
    # Check if file is locked
    lock_info = check_file_locks(file_path, registry)
    
    if lock_info['locked']:
        # File is being edited by someone else
        message = (
            f"⚠️ TEAM CONFLICT: {lock_info['by']} is editing this file "
            f"(started {lock_info['since']} on branch '{lock_info['branch']}')\n\n"
            f"Options:\n"
            f"1. Coordinate with {lock_info['by']}\n"
            f"2. Work on a different file\n"
            f"3. Override and continue (may cause conflicts)"
        )
        
        print(json.dumps({
            "decision": "warn",
            "message": message,
            "continue": True,  # Allow override
            "metadata": lock_info
        }))
        
        # Register our activity anyway
        register_file_activity(file_path)
        return
    
    # Check related files
    related_warnings = check_related_files(file_path)
    if related_warnings:
        message = "📝 FYI: Related files being edited:\n"
        for warning in related_warnings:
            message += f"  • {warning['file']} by {warning['locked_by']} ({warning['since']})\n"
        
        print(json.dumps({
            "decision": "info",
            "message": message,
            "continue": True
        }))
    
    # Register our activity
    register_file_activity(file_path)
    
    # All clear
    sys.exit(0)

if __name__ == "__main__":
    main()
