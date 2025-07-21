#!/usr/bin/env python3
"""
Python Import Validator Hook - Ensures proper Python import patterns
Validates import statements and checks for common issues
"""

import json
import sys
import re
import ast
from pathlib import Path

def get_project_root():
    """Find the project root (where pyproject.toml or setup.py is)"""
    current = Path.cwd()
    while current != current.parent:
        if (current / 'pyproject.toml').exists() or (current / 'setup.py').exists():
            return current
        current = current.parent
    return Path.cwd()

def is_python_file(file_path):
    """Check if this is a Python file"""
    return file_path.endswith('.py') or file_path.endswith('.pyi')

def validate_imports(content, file_path):
    """Validate Python import statements"""
    issues = []
    
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return [{
            'line': e.lineno,
            'message': f'Syntax error: {e.msg}',
            'type': 'error'
        }]
    
    # Check imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                # Check for star imports in regular imports
                if alias.name == '*':
                    issues.append({
                        'line': node.lineno,
                        'message': 'Avoid star imports',
                        'type': 'warning',
                        'fix': 'Import specific names'
                    })
        
        elif isinstance(node, ast.ImportFrom):
            # Check for relative imports beyond current package
            if node.level > 1:
                issues.append({
                    'line': node.lineno,
                    'message': f'Avoid deep relative imports ({"." * node.level})',
                    'type': 'warning',
                    'fix': 'Use absolute imports'
                })
            
            # Check for star imports
            if any(alias.name == '*' for alias in node.names):
                # Allow star imports from __future__
                if node.module != '__future__':
                    issues.append({
                        'line': node.lineno,
                        'message': f'Avoid "from {node.module} import *"',
                        'type': 'warning',
                        'fix': 'Import specific names'
                    })
    
    # Check import order (standard lib, third party, local)
    import_lines = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if line.strip().startswith(('import ', 'from ')):
            import_lines.append((i + 1, line.strip()))
    
    # Basic import ordering check
    if len(import_lines) > 1:
        in_stdlib_section = True
        in_third_party_section = False
        
        for line_no, import_line in import_lines:
            # Simple heuristic: stdlib imports don't have dots at the start
            is_stdlib = not (import_line.split()[1] if import_line.startswith('import') else import_line.split()[1]).startswith('.')
            
            if not is_stdlib and in_stdlib_section:
                in_stdlib_section = False
                in_third_party_section = True
    
    return issues

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
    
    # Validate imports
    issues = validate_imports(content, file_path)
    
    # Filter critical issues
    errors = [i for i in issues if i.get('type') == 'error']
    warnings = [i for i in issues if i.get('type') == 'warning']
    
    # Block on errors
    if errors:
        response = {
            "decision": "block",
            "message": f"❌ Import errors in {file_path}",
            "details": errors[:3]
        }
        json.dump(response, sys.stdout)
        return
    
    # Notify on warnings
    if warnings:
        response = {
            sys.exit(0)  # Allow,
            "message": f"⚠️  Import warnings in {file_path}",
            "details": warnings[:3]
        }
    else:
        response = {sys.exit(0)  # Allow}
    
    json.dump(response, sys.stdout)

    sys.exit(0)

if __name__ == "__main__":
    main()
