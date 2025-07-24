#!/usr/bin/env python3
"""
Python Import Updater Hook - Automatically update imports after refactoring
Updates import statements when modules are moved or renamed
"""

import json
import sys
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import difflib
from datetime import datetime

def find_python_files(root_path: Path) -> List[Path]:
    """Find all Python files in project."""
    python_files = []
    ignore_dirs = {'.venv', 'venv', '__pycache__', '.git', 'node_modules', 'build', 'dist'}
    
    for path in root_path.rglob('*.py'):
        if not any(ignored in path.parts for ignored in ignore_dirs):
            python_files.append(path)
    
    return python_files

def detect_module_changes(old_path: str, new_path: str) -> Dict[str, str]:
    """Detect if a module was moved or renamed."""
    changes = {
        'type': None,
        'old_module': None,
        'new_module': None
    }
    
    # Convert file paths to module paths
    old_module = old_path.replace('.py', '').replace('/', '.')
    new_module = new_path.replace('.py', '').replace('/', '.')
    
    if old_path != new_path:
        if Path(old_path).name != Path(new_path).name:
            changes['type'] = 'rename'
        else:
            changes['type'] = 'move'
        
        changes['old_module'] = old_module
        changes['new_module'] = new_module
    
    return changes

def find_imports_to_update(root_path: Path, old_module: str, new_module: str) -> List[Tuple[Path, List[str]]]:
    """Find all files that need import updates."""
    files_to_update = []
    python_files = find_python_files(root_path)
    
    # Different import patterns to check
    import_patterns = [
        # import module
        (rf'^\s*import\s+{re.escape(old_module)}\b', f'import {new_module}'),
        # from module import something
        (rf'^\s*from\s+{re.escape(old_module)}\s+import', f'from {new_module} import'),
        # from parent import module (for simple renames)
        (rf'^\s*from\s+([\w\.]+)\s+import\s+.*\b{re.escape(old_module.split(".")[-1])}\b',
         lambda m: m.group(0).replace(old_module.split(".")[-1], new_module.split(".")[-1]))
    ]
    
    for py_file in python_files:
        try:
            content = py_file.read_text()
            lines_to_update = []
            
            for line_num, line in enumerate(content.splitlines(), 1):
                for pattern, replacement in import_patterns:
                    if re.match(pattern, line):
                        if callable(replacement):
                            new_line = re.sub(pattern, replacement, line)
                        else:
                            new_line = re.sub(pattern, replacement, line)
                        
                        if new_line != line:
                            lines_to_update.append({
                                'line_num': line_num,
                                'old': line,
                                'new': new_line
                            })
            
            if lines_to_update:
                files_to_update.append((py_file, lines_to_update))
        
        except Exception:
            continue
    
    return files_to_update

def update_relative_imports(file_path: Path, old_path: str, new_path: str) -> List[Dict]:
    """Update relative imports if file was moved to different directory level."""
    updates = []
    
    old_depth = len(Path(old_path).parts) - 1
    new_depth = len(Path(new_path).parts) - 1
    
    if old_depth != new_depth:
        try:
            content = file_path.read_text()
            lines = content.splitlines()
            
            for line_num, line in enumerate(lines, 1):
                # Check for relative imports
                relative_import = re.match(r'^(\s*)from\s+(\.+)\s*import', line)
                if relative_import:
                    indent = relative_import.group(1)
                    dots = relative_import.group(2)
                    current_level = len(dots)
                    
                    # Adjust relative import level
                    if new_depth > old_depth:
                        new_level = current_level + (new_depth - old_depth)
                    else:
                        new_level = current_level - (old_depth - new_depth)
                    
                    if new_level > 0:
                        new_dots = '.' * new_level
                        new_line = re.sub(r'^(\s*)from\s+(\.+)', f'{indent}from {new_dots}', line)
                        
                        if new_line != line:
                            updates.append({
                                'line_num': line_num,
                                'old': line,
                                'new': new_line
                            })
        
        except Exception:
            pass
    
    return updates

def format_update_message(files_to_update: List[Tuple[Path, List[Dict]]]) -> str:
    """Format the update message for user notification."""
    if not files_to_update:
        return None
    
    msg = "🔄 Import Updates Needed\n\n"
    msg += f"Found {len(files_to_update)} file(s) with imports to update:\n\n"
    
    for file_path, updates in files_to_update[:5]:  # Show first 5 files
        msg += f"📄 {file_path.relative_to(Path.cwd())}\n"
        for update in updates[:3]:  # Show first 3 updates per file
            msg += f"  Line {update['line_num']}:\n"
            msg += f"    - {update['old']}\n"
            msg += f"    + {update['new']}\n"
        
        if len(updates) > 3:
            msg += f"  ... and {len(updates) - 3} more import(s)\n"
        msg += "\n"
    
    if len(files_to_update) > 5:
        msg += f"... and {len(files_to_update) - 5} more file(s)\n\n"
    
    msg += "Options:\n"
    msg += "1. Run: /pydeps update <module> - Auto-update all imports\n"
    msg += "2. Review and update manually\n"
    msg += "3. Continue without updating (may break imports)"
    
    return msg

def save_update_plan(module_changes: Dict, files_to_update: List) -> str:
    """Save the update plan for later execution."""
    update_dir = Path('.claude/python-deps/updates')
    update_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    plan_file = update_dir / f"update_plan_{timestamp}.json"
    
    plan = {
        'timestamp': timestamp,
        'module_changes': module_changes,
        'files_to_update': [
            {
                'file': str(file_path),
                'updates': updates
            }
            for file_path, updates in files_to_update
        ]
    }
    
    try:
        with open(plan_file, 'w') as f:
            json.dump(plan, f, indent=2)
        return str(plan_file)
    except Exception:
        return None

def main():
    """Main hook logic."""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Only check on file operations that might move/rename
    if input_data['tool'] not in ['move_file', 'rename_file']:
        sys.exit(0)
        return
    
    # Get file paths
    old_path = input_data.get('source', input_data.get('old_path', ''))
    new_path = input_data.get('destination', input_data.get('new_path', ''))
    
    # Only check Python files
    if not (old_path.endswith('.py') and new_path.endswith('.py')):
        sys.exit(0)
        return
    
    # Detect module changes
    changes = detect_module_changes(old_path, new_path)
    
    if changes['type']:
        # Find files that need updates
        root_path = Path.cwd()
        files_to_update = find_imports_to_update(
            root_path, 
            changes['old_module'], 
            changes['new_module']
        )
        
        # Also check for relative import updates if file was moved
        if changes['type'] == 'move' and Path(new_path).exists():
            relative_updates = update_relative_imports(Path(new_path), old_path, new_path)
            if relative_updates:
                files_to_update.append((Path(new_path), relative_updates))
        
        # Format and show message
        if files_to_update:
            # Save update plan
            plan_file = save_update_plan(changes, files_to_update)
            
            message = format_update_message(files_to_update)
            
            response = {
                "decision": "notify",
                "message": message,
                "metadata": {
                    "update_plan": plan_file,
                    "files_affected": len(files_to_update),
                    "module_change_type": changes['type']
                }
            }
            
            print(json.dumps(response))
        else:
            sys.exit(0)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
