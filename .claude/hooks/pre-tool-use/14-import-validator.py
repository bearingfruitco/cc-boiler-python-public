#!/usr/bin/env python3
"""
Import Validator Hook - Fixes common import path mistakes
Ensures consistent import patterns across the codebase
"""

import json
import sys
import re
from pathlib import Path

def get_project_root():
    """Find the project root (where package.json is)"""
    current = Path.cwd()
    while current != current.parent:
        if (current / 'package.json').exists():
            return current
        current = current.parent
    return Path.cwd()

def get_relative_depth(file_path):
    """Get how many directories deep the file is"""
    return len(Path(file_path).parts) - 1

def validate_imports(content, file_path):
    """Validate and fix import statements"""
    issues = []
    project_root = get_project_root()
    
    # Find all import statements
    import_pattern = r'^(import\s+(?:{[^}]+}|[\w\s,]+)\s+from\s+[\'"])([^\'"]+)([\'"];?)$'
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        match = re.match(import_pattern, line.strip())
        if match:
            import_prefix = match.group(1)
            import_path = match.group(2)
            import_suffix = match.group(3)
            
            # Check for common issues
            issue = check_import_issue(import_path, file_path, project_root)
            if issue:
                issues.append({
                    'line': i + 1,
                    'original': line,
                    'path': import_path,
                    'issue': issue['message'],
                    'fixed_path': issue['fixed'],
                    'fixed_line': f"{import_prefix}{issue['fixed']}{import_suffix}"
                })
    
    return issues

def check_import_issue(import_path, file_path, project_root):
    """Check for specific import issues"""
    
    # Issue 1: Using relative paths instead of @ alias
    if import_path.startswith('../'):
        # Count how many levels up
        levels_up = import_path.count('../')
        current_depth = get_relative_depth(file_path)
        
        # If going up to or past root, should use @ alias
        if levels_up >= current_depth - 1:
            # Extract the final path after all ../
            final_path = re.sub(r'^(\.\./)+', '', import_path)
            
            # Common mappings
            if final_path.startswith('components/'):
                return {
                    'message': 'Use @ alias instead of relative imports for root-level directories',
                    'fixed': f"@/{final_path}"
                }
            elif final_path.startswith('lib/'):
                return {
                    'message': 'Use @ alias for lib imports',
                    'fixed': f"@/{final_path}"
                }
            elif final_path.startswith('hooks/'):
                return {
                    'message': 'Use @ alias for hooks imports',
                    'fixed': f"@/{final_path}"
                }
            elif final_path.startswith('types/'):
                return {
                    'message': 'Use @ alias for types imports',
                    'fixed': f"@/{final_path}"
                }
    
    # Issue 2: Missing file extensions for relative imports
    if import_path.startswith('./') and not any(import_path.endswith(ext) for ext in ['.css', '.json', '.svg']):
        # Check if it's likely a TS/JS file without extension
        if not '.' in import_path.split('/')[-1]:
            return {
                'message': 'Relative imports should include file extension',
                'fixed': import_path  # Keep as is, just warn
            }
    
    # Issue 3: Incorrect @ alias usage
    if import_path.startswith('@/'):
        # Check if path exists
        resolved_path = project_root / import_path[2:]
        
        # Check with common extensions
        exists = False
        for ext in ['', '.ts', '.tsx', '.js', '.jsx', '/index.ts', '/index.tsx']:
            if (resolved_path.parent / f"{resolved_path.name}{ext}").exists():
                exists = True
                break
        
        if not exists:
            # Check if it's a mistyped path
            path_parts = import_path[2:].split('/')
            if path_parts[0] == 'component':  # Common typo
                fixed_path = '@/components/' + '/'.join(path_parts[1:])
                return {
                    'message': 'Typo in import path: "component" should be "components"',
                    'fixed': fixed_path
                }
            elif path_parts[0] == 'lib' and len(path_parts) > 1:
                # Check if it should be libs or lib
                if (project_root / 'libs' / path_parts[1]).exists():
                    fixed_path = '@/libs/' + '/'.join(path_parts[1:])
                    return {
                        'message': 'Use "libs" not "lib" for this import',
                        'fixed': fixed_path
                    }
    
    # Issue 4: Importing from node_modules with relative path
    if 'node_modules' in import_path:
        # Extract package name
        package_match = re.search(r'node_modules/([^/]+)', import_path)
        if package_match:
            package_name = package_match.group(1)
            return {
                'message': 'Import packages directly, not through node_modules',
                'fixed': package_name
            }
    
    # Issue 5: Wrong casing
    if import_path.startswith('@/'):
        path_parts = import_path[2:].split('/')
        
        # Check component casing
        if path_parts[0] == 'components' and len(path_parts) > 2:
            # Components should be PascalCase
            component_name = path_parts[-1].replace('.tsx', '').replace('.jsx', '')
            if component_name and component_name[0].islower():
                path_parts[-1] = component_name[0].upper() + component_name[1:]
                if import_path.endswith('.tsx'):
                    path_parts[-1] += '.tsx'
                elif import_path.endswith('.jsx'):
                    path_parts[-1] += '.jsx'
                
                fixed_path = '@/' + '/'.join(path_parts)
                return {
                    'message': 'Component names should be PascalCase',
                    'fixed': fixed_path
                }
    
    return None

def main():
    """Main hook logic"""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Only check file writes with imports
    tool_use = input_data.get('tool_use', {})
    if tool_use.get('name') not in ['str_replace_editor', 'create_file', 'edit_file']:
        print(json.dumps({"action": "continue"}))
        return
    
    file_path = tool_use.get('path', '')
    content = tool_use.get('new_str', tool_use.get('content', ''))
    
    # Only check TS/JS files
    if not any(file_path.endswith(ext) for ext in ['.ts', '.tsx', '.js', '.jsx']):
        print(json.dumps({"action": "continue"}))
        return
    
    # Skip if no imports
    if 'import ' not in content:
        print(json.dumps({"action": "continue"}))
        return
    
    # Validate imports
    issues = validate_imports(content, file_path)
    
    if issues:
        # Format message
        error_msg = "🔧 Import Path Issues Detected\n\n"
        error_msg += f"Found {len(issues)} import issue(s) in {file_path}:\n\n"
        
        for issue in issues:
            error_msg += f"Line {issue['line']}: {issue['path']}\n"
            error_msg += f"  ❌ {issue['issue']}\n"
            error_msg += f"  ✅ Use: {issue['fixed_path']}\n\n"
        
        error_msg += "Import conventions:\n"
        error_msg += "- Use @/ alias for imports from project root\n"
        error_msg += "- Use relative imports only for same-directory files\n"
        error_msg += "- Component names should be PascalCase\n"
        error_msg += "- Don't import through node_modules path"
        
        # For now, warn instead of block
        print(json.dumps({
            "action": "warn",
            "message": error_msg,
            "continue": True
        }))
    else:
        print(json.dumps({"action": "continue"}))

if __name__ == "__main__":
    main()
