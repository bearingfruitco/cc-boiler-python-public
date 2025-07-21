#!/usr/bin/env python3
"""
Handoff Preparation Hook - Prepare detailed handoff package
Creates comprehensive handoff documentation for team members
"""

import json
import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime

def analyze_session_for_handoff(chat_history):
    """Analyze session to create handoff summary"""
    handoff = {
        'session_end': datetime.now().isoformat(),
        'user': get_current_user(),
        'work_summary': extract_work_summary(chat_history),
        'current_state': get_current_state(),
        'next_actions': extract_next_actions(chat_history),
        'blockers': extract_blockers(chat_history),
        'decisions_made': extract_decisions(chat_history),
        'code_context': extract_code_context(chat_history)
    }
    
    return handoff

def get_current_user():
    """Get current user"""
    config_path = Path(__file__).parent.parent.parent / 'team' / 'config.json'
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f).get('current_user', 'unknown')
    return 'unknown'

def extract_work_summary(chat_history):
    """Extract summary of work done"""
    summary = {
        'files_modified': set(),
        'components_worked_on': set(),
        'features_implemented': [],
        'bugs_fixed': []
    }
    
    for entry in chat_history:
        # Track modified files
        if entry.get('tool') in ['write_file', 'edit_file']:
            file_path = entry.get('path', '')
            summary['files_modified'].add(file_path)
            
            # Track components
            if 'components/' in file_path:
                component = Path(file_path).stem
                summary['components_worked_on'].add(component)
    
    summary['files_modified'] = list(summary['files_modified'])
    summary['components_worked_on'] = list(summary['components_worked_on'])
    
    return summary

def get_current_state():
    """Get current git and project state"""
    state = {}
    
    # Get current branch
    try:
        branch_result = subprocess.run(
            "git branch --show-current",
            shell=True,
            capture_output=True,
            text=True
        )
        state['branch'] = branch_result.stdout.strip()
    except:
        state['branch'] = 'unknown'
    
    # Get uncommitted changes
    try:
        status_result = subprocess.run(
            "git status --porcelain",
            shell=True,
            capture_output=True,
            text=True
        )
        
        changes = []
        for line in status_result.stdout.strip().split('\n'):
            if line.strip():
                status = line[:2].strip()
                file_path = line[3:]
                changes.append({
                    'file': file_path,
                    'status': status
                })
        
        state['uncommitted_changes'] = changes
    except:
        state['uncommitted_changes'] = []
    
    # Get current file being edited (if any)
    state['last_file_edited'] = None
    
    return state

def extract_next_actions(chat_history):
    """Extract next actions from TODOs and context"""
    actions = []
    
    # Look for TODO comments in recent files
    try:
        result = subprocess.run(
            "grep -r 'TODO:' --include='*.tsx' --include='*.ts' . | head -5",
            shell=True,
            capture_output=True,
            text=True
        )
        
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                parts = line.split(':', 2)
                if len(parts) >= 3:
                    actions.append({
                        'type': 'todo',
                        'file': parts[0].replace('./', ''),
                        'description': parts[2].strip()
                    })
    except:
        pass
    
    # Add inferred actions based on state
    state = get_current_state()
    if state['uncommitted_changes']:
        actions.append({
            'type': 'commit',
            'description': f"Commit {len(state['uncommitted_changes'])} uncommitted files"
        })
    
    return actions

def extract_blockers(chat_history):
    """Extract any blockers or issues encountered"""
    blockers = []
    
    for entry in chat_history:
        message = str(entry.get('message', '')).lower()
        
        # Look for error indicators
        if any(word in message for word in ['error', 'failed', 'blocked', 'issue']):
            # Check if it was resolved
            resolved = False
            for next_entry in chat_history[chat_history.index(entry)+1:]:
                if 'fixed' in str(next_entry.get('message', '')).lower():
                    resolved = True
                    break
            
            if not resolved:
                blockers.append({
                    'description': entry.get('message', '')[:200],
                    'type': 'unresolved_error'
                })
    
    return blockers

def extract_decisions(chat_history):
    """Extract key decisions made during session"""
    decisions = []
    
    # Look for decision indicators
    decision_keywords = ['decided', 'chose', 'selected', 'using', 'going with']
    
    for entry in chat_history:
        message = str(entry.get('message', '')).lower()
        
        if any(keyword in message for keyword in decision_keywords):
            decisions.append({
                'decision': entry.get('message', '')[:200],
                'context': 'See chat history for details'
            })
    
    return decisions[:5]  # Top 5 decisions

def extract_code_context(chat_history):
    """Extract relevant code context for handoff"""
    context = {
        'last_function_edited': None,
        'current_focus': None,
        'recent_imports': []
    }
    
    # Find last edited component/function
    for entry in reversed(chat_history):
        if entry.get('tool') in ['write_file', 'edit_file']:
            file_path = entry.get('path', '')
            if file_path.endswith('.tsx') or file_path.endswith('.ts'):
                context['last_function_edited'] = file_path
                
                # Try to extract function name from content
                content = entry.get('content', '')
                func_match = re.search(r'function\s+(\w+)|const\s+(\w+)\s*=', content)
                if func_match:
                    context['current_focus'] = func_match.group(1) or func_match.group(2)
                break
    
    return context

