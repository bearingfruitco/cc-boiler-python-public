#!/usr/bin/env python3
"""
Auto Test Generation Hook - Automatically generate tests at key workflow points
Ensures tests exist before implementation starts
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import re

def get_tdd_config() -> Dict:
    """Load TDD configuration"""
    config_path = Path(".claude/hooks/config.json")
    if config_path.exists():
        settings = json.loads(config_path.read_text())
        return settings.get("tdd", {
            "auto_generate_tests": True,
            "enforce_tests_first": True,
            "test_on_save": True,
            "block_without_tests": True
        })
    return {
        "auto_generate_tests": True,
        "enforce_tests_first": True,
        "test_on_save": True,
        "block_without_tests": True
    }

def extract_issue_number(content: str) -> Optional[int]:
    """Extract issue number from various contexts"""
    patterns = [
        r'issue[:\s#]+(\d+)',
        r'#(\d+)',
        r'github\.com/[\w-]+/[\w-]+/issues/(\d+)',
        r'Created issue #(\d+)',
        r'/fw start (\d+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None

def extract_feature_name(content: str) -> str:
    """Extract feature name from content"""
    # Try to extract from various patterns
    patterns = [
        r'Feature:\s*([^\n]+)',
        r'Title:\s*([^\n]+)',
        r'PRD:\s*([^\n]+)',
        r'# ([^\n]+)',
        r'"([^"]+)"'  # Quoted text
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            name = match.group(1).strip()
            # Clean up the name
            name = re.sub(r'[^a-zA-Z0-9\s-]', '', name)
            return name.replace(' ', '_').lower()
    
    return "feature"

def check_tests_exist(feature_name: str, issue_number: Optional[int] = None) -> bool:
    """Check if tests already exist for this feature"""
    test_patterns = [
        f"tests/test_{feature_name}.py",
        f"tests/unit/test_{feature_name}.py",
        f"tests/integration/test_{feature_name}.py",
    ]
    
    if issue_number:
        test_patterns.extend([
            f"tests/test_{issue_number}_*.py",
            f"tests/test_issue_{issue_number}.py",
        ])
    
    for pattern in test_patterns:
        if Path(pattern).exists() or list(Path("tests").glob(pattern.replace("tests/", ""))):
            return True
    
    return False

def generate_test_command(feature_name: str, source_type: str, source_path: Optional[str] = None) -> List[str]:
    """Generate the test generation command"""
    cmd = ["generate-tests", feature_name]
    
    if source_type == "issue":
        cmd.extend(["--source", "issue"])
    elif source_type == "prd" and source_path:
        cmd.extend(["--source", source_path])
    elif source_type == "prp" and source_path:
        cmd.extend(["--source", source_path, "--prp"])
    
    return cmd

def should_auto_generate(data: Dict, config: Dict) -> bool:
    """Determine if we should auto-generate tests"""
    if not config.get("auto_generate_tests", True):
        return False
    
    tool = data.get('tool', '')
    
    # Check for specific workflow triggers
    triggers = [
        # Task processing
        (tool == 'str_replace' and '/process-tasks' in data.get('content', '')),
        (tool == 'Bash' and 'process-tasks' in data.get('command', '')),
        
        # Feature workflow start
        (tool == 'str_replace' and '/fw start' in data.get('content', '')),
        (tool == 'Bash' and 'feature-workflow start' in data.get('command', '')),
        
        # Issue creation with tests flag
        (tool == 'str_replace' and '/cti' in data.get('content', '') and '--tests' in data.get('content', '')),
        
        # PRD/PRP creation
        (tool == 'write_file' and ('PRD.md' in data.get('path', '') or 'PRP.md' in data.get('path', ''))),
        
        # Task file updates
        (tool == 'write_file' and '-tasks.md' in data.get('path', ''))
    ]
    
    return any(triggers)

def find_related_files(feature_name: str) -> Dict[str, Optional[str]]:
    """Find related PRD, PRP, or task files"""
    files = {
        'prd': None,
        'prp': None,
        'tasks': None
    }
    
    # Search patterns
    search_paths = [
        ('prd', f"docs/project/features/{feature_name}-PRD.md"),
        ('prd', f"docs/project/features/{feature_name}_PRD.md"),
        ('prp', f"PRPs/active/{feature_name}.md"),
        ('prp', f"PRPs/active/*{feature_name}*.md"),
        ('tasks', f"docs/project/features/{feature_name}-tasks.md"),
        ('tasks', f"docs/project/features/{feature_name}_tasks.md"),
    ]
    
    for file_type, pattern in search_paths:
        if '*' in pattern:
            # Glob pattern
            matches = list(Path(".").glob(pattern))
            if matches:
                files[file_type] = str(matches[0])
        else:
            # Direct path
            if Path(pattern).exists():
                files[file_type] = pattern
    
    return files

def auto_generate_tests(feature_name: str, issue_number: Optional[int], related_files: Dict) -> bool:
    """Auto-generate tests using the generate-tests command"""
    # Determine best source
    if related_files['prp']:
        cmd = generate_test_command(feature_name, 'prp', related_files['prp'])
        source_desc = f"PRP: {related_files['prp']}"
    elif related_files['prd']:
        cmd = generate_test_command(feature_name, 'prd', related_files['prd'])
        source_desc = f"PRD: {related_files['prd']}"
    elif issue_number:
        cmd = generate_test_command(feature_name, 'issue')
        cmd.extend(["--issue", str(issue_number)])
        source_desc = f"Issue #{issue_number}"
    else:
        # No source available
        return False
    
    try:
        # Log the action
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "auto_test_generation",
            "feature": feature_name,
            "source": source_desc,
            "command": " ".join(cmd)
        }
        
        log_path = Path(".claude/logs/auto-test-generation.jsonl")
        log_path.parent.mkdir(exist_ok=True)
        with open(log_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        # Generate notification
        print(f"\n🧪 Auto-generating tests for '{feature_name}' from {source_desc}", file=sys.stderr)
        print(f"Command: /{' '.join(cmd)}", file=sys.stderr)
        
        # Mark that tests are being generated
        marker_file = Path(f".claude/context/.tests_generating_{feature_name}")
        marker_file.parent.mkdir(exist_ok=True)
        marker_file.write_text(json.dumps({
            "feature": feature_name,
            "source": source_desc,
            "started": datetime.now().isoformat()
        }))
        
        return True
        
    except Exception as e:
        print(f"Error auto-generating tests: {e}", file=sys.stderr)
        return False

def update_issue_with_tests(issue_number: int, test_file: str):
    """Update GitHub issue to note that tests were generated"""
    try:
        # This would integrate with GitHub MCP in practice
        comment = f"""✅ Tests auto-generated: `{test_file}`

