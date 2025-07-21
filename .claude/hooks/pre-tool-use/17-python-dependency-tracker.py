#!/usr/bin/env python3
"""
Python Dependency Tracker Hook - Track and alert on Python module dependencies
Monitors imports and warns about breaking changes
"""

import json
import sys
import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import subprocess

def get_project_root() -> Path:
    """Get project root directory."""
    return Path.cwd()

def find_python_files(root_path: Path) -> List[Path]:
    """Find all Python files in project."""
    python_files = []
    ignore_dirs = {'.venv', 'venv', '__pycache__', '.git', 'node_modules', 'build', 'dist'}
    
    for path in root_path.rglob('*.py'):
        if not any(ignored in path.parts for ignored in ignore_dirs):
            python_files.append(path)
    
    return python_files

def extract_imports(file_path: Path) -> Dict[str, List[str]]:
    """Extract all imports from a Python file."""
    imports = {
        'imports': [],          # import x
        'from_imports': [],     # from x import y
        'local_imports': [],    # from . import x
        'type_imports': []      # TYPE_CHECKING imports
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports['imports'].append(alias.name)
            
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                level = node.level
                
                if level > 0:  # Relative import
                    imports['local_imports'].append({
                        'module': module,
                        'names': [alias.name for alias in node.names],
                        'level': level
                    })
                else:
                    for alias in node.names:
                        imports['from_imports'].append(f"{module}.{alias.name}")
        
        # Check for TYPE_CHECKING imports
        content = file_path.read_text()
        type_checking_match = re.search(
            r'if\s+TYPE_CHECKING:.*?(?=\n(?:\S|$))', 
            content, 
            re.DOTALL | re.MULTILINE
        )
        if type_checking_match:
            type_section = type_checking_match.group()
            type_imports_found = re.findall(r'from\s+([\w\.]+)\s+import\s+([\w,\s]+)', type_section)
            for module, names in type_imports_found:
                for name in names.split(','):
                    imports['type_imports'].append(f"{module}.{name.strip()}")
    
    except Exception:
        # Fallback to regex if AST fails
        try:
            content = file_path.read_text()
            import_lines = re.findall(r'^(?:from\s+[\w\.]+\s+)?import\s+.*$', content, re.MULTILINE)
            for line in import_lines:
                imports['imports'].append(line)
        except Exception:
            pass
    
    return imports

def extract_exports(file_path: Path) -> Dict[str, List[str]]:
    """Extract what a module exports (classes, functions, etc.)."""
    exports = {
        'classes': [],
        'functions': [],
        'variables': [],
        'type_aliases': []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                exports['classes'].append(node.name)
            
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                if not node.name.startswith('_'):  # Skip private functions
                    exports['functions'].append(node.name)
            
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and not target.id.startswith('_'):
                        exports['variables'].append(target.id)
            
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                if not node.target.id.startswith('_'):
                    exports['variables'].append(node.target.id)
    
    except Exception:
        pass
    
    return exports

def build_dependency_graph(root_path: Path) -> Dict[str, Dict]:
    """Build a complete dependency graph of the project."""
    graph = {}
    python_files = find_python_files(root_path)
    
    # First pass: collect all exports
    all_exports = {}
    for py_file in python_files:
        module_path = str(py_file.relative_to(root_path)).replace('.py', '').replace('/', '.')
        exports = extract_exports(py_file)
        all_exports[module_path] = exports
    
    # Second pass: build import relationships
    for py_file in python_files:
        module_path = str(py_file.relative_to(root_path)).replace('.py', '').replace('/', '.')
        imports = extract_imports(py_file)
        
        # Track who imports this module
        imported_by = []
        module_name = py_file.stem
        
        for other_file in python_files:
            if other_file == py_file:
                continue
            
            other_content = other_file.read_text()
            if module_name in other_content and ('import' in other_content or 'from' in other_content):
                other_module = str(other_file.relative_to(root_path)).replace('.py', '').replace('/', '.')
                imported_by.append(other_module)
        
        graph[module_path] = {
            'file': str(py_file.relative_to(root_path)),
            'imports': imports,
            'exports': all_exports.get(module_path, {}),
            'imported_by': imported_by
        }
    
    return graph

def detect_breaking_changes(old_content: str, new_content: str) -> Dict[str, List[str]]:
    """Detect breaking changes between old and new content."""
    changes = {
        'removed_exports': [],
        'signature_changes': [],
        'type_changes': []
    }
    
    try:
        old_tree = ast.parse(old_content)
        new_tree = ast.parse(new_content)
        
        # Extract old definitions
        old_defs = {}
        for node in ast.walk(old_tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                old_defs[node.name] = node
        
        # Extract new definitions
        new_defs = {}
        for node in ast.walk(new_tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                new_defs[node.name] = node
        
        # Find removed exports
        for name in old_defs:
            if name not in new_defs:
                changes['removed_exports'].append(name)
        
        # Find signature changes
        for name, old_node in old_defs.items():
            if name in new_defs:
                new_node = new_defs[name]
                if isinstance(old_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    old_args = len(old_node.args.args)
                    new_args = len(new_node.args.args)
                    if old_args != new_args:
                        changes['signature_changes'].append(f"{name}: {old_args} args → {new_args} args")
    
    except Exception:
        pass
    
    return changes

def check_module_dependencies(module_path: str, graph: Dict) -> Dict:
    """Check dependencies for a specific module."""
    if module_path not in graph:
        # Try to find by file path
        for mod, info in graph.items():
            if info['file'] == module_path or mod.endswith(module_path):
                module_path = mod
                break
    
    if module_path not in graph:
        return {'error': 'Module not found'}
    
    module_info = graph[module_path]
    imported_by = module_info.get('imported_by', [])
    
    return {
        'module': module_path,
        'imported_by': imported_by,
        'import_count': len(imported_by),
        'exports': module_info.get('exports', {}),
        'risk_level': 'high' if len(imported_by) > 5 else 'medium' if len(imported_by) > 2 else 'low'
    }

def format_dependency_alert(deps: Dict, changes: Dict) -> str:
    """Format a dependency alert message."""
    if deps.get('error'):
        return None
    
    if deps['import_count'] == 0:
        return None
    
    msg = f"📦 Dependency Alert: {deps['module']}\n\n"
    msg += f"This module is imported by {deps['import_count']} other modules:\n"
    
    for imp in deps['imported_by'][:5]:
        msg += f"  • {imp}\n"
    
    if len(deps['imported_by']) > 5:
        msg += f"  • ... and {len(deps['imported_by']) - 5} more\n"
    
    if changes and any(changes.values()):
        msg += "\n⚠️ Breaking Changes Detected:\n"
        
        if changes['removed_exports']:
            msg += "  Removed exports:\n"
            for exp in changes['removed_exports']:
                msg += f"    • {exp}\n"
        
        if changes['signature_changes']:
            msg += "  Signature changes:\n"
            for change in changes['signature_changes']:
                msg += f"    • {change}\n"
        
        msg += "\nSuggested Actions:\n"
        msg += "  • /pydeps check " + deps['module'] + " - Full dependency analysis\n"
        msg += "  • /pydeps update " + deps['module'] + " - Update all imports\n"
        msg += "  • Review changes carefully\n"
    
    return msg

def load_dependency_cache() -> Dict:
    """Load cached dependency graph."""
    cache_file = Path('.claude/python-deps/import_graph.json')
    if cache_file.exists():
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_dependency_cache(graph: Dict):
    """Save dependency graph to cache."""
    cache_dir = Path('.claude/python-deps')
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    cache_file = cache_dir / 'import_graph.json'
    try:
        with open(cache_file, 'w') as f:
            json.dump(graph, f, indent=2)
    except Exception:
        pass

def main():
    """Main hook logic."""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Only check on file modifications
    if input_data['tool'] not in ['write_file', 'str_replace', 'edit_file']:
        sys.exit(0)
        return
    
    file_path = input_data.get('path', '')
    
    # Only check Python files
    if not file_path.endswith('.py'):
        sys.exit(0)
        return
    
    # Load or build dependency graph
    graph = load_dependency_cache()
    if not graph:
        root = get_project_root()
        graph = build_dependency_graph(root)
        save_dependency_cache(graph)
    
    # Check dependencies for this file
    module_path = file_path.replace('.py', '').replace('/', '.')
    deps = check_module_dependencies(module_path, graph)
    
    # Check for breaking changes if we have old content
    changes = {}
    if 'old_content' in input_data and 'content' in input_data:
        changes = detect_breaking_changes(
            input_data['old_content'], 
            input_data['content']
        )
    
    # Format alert if needed
    alert = format_dependency_alert(deps, changes)
    
    if alert and deps['import_count'] >= 3:  # Only alert if 3+ modules depend on this
        sys.exit(0)  # Continue normally
        }
        print(json.dumps(response))
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
