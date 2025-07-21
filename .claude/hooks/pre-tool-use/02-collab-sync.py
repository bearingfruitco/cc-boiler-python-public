#!/usr/bin/env python3
"""
Collaboration Sync Hook - Sync with GitHub before file operations
Prevents conflicts between multiple agents working on the same codebase
"""

import json
import sys
import subprocess
import os
from datetime import datetime, timedelta
from pathlib import Path

def get_config():
    """Load hook configuration"""
    config_path = Path(__file__).parent.parent / 'config.json'
    with open(config_path) as f:
        return json.load(f)

def get_team_config():
    """Load team configuration"""
    team_config_path = Path(__file__).parent.parent.parent / 'team' / 'config.json'
    if team_config_path.exists():
        with open(team_config_path) as f:
            return json.load(f)
    return {"current_user": "unknown"}

def run_git_command(cmd):
    """Run a git command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return {"success": True, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr}

def get_last_sync():
    """Get timestamp of last sync"""
    sync_file = Path(__file__).parent.parent.parent / 'team' / 'last_sync.json'
    if sync_file.exists():
        with open(sync_file) as f:
            data = json.load(f)
            return datetime.fromisoformat(data.get('timestamp', '2000-01-01'))
    return datetime(2000, 1, 1)

def update_last_sync():
    """Update last sync timestamp"""
    sync_file = Path(__file__).parent.parent.parent / 'team' / 'last_sync.json'
    with open(sync_file, 'w') as f:
        json.dump({"timestamp": datetime.now().isoformat()}, f)

def should_sync(file_path, config):
    """Determine if we should sync before this operation"""
    # Always sync for certain file types
    critical_files = [
        'package.json',
        'tsconfig.json',
        '.env',
        'schema.prisma',
        'tailwind.config.js'
    ]
    
    if any(cf in file_path for cf in critical_files):
        return True
    
    # Check time since last sync
    last_sync = get_last_sync()
    sync_interval = config['team']['sync_interval']
    
    if datetime.now() - last_sync > timedelta(seconds=sync_interval):
        return True
    
    return False

def check_for_conflicts(file_path):
    """Check if file has been modified by others"""
    # Get last commit author for this file
    result = run_git_command(f"git log -1 --format='%an' -- {file_path}")
    if result['success'] and result['output'].strip():
        last_author = result['output'].strip()
        current_user = get_team_config().get('current_user', 'unknown')
        
        if last_author != current_user and last_author != 'unknown':
            # Get time of last modification
            time_result = run_git_command(f"git log -1 --format='%cr' -- {file_path}")
            time_ago = time_result['output'].strip() if time_result['success'] else 'unknown time'
            
            return {
                'has_conflict': True,
                'last_author': last_author,
                'time_ago': time_ago
            }
    
    return {'has_conflict': False}

def main():
    """Main hook logic"""
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    # Only process file operations
    if input_data['tool'] not in ['write_file', 'edit_file', 'str_replace']:
        # Pass through - not a file operation
        sys.exit(0)
        return
    
    config = get_config()
    file_path = input_data.get('path', '')
    
    # Check if we should sync
    if should_sync(file_path, config):
        # Fetch latest changes
        fetch_result = run_git_command("git fetch origin")
        
        if fetch_result['success']:
            # Check for upstream changes
            status_result = run_git_command("git status -uno")
            
            if "Your branch is behind" in status_result.get('output', ''):
                # Try to pull and rebase
                pull_result = run_git_command("git pull --rebase origin $(git branch --show-current)")
                
                if not pull_result['success']:
                    # Conflict detected
                    print(json.dumps({
                        "decision": "block",
                        "message": f"⚠️ SYNC REQUIRED: Cannot auto-merge changes from remote. Please resolve conflicts first.",
                        "suggestion": "Run: git status to see conflicts, then /collab-sync resolve"
                    }))
                    return
                else:
                    update_last_sync()
    
    # Check if file was modified by someone else
    conflict_info = check_for_conflicts(file_path)
    
    if conflict_info['has_conflict']:
        # Warn but don't block
        team_config = get_team_config()
        current_user = team_config.get('current_user', 'unknown')
        
        print(json.dumps({
            "decision": "warn",
            "message": f"📝 NOTE: {conflict_info['last_author']} edited this file {conflict_info['time_ago']}",
            "continue": True
        }))
        return
    
    # All clear - continue
    sys.exit(0)

if __name__ == "__main__":
    main()
