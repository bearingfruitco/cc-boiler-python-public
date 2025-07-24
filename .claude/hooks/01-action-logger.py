#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Post-tool use logger for observability
Logs every action Claude Code takes for debugging and improvement
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def main():
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    # Create logs directory if it doesn't exist
    log_dir = Path(".claude/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create daily log file
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"actions-{today}.jsonl"
    
    # Extract relevant information
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tool_name": input_data.get("tool_name", "unknown"),
        "tool_input": input_data.get("tool_input", {}),
        "session_id": input_data.get("session_id", "unknown")
    }
    
    # Append to log file (JSONL format for easy parsing)
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    # Output success (Claude Code expects JSON response)
    print(json.dumps({"success": True}))

    sys.exit(0)

if __name__ == "__main__":
    main()
