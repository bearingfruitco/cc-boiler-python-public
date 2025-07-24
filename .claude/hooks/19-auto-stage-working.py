#!/usr/bin/env python3
"""
Auto-Stage Working Files Hook - Automatically stage files after successful operations
Stages files to git after tests pass or successful edits
Links to Task Ledger for tracking progress
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

def is_git_repo():
    """Check if we're in a git repository."""
    try:
        subprocess.run(['git', 'rev-parse', '--git-dir'], 
                      capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_modified_files():
    """Get list of modified files in git."""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        files = []
        for line in result.stdout.strip().split('\n'):
            if line:
                # Status code is first 2 chars, filename starts at char 3
                status = line[:2]
                filename = line[3:]
                if status in [' M', 'M ', 'MM', 'A ', 'AM']:  # Modified or added
                    files.append(filename)
        return files
    except subprocess.CalledProcessError:
        return []

def should_auto_stage(filepath):
    """Determine if a file should be auto-staged."""
    # Don't auto-stage sensitive files
    sensitive_patterns = [
        '.env',
        '.env.local',
        '.env.production',
        'secrets/',
        '.pem',
        '.key',
        'id_rsa',
        'id_dsa',
        '.git/'
    ]
    
    filepath_str = str(filepath)
    for pattern in sensitive_patterns:
        if pattern in filepath_str:
            return False
    
    # Auto-stage source and test files
    auto_stage_patterns = [
        'src/',
        'tests/',
        'test/',
        '__tests__/',
        '.py',
        '.ts',
        '.tsx',
        '.js',
        '.jsx'
    ]
    
    for pattern in auto_stage_patterns:
        if pattern in filepath_str:
            return True
    
    return False

def update_staging_log(staged_files, context):
    """Update the staging log for tracking."""
    log_path = Path('.claude/logs/staging.jsonl')
    log_path.parent.mkdir(exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "staged_files": staged_files,
        "trigger": context.get('trigger', 'unknown'),
        "session_id": context.get('session_id', 'unknown'),
        "tool_name": context.get('tool_name', 'unknown')
    }
    
    with open(log_path, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def main():
    """Main hook logic."""
    try:
        # Read input
        input_data = json.loads(sys.stdin.read())
        
        # Only process after successful file operations or tests
        tool_name = input_data.get('tool_name', '')
        if tool_name not in ['filesystem:write_file', 'filesystem:edit_file', 
                           'shell_command', 'Bash']:
            sys.exit(0)
        
        # Check if git is available
        if not is_git_repo():
            sys.exit(0)
        
        # For shell commands, only process after successful test runs
        if tool_name in ['shell_command', 'Bash']:
            tool_input = input_data.get('tool_input', {})
            command = tool_input.get('command', '')
            
            # Check if it was a test command
            test_keywords = ['pytest', 'test', 'npm test', 'ruff', 'mypy']
            if not any(keyword in command.lower() for keyword in test_keywords):
                sys.exit(0)
            
            # Check if tests passed
            tool_response = input_data.get('tool_response', {})
            exit_code = tool_response.get('exit_code', 1)
            if exit_code != 0:
                sys.exit(0)  # Don't stage if tests failed
            
            trigger = f"tests_passed: {command}"
        else:
            # File operation
            tool_input = input_data.get('tool_input', {})
            filepath = tool_input.get('path', '')
            
            if not should_auto_stage(filepath):
                sys.exit(0)
            
            trigger = f"file_edited: {filepath}"
        
        # Get modified files
        modified_files = get_modified_files()
        if not modified_files:
            sys.exit(0)
        
        # Filter files to stage
        files_to_stage = [f for f in modified_files if should_auto_stage(f)]
        if not files_to_stage:
            sys.exit(0)
        
        # Stage the files
        try:
            subprocess.run(['git', 'add'] + files_to_stage, 
                         capture_output=True, check=True)
            
            # Log what was staged
            update_staging_log(files_to_stage, {
                'trigger': trigger,
                'session_id': input_data.get('session_id', 'unknown'),
                'tool_name': tool_name
            })
            
            # Provide feedback
            print(f"📦 Auto-staged {len(files_to_stage)} file(s) after {trigger}")
            for f in files_to_stage[:5]:  # Show first 5
                print(f"   + {f}")
            if len(files_to_stage) > 5:
                print(f"   ... and {len(files_to_stage) - 5} more")
            
        except subprocess.CalledProcessError as e:
            # Log error but don't block
            if os.environ.get('DEBUG_HOOKS'):
                print(f"Failed to stage files: {e}", file=sys.stderr)
        
    except Exception as e:
        # Log error but don't block workflow
        if os.environ.get('DEBUG_HOOKS'):
            print(f"Auto-staging hook error: {e}", file=sys.stderr)
        sys.exit(0)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
