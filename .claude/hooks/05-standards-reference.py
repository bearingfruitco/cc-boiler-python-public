#!/usr/bin/env python3
"""
Standards Reference Hook - Provides standards context to other hooks
This is a notification hook that makes standards available to the system
"""

import json
import sys
import os
from pathlib import Path

def main():
    """Reference standards for context - notification only"""
    try:
        # Read the hook event
        event = json.loads(sys.stdin.read())
        
        # Only activate on certain commands that might benefit from standards
        if event.get('type') == 'command_execution':
            command = event.get('command', '')
            
            # Commands that might benefit from standards reference
            relevant_commands = [
                'py-prd', 'py-agent', 'py-api', 'py-pipeline',
                'create-prd', 'generate-tasks', 'code-review'
            ]
            
            if any(cmd in command for cmd in relevant_commands):
                standards_path = Path('.claude/standards/python-patterns.md')
                
                if standards_path.exists():
                    # Just log that standards are available
                    response = {
                        "type": "info",
                        "message": "📚 Python patterns reference available in .claude/standards/",
                        "details": {
                            "patterns_file": str(standards_path),
                            "purpose": "Reference for design decisions"
                        }
                    }
                else:
                    response = {}
            else:
                response = {}
        else:
            response = {}
        
        # Output response
        json.dump(response, sys.stdout)
        sys.exit(0)
        
    except Exception as e:
        # Fail silently - this is just a reference hook
        json.dump({}, sys.stdout)
        sys.exit(0)

if __name__ == "__main__":
    main()
