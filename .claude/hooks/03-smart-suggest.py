#!/usr/bin/env python3
"""
Smart Suggest Hook - Context-aware command suggestions
Suggests the most relevant commands based on current work context
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def get_current_context():
    """Analyze current work context"""
    context = {
        'branch': get_current_branch(),
        'modified_files': get_modified_files(),
        'last_command': get_last_command(),
        'todos': count_todos(),
        'time_of_day': datetime.now().hour
    }
    
    # Infer work type
    context['work_type'] = infer_work_type(context['modified_files'])
    context['work_stage'] = infer_work_stage(context)
    
    return context

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
        return None

def get_modified_files():
    """Get list of modified files"""
    try:
        result = subprocess.run(
            "git status --porcelain",
            shell=True,
            capture_output=True,
            text=True
        )
        
        files = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                files.append(line[3:])
        
        return files
    except:
        return []

def get_last_command():
    """Get last executed command from history"""
    # This would need integration with Claude Code's command history
    # For now, return None
    return None

def count_todos():
    """Count TODOs in current branch"""
    try:
        result = subprocess.run(
            "grep -r 'TODO:' --include='*.tsx' --include='*.ts' . | wc -l",
            shell=True,
            capture_output=True,
            text=True
        )
        return int(result.stdout.strip())
    except:
        return 0

def infer_work_type(modified_files):
    """Infer type of work from modified files"""
    if not modified_files:
        return 'starting'
    
    # Check file types
    has_components = any('components/' in f or f.endswith('.tsx') for f in modified_files)
    has_api = any('api/' in f for f in modified_files)
    has_tests = any('.test.' in f or '.spec.' in f for f in modified_files)
    has_docs = any('.md' in f for f in modified_files)
    
    if has_components and not has_tests:
        return 'component-development'
    elif has_api:
        return 'api-development'
    elif has_tests:
        return 'testing'
    elif has_docs:
        return 'documentation'
    else:
        return 'general'

def infer_work_stage(context):
    """Infer current stage of work"""
    modified_count = len(context['modified_files'])
    
    if modified_count == 0:
        return 'starting'
    elif modified_count < 3:
        return 'early'
    elif modified_count < 10:
        return 'active'
    else:
        return 'wrapping-up'

def generate_suggestions(notification_data, context):
    """Generate smart command suggestions based on context"""
    suggestions = []
    
    # Time-based suggestions
    if context['time_of_day'] < 10:  # Morning
        suggestions.append("/morning-setup - Start your day right")
    elif context['time_of_day'] > 17:  # Evening
        suggestions.append("/checkpoint create - Save before leaving")
    
    # Work type suggestions
    if context['work_type'] == 'component-development':
        suggestions.extend([
            "/cc ui ComponentName - Create another component",
            "/vd - Validate design compliance",
            "/tr current - Test current component"
        ])
    elif context['work_type'] == 'api-development':
        suggestions.extend([
            "/tr api - Test API endpoints",
            "/security-check code - Check for vulnerabilities"
        ])
    elif context['work_type'] == 'starting':
        suggestions.extend([
            "/sr - Resume previous work",
            "/work-status - See active tasks",
            "/fw start [issue#] - Start new feature"
        ])
    
    # Stage-based suggestions
    if context['work_stage'] == 'wrapping-up':
        suggestions.extend([
            "/pp - Pre-PR validation",
            "/checkpoint create - Save progress",
            "/todo list - Review remaining tasks"
        ])
    elif context['work_stage'] == 'active' and context['todos'] > 5:
        suggestions.append("/todo list - You have {} TODOs".format(context['todos']))
    
    # Context-specific suggestions
    if 'feature/' in context.get('branch', ''):
        issue_num = extract_issue_number(context['branch'])
        if issue_num:
            suggestions.append(f"/fw validate {issue_num} - Validate feature")
    
    # Limit suggestions to top 5 most relevant
    return suggestions[:5]

def extract_issue_number(branch_name):
    """Extract issue number from branch name"""
    parts = branch_name.split('/')[-1].split('-')
    if parts[0].isdigit():
        return parts[0]
    return None

def format_suggestion_message(suggestions, context):
    """Format suggestions into readable message"""
    if not suggestions:
        return "No specific suggestions at this time"
    
    message = "💡 Suggested commands:\n"
    for i, suggestion in enumerate(suggestions, 1):
        message += f"{i}. {suggestion}\n"
    
    # Add context info
    if context['work_stage'] == 'wrapping-up':
        message += "\n🏁 Looks like you're wrapping up. Don't forget to validate!"
    elif context['work_stage'] == 'starting':
        message += "\n🚀 Starting fresh? Check your previous work first."
    
    return message

def main():
    """Main hook logic"""
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    # Get current context
    context = get_current_context()
    
    # Generate suggestions
    suggestions = generate_suggestions(input_data, context)
    
    # Format response
    response = {
        "decision": "suggest",
        "message": format_suggestion_message(suggestions, context),
        "suggestions": suggestions,
        "context": {
            "work_type": context['work_type'],
            "work_stage": context['work_stage']
        }
    }
    
    # Add voice for important stages
    if context['work_stage'] == 'wrapping-up':
        response["voice"] = "Ready to wrap up? Run pre-PR validation"
    elif context['work_stage'] == 'starting' and context['time_of_day'] < 10:
        response["voice"] = "Good morning! Run morning setup to start"
    
    print(json.dumps(response))

    sys.exit(0)

if __name__ == "__main__":
    main()
