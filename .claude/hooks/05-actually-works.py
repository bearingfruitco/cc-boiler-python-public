#!/usr/bin/env python3
"""
Actually Works Protocol - Enforce testing before claiming fixes
Prevents the AI from saying "this should work" without verification
"""

import json
import sys
import re
from pathlib import Path

def check_for_untested_claims(tool_input):
    """Check if AI is making untested claims about fixes"""
    
    # Get the content/message
    content = str(tool_input.get('content', '')) + str(tool_input.get('message', ''))
    
    # Red flag phrases that indicate untested code
    red_flags = [
        r"should\s+work\s+now",
        r"this\s+should\s+fix",
        r"i've\s+fixed\s+the\s+issue",
        r"try\s+it\s+now",
        r"the\s+logic\s+is\s+correct",
        r"i've\s+made\s+the\s+necessary\s+changes",
        r"that\s+ought\s+to\s+do\s+it",
        r"this\s+will\s+solve",
        r"should\s+be\s+working"
    ]
    
    violations = []
    for flag in red_flags:
        if re.search(flag, content, re.IGNORECASE):
            violations.append(flag.replace(r'\s+', ' '))
    
    return violations

def check_for_test_evidence(tool_input):
    """Check if there's evidence of actual testing"""
    content = str(tool_input.get('content', '')) + str(tool_input.get('message', ''))
    
    # Positive indicators of testing
    test_indicators = [
        r"i\s+tested",
        r"i\s+ran",
        r"i\s+verified",
        r"test\s+output",
        r"console\s+shows",
        r"result\s+was",
        r"confirmed\s+working"
    ]
    
    for indicator in test_indicators:
        if re.search(indicator, content, re.IGNORECASE):
            return True
    
    return False

def generate_testing_reminder():
    """Generate the Actually Works protocol reminder"""
    return """
🛑 ACTUALLY WORKS PROTOCOL VIOLATION DETECTED

You appear to be claiming something works without testing it.

✅ The 30-Second Reality Check - Answer ALL with YES:
□ Did you run/build the code?
□ Did you trigger the exact feature you changed?
□ Did you see the expected result with your own observation?
□ Did you check for error messages?
□ Would you bet $100 this works?

❌ Red Flag Phrases Detected in Your Response

💡 Required Actions:
1. Actually run the code
2. Test the specific feature
3. Verify the output
4. Only then claim it works

⏱️ Time Reality:
- Time saved skipping tests: 30 seconds
- Time wasted when it doesn't work: 30 minutes
- User trust lost: Immeasurable

Remember: "Should work" ≠ "Does work"
"""

def main():
    """Main hook logic"""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Only check on write operations that might contain claims
    if input_data.get('tool') not in ['write_file', 'edit_file', 'str_replace']:
        sys.exit(0)
        return
    
    # Check for untested claims
    violations = check_for_untested_claims(input_data)
    
    if violations:
        # Check if there's test evidence
        has_test_evidence = check_for_test_evidence(input_data)
        
        if not has_test_evidence:
            print(json.dumps({
                "decision": "warn",
                "message": generate_testing_reminder(),
                "violations": violations,
                "suggestion": "Test your changes before claiming they work",
                "continue": True  # Warn but don't block
            }))
            return
    
    # All good
    sys.exit(0)

if __name__ == "__main__":
    main()
