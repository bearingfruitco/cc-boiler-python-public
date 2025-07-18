#!/usr/bin/env python3
"""
Auto-Approve Safe Operations Hook
Prevents workflow interruption by auto-approving genuinely safe operations
Only approves read operations and test file modifications
"""

import json
import sys
import os
from pathlib import Path

# Define safe operations that can be auto-approved
SAFE_READ_OPERATIONS = {
    'filesystem:read_file',
    'filesystem:read_multiple_files',
    'filesystem:list_directory',
    'filesystem:list_directory_with_sizes',
    'filesystem:directory_tree',
    'filesystem:get_file_info',
    'filesystem:search_files',
    'filesystem:list_allowed_directories'
}

# Safe directories for write operations
SAFE_WRITE_DIRECTORIES = [
    '/tests/',
    '/test/',
    '/__tests__/',
    '/.claude/checkpoints/',
    '/.claude/transcripts/',
    '/tmp/',
    '/.cache/'
]

# Safe shell commands that can be auto-approved
SAFE_SHELL_COMMANDS = [
    'npm test',
    'npm run test',
    'npm run lint',
    'npm run typecheck',
    'npm run type-check',
    'npm run validate',
    'jest',
    'vitest',
    'playwright test',
    'tsc --noEmit',
    'eslint',
    'prettier --check'
]

def is_safe_write_path(path):
    """Check if the path is in a safe directory for auto-approval"""
    if not path:
        return False
    
    # Normalize path
    path_str = str(path).replace('\\', '/')
    
    # Check if path is in any safe directory
    for safe_dir in SAFE_WRITE_DIRECTORIES:
        if safe_dir in path_str:
            return True
    
    # Check if it's a test file by name
    path_obj = Path(path_str)
    if path_obj.name.endswith(('.test.ts', '.test.tsx', '.test.js', '.test.jsx', 
                              '.spec.ts', '.spec.tsx', '.spec.js', '.spec.jsx')):
        return True
    
    return False

def is_safe_shell_command(command):
    """Check if the shell command is safe for auto-approval"""
    if not command:
        return False
    
    # Check if command starts with any safe command
    command_lower = command.strip().lower()
    for safe_cmd in SAFE_SHELL_COMMANDS:
        if command_lower.startswith(safe_cmd.lower()):
            return True
    
    return False

def should_auto_approve(tool_use):
    """Determine if this operation should be auto-approved"""
    tool_name = tool_use.get('toolName', '')
    parameters = tool_use.get('parameters', {})
    
    # Auto-approve all read operations
    if tool_name in SAFE_READ_OPERATIONS:
        return True, "Read operation - auto-approved"
    
    # Check write operations in safe directories
    if tool_name in ['filesystem:write_file', 'filesystem:edit_file', 'filesystem:create_directory']:
        path = parameters.get('path', '')
        if is_safe_write_path(path):
            return True, f"Test/cache file operation - auto-approved"
    
    # Check safe shell commands
    if tool_name == 'shell_command':
        command = parameters.get('command', '')
        if is_safe_shell_command(command):
            return True, f"Safe command - auto-approved"
    
    # Default to not auto-approving
    return False, None

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        hook_input = json.loads(sys.stdin.read())
        tool_use = hook_input.get('toolUse', {})
        
        # Check if this operation should be auto-approved
        should_approve, reason = should_auto_approve(tool_use)
        
        if should_approve:
            # Log the auto-approval (visible in Claude's output)
            tool_name = tool_use.get('toolName', '')
            
            # For read operations, use minimal logging
            if tool_name in SAFE_READ_OPERATIONS:
                print(f"✓ Auto-approved: {tool_name}")
            else:
                # For write operations, be more explicit
                print(f"✅ Auto-approved: {tool_name} - {reason}")
            
            # Exit with success to auto-approve
            sys.exit(0)
        
        # If not auto-approved, let normal flow continue
        # This means Claude will ask for permission as usual
        
    except Exception as e:
        # On any error, fail safely by not auto-approving
        # This ensures we don't accidentally approve unsafe operations
        if os.environ.get('DEBUG_HOOKS'):
            print(f"Auto-approval hook error: {e}")
        pass

if __name__ == '__main__':
    main()
