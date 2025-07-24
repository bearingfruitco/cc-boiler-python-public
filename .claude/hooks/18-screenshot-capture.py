#!/usr/bin/env python3
"""
Screenshot Capture Hook - Capture browser screenshots on test failures
Integrates with browser-test-flow and stores screenshots with context
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
import subprocess
import base64

def capture_browser_screenshot():
    """Attempt to capture browser screenshot using available tools."""
    screenshot_methods = [
        # Method 1: Using Playwright if available
        ["npx", "playwright", "screenshot", "--full-page", "--wait-for-timeout=1000"],
        # Method 2: Using Chrome DevTools Protocol
        ["node", "-e", "require('puppeteer').launch().then(b => b.newPage().then(p => p.screenshot({fullPage: true})))"],
        # Method 3: macOS screenshot
        ["screencapture", "-x", "-t", "png", "-"]
    ]
    
    for method in screenshot_methods:
        try:
            result = subprocess.run(method, capture_output=True, timeout=5)
            if result.returncode == 0 and result.stdout:
                return base64.b64encode(result.stdout).decode('utf-8')
        except Exception:
            continue
    
    return None

def main():
    """Main hook logic."""
    try:
        # Read input
        input_data = json.loads(sys.stdin.read())
        
        # Only process test-related tools
        tool_name = input_data.get('tool_name', '')
        if tool_name not in ['Bash', 'Task'] or 'tool_response' not in input_data:
            sys.exit(0)
        
        # Check if this was a test command
        tool_input = input_data.get('tool_input', {})
        command = tool_input.get('command', '') if tool_name == 'Bash' else ''
        
        # Look for test-related commands
        test_keywords = ['pytest', 'test', 'npm test', 'yarn test', 'playwright']
        if not any(keyword in command.lower() for keyword in test_keywords):
            sys.exit(0)
        
        # Check if tests failed
        tool_response = input_data.get('tool_response', {})
        exit_code = tool_response.get('exit_code', 0)
        stderr = tool_response.get('stderr', '')
        stdout = tool_response.get('stdout', '')
        
        if exit_code == 0:  # Tests passed
            sys.exit(0)
        
        # Tests failed - capture screenshot if browser-related
        browser_keywords = ['browser', 'playwright', 'puppeteer', 'selenium', 'ui', 'e2e']
        if any(keyword in (command + stderr + stdout).lower() for keyword in browser_keywords):
            
            # Create screenshots directory
            screenshots_dir = Path('.claude/screenshots')
            screenshots_dir.mkdir(exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            test_name = command.split()[-1] if command else 'unknown'
            filename = f"test_failure_{test_name}_{timestamp}.png"
            filepath = screenshots_dir / filename
            
            # Attempt to capture screenshot
            screenshot_data = capture_browser_screenshot()
            
            if screenshot_data:
                # Save screenshot
                with open(filepath, 'wb') as f:
                    f.write(base64.b64decode(screenshot_data))
                
                # Update captures index
                captures_index = Path('.claude/captures/index.json')
                if captures_index.exists():
                    with open(captures_index, 'r') as f:
                        captures = json.load(f)
                else:
                    captures = {"captures": []}
                
                # Add capture entry
                capture_entry = {
                    "id": f"screenshot_{timestamp}",
                    "type": "test_failure_screenshot",
                    "timestamp": datetime.now().isoformat(),
                    "command": command,
                    "exit_code": exit_code,
                    "screenshot_path": str(filepath),
                    "linked_to": {
                        "task_ledger": input_data.get('session_id', 'unknown'),
                        "test_output": {
                            "stderr": stderr[:500],  # First 500 chars
                            "stdout": stdout[:500]
                        }
                    }
                }
                
                captures["captures"].append(capture_entry)
                
                # Save updated index
                with open(captures_index, 'w') as f:
                    json.dump(captures, f, indent=2)
                
                # Log to stdout for visibility
                print(f"📸 Screenshot captured: {filepath}")
                print(f"   Test failed with exit code {exit_code}")
                
    except Exception as e:
        # Log error but don't block
        print(f"Screenshot capture error: {e}", file=sys.stderr)
        sys.exit(0)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
