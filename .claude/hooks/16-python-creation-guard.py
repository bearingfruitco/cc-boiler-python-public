#!/usr/bin/env python3
"""
Python Creation Guard Hook - Prevent duplicate modules, classes, and functions
Checks existence before creating new Python components
"""

import json
import sys
import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Optional, Set
import difflib

def find_python_files(root_path: Path) -> List[Path]:
    """Find all Python files in project."""
    python_files = []
    ignore_dirs = {'.venv', 'venv', '__pycache__', '.git', 'node_modules'}
    
    for path in root_path.rglob('*.py'):
        if not any(ignored in path.parts for ignored in ignore_dirs):
            python_files.append(path)
    
    return python_files

def extract_definitions(file_path: Path) -> Dict[str, List[str]]:
    """Extract classes, functions, and constants from Python file."""
    definitions = {
        'classes': [],
        'functions': [],
        'constants': [],
        'models': []  # Pydantic models
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                definitions['classes'].append(node.name)
                # Check if it's a Pydantic model
                if any(base.id == 'BaseModel' for base in node.bases 
                      if isinstance(base, ast.Name)):
                    definitions['models'].append(node.name)
            
            elif isinstance(node, ast.FunctionDef):
                definitions['functions'].append(node.name)
            
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                # Constants with type annotations
                if node.target.id.isupper():
                    definitions['constants'].append(node.target.id)
    
    except Exception:
        # If AST parsing fails, try regex
        try:
            content = file_path.read_text()
            definitions['classes'] = re.findall(r'class\s+(\w+)', content)
            definitions['functions'] = re.findall(r'def\s+(\w+)', content)
            definitions['constants'] = re.findall(r'^([A-Z_]+)\s*=', content, re.MULTILINE)
        except Exception:
            pass
    
    return definitions

def find_similar_names(name: str, existing_names: List[str], threshold: float = 0.8) -> List[str]:
    """Find similar names using string similarity."""
    similar = []
    for existing in existing_names:
        ratio = difflib.SequenceMatcher(None, name.lower(), existing.lower()).ratio()
        if ratio >= threshold:
            similar.append((existing, ratio))
    
    return [name for name, _ in sorted(similar, key=lambda x: x[1], reverse=True)]

def check_exists(name: str, component_type: str = 'any') -> Dict:
    """Check if a Python component already exists."""
    project_root = Path.cwd()
    python_files = find_python_files(project_root)
    
    results = {
        'exact_matches': [],
        'similar_names': [],
        'type': component_type,
        'search_name': name
    }
    
    all_definitions = {
        'classes': {},
        'functions': {},
        'constants': {},
        'models': {}
    }
    
    # Extract all definitions
    for py_file in python_files:
        defs = extract_definitions(py_file)
        for def_type, names in defs.items():
            for def_name in names:
                if def_name not in all_definitions[def_type]:
                    all_definitions[def_type][def_name] = []
                all_definitions[def_type][def_name].append(str(py_file.relative_to(project_root)))
    
    # Check for exact matches
    if component_type == 'any':
        search_types = ['classes', 'functions', 'models']
    else:
        # Convert singular to plural for the internal dictionary
        type_map = {
            'class': 'classes',
            'function': 'functions',
            'model': 'models',
            'constant': 'constants'
        }
        search_types = [type_map.get(component_type, component_type + 's')]
    
    for def_type in search_types:
        if name in all_definitions[def_type]:
            results['exact_matches'].append({
                'type': def_type.rstrip('es'),  # Remove plural
                'locations': all_definitions[def_type][name]
            })
    
    # Find similar names
    all_names = []
    for def_type in all_definitions:
        all_names.extend(all_definitions[def_type].keys())
    
    similar = find_similar_names(name, all_names)
    if similar:
        results['similar_names'] = similar[:5]  # Top 5 similar
    
    return results

def find_imports(component_name: str) -> List[Dict]:
    """Find where a component is imported."""
    imports = []
    project_root = Path.cwd()
    python_files = find_python_files(project_root)
    
    import_patterns = [
        rf'from\s+[\w\.]+\s+import\s+.*\b{component_name}\b',
        rf'import\s+[\w\.]+\.{component_name}\b',
        rf'from\s+[\w\.]+\s+import\s+\(\s*[^)]*\b{component_name}\b[^)]*\)',
    ]
    
    for py_file in python_files:
        try:
            content = py_file.read_text()
            for pattern in import_patterns:
                if re.search(pattern, content, re.MULTILINE):
                    # Find the actual import line
                    for i, line in enumerate(content.splitlines(), 1):
                        if component_name in line and ('import' in line or 'from' in line):
                            imports.append({
                                'file': str(py_file.relative_to(project_root)),
                                'line': i,
                                'statement': line.strip()
                            })
                            break
        except Exception:
            continue
    
    return imports

def format_alert_message(results: Dict, imports: List[Dict]) -> str:
    """Format the alert message for existing components."""
    name = results['search_name']
    
    if not results['exact_matches']:
        if results['similar_names']:
            msg = f"ℹ️ No exact match for '{name}', but found similar:\n\n"
            for similar in results['similar_names']:
                msg += f"  • {similar}\n"
            msg += "\nConsider using one of these instead."
            return msg
        return None
    
    # Exact match found
    match = results['exact_matches'][0]
    match_type = match['type']
    locations = match['locations']
    
    msg = f"⚠️ {match_type.title()} '{name}' Already Exists!\n\n"
    msg += f"📍 Found in {len(locations)} location(s):\n"
    
    for loc in locations[:3]:  # Show first 3
        msg += f"  • {loc}\n"
    
    if len(locations) > 3:
        msg += f"  • ... and {len(locations) - 3} more\n"
    
    # Show imports
    if imports:
        msg += f"\n📦 Imported in {len(imports)} places:\n"
        for imp in imports[:5]:
            msg += f"  • {imp['file']}:{imp['line']}\n"
            msg += f"    {imp['statement']}\n"
    
    # Get file info
    first_file = Path(locations[0])
    if first_file.exists():
        stat = first_file.stat()
        import datetime
        modified = datetime.datetime.fromtimestamp(stat.st_mtime)
        msg += f"\n📅 Last modified: {modified.strftime('%Y-%m-%d %H:%M')}\n"
    
    # Provide options
    msg += "\n🔧 Options:\n"
    msg += "1. Import and use existing component (recommended)\n"
    msg += "2. Extend existing component with new functionality\n"
    msg += "3. Create with different name\n"
    msg += "4. Override (requires confirmation)\n"
    
    # Show how to import
    if match_type in ['class', 'function', 'model']:
        module_path = locations[0].replace('.py', '').replace('/', '.')
        if module_path.startswith('src.'):
            msg += f"\n📝 To import:\n"
            msg += f"from {module_path} import {name}\n"
    
    return msg

def main():
    """Main hook logic."""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Only check on file creation or write operations
    if input_data['tool'] not in ['write_file', 'str_replace']:
        sys.exit(0)
        return
    
    file_path = input_data.get('path', '')
    
    # Only check Python files
    if not file_path.endswith('.py'):
        sys.exit(0)
        return
    
    content = input_data.get('content', '')
    
    # Extract what's being created
    creating = []
    
    # Check for class definitions
    class_matches = re.findall(r'class\s+(\w+)', content)
    for class_name in class_matches:
        creating.append(('class', class_name))
    
    # Check for function definitions
    func_matches = re.findall(r'def\s+(\w+)', content)
    for func_name in func_matches:
        if not func_name.startswith('_'):  # Skip private functions
            creating.append(('function', func_name))
    
    # Check for Pydantic models specifically
    if 'BaseModel' in content:
        model_matches = re.findall(r'class\s+(\w+).*\(.*BaseModel.*\)', content)
        for model_name in model_matches:
            creating.append(('model', model_name))
    
    # Check each component being created
    alerts = []
    for component_type, name in creating:
        results = check_exists(name, component_type)
        
        if results['exact_matches']:
            imports = find_imports(name)
            alert_msg = format_alert_message(results, imports)
            if alert_msg:
                alerts.append(alert_msg)
    
    if alerts:
        # Combine all alerts and print to stderr as warning
        full_message = "\n\n" + "="*50 + "\n\n".join(alerts)
        print(full_message, file=sys.stderr)
        sys.exit(2)  # Warn but continue
    else:
        sys.exit(0)  # Continue normally

if __name__ == "__main__":
    main()
