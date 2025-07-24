#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Track sub-agent completion for parallel tasks
Useful for monitoring progress of multiple concurrent operations
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def main():
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    # Create logs directory
    log_dir = Path(".claude/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Log sub-agent completion
    sub_agent_log = log_dir / f"sub-agents-{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "task_id": input_data.get('task_id', 'unknown'),
        "task_description": input_data.get('task_description', ''),
        "status": "completed",
        "duration": input_data.get('duration', 0),
        "parent_session": input_data.get('parent_session_id', 'unknown')
    }
    
    with open(sub_agent_log, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    # Check if all sub-agents are complete (simplified version)
    # In a real implementation, you'd track active sub-agents
    
    print(json.dumps({
        "success": True,
        "message": f"Sub-agent task completed: {log_entry['task_description'][:50]}"
    }))

    sys.exit(0)

if __name__ == "__main__":
    main()
