#!/usr/bin/env python3
"""
Code Quality Hook - Enforce code quality standards
Inspired by community hooks but enhanced for our needs
"""

import json
import sys
import re
from pathlib import Path

def check_code_quality(content, file_path):
    """Check various code quality metrics"""
    issues = []
    
    # Check for console.logs in production code
    if not any(test in file_path for test in ['.test.', '.spec.', 'test/']):
        console_logs = len(re.findall(r'console\.(log|error|warn|info)', content))
        if console_logs > 0:
            issues.append({
                'type': 'console-log',
                'severity': 'warning',
                'message': f'Found {console_logs} console statements in production code'
            })
    
    # Check for TODO comments that need tracking
    todos = re.findall(r'//\s*TODO:?\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
    if todos:
        issues.append({
            'type': 'untracked-todo',
            'severity': 'info',
            'message': f'Found {len(todos)} TODO comments',
            'todos': todos[:3]  # First 3
        })
    
    # Check for any or unknown types in TypeScript
    if file_path.endswith(('.ts', '.tsx')):
        any_types = len(re.findall(r':\s*any\b', content))
        if any_types > 0:
            issues.append({
                'type': 'any-type',
                'severity': 'warning',
                'message': f'Found {any_types} uses of "any" type'
            })
    
    # Check for missing error handling
    try_without_catch = len(re.findall(r'\btry\s*{(?:(?!catch).)*?}\s*(?!catch)', content, re.DOTALL))
    if try_without_catch > 0:
        issues.append({
            'type': 'missing-error-handling',
            'severity': 'error',
            'message': 'Found try block without catch'
        })
    
    # Check component file structure
    if '/components/' in file_path and file_path.endswith('.tsx'):
        has_interface = 'interface' in content or 'type' in content
        has_export = 'export' in content
        
        if not has_interface:
            issues.append({
                'type': 'missing-types',
                'severity': 'warning',
                'message': 'Component missing TypeScript interface/type'
            })
        
        if not has_export:
            issues.append({
                'type': 'missing-export',
                'severity': 'error',
                'message': 'Component missing export'
            })
    
    return issues

def calculate_complexity(content):
    """Simple cyclomatic complexity estimate"""
    complexity_indicators = [
        r'\bif\b',
        r'\belse\b',
        r'\bfor\b',
        r'\bwhile\b',
        r'\bcase\b',
        r'\bcatch\b',
        r'\?.*:',  # ternary
        r'&&',
        r'\|\|'
    ]
    
    complexity = 1  # Base complexity
    for pattern in complexity_indicators:
        complexity += len(re.findall(pattern, content))
    
    return complexity

def format_quality_report(issues, complexity, file_path):
    """Format quality issues into readable report"""
    if not issues and complexity < 10:
        return None
    
    report = f"📊 Code Quality Check: {Path(file_path).name}\n\n"
    
    # Complexity warning
    if complexity > 15:
        report += f"⚠️ High Complexity: {complexity} (consider refactoring)\n\n"
    
    # Group by severity
    errors = [i for i in issues if i['severity'] == 'error']
    warnings = [i for i in issues if i['severity'] == 'warning']
    info = [i for i in issues if i['severity'] == 'info']
    
    if errors:
        report += "❌ Errors (must fix):\n"
        for issue in errors:
            report += f"  • {issue['message']}\n"
    
    if warnings:
        report += "\n⚠️ Warnings (should fix):\n"
        for issue in warnings:
            report += f"  • {issue['message']}\n"
    
    if info:
        report += "\n💡 Info:\n"
        for issue in info:
            report += f"  • {issue['message']}\n"
            if issue['type'] == 'untracked-todo' and issue.get('todos'):
                for todo in issue['todos']:
                    report += f"    - TODO: {todo}\n"
    
    return report

def suggest_fixes(issues):
    """Suggest fixes for common issues"""
    fixes = {}
    
    for issue in issues:
        if issue['type'] == 'console-log':
            fixes['console-log'] = "Replace with proper logging service or remove"
        elif issue['type'] == 'any-type':
            fixes['any-type'] = "Define proper TypeScript types"
        elif issue['type'] == 'missing-error-handling':
            fixes['missing-error-handling'] = "Add catch block or finally"
    
    return fixes

def main():
    """Main hook logic"""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Only check on write operations
    if input_data.get('tool') not in ['write_file', 'edit_file']:
        sys.exit(0)
        return
    
    file_path = input_data.get('path', '')
    content = input_data.get('content', '')
    
    # Skip non-code files
    if not any(file_path.endswith(ext) for ext in ['.ts', '.tsx', '.js', '.jsx']):
        sys.exit(0)
        return
    
    # Check quality
    issues = check_code_quality(content, file_path)
    complexity = calculate_complexity(content)
    
    # Generate report
    report = format_quality_report(issues, complexity, file_path)
    
    if report:
        # Get severity level
        has_errors = any(i['severity'] == 'error' for i in issues)
        
        sys.exit(0)  # Continue normally
        
        # Add fixes if available
        fixes = suggest_fixes(issues)
        if fixes:
            response["suggested_fixes"] = fixes
        
        # Allow continuation for warnings
        if not has_errors:
            response["continue"] = True
        
        print(json.dumps(response))
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
