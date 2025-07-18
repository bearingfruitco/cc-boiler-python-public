#!/usr/bin/env python3
"""
PRD Clarity Linter Hook
Detects ambiguous language in PRDs and suggests specific alternatives
Based on Grove's "Integrated Thought Clarifier" concept
"""

import json
import re
import sys
from pathlib import Path

# Ambiguous terms and their suggested replacements
AMBIGUOUS_TERMS = {
    # Performance terms
    r'\b(fast|quick|speedy|rapid)\b': {
        'level': 'warning',
        'message': 'Specify concrete performance metrics',
        'suggestions': [
            'Response time < 200ms',
            'Page load < 3 seconds',
            'Processing time < 500ms'
        ]
    },
    r'\b(slow|sluggish|delayed)\b': {
        'level': 'warning',
        'message': 'Define acceptable performance threshold',
        'suggestions': [
            'Response time > 1 second triggers warning',
            'Timeout after 30 seconds'
        ]
    },
    
    # Quality terms
    r'\b(optimal|optimized|best|perfect)\b': {
        'level': 'warning',
        'message': 'Define specific optimization goals',
        'suggestions': [
            'Bundle size < 250KB',
            'Memory usage < 100MB',
            'CPU usage < 20%'
        ]
    },
    r'\b(secure|safe|protected)\b': {
        'level': 'warning',
        'message': 'Specify security requirements',
        'suggestions': [
            'Encrypted with AES-256',
            'OWASP Top 10 compliant',
            'SOC 2 certified'
        ]
    },
    
    # User experience terms
    r'\b(user[- ]friendly|intuitive|easy to use)\b': {
        'level': 'warning',
        'message': 'Define specific UX metrics',
        'suggestions': [
            'Task completion < 3 clicks',
            'Accessibility score > 90',
            'Mobile responsive at 320px+'
        ]
    },
    r'\b(modern|contemporary|cutting[- ]edge)\b': {
        'level': 'warning',
        'message': 'Specify concrete features or standards',
        'suggestions': [
            'Supports ES2022+ features',
            'Uses React 18+ features',
            'Implements Web Components v1'
        ]
    },
    
    # Scale terms
    r'\b(scalable|high[- ]performance|enterprise[- ]grade)\b': {
        'level': 'warning',
        'message': 'Define specific scale requirements',
        'suggestions': [
            'Handles 10,000 concurrent users',
            'Processes 1M requests/day',
            '99.9% uptime SLA'
        ]
    },
    
    # Vague requirements
    r'\bshould\s+(be|have|support)\b': {
        'level': 'info',
        'message': 'Consider using MUST/MAY/SHOULD (RFC 2119)',
        'suggestions': [
            'MUST support...',
            'SHOULD handle...',
            'MAY include...'
        ]
    },
    r'\b(various|multiple|several|some)\b': {
        'level': 'warning',
        'message': 'Specify exact quantities or examples',
        'suggestions': [
            'At least 3...',
            'Between 5-10...',
            'Specifically: A, B, and C'
        ]
    }
}

def check_prd_clarity(file_path):
    """Check PRD file for ambiguous language"""
    issues = []
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except:
        return issues
    
    # Only check certain sections
    in_requirements = False
    in_acceptance = False
    in_background = False
    
    for line_num, line in enumerate(lines, 1):
        # Track which section we're in
        if '## Requirements' in line or '## Acceptance Criteria' in line:
            in_requirements = True
            in_acceptance = True
            in_background = False
        elif '## Background' in line or '## Context' in line:
            in_requirements = False
            in_acceptance = False
            in_background = True
        elif line.startswith('## '):
            in_requirements = False
            in_acceptance = False
            in_background = False
        
        # Skip ambiguity checks in background sections
        if in_background:
            continue
        
        # Check each pattern
        for pattern, config in AMBIGUOUS_TERMS.items():
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                issue = {
                    'line': line_num,
                    'column': match.start() + 1,
                    'level': config['level'],
                    'message': config['message'],
                    'text': match.group(),
                    'suggestions': config['suggestions'],
                    'context': line.strip(),
                    'in_requirements': in_requirements or in_acceptance
                }
                issues.append(issue)
    
    return issues

def format_issue(issue):
    """Format issue for display"""
    level_symbol = {
        'error': '❌',
        'warning': '⚠️ ',
        'info': '💡'
    }
    
    symbol = level_symbol.get(issue['level'], '📝')
    
    # More prominent for requirements sections
    if issue['in_requirements']:
        output = f"\n{symbol} Line {issue['line']}: \"{issue['text']}\" - {issue['message']}"
    else:
        output = f"\n{symbol} Line {issue['line']}: \"{issue['text']}\" - {issue['message']}"
    
    output += f"\n   Context: {issue['context']}"
    output += "\n   Suggestions:"
    for suggestion in issue['suggestions']:
        output += f"\n     → {suggestion}"
    
    return output

def main():
    # Read hook input
    try:
        hook_input = json.loads(sys.stdin.read())
        tool_use = hook_input['toolUse']
        
        # Only check PRD-related file operations
        if tool_use['toolName'] not in ['filesystem:write_file', 'filesystem:edit_file']:
            return
        
        file_path = None
        if 'path' in tool_use['parameters']:
            file_path = tool_use['parameters']['path']
        
        if not file_path:
            return
        
        # Check if it's a PRD file
        if not ('PRD.md' in file_path or 'prd.md' in file_path or '/features/' in file_path):
            return
        
        # For write operations, check if we're writing a PRD
        if tool_use['toolName'] == 'filesystem:write_file':
            content = tool_use['parameters'].get('content', '')
            # Save temporarily to check
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            
            issues = check_prd_clarity(tmp_path)
            Path(tmp_path).unlink()  # Clean up
        else:
            # For edits, wait a moment for the file to be written
            import time
            time.sleep(0.1)
            issues = check_prd_clarity(file_path)
        
        if not issues:
            return
        
        # Check for strict mode
        config_path = Path.home() / '.claude' / 'config.json'
        strict_mode = False
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
                strict_mode = config.get('grove_enhancements', {}).get('prd_linter', {}).get('blocking', False)
        
        # Format output
        print("\n🔍 PRD CLARITY CHECK")
        print("=" * 50)
        
        error_count = sum(1 for i in issues if i['level'] == 'error')
        warning_count = sum(1 for i in issues if i['level'] == 'warning')
        info_count = sum(1 for i in issues if i['level'] == 'info')
        
        print(f"Found: {error_count} errors, {warning_count} warnings, {info_count} suggestions")
        
        # Group by requirements vs other sections
        req_issues = [i for i in issues if i['in_requirements']]
        other_issues = [i for i in issues if not i['in_requirements']]
        
        if req_issues:
            print("\n📋 In Requirements/Acceptance Criteria (HIGH PRIORITY):")
            for issue in req_issues:
                print(format_issue(issue))
        
        if other_issues and warning_count < 5:  # Don't overwhelm
            print("\n📄 In Other Sections:")
            for issue in other_issues[:3]:  # Limit to 3
                print(format_issue(issue))
        
        print("\n" + "=" * 50)
        print("💡 Tip: Use specific, measurable criteria in requirements")
        print("📚 Reference: RFC 2119 for requirement levels (MUST/SHOULD/MAY)")
        
        if strict_mode and error_count > 0:
            print("\n❌ PRD clarity check failed in strict mode!")
            sys.exit(1)
        
    except json.JSONDecodeError:
        pass
    except Exception as e:
        # Fail silently in production
        if Path('DEBUG_HOOKS').exists():
            print(f"PRD Clarity Hook Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main()
