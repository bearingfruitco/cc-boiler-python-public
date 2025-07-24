#!/usr/bin/env python3
"""
Python Code Style Enforcement Hook
Ensures Python code follows PEP 8 and project conventions
"""

import json
import sys
import re
from pathlib import Path

def get_config():
    """Load hook configuration"""
    config_path = Path(__file__).parent.parent / 'config.json'
    with open(config_path) as f:
        return json.load(f)

def is_python_file(file_path):
    """Check if this is a Python file that needs validation"""
    python_extensions = ['.py', '.pyi']
    ignore_paths = ['venv', '.venv', '__pycache__', '.git', 'node_modules']
    
    # Check if it's a Python file
    if not any(file_path.endswith(ext) for ext in python_extensions):
        return False
    
    # Ignore certain paths
    if any(ignore in file_path for ignore in ignore_paths):
        return False
    
    return True

def find_style_violations(content, config):
    """Find Python style violations"""
    violations = {
        'critical': [],
        'warnings': []
    }
    
    lines = content.split('\n')
    
    # Check line length (PEP 8: 79 chars, but we allow 88 for Black)
    for i, line in enumerate(lines):
        if len(line) > 88:
            violations['warnings'].append({
                'line': i + 1,
                'message': f'Line too long ({len(line)} > 88 characters)',
                'fix': 'Break line or refactor'
            })
    
    # Check for tabs (should use spaces)
    for i, line in enumerate(lines):
        if '\t' in line:
            violations['critical'].append({
                'line': i + 1,
                'message': 'Tabs found (use 4 spaces)',
                'fix': line.replace('\t', '    ')
            })
    
    # Check for trailing whitespace
    for i, line in enumerate(lines):
        if line.endswith(' ') or line.endswith('\t'):
            violations['warnings'].append({
                'line': i + 1,
                'message': 'Trailing whitespace',
                'fix': line.rstrip()
            })
    
    # Check import order
    import_lines = []
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            import_lines.append((i, line))
    
    # Check for common bad patterns
    bad_patterns = [
        (r'except\s*:', 'Bare except clause', 'Specify exception type'),
        (r'print\(', 'Print statement in production code', 'Use logging instead'),
        (r'==\s*True|==\s*False', 'Comparison to True/False', 'Use `if var:` or `if not var:`'),
        (r'type\(.*\)\s*==', 'Type comparison with ==', 'Use isinstance()'),
    ]
    
    for pattern, message, fix in bad_patterns:
        for i, line in enumerate(lines):
            if re.search(pattern, line):
                violations['warnings'].append({
                    'line': i + 1,
                    'message': message,
                    'fix': fix
                })
    
    return violations

def main():
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Skip if not a file edit
    if input_data.get('name') not in ['str_replace', 'write_file']:
        json.dump({sys.exit(0)  # Allow}, sys.stdout)
        return
    
    # Get file path
    file_path = input_data.get('parameters', {}).get('path', '')
    
    # Skip if not a Python file
    if not is_python_file(file_path):
        json.dump({sys.exit(0)  # Allow}, sys.stdout)
        return
    
    # Get content
    content = input_data.get('parameters', {}).get('content', '')
    if not content and input_data.get('name') == 'str_replace':
        content = input_data.get('parameters', {}).get('new_str', '')
    
    # Load config
    config = get_config()
    
    # Check if style enforcement is enabled
    if not config.get('python_style', {}).get('enforce', True):
        json.dump({sys.exit(0)  # Allow}, sys.stdout)
        return
    
    # Find violations
    violations = find_style_violations(content, config)
    
    # If critical violations, block
    if violations['critical']:
        response = {
            "decision": "block",
            "message": f"❌ Python style violations detected in {file_path}",
            "details": violations['critical'][:3]  # Show first 3
        }
        json.dump(response, sys.stdout)
        return
    
    # If warnings, allow but notify
    if violations['warnings']:
        response = {
            sys.exit(0)  # Allow,
            "message": f"⚠️  Python style warnings in {file_path}",
            "details": violations['warnings'][:3]
        }
    else:
        response = {sys.exit(0)  # Allow}
    
    json.dump(response, sys.stdout)

    sys.exit(0)

if __name__ == "__main__":
    main()
