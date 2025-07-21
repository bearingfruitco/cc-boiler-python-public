#!/usr/bin/env python3
"""
Test Generation Enforcer - Ensures tests exist before code implementation
Part of TDD workflow enforcement
"""

import json
import sys
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def find_test_file(source_file: Path) -> Optional[Path]:
    """Find corresponding test file for a source file."""
    # Common test file patterns
    test_patterns = [
        ('src/', 'tests/unit/test_'),
        ('src/models/', 'tests/unit/test_'),
        ('src/services/', 'tests/unit/test_'),
        ('src/api/', 'tests/integration/test_'),
        ('src/agents/', 'tests/unit/test_'),
        ('src/pipelines/', 'tests/integration/test_')
    ]
    
    source_str = str(source_file)
    
    for src_pattern, test_prefix in test_patterns:
        if src_pattern in source_str:
            # Extract relative path after src pattern
            relative = source_str.split(src_pattern)[1]
            # Remove .py and add test prefix
            test_name = relative.replace('.py', '')
            test_path = Path(f"{test_prefix}{test_name}.py")
            
            if test_path.exists():
                return test_path
    
    # Fallback: look for any test file with similar name
    stem = source_file.stem
    for test_dir in ['tests/unit', 'tests/integration', 'tests/e2e']:
        test_path = Path(test_dir) / f"test_{stem}.py"
        if test_path.exists():
            return test_path
    
    return None

def extract_testable_components(content: str) -> Dict[str, List[str]]:
    """Extract functions, classes, and endpoints that need tests."""
    components = {
        'classes': [],
        'functions': [],
        'async_functions': [],
        'endpoints': []
    }
    
    # Extract classes
    class_pattern = r'class\s+(\w+)'
    for match in re.finditer(class_pattern, content):
        components['classes'].append(match.group(1))
    
    # Extract functions
    func_pattern = r'def\s+(\w+)\s*\('
    async_func_pattern = r'async\s+def\s+(\w+)\s*\('
    
    for match in re.finditer(func_pattern, content):
        func_name = match.group(1)
        if not func_name.startswith('_'):  # Skip private functions
            components['functions'].append(func_name)
    
    for match in re.finditer(async_func_pattern, content):
        func_name = match.group(1)
        if not func_name.startswith('_'):
            components['async_functions'].append(func_name)
    
    # Extract API endpoints
    endpoint_pattern = r'@(?:app|router)\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)'
    for match in re.finditer(endpoint_pattern, content):
        method = match.group(1).upper()
        path = match.group(2)
        components['endpoints'].append(f"{method} {path}")
    
    return components

def check_test_coverage(test_file: Path, components: Dict[str, List[str]]) -> Tuple[bool, List[str]]:
    """Check if test file covers all components."""
    if not test_file.exists():
        return False, ["Test file does not exist"]
    
    with open(test_file, 'r') as f:
        test_content = f.read()
    
    missing = []
    
    # Check for test coverage of each component
    for class_name in components['classes']:
        if f"Test{class_name}" not in test_content and f"test_{class_name.lower()}" not in test_content:
            missing.append(f"No tests for class '{class_name}'")
    
    for func_name in components['functions']:
        if f"test_{func_name}" not in test_content:
            missing.append(f"No tests for function '{func_name}'")
    
    for async_func in components['async_functions']:
        if f"test_{async_func}" not in test_content and "async def test" not in test_content:
            missing.append(f"No tests for async function '{async_func}'")
    
    for endpoint in components['endpoints']:
        method, path = endpoint.split(' ')
        if path not in test_content or method.lower() not in test_content.lower():
            missing.append(f"No tests for endpoint '{endpoint}'")
    
    return len(missing) == 0, missing

def find_related_issue_or_task() -> Optional[str]:
    """Find current issue or task being worked on."""
    # Check workflow state
    workflow_state_file = Path('.claude/context/workflow_state.json')
    if workflow_state_file.exists():
        try:
            with open(workflow_state_file, 'r') as f:
                state = json.load(f)
                return state.get('current_task') or state.get('current_issue')
        except:
            pass
    
    # Check git branch name
    try:
        import subprocess
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            branch = result.stdout.strip()
            # Extract issue number from branch name
            match = re.search(r'(?:issue|feature|task)[/-](\d+)', branch)
            if match:
                return f"Issue #{match.group(1)}"
    except:
        pass
    
    return None

