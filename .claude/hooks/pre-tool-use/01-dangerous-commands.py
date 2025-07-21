#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Pre-tool use safety hook
Blocks dangerous commands and protects sensitive files
"""

import json
import sys
import re

DANGEROUS_PATTERNS = [
    # Dangerous file operations
    r'rm\s+-rf?\s+[/.]',  # rm -rf / or rm -rf .
    r'rm\s+.*\*',         # rm with wildcards
    r'chmod\s+777',       # Overly permissive permissions
    
    # Sensitive files
    r'\.env',             # Environment files
    r'\.env\.local',      
    r'\.env\.production',
    r'secrets',           # Any secrets files
    r'credentials',       # Credential files
    r'private\.key',      # Private keys
    r'id_rsa',           # SSH keys
    
    # Database operations
    r'DROP\s+DATABASE',   # Database deletion
    r'DELETE\s+FROM.*WHERE\s+1=1',  # Delete all records
    
    # System files
    r'/etc/passwd',       # System passwords
    r'~/.ssh',           # SSH directory
]

BLOCKED_TOOLS = {
    'shell_command': ['rm', 'chmod', 'chown'],  # Commands to check
}

def is_dangerous(tool_name, tool_input):
    """Check if the tool use is dangerous"""
    
    # Convert input to string for pattern matching
    input_str = json.dumps(tool_input) if isinstance(tool_input, dict) else str(tool_input)
    
    # Check dangerous patterns
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, input_str, re.IGNORECASE):
            return True, f"Blocked: Dangerous pattern detected: {pattern}"
    
    # Check blocked tools
    if tool_name in BLOCKED_TOOLS:
        command = tool_input.get('command', '')
        for blocked_cmd in BLOCKED_TOOLS[tool_name]:
            if command.startswith(blocked_cmd):
                return True, f"Blocked: Command '{blocked_cmd}' is not allowed"
    
    # Check for production environment access
    if 'production' in input_str.lower() or 'prod' in input_str.lower():
        if any(keyword in input_str.lower() for keyword in ['delete', 'drop', 'remove', 'destroy']):
            return True, "Blocked: Destructive operations in production environment"
    
    return False, None

def main():
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    tool_name = input_data.get('tool_name', '')
    tool_input = input_data.get('tool_input', {})
    
    # Check if dangerous
    is_blocked, reason = is_dangerous(tool_name, tool_input)
    
    if is_blocked:
        # Log the blocked attempt
        log_dir = Path(".claude/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        blocked_log = log_dir / "blocked-commands.jsonl"
        with open(blocked_log, "a") as f:
            f.write(json.dumps({
                "timestamp": datetime.now().isoformat(),
                "tool_name": tool_name,
                "tool_input": tool_input,
                "reason": reason
            }) + "\n")
        
        # Return error to block the command
        print(reason, file=sys.stderr)
        print("Suggestion: Please use a safer alternative or request permission", file=sys.stderr)
        sys.exit(2)  # Block the command
    
    # Allow the command
    sys.exit(0)  # Allow the command

if __name__ == "__main__":
    from datetime import datetime
    from pathlib import Path
    main()
