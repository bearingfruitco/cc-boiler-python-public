#!/usr/bin/env python3
"""
PII Protection Hook - Prevents PII from being logged or exposed client-side
"""

import json
import sys
import re
from pathlib import Path

def get_pii_patterns():
    """Get patterns that indicate PII"""
    return {
        'console_log': [
            r'console\.(log|warn|error|info|debug)\s*\([^)]*\b(email|phone|ssn|firstName|lastName|address|dob|dateOfBirth)\b',
            r'console\.(log|warn|error|info|debug)\s*\([^)]*\b(formData|userData|personalInfo|customerData)\b',
        ],
        'localStorage': [
            r'localStorage\.(setItem|getItem)\s*\([\'"][^\'"]*\b(email|phone|ssn|user|customer|personal)\b',
            r'sessionStorage\.(setItem|getItem)\s*\([\'"][^\'"]*\b(email|phone|ssn|user|customer|personal)\b',
        ],
        'url_params': [
            r'[?&](email|phone|ssn|name|firstName|lastName|address)=',
            r'URLSearchParams.*append\s*\([\'"]?(email|phone|ssn|firstName|lastName)',
        ],
        'dangerous_fields': [
            r'value\s*=\s*[\'"]?\$?\{?.*?(ssn|creditCard|bankAccount)',
            r'defaultValue\s*=\s*[\'"]?\$?\{?.*?(email|phone|address)',
        ]
    }

def check_file_content(content, file_path):
    """Check file content for PII exposure"""
    violations = []
    
    # Skip test files and node_modules
    if 'test' in file_path or 'node_modules' in file_path:
        return violations
    
    patterns = get_pii_patterns()
    lines = content.split('\n')
    
    for category, pattern_list in patterns.items():
        for pattern in pattern_list:
            for i, line in enumerate(lines):
                if re.search(pattern, line, re.IGNORECASE):
                    violations.append({
                        'type': category,
                        'line': i + 1,
                        'content': line.strip(),
                        'pattern': pattern
                    })
    
    # Check for specific anti-patterns
    if '.tsx' in file_path or '.jsx' in file_path:
        # Check for client-side encryption attempts
        if 'crypto' in content and 'encrypt' in content:
            for i, line in enumerate(lines):
                if 'crypto' in line and 'email' in line.lower():
                    violations.append({
                        'type': 'client_encryption',
                        'line': i + 1,
                        'content': line.strip(),
                        'message': 'PII encryption must be server-side only'
                    })
    
    return violations

def suggest_fixes(violations):
    """Suggest fixes for violations"""
    fixes = []
    
    for violation in violations:
        if violation['type'] == 'console_log':
            fixes.append({
                'violation': violation,
                'fix': 'Use PIIDetector.createSafeObject() before logging',
                'example': 'console.log(PIIDetector.createSafeObject(userData))'
            })
        elif violation['type'] == 'localStorage':
            fixes.append({
                'violation': violation,
                'fix': 'Store PII server-side only, use session tokens',
                'example': 'Use secure HTTP-only cookies or server sessions'
            })
        elif violation['type'] == 'url_params':
            fixes.append({
                'violation': violation,
                'fix': 'Never put PII in URLs, use POST requests',
                'example': 'POST /api/users with body instead of GET /api/users?email='
            })
        elif violation['type'] == 'dangerous_fields':
            fixes.append({
                'violation': violation,
                'fix': 'Never prepopulate PII fields from URLs or client storage',
                'example': 'Only prepopulate whitelisted tracking fields'
            })
    
    return fixes

def format_violation_message(violations, fixes):
    """Format violations into readable message"""
    if not violations:
        return None
    
    message = "🔒 PII PROTECTION VIOLATIONS DETECTED\n\n"
    
    # Group by type
    by_type = {}
    for v in violations:
        if v['type'] not in by_type:
            by_type[v['type']] = []
        by_type[v['type']].append(v)
    
    # Show violations
    for vtype, items in by_type.items():
        type_names = {
            'console_log': '❌ PII in Console Logs',
            'localStorage': '❌ PII in Client Storage',
            'url_params': '❌ PII in URLs',
            'dangerous_fields': '❌ Dangerous Field Usage',
            'client_encryption': '❌ Client-Side Encryption'
        }
        
        message += f"{type_names.get(vtype, vtype)}:\n"
        for item in items[:3]:  # Show first 3
            message += f"  Line {item['line']}: {item['content'][:60]}...\n"
        
        if len(items) > 3:
            message += f"  ... and {len(items) - 3} more\n"
        message += "\n"
    
    # Show fixes
    message += "📋 REQUIRED FIXES:\n"
    for i, fix in enumerate(fixes[:5], 1):
        message += f"{i}. {fix['fix']}\n"
        if 'example' in fix:
            message += f"   Example: {fix['example']}\n"
    
    message += "\n🛡️ SECURITY RULES:\n"
    message += "• NEVER log PII to console (use PIIDetector.createSafeObject)\n"
    message += "• NEVER store PII in localStorage/sessionStorage\n"
    message += "• NEVER put PII in URLs or query parameters\n"
    message += "• NEVER encrypt PII client-side\n"
    message += "• ALWAYS handle PII server-side only\n"
    
    return message

def main():
    """Main hook logic"""
    input_data = json.loads(sys.stdin.read())
    
    # Only check write operations
    if input_data['tool'] not in ['write_file', 'edit_file', 'str_replace']:
        sys.exit(0)
        return
    
    file_path = input_data.get('path', '')
    
    # Only check code files
    if not any(file_path.endswith(ext) for ext in ['.ts', '.tsx', '.js', '.jsx']):
        sys.exit(0)
        return
    
    content = input_data.get('content', '')
    
    # Check for violations
    violations = check_file_content(content, file_path)
    
    if violations:
        fixes = suggest_fixes(violations)
        message = format_violation_message(violations, fixes)
        
        # For critical violations (PII in logs/storage), block
        critical_types = ['console_log', 'localStorage', 'url_params']
        has_critical = any(v['type'] in critical_types for v in violations)
        
        if has_critical:
            print(json.dumps({
                "decision": "block",
                "message": message,
                "violations": violations
            }))
        else:
            # Warn but allow for other issues
            print(json.dumps({
                "decision": "warn",
                "message": message,
                "continue": True
            }))
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