def check_test_manifest(feature: str) -> Optional[Dict]:
    """Check if test manifest exists for feature."""
    manifest_path = Path(f'tests/{feature}_manifest.json')
    if manifest_path.exists():
        try:
            with open(manifest_path, 'r') as f:
                return json.load(f)
        except:
            pass
    return None

def format_alert_message(source_file: Path, test_file: Optional[Path], 
                        components: Dict, missing: List[str]) -> str:
    """Format alert message for missing tests."""
    msg = "⚠️ TDD Violation: Tests Required Before Implementation!\n\n"
    
    msg += f"📄 Creating: {source_file}\n"
    
    if not test_file:
        msg += "❌ No test file found!\n\n"
        msg += "🔧 Required Actions:\n"
        msg += f"1. Run: /generate-tests {source_file.stem}\n"
        msg += "2. Create test file first\n"
        msg += "3. Then implement code\n"
    else:
        msg += f"🧪 Test file: {test_file}\n"
        msg += f"⚠️ Missing coverage:\n"
        for issue in missing[:5]:  # Show first 5
            msg += f"  • {issue}\n"
        if len(missing) > 5:
            msg += f"  • ... and {len(missing) - 5} more\n"
    
    # Add context
    task = find_related_issue_or_task()
    if task:
        msg += f"\n📋 Working on: {task}\n"
    
    # Component summary
    total_components = (len(components['classes']) + len(components['functions']) + 
                       len(components['async_functions']) + len(components['endpoints']))
    if total_components > 0:
        msg += f"\n📊 Components to test:\n"
        if components['classes']:
            msg += f"  • {len(components['classes'])} classes\n"
        if components['functions']:
            msg += f"  • {len(components['functions'])} functions\n"
        if components['async_functions']:
            msg += f"  • {len(components['async_functions'])} async functions\n"
        if components['endpoints']:
            msg += f"  • {len(components['endpoints'])} endpoints\n"
    
    msg += "\n💡 TDD Workflow:\n"
    msg += "1. Write tests first (Red)\n"
    msg += "2. Implement minimal code (Green)\n"
    msg += "3. Refactor with confidence (Refactor)\n"
    
    return msg

def should_enforce_tdd(file_path: str, content: str) -> bool:
    """Determine if TDD should be enforced for this file."""
    # Skip test files themselves
    if 'test_' in file_path or '/tests/' in file_path:
        return False
    
    # Skip migrations, configs, etc.
    skip_patterns = [
        'migrations/', '__pycache__/', '.pyc',
        'setup.py', 'config.py', '__init__.py',
        'requirements.txt', '.env'
    ]
    
    for pattern in skip_patterns:
        if pattern in file_path:
            return False
    
    # Skip files with no testable components
    components = extract_testable_components(content)
    total = sum(len(v) for v in components.values())
    
    return total > 0

def get_tdd_config() -> Dict:
    """Get TDD configuration."""
    config_path = Path('.claude/hooks/config.json')
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return config.get('tdd', {
                    'enforce': True,
                    'coverage_threshold': 80,
                    'allow_override': False
                })
        except:
            pass
    
    return {'enforce': True, 'coverage_threshold': 80, 'allow_override': False}

def main():
    """Main hook logic."""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Only check on file creation or modification
    if input_data['tool'] not in ['write_file', 'str_replace']:
        sys.exit(0)
        return
    
    file_path = input_data.get('path', '')
    
    # Only check Python files
    if not file_path.endswith('.py'):
        sys.exit(0)
        return
    
    content = input_data.get('content', '')
    
    # Check if TDD should be enforced
    if not should_enforce_tdd(file_path, content):
        sys.exit(0)
        return
    
    # Get TDD config
    config = get_tdd_config()
    if not config.get('enforce', True):
        sys.exit(0)
        return
    
    # Extract components that need testing
    components = extract_testable_components(content)
    if not any(components.values()):
        sys.exit(0)
        return
    
    # Find corresponding test file
    source_file = Path(file_path)
    test_file = find_test_file(source_file)
    
    # Check test coverage
    if test_file and test_file.exists():
        covered, missing = check_test_coverage(test_file, components)
        if covered:
            sys.exit(0)
            return
    else:
        missing = ["Test file not found"]
    
    # Check for test manifest
    feature = source_file.stem
    manifest = check_test_manifest(feature)
    
    # Format alert
    alert_msg = format_alert_message(source_file, test_file, components, missing)
    
    # Check if we should block
    if config.get('allow_override', False):
        # Warn but allow - exit code 2
        print(alert_msg, file=sys.stderr)
        sys.exit(2)
    else:
        # Block the operation - exit code 1
        print(alert_msg, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()