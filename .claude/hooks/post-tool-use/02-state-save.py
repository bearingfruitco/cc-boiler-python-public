#!/usr/bin/env python3
"""
State Save Hook - Automatically save work state to GitHub
Enables seamless handoffs between team members
"""

import json
import sys
import subprocess
import os
from datetime import datetime
from pathlib import Path
import hashlib

def get_config():
    """Load hook configuration"""
    config_path = Path(__file__).parent.parent / 'config.json'
    with open(config_path) as f:
        return json.load(f)

def get_current_user():
    """Get current user from team config"""
    config_path = Path(__file__).parent.parent.parent / 'team' / 'config.json'
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f).get('current_user', 'unknown')
    return 'unknown'

def get_git_info():
    """Get current git branch and commit info"""
    try:
        branch = subprocess.run(
            "git branch --show-current",
            shell=True,
            capture_output=True,
            text=True
        ).stdout.strip()
        
        commit = subprocess.run(
            "git rev-parse --short HEAD",
            shell=True,
            capture_output=True,
            text=True
        ).stdout.strip()
        
        # Extract issue number from branch name
        issue_number = None
        if '/' in branch:
            parts = branch.split('/')[-1].split('-')
            if parts[0].isdigit():
                issue_number = parts[0]
        
        return {
            'branch': branch,
            'commit': commit,
            'issue': issue_number
        }
    except:
        return {'branch': 'unknown', 'commit': 'unknown', 'issue': None}

def get_modified_files():
    """Get list of modified files"""
    try:
        result = subprocess.run(
            "git status --porcelain",
            shell=True,
            capture_output=True,
            text=True
        )
        
        modified = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                status = line[:2]
                file_path = line[3:]
                modified.append({
                    'path': file_path,
                    'status': status.strip()
                })
        
        return modified
    except:
        return []

def get_work_context(file_path=None):
    """Get current work context"""
    context = {
        'timestamp': datetime.now().isoformat(),
        'user': get_current_user(),
        'git': get_git_info(),
        'modified_files': get_modified_files(),
        'current_file': file_path
    }
    
    # Add recent TODOs
    todos = get_recent_todos()
    if todos:
        context['todos'] = todos
    
    return context

def get_recent_todos():
    """Extract recent TODOs from codebase"""
    try:
        result = subprocess.run(
            "grep -r 'TODO:' --include='*.tsx' --include='*.ts' . | head -10",
            shell=True,
            capture_output=True,
            text=True
        )
        
        todos = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                parts = line.split(':', 2)
                if len(parts) >= 3:
                    todos.append({
                        'file': parts[0].replace('./', ''),
                        'line': parts[1] if parts[1].isdigit() else None,
                        'text': parts[2].strip() if len(parts) > 2 else parts[1].strip()
                    })
        
        return todos[:5]  # Return top 5
    except:
        return []

def should_save_state(last_save_time, config):
    """Determine if we should save state now"""
    if not last_save_time:
        return True
    
    # Check throttle setting
    throttle = config['hooks']['post-tool-use'][0].get('throttle', 60)
    elapsed = (datetime.now() - last_save_time).seconds
    
    return elapsed >= throttle

def save_to_github_gist(state, config):
    """Save state to GitHub gist"""
    git_info = state['git']
    
    if not git_info['issue']:
        # No issue number - use branch name
        gist_name = f"work-state-{git_info['branch'].replace('/', '-')}.json"
    else:
        gist_name = f"work-state-issue-{git_info['issue']}.json"
    
    # Create gist content
    gist_content = json.dumps(state, indent=2)
    
    # Check if gist exists
    try:
        # List gists and find ours
        list_result = subprocess.run(
            "gh gist list --limit 100",
            shell=True,
            capture_output=True,
            text=True
        )
        
        gist_id = None
        for line in list_result.stdout.strip().split('\n'):
            if gist_name in line:
                # Extract gist ID (first field)
                gist_id = line.split('\t')[0]
                break
        
        if gist_id:
            # Update existing gist
            with open(f'/tmp/{gist_name}', 'w') as f:
                f.write(gist_content)
            
            result = subprocess.run(
                f"gh gist edit {gist_id} /tmp/{gist_name}",
                shell=True,
                capture_output=True,
                text=True
            )
            
            os.remove(f'/tmp/{gist_name}')
            return {'success': True, 'gist_id': gist_id, 'decision': 'updated'}
        else:
            # Create new gist
            with open(f'/tmp/{gist_name}', 'w') as f:
                f.write(gist_content)
            
            visibility = "--public" if config['github']['gist_visibility'] == 'public' else ""
            result = subprocess.run(
                f"gh gist create /tmp/{gist_name} --desc 'Work state for {git_info[\"branch\"]}' {visibility}",
                shell=True,
                capture_output=True,
                text=True
            )
            
            os.remove(f'/tmp/{gist_name}')
            
            if result.returncode == 0:
                # Extract gist URL from output
                gist_url = result.stdout.strip()
                gist_id = gist_url.split('/')[-1]
                return {'success': True, 'gist_id': gist_id, 'decision': 'created', 'url': gist_url}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}
    
    return {'success': False, 'error': 'Unknown error'}

def update_pr_description(state):
    """Update PR description with current state"""
    git_info = state['git']
    
    if not git_info['issue']:
        return
    
    try:
        # Check if PR exists for this branch
        result = subprocess.run(
            f"gh pr view {git_info['branch']} --json number",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            pr_data = json.loads(result.stdout)
            pr_number = pr_data['number']
            
            # Create state summary
            state_summary = f"""
<!-- WORK STATE -->
## 🔄 Current Work State
- **Last Updated**: {state['timestamp']}
- **Agent**: {state['user']}
- **Modified Files**: {len(state['modified_files'])}
- **Active TODOs**: {len(state.get('todos', []))}

### Resume Command
```bash
/compact-prepare resume {git_info['issue']}
```
<!-- END WORK STATE -->
"""
            
            # Update PR description
            subprocess.run(
                f"gh pr edit {pr_number} --add-section 'work-state' --body-file -",
                shell=True,
                input=state_summary,
                text=True
            )
    except:
        pass  # Silently fail - PR might not exist yet

# Track last save time in memory
last_save_time = None

def main():
    """Main hook logic"""
    global last_save_time
    
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    config = get_config()
    
    # Check if we should save
    if not should_save_state(last_save_time, config):
        sys.exit(0)
        return
    
    # Get current work context
    file_path = input_data.get('path')
    state = get_work_context(file_path)
    
    # Save to GitHub
    result = save_to_github_gist(state, config)
    
    if result['success']:
        last_save_time = datetime.now()
        
        # Update PR if exists
        if config['github']['pr_update_frequency'] == 'on_change':
            update_pr_description(state)
        
        # Log success (visible in Claude Code logs)
        action = result.get('action', 'saved')
        message = f"✅ Work state {action}"
        if 'url' in result:
            message += f" → {result['url']}"
        
        print(json.dumps({
            "decision": "log",
            "message": message,
            "continue": True
        }))
    else:
        # Log error but don't block
        print(json.dumps({
            "decision": "log",
            "message": f"⚠️ Failed to save work state: {result.get('error', 'Unknown error')}",
            "continue": True
        }))

if __name__ == "__main__":
    main()