def create_handoff_document(handoff):
    """Create formatted handoff document"""
    doc = f"""# 🤝 Handoff Document

**From**: {handoff['user']}
**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Branch**: {handoff['current_state']['branch']}

## 📋 Work Summary

### Files Modified ({len(handoff['work_summary']['files_modified'])})
"""
    
    for file in handoff['work_summary']['files_modified'][:10]:
        doc += f"- {file}\n"
    
    if handoff['work_summary']['components_worked_on']:
        doc += f"\n### Components Worked On\n"
        for component in handoff['work_summary']['components_worked_on']:
            doc += f"- {component}\n"
    
    doc += f"\n## 🎯 Current State\n"
    
    if handoff['current_state']['uncommitted_changes']:
        doc += f"\n### Uncommitted Changes ({len(handoff['current_state']['uncommitted_changes'])})\n"
        for change in handoff['current_state']['uncommitted_changes'][:5]:
            doc += f"- [{change['status']}] {change['file']}\n"
    
    doc += f"\n## ⏭️ Next Actions\n"
    
    for i, action in enumerate(handoff['next_actions'], 1):
        doc += f"{i}. {action['description']}"
        if action['type'] == 'todo':
            doc += f" (in {action['file']})"
        doc += "\n"
    
    if handoff['blockers']:
        doc += f"\n## 🚧 Blockers\n"
        for blocker in handoff['blockers']:
            doc += f"- {blocker['description']}\n"
    
    if handoff['decisions_made']:
        doc += f"\n## 💡 Key Decisions Made\n"
        for decision in handoff['decisions_made']:
            doc += f"- {decision['decision']}\n"
    
    doc += f"\n## 🔄 Resume Instructions\n\n"
    doc += f"```bash\n"
    doc += f"# 1. Pull latest changes\n"
    doc += f"git pull origin {handoff['current_state']['branch']}\n\n"
    doc += f"# 2. Resume work\n"
    doc += f"/sr\n"
    
    if handoff['code_context']['last_function_edited']:
        doc += f"\n# 3. Continue editing\n"
        doc += f"# Open: {handoff['code_context']['last_function_edited']}\n"
        if handoff['code_context']['current_focus']:
            doc += f"# Focus: {handoff['code_context']['current_focus']}()\n"
    
    doc += f"```\n"
    
    return doc

def save_handoff(handoff, document):
    """Save handoff to multiple locations"""
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    
    # Save to handoffs directory
    handoff_dir = Path(__file__).parent.parent.parent / 'team' / 'handoffs'
    handoff_file = handoff_dir / f"handoff-{timestamp}.md"
    
    with open(handoff_file, 'w') as f:
        f.write(document)
    
    # Save JSON version
    json_file = handoff_dir / f"handoff-{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump(handoff, f, indent=2)
    
    # Create latest symlink
    latest_link = handoff_dir / 'latest.md'
    if latest_link.exists():
        latest_link.unlink()
    latest_link.symlink_to(handoff_file.name)
    
    return handoff_file

def notify_team(handoff_file, handoff):
    """Notify team about handoff"""
    # Could integrate with Slack, Discord, etc.
    # For now, just create a notification file
    
    notify_file = Path(__file__).parent.parent.parent / 'team' / 'notifications.json'
    
    if notify_file.exists():
        with open(notify_file) as f:
            notifications = json.load(f)
    else:
        notifications = []
    
    notifications.append({
        'type': 'handoff',
        'from': handoff['user'],
        'timestamp': datetime.now().isoformat(),
        'file': str(handoff_file),
        'summary': f"{len(handoff['work_summary']['files_modified'])} files modified, {len(handoff['next_actions'])} next actions"
    })
    
    # Keep last 20 notifications
    notifications = notifications[-20:]
    
    with open(notify_file, 'w') as f:
        json.dump(notifications, f, indent=2)

def main():
    """Main hook logic"""
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    # Get chat history
    chat_history = input_data.get('history', [])
    
    # Analyze session for handoff
    handoff = analyze_session_for_handoff(chat_history)
    
    # Only create handoff if significant work was done
    if not handoff['work_summary']['files_modified']:
        print(json.dumps({
            "decision": "skip",
            "message": "No files modified - handoff not needed"
        }))
        return
    
    # Create handoff document
    document = create_handoff_document(handoff)
    
    # Save handoff
    handoff_file = save_handoff(handoff, document)
    
    # Notify team
    notify_team(handoff_file, handoff)
    
    # Return response
    response = {
        "decision": "display",
        "message": f"""
🤝 Handoff Prepared
==================
Files Modified: {len(handoff['work_summary']['files_modified'])}
Next Actions: {len(handoff['next_actions'])}
Blockers: {len(handoff['blockers'])}

Handoff saved to:
{handoff_file}

Team member can resume with:
/handoff receive {handoff['user']}
""",
        "handoff_file": str(handoff_file)
    }
    
    # Add voice notification
    if handoff['blockers']:
        response["voice"] = f"Handoff ready. Warning: {len(handoff['blockers'])} blockers need attention"
    else:
        response["voice"] = "Handoff ready for next team member"
    
    print(json.dumps(response))

    sys.exit(0)

if __name__ == "__main__":
    main()
