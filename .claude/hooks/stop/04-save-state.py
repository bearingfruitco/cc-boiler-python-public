#!/usr/bin/env python3
"""
Save State Hook - Final state save and metrics when session ends
Ensures work is never lost and provides session summary
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import hashlib

def get_session_summary(chat_history):
    """Generate summary of the session"""
    summary = {
        'duration': calculate_session_duration(chat_history),
        'files_modified': extract_modified_files(chat_history),
        'components_created': extract_created_components(chat_history),
        'design_violations': count_design_violations(chat_history),
        'commands_used': extract_commands_used(chat_history),
        'progress_made': estimate_progress(chat_history)
    }
    
    return summary

def calculate_session_duration(chat_history):
    """Calculate session duration from chat history"""
    # This is a simplified version - would need actual timestamps
    return "45 minutes"

def extract_modified_files(chat_history):
    """Extract list of files modified during session"""
    files = set()
    
    for entry in chat_history:
        if entry.get('tool') in ['write_file', 'edit_file']:
            files.add(entry.get('path', ''))
    
    return list(files)

def extract_created_components(chat_history):
    """Extract components created during session"""
    components = []
    
    for entry in chat_history:
        if entry.get('tool') == 'write_file':
            path = entry.get('path', '')
            if 'components/' in path and path.endswith('.tsx'):
                component_name = Path(path).stem
                components.append(component_name)
    
    return components

def count_design_violations(chat_history):
    """Count design violations encountered"""
    violations = 0
    
    for entry in chat_history:
        if 'DESIGN VIOLATION' in str(entry.get('message', '')):
            violations += 1
    
    return violations

def extract_commands_used(chat_history):
    """Extract Claude Code commands used"""
    commands = []
    
    for entry in chat_history:
        message = entry.get('message', '')
        if isinstance(message, str) and message.startswith('/'):
            command = message.split()[0]
            if command not in commands:
                commands.append(command)
    
    return commands

def estimate_progress(chat_history):
    """Estimate progress made during session"""
    # Simple heuristic based on activity
    files_count = len(extract_modified_files(chat_history))
    
    if files_count == 0:
        return "Planning/Setup"
    elif files_count < 3:
        return "Early Development"
    elif files_count < 10:
        return "Active Development"
    else:
        return "Major Progress"

def create_final_state(summary, chat_history):
    """Create final state document"""
    git_info = get_git_info()
    
    state = {
        'session': {
            'ended_at': datetime.now().isoformat(),
            'user': get_current_user(),
            'summary': summary
        },
        'git': git_info,
        'next_steps': generate_next_steps(summary, git_info),
        'handoff_notes': generate_handoff_notes(summary)
    }
    
    return state

def get_git_info():
    """Get current git state"""
    try:
        branch = subprocess.run(
            "git branch --show-current",
            shell=True,
            capture_output=True,
            text=True
        ).stdout.strip()
        
        # Get uncommitted changes count
        status_result = subprocess.run(
            "git status --porcelain | wc -l",
            shell=True,
            capture_output=True,
            text=True
        )
        uncommitted = int(status_result.stdout.strip())
        
        return {
            'branch': branch,
            'uncommitted_files': uncommitted
        }
    except:
        return {'branch': 'unknown', 'uncommitted_files': 0}

def get_current_user():
    """Get current user"""
    config_path = Path(__file__).parent.parent.parent / 'team' / 'config.json'
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f).get('current_user', 'unknown')
    return 'unknown'

def generate_next_steps(summary, git_info):
    """Generate suggested next steps"""
    steps = []
    
    # Based on progress
    if summary['progress_made'] == "Planning/Setup":
        steps.append("Start implementing first component")
    elif summary['design_violations'] > 0:
        steps.append(f"Fix {summary['design_violations']} design violations")
    
    # Based on git state
    if git_info['uncommitted_files'] > 0:
        steps.append(f"Commit {git_info['uncommitted_files']} uncommitted files")
    
    # Based on components
    if summary['components_created']:
        steps.append(f"Add tests for {', '.join(summary['components_created'])}")
    
    return steps

def generate_handoff_notes(summary):
    """Generate notes for team handoff"""
    notes = []
    
    if summary['files_modified']:
        notes.append(f"Modified {len(summary['files_modified'])} files")
    
    if summary['components_created']:
        notes.append(f"Created components: {', '.join(summary['components_created'])}")
    
    if summary['design_violations'] > 0:
        notes.append(f"⚠️ {summary['design_violations']} design violations need fixing")
    
    return " | ".join(notes)

def save_session_state(state):
    """Save session state to GitHub gist"""
    try:
        # Create gist content
        gist_content = json.dumps(state, indent=2)
        gist_name = f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        
        with open(f'/tmp/{gist_name}', 'w') as f:
            f.write(gist_content)
        
        # Create gist
        result = subprocess.run(
            f"gh gist create /tmp/{gist_name} --desc 'Session ended: {state['session']['summary']['progress_made']}'",
            shell=True,
            capture_output=True,
            text=True
        )
        
        return result.returncode == 0
    except:
        return False

def update_daily_log(summary):
    """Update daily activity log"""
    log_dir = Path(__file__).parent.parent.parent / 'team' / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = log_dir / f'{today}.json'
    
    # Load existing log
    if log_file.exists():
        with open(log_file) as f:
            daily_log = json.load(f)
    else:
        daily_log = {'sessions': []}
    
    # Add this session
    daily_log['sessions'].append({
        'time': datetime.now().isoformat(),
        'user': get_current_user(),
        'summary': summary
    })
    
    # Save updated log
    with open(log_file, 'w') as f:
        json.dump(daily_log, f, indent=2)

def format_session_report(summary, state):
    """Format session report for display"""
    report = f"""
📊 Session Summary
═══════════════════
Duration: {summary['duration']}
Progress: {summary['progress_made']}
Files Modified: {len(summary['files_modified'])}
Components Created: {len(summary['components_created'])}
Design Violations: {summary['design_violations']}

📝 Next Steps:
"""
    
    for i, step in enumerate(state['next_steps'], 1):
        report += f"{i}. {step}\n"
    
    if state['handoff_notes']:
        report += f"\n🤝 Handoff: {state['handoff_notes']}"
    
    return report

def main():
    """Main hook logic"""
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    # Get chat history
    chat_history = input_data.get('history', [])
    
    # Generate session summary
    summary = get_session_summary(chat_history)
    
    # Create final state
    state = create_final_state(summary, chat_history)
    
    # Save to GitHub
    saved = save_session_state(state)
    
    # Update daily log
    update_daily_log(summary)
    
    # Format report
    report = format_session_report(summary, state)
    
    # Return response
    response = {
        "decision": "display",
        "message": report,
        "saved": saved
    }
    
    # Add voice summary
    if summary['progress_made'] == "Major Progress":
        response["voice"] = f"Great session! Made major progress with {len(summary['components_created'])} new components"
    elif summary['design_violations'] > 0:
        response["voice"] = f"Session complete. Remember to fix {summary['design_violations']} design violations"
    else:
        response["voice"] = "Session saved. See you next time!"
    
    print(json.dumps(response))

    sys.exit(0)

if __name__ == "__main__":
    main()
