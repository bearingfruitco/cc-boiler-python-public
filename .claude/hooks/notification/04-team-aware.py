#!/usr/bin/env python3
"""
Team Awareness Hook - Show team activity and coordination suggestions
Helps prevent conflicts and suggests optimal task distribution
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

def get_team_registry():
    """Load team work registry"""
    registry_path = Path(__file__).parent.parent.parent / 'team' / 'registry.json'
    if registry_path.exists():
        with open(registry_path) as f:
            return json.load(f)
    return {"active_work": {}, "worktrees": {}}

def get_current_user():
    """Get current user from team config"""
    config_path = Path(__file__).parent.parent.parent / 'team' / 'config.json'
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f).get('current_user', 'unknown')
    return 'unknown'

def analyze_team_activity(registry):
    """Analyze what team members are working on"""
    current_user = get_current_user()
    team_activity = []
    
    for user, work_info in registry.get('active_work', {}).items():
        if user != current_user:
            # Check if activity is recent (within last hour)
            last_activity = work_info.get('last_activity')
            if is_recent_activity(last_activity):
                team_activity.append({
                    'user': user,
                    'branch': work_info.get('branch', 'unknown'),
                    'files': work_info.get('active_files', []),
                    'last_seen': format_time_ago(last_activity),
                    'focus_area': infer_focus_area(work_info.get('active_files', []))
                })
    
    return team_activity

def is_recent_activity(timestamp):
    """Check if activity is within last hour"""
    if not timestamp:
        return False
    
    try:
        then = datetime.fromisoformat(timestamp)
        now = datetime.now()
        return (now - then) < timedelta(hours=1)
    except:
        return False

def format_time_ago(timestamp):
    """Format timestamp as human-readable time ago"""
    if not timestamp:
        return 'unknown'
    
    try:
        then = datetime.fromisoformat(timestamp)
        now = datetime.now()
        delta = now - then
        
        if delta.seconds < 60:
            return 'just now'
        elif delta.seconds < 3600:
            minutes = delta.seconds // 60
            return f'{minutes}m ago'
        else:
            hours = delta.seconds // 3600
            return f'{hours}h ago'
    except:
        return 'unknown'

def infer_focus_area(files):
    """Infer what area someone is working on based on files"""
    if not files:
        return 'unknown'
    
    # Count file types/areas
    areas = {
        'components': 0,
        'api': 0,
        'config': 0,
        'docs': 0,
        'tests': 0
    }
    
    for file in files:
        if 'components/' in file or file.endswith('.tsx'):
            areas['components'] += 1
        elif 'api/' in file or 'lib/api' in file:
            areas['api'] += 1
        elif any(cfg in file for cfg in ['config', 'package.json', '.env']):
            areas['config'] += 1
        elif 'docs/' in file or file.endswith('.md'):
            areas['docs'] += 1
        elif '.test.' in file or '.spec.' in file:
            areas['tests'] += 1
    
    # Return primary focus area
    if areas['components'] > 0:
        return 'frontend/components'
    elif areas['api'] > 0:
        return 'backend/api'
    elif areas['config'] > 0:
        return 'configuration'
    elif areas['docs'] > 0:
        return 'documentation'
    elif areas['tests'] > 0:
        return 'testing'
    
    return 'general'

def generate_suggestions(notification_type, team_activity, current_context):
    """Generate smart suggestions based on team activity"""
    suggestions = []
    warnings = []
    
    # Check for potential conflicts
    for activity in team_activity:
        if overlaps_with_context(activity, current_context):
            warnings.append(
                f"⚠️ {activity['user']} is working on {activity['focus_area']} "
                f"({activity['last_seen']})"
            )
            suggestions.append(f"/collab-sync {activity['user']}")
    
    # Suggest complementary work
    team_focus_areas = {a['focus_area'] for a in team_activity}
    
    if 'frontend/components' in team_focus_areas:
        if 'backend/api' not in team_focus_areas:
            suggestions.append("/focus api - Frontend is covered")
    elif 'backend/api' in team_focus_areas:
        if 'frontend/components' not in team_focus_areas:
            suggestions.append("/focus components - Backend is covered")
    
    # Add standard suggestions based on notification type
    if notification_type == 'permission_needed':
        suggestions.extend([
            "/work-status - See all active work",
            "/checkpoint create - Save current progress"
        ])
    
    return suggestions, warnings

def overlaps_with_context(activity, context):
    """Check if team activity overlaps with current context"""
    # Simple check - could be made more sophisticated
    current_area = context.get('focus_area', '')
    return activity['focus_area'] == current_area

def format_team_status(team_activity):
    """Format team status as readable message"""
    if not team_activity:
        return "No team members currently active"
    
    status = "👥 Team Activity:\n"
    for activity in team_activity:
        status += f"  • {activity['user']}: {activity['focus_area']} ({activity['last_seen']})\n"
    
    return status

def main():
    """Main hook logic"""
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    # Get current context
    notification_type = input_data.get('type', 'general')
    current_context = {
        'user': get_current_user(),
        'focus_area': 'unknown'  # Could be enhanced to detect current work area
    }
    
    # Get team activity
    registry = get_team_registry()
    team_activity = analyze_team_activity(registry)
    
    # Generate suggestions
    suggestions, warnings = generate_suggestions(
        notification_type, 
        team_activity, 
        current_context
    )
    
    # Format response
    response = {
        "decision": "suggest",
        "team_status": format_team_status(team_activity)
    }
    
    if warnings:
        response["warnings"] = warnings
    
    if suggestions:
        response["suggestions"] = suggestions
        
    # Add voice notification for important warnings
    if warnings:
        response["voice"] = f"Heads up: {warnings[0]}"
    elif team_activity:
        response["voice"] = f"{len(team_activity)} team member{'s' if len(team_activity) > 1 else ''} active"
    
    print(json.dumps(response))

    sys.exit(0)

if __name__ == "__main__":
    main()
