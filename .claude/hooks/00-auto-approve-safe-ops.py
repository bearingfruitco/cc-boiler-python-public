#!/usr/bin/env python3
"""
Auto-Approve Safe Operations Hook with Permission Profiles
Prevents workflow interruption by auto-approving based on permission profiles
Supports multiple permission levels: exploration, development, ci_pipeline
"""

import json
import sys
import os
from pathlib import Path

# Load permission profiles
def load_permission_profiles():
    """Load permission profiles from config."""
    profiles_path = Path('.claude/permission-profiles.json')
    if profiles_path.exists():
        with open(profiles_path, 'r') as f:
            return json.load(f).get('profiles', {})
    
    # Default profiles if file doesn't exist
    return {
        "exploration": {
            "description": "Read-only exploration mode",
            "auto_approve": [
                "filesystem:read_file",
                "filesystem:read_multiple_files", 
                "filesystem:list_directory",
                "filesystem:list_directory_with_sizes",
                "filesystem:directory_tree",
                "filesystem:get_file_info",
                "filesystem:search_files",
                "filesystem:list_allowed_directories"
            ],
            "require_approval": ["*"]
        },
        "development": {
            "description": "Standard development mode",
            "auto_approve": [
                # All read operations
                "filesystem:read_*",
                "filesystem:list_*",
                "filesystem:directory_tree",
                "filesystem:get_file_info",
                "filesystem:search_files",
                # Safe write locations
                "filesystem:write_file:tests/**",
                "filesystem:write_file:**/*.test.*",
                "filesystem:write_file:.claude/checkpoints/**",
                "filesystem:write_file:.claude/transcripts/**",
                # Safe commands
                "shell_command:npm test",
                "shell_command:npm run test",
                "shell_command:npm run lint",
                "shell_command:pytest",
                "shell_command:python -m pytest",
                "shell_command:ruff check",
                "shell_command:mypy"
            ],
            "require_approval": [
                "shell_command:rm *",
                "shell_command:sudo *",
                "filesystem:write_file:.env*",
                "filesystem:write_file:**/production/**"
            ]
        },
        "ci_pipeline": {
            "description": "CI/CD pipeline mode",
            "auto_approve": ["*"],
            "except": [
                "shell_command:rm -rf /",
                "shell_command:sudo rm -rf",
                "filesystem:write_file:/etc/**",
                "filesystem:write_file:~/.ssh/**"
            ]
        }
    }

def get_current_profile():
    """Get the current permission profile."""
    # Check environment variable
    profile_name = os.environ.get('CLAUDE_PERMISSION_PROFILE')
    if profile_name:
        return profile_name
    
    # Check workflow state
    workflow_state_path = Path('.claude/context/workflow_state.json')
    if workflow_state_path.exists():
        with open(workflow_state_path, 'r') as f:
            state = json.load(f)
            if state.get('ci_mode'):
                return 'ci_pipeline'
            if state.get('exploration_mode'):
                return 'exploration'
    
    # Default to development
    return 'development'

def match_pattern(pattern, tool_name, parameters):
    """Check if a pattern matches the current tool use."""
    parts = pattern.split(':')
    
    # Simple tool name match
    if len(parts) == 1:
        if pattern == '*':
            return True
        if pattern.endswith('*'):
            return tool_name.startswith(pattern[:-1])
        return tool_name == pattern
    
    # Tool name + parameter match
    if len(parts) >= 2:
        tool_pattern = parts[0]
        param_pattern = ':'.join(parts[1:])
        
        # Check tool name
        if tool_pattern.endswith('*'):
            if not tool_name.startswith(tool_pattern[:-1]):
                return False
        elif tool_name != tool_pattern:
            return False
        
        # Check parameter patterns
        if tool_name.startswith('filesystem:') and 'path' in parameters:
            path = parameters['path']
            # Convert glob pattern to simple check
            if '**' in param_pattern:
                param_pattern = param_pattern.replace('**', '')
            if param_pattern.startswith('*'):
                return path.endswith(param_pattern[1:])
            if param_pattern.endswith('*'):
                return path.startswith(param_pattern[:-1])
            return param_pattern in path
            
        elif tool_name == 'shell_command' and 'command' in parameters:
            command = parameters['command'].strip()
            if param_pattern.endswith('*'):
                return command.startswith(param_pattern[:-1])
            return command == param_pattern
    
    return False

def should_auto_approve(tool_use, profile):
    """Determine if this operation should be auto-approved based on profile."""
    tool_name = tool_use.get('toolName', '')
    parameters = tool_use.get('parameters', {})
    
    # Check exceptions first (never auto-approve these)
    exceptions = profile.get('except', [])
    for pattern in exceptions:
        if match_pattern(pattern, tool_name, parameters):
            return False, "Blocked by security exception"
    
    # Check explicit denials
    require_approval = profile.get('require_approval', [])
    for pattern in require_approval:
        if match_pattern(pattern, tool_name, parameters):
            return False, "Requires manual approval"
    
    # Check auto-approvals
    auto_approve = profile.get('auto_approve', [])
    for pattern in auto_approve:
        if match_pattern(pattern, tool_name, parameters):
            return True, f"Auto-approved by {get_current_profile()} profile"
    
    return False, None

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        hook_input = json.loads(sys.stdin.read())
        tool_use = hook_input.get('toolUse', {})
        
        # Load profiles and get current
        profiles = load_permission_profiles()
        current_profile_name = get_current_profile()
        current_profile = profiles.get(current_profile_name, profiles['development'])
        
        # Check if this operation should be auto-approved
        should_approve, reason = should_auto_approve(tool_use, current_profile)
        
        if should_approve:
            # Log the auto-approval
            tool_name = tool_use.get('toolName', '')
            
            # Minimal logging for read operations
            if tool_name.startswith('filesystem:read') or tool_name.startswith('filesystem:list'):
                print(f"✓ [{current_profile_name}] {tool_name}")
            else:
                # More explicit for write operations
                print(f"✅ [{current_profile_name}] {tool_name} - {reason}")
            
            # Exit with success to auto-approve
            sys.exit(0)
        
        # If not auto-approved, let normal flow continue
        # Log why it wasn't approved if in debug mode
        if os.environ.get('DEBUG_HOOKS'):
            print(f"🔸 [{current_profile_name}] {tool_use.get('toolName', '')} - {reason or 'No matching rule'}")
        
    except Exception as e:
        # On any error, fail safely by not auto-approving
        if os.environ.get('DEBUG_HOOKS'):
            print(f"Auto-approval hook error: {e}", file=sys.stderr)
        pass

if __name__ == '__main__':
    main()
