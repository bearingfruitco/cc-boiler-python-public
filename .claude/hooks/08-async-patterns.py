#!/usr/bin/env python3
"""
Hook to detect and warn about async anti-patterns
Ensures proper async/await usage and event-driven patterns
"""

import json
import re
import sys

def check_async_patterns(content, filename):
    """Check for common async anti-patterns"""
    issues = []
    suggestions = []
    
    # Pattern 1: Sequential awaits that could be parallel
    sequential_pattern = r'await\s+(\w+)\([^)]*\);\s*\n\s*await\s+(\w+)\([^)]*\);'
    matches = re.finditer(sequential_pattern, content)
    for match in matches:
        if 'api' in match.group(0) or 'fetch' in match.group(0):
            issues.append({
                'type': 'sequential_awaits',
                'line': content[:match.start()].count('\n') + 1,
                'message': 'Sequential API calls detected - consider using Promise.all()',
                'severity': 'warning',
                'suggestion': f'const [{match.group(1)}Result, {match.group(2)}Result] = await Promise.all([{match.group(1)}(), {match.group(2)}()]);'
            })
    
    # Pattern 2: Missing error handling in async functions
    async_functions = re.finditer(r'async\s+(?:function\s+)?(\w+)?\s*\([^)]*\)\s*(?:=>)?\s*{([^}]+)}', content, re.DOTALL)
    for func in async_functions:
        func_body = func.group(2)
        if 'await' in func_body and 'try' not in func_body and 'catch' not in func_body:
            func_name = func.group(1) or 'anonymous'
            issues.append({
                'type': 'missing_error_handling',
                'line': content[:func.start()].count('\n') + 1,
                'message': f'Async function "{func_name}" lacks error handling',
                'severity': 'error',
                'suggestion': 'Wrap await calls in try/catch blocks'
            })
    
    # Pattern 3: Blocking form submission with tracking
    form_submit_pattern = r'onSubmit\s*=\s*{?\s*async[^}]+await\s+(?:track|fire|send)(?:Pixel|Analytics|Event)'
    if re.search(form_submit_pattern, content):
        issues.append({
            'type': 'blocking_tracking',
            'message': 'Form submission blocked by tracking - use eventQueue.emit() instead',
            'severity': 'error',
            'suggestion': 'Replace: await trackAnalytics(data)\nWith: eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, data)'
        })
    
    # Pattern 4: Missing loading states for async operations
    if 'useState' in content and 'await' in content:
        # Check if there's a loading state
        if not re.search(r'(?:loading|isLoading|pending|isPending)', content, re.IGNORECASE):
            suggestions.append({
                'type': 'missing_loading_state',
                'message': 'Consider adding loading states for async operations',
                'suggestion': 'const [isLoading, setIsLoading] = useState(false);'
            })
    
    # Pattern 5: Fire and forget without proper handling
    fire_forget_pattern = r'(?<!await\s)(?<!return\s)(\w+(?:Async|Event|Pixel))\([^)]*\)(?!\.then)(?!\.catch)'
    matches = re.finditer(fire_forget_pattern, content)
    for match in matches:
        if match.group(1) not in ['preventDefault', 'stopPropagation']:
            suggestions.append({
                'type': 'unhandled_promise',
                'line': content[:match.start()].count('\n') + 1,
                'message': f'Fire-and-forget call to {match.group(1)} - consider using eventQueue',
                'suggestion': f'eventQueue.emit("event.name", data);'
            })
    
    # Pattern 6: Timeout missing for critical operations
    if 'fetch' in content and 'AbortController' not in content:
        suggestions.append({
            'type': 'missing_timeout',
            'message': 'API calls should have timeout handling',
            'suggestion': 'Use AbortController or the apiClient utility with timeout'
        })
    
    # Pattern 7: Check for event queue usage in lead forms
    if 'form' in filename.lower() and 'submit' in content.lower():
        if 'eventQueue' not in content and 'LEAD_EVENTS' not in content:
            suggestions.append({
                'type': 'missing_event_system',
                'message': 'Lead forms should use the event system for tracking',
                'suggestion': 'import { eventQueue, LEAD_EVENTS } from "@/lib/events";'
            })
    
    return issues, suggestions

def main():
    """Main hook execution"""
    input_data = json.loads(sys.stdin.read())
    
    # Only check TypeScript/JavaScript files
    command = input_data.get('command', '')
    if not any(ext in command for ext in ['.ts', '.tsx', '.js', '.jsx']):
        sys.exit(0)
        return
    
    # Skip test files
    if any(pattern in command for pattern in ['test.', 'spec.', '.test.', '.spec.']):
        sys.exit(0)
        return
    
    # Check for file edits
    if input_data.get('__tool') == 'str_replace:str_replace_editor':
        content = input_data.get('new_str', '')
        filename = command.split()[-1] if command else ''
        
        issues, suggestions = check_async_patterns(content, filename)
        
        if issues:
            # Critical issues block the operation
            print(json.dumps({
                "decision": "block",
                'message': 'Async pattern issues detected',
                'issues': issues,
                'help': 'Fix these issues:\n' + '\n'.join([
                    f"- Line {i.get('line', '?')}: {i['message']}\n  Fix: {i.get('suggestion', '')}"
                    for i in issues
                ])
            }))
            return
        
        if suggestions:
            # Suggestions are shown but don't block
            print(json.dumps({
                'decision': 'warn',
                'message': 'Async pattern suggestions',
                'suggestions': suggestions,
                'help': 'Consider these improvements:\n' + '\n'.join([
                    f"- {s['message']}"
                    for s in suggestions
                ])
            }))
            return
    
    sys.exit(0)

if __name__ == '__main__':
    main()
    sys.exit(0)
