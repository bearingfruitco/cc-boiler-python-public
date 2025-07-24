#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Save complete chat transcript when Claude Code stops
Essential for observability and learning from agent sessions
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def main():
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    # Create transcripts directory
    transcript_dir = Path(".claude/transcripts")
    transcript_dir.mkdir(parents=True, exist_ok=True)
    
    # Get transcript data
    transcript = input_data.get('transcript', {})
    messages = transcript.get('messages', [])
    
    if messages:
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        transcript_file = transcript_dir / f"chat_{timestamp}.json"
        
        # Save full transcript
        transcript_data = {
            "timestamp": datetime.now().isoformat(),
            "message_count": len(messages),
            "session_id": input_data.get('session_id', 'unknown'),
            "messages": messages
        }
        
        with open(transcript_file, "w") as f:
            json.dump(transcript_data, f, indent=2)
        
        # Also create a summary
        summary_file = transcript_dir / f"summary_{timestamp}.md"
        with open(summary_file, "w") as f:
            f.write(f"# Chat Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Total Messages**: {len(messages)}\n")
            f.write(f"**Session ID**: {input_data.get('session_id', 'unknown')}\n\n")
            
            # Extract key information
            f.write("## Key Actions:\n")
            for msg in messages:
                if msg.get('role') == 'assistant':
                    content = msg.get('content', '')
                    # Look for file operations
                    if 'created' in content.lower() or 'updated' in content.lower():
                        f.write(f"- {content[:100]}...\n")
            
            f.write("\n## Commands Used:\n")
            for msg in messages:
                if msg.get('role') == 'user':
                    content = msg.get('content', '')
                    if content.startswith('/'):
                        f.write(f"- `{content}`\n")
    
    # Output success
    print(json.dumps({"success": True, "transcript_saved": bool(messages)}))

    sys.exit(0)

if __name__ == "__main__":
    main()