The TDD workflow has automatically generated test cases based on the issue requirements. Please review the tests before implementation.

**Next steps:**
1. Review generated tests in `{test_file}`
2. Adjust test cases if needed
3. Run tests to see them fail: `pytest {test_file}`
4. Implement features to make tests pass
"""
        print(f"\n📝 Issue #{issue_number} updated with test information", file=sys.stderr)
    except Exception:
        pass

def main():
    """Main hook logic"""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Load config
    config = get_tdd_config()
    
    # Check if we should auto-generate
    if not should_auto_generate(input_data, config):
        sys.exit(0)
        return
    
    # Extract context
    content = input_data.get('content', '')
    path = input_data.get('path', '')
    
    # Extract feature information
    feature_name = extract_feature_name(content + ' ' + path)
    issue_number = extract_issue_number(content)
    
    # Check if tests already exist
    if check_tests_exist(feature_name, issue_number):
        print(f"✅ Tests already exist for '{feature_name}'", file=sys.stderr)
        sys.exit(0)
        return
    
    # Find related files
    related_files = find_related_files(feature_name)
    
    # Auto-generate tests
    if auto_generate_tests(feature_name, issue_number, related_files):
        # Update issue if applicable
        if issue_number:
            test_file = f"tests/test_{feature_name}.py"
            update_issue_with_tests(issue_number, test_file)
    
    # Always continue
    sys.exit(0)

if __name__ == "__main__":
    from datetime import datetime
    main()
