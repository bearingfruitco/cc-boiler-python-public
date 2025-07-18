#!/usr/bin/env python3
"""
Hydration Guard Hook - Prevents Next.js hydration errors
Catches common SSR/CSR mismatches before they happen
"""

import json
import sys
import re
from pathlib import Path

# Patterns that cause hydration errors
HYDRATION_VIOLATIONS = [
    {
        'pattern': r'Date\.now\(\)|new Date\(\)\.getTime\(\)',
        'message': 'Date.now() causes hydration mismatch',
        'fix': 'Use static timestamp or wrap in useEffect',
        'example': 'const [timestamp] = useState(() => Date.now())'
    },
    {
        'pattern': r'Math\.random\(\)',
        'message': 'Math.random() causes hydration mismatch',
        'fix': 'Use useId() or stable random seed',
        'example': 'const id = useId() or const [random] = useState(() => Math.random())'
    },
    {
        'pattern': r'(?<!typeof\s)window\.|document\.|navigator\.',
        'message': 'Browser APIs not available during SSR',
        'fix': 'Wrap in useEffect or check typeof window !== "undefined"',
        'example': 'useEffect(() => { window.localStorage.setItem(...) }, [])'
    },
    {
        'pattern': r'localStorage|sessionStorage',
        'message': 'Storage APIs not available during SSR',
        'fix': 'Use useEffect for client-side storage access',
        'example': 'useEffect(() => { const saved = localStorage.getItem(...) }, [])'
    },
    {
        'pattern': r'\{[^}]*new\s+Date\([^)]*\)\.to(?:Locale)?(?:Date)?(?:Time)?String\([^)]*\)[^}]*\}',
        'message': 'Dynamic date formatting causes hydration mismatch',
        'fix': 'Format dates in useEffect or use consistent locale',
        'example': 'const [dateStr, setDateStr] = useState(""); useEffect(() => setDateStr(new Date().toLocaleDateString()), [])'
    },
    {
        'pattern': r'crypto\.getRandomValues|crypto\.randomUUID',
        'message': 'Crypto API causes hydration mismatch',
        'fix': 'Generate IDs in useEffect or use stable IDs',
        'example': 'const [id, setId] = useState(""); useEffect(() => setId(crypto.randomUUID()), [])'
    }
]

# Component patterns to check
COMPONENT_PATTERNS = [
    r'export\s+(?:default\s+)?function\s+\w+Component',
    r'export\s+(?:default\s+)?function\s+\w+Page',
    r'export\s+(?:const|let)\s+\w+\s*=\s*\([^)]*\)\s*=>'
]

def is_react_component(file_path, content):
    """Check if file contains React components"""
    # Check file extension
    if not file_path.endswith(('.tsx', '.jsx')):
        return False
    
    # Check for component patterns
    for pattern in COMPONENT_PATTERNS:
        if re.search(pattern, content):
            return True
    
    # Check for JSX
    return bool(re.search(r'<[A-Z]\w*[^>]*>', content))

def check_hydration_issues(content, file_path):
    """Check for potential hydration errors"""
    violations = []
    
    # Only check React component files
    if not is_react_component(file_path, content):
        return violations
    
    # Check each pattern
    for violation in HYDRATION_VIOLATIONS:
        matches = list(re.finditer(violation['pattern'], content))
        for match in matches:
            # Get line number
            line_num = content[:match.start()].count('\n') + 1
            
            # Check if it's inside useEffect (safe)
            before_match = content[:match.start()]
            after_match = content[match.end():]
            
            # Simple heuristic: if inside useEffect, it's probably safe
            if 'useEffect(' in before_match[-200:] and '})' in after_match[:200]:
                continue
            
            violations.append({
                'line': line_num,
                'code': match.group(0),
                'message': violation['message'],
                'fix': violation['fix'],
                'example': violation.get('example', '')
            })
    
    return violations

def main():
    """Main hook logic"""
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    # Only check file writes
    tool_use = input_data.get('tool_use', {})
    if tool_use.get('name') not in ['str_replace_editor', 'create_file', 'edit_file']:
        print(json.dumps({"action": "continue"}))
        return
    
    # Get file content
    file_path = tool_use.get('path', '')
    content = tool_use.get('content', tool_use.get('new_str', ''))
    
    if not content:
        print(json.dumps({"action": "continue"}))
        return
    
    # Check for hydration issues
    violations = check_hydration_issues(content, file_path)
    
    if violations:
        # Format error message
        error_msg = f"🚨 Next.js Hydration Error Prevention\n\n"
        error_msg += f"Found {len(violations)} potential hydration error(s) in {file_path}:\n\n"
        
        for v in violations:
            error_msg += f"Line {v['line']}: {v['code']}\n"
            error_msg += f"  ❌ {v['message']}\n"
            error_msg += f"  ✅ Fix: {v['fix']}\n"
            if v['example']:
                error_msg += f"  📝 Example: {v['example']}\n"
            error_msg += "\n"
        
        error_msg += "These patterns will cause React hydration mismatches in production.\n"
        error_msg += "Please fix them before proceeding."
        
        print(json.dumps({
            "action": "block",
            "message": error_msg,
            "suggestion": "Wrap browser-only code in useEffect or use proper SSR-safe patterns"
        }))
    else:
        print(json.dumps({"action": "continue"}))

if __name__ == "__main__":
    main()
