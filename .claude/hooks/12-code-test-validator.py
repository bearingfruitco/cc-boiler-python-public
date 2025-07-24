#!/usr/bin/env python3
"""
Code-Test Validator - Ensures code passes pre-written tests
Runs after code generation, validates implementation against tests
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def find_test_files(source_file: Path) -> List[Path]:
    """Find all test files related to source file."""
    test_files = []
    stem = source_file.stem
    
    # Look in standard test directories
    test_dirs = ['tests/unit', 'tests/integration', 'tests/e2e']
    
    for test_dir in test_dirs:
        test_path = Path(test_dir)
        if test_path.exists():
            # Direct match
            direct = test_path / f"test_{stem}.py"
            if direct.exists():
                test_files.append(direct)
            
            # Pattern match (e.g., test_user_*.py for user.py)
            for test_file in test_path.glob(f"test_{stem}_*.py"):
                test_files.append(test_file)
    
    return test_files

def run_specific_tests(test_files: List[Path]) -> Tuple[bool, Dict]:
    """Run specific test files and return results."""
    if not test_files:
        return True, {"message": "No tests found", "passed": 0, "failed": 0}
    
    # Construct pytest command
    cmd = ['pytest', '-v', '--tb=short', '--no-header']
    cmd.extend(str(tf) for tf in test_files)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Parse pytest output
        output = result.stdout + result.stderr
        
        # Look for test results
        passed = failed = 0
        failed_tests = []
        
        for line in output.split('\n'):
            if ' PASSED' in line:
                passed += 1
            elif ' FAILED' in line:
                failed += 1
                # Extract test name
                test_name = line.split('::')[1].split(' ')[0] if '::' in line else line
                failed_tests.append(test_name)
        
        # Look for coverage if available
        coverage = None
        if '--cov' in output:
            for line in output.split('\n'):
                if 'TOTAL' in line and '%' in line:
                    parts = line.split()
                    for part in parts:
                        if part.endswith('%'):
                            coverage = int(part.rstrip('%'))
                            break
        
        return result.returncode == 0, {
            "passed": passed,
            "failed": failed,
            "failed_tests": failed_tests,
            "coverage": coverage,
            "output": output if failed > 0 else None
        }
        
    except subprocess.TimeoutExpired:
        return False, {
            "message": "Tests timed out after 30 seconds",
            "passed": 0,
            "failed": 0
        }
    except Exception as e:
        return False, {
            "message": f"Test execution error: {str(e)}",
            "passed": 0,
            "failed": 0
        }

def check_test_manifest(source_file: Path) -> Optional[Dict]:
    """Check for test requirements in manifest."""
    feature = source_file.stem
    manifest_path = Path(f'tests/{feature}_manifest.json')
    
    if manifest_path.exists():
        try:
            with open(manifest_path, 'r') as f:
                return json.load(f)
        except:
            pass
    
    return None

def validate_against_requirements(test_results: Dict, manifest: Dict) -> List[str]:
    """Validate test results against requirements."""
    violations = []
    
    if not manifest:
        return violations
    
    # Check coverage requirements
    if 'coverage_target' in manifest:
        target = manifest['coverage_target']
        actual = test_results.get('coverage', 0)
        if actual < target:
            violations.append(f"Coverage {actual}% below target {target}%")
    
    # Check all required tests passed
    if test_results['failed'] > 0:
        violations.append(f"{test_results['failed']} tests failing")
    
    return violations

def format_results_message(source_file: Path, test_files: List[Path], 
                          success: bool, results: Dict, violations: List[str]) -> str:
    """Format test results message."""
    if success and not violations:
        msg = "✅ Tests Passing - Implementation Valid!\n\n"
        msg += f"📄 File: {source_file}\n"
        msg += f"🧪 Tests run: {len(test_files)}\n"
        msg += f"✅ Passed: {results['passed']}\n"
        
        if results.get('coverage'):
            msg += f"📊 Coverage: {results['coverage']}%\n"
        
        return msg
    
    # Failure message
    msg = "❌ Test Validation Failed!\n\n"
    msg += f"📄 File: {source_file}\n"
    msg += f"🧪 Tests run: {len(test_files)}\n"
    
    if results.get('passed', 0) > 0:
        msg += f"✅ Passed: {results['passed']}\n"
    if results.get('failed', 0) > 0:
        msg += f"❌ Failed: {results['failed']}\n"
        
        # Show failed test names
        failed_tests = results.get('failed_tests', [])
        if failed_tests:
            msg += "\n🔴 Failed tests:\n"
            for test in failed_tests[:5]:
                msg += f"  • {test}\n"
            if len(failed_tests) > 5:
                msg += f"  • ... and {len(failed_tests) - 5} more\n"
    
    if violations:
        msg += "\n⚠️ Requirement Violations:\n"
        for violation in violations:
            msg += f"  • {violation}\n"
    
    msg += "\n🔧 Next Steps:\n"
    msg += "1. Review failing tests\n"
    msg += "2. Fix implementation\n"
    msg += "3. Run tests again\n"
    
    # Add abbreviated output for debugging
    if results.get('output'):
        output_lines = results['output'].split('\n')
        relevant_lines = [l for l in output_lines if 'FAILED' in l or 'ERROR' in l or 'assert' in l]
        if relevant_lines:
            msg += "\n📋 Test Output (abbreviated):\n```\n"
            msg += '\n'.join(relevant_lines[:10])
            msg += "\n```\n"
    
    return msg

def should_run_validation(file_path: str) -> bool:
    """Determine if test validation should run."""
    # Skip test files
    if 'test_' in file_path or '/tests/' in file_path:
        return False
    
    # Skip non-implementation files
    skip_patterns = [
        '__pycache__/', '.pyc', 'migrations/',
        'requirements.txt', 'setup.py', '__init__.py',
        '.env', 'config.py'
    ]
    
    for pattern in skip_patterns:
        if pattern in file_path:
            return False
    
    # Only validate main source files
    return '/src/' in file_path or file_path.startswith('src/')

def get_validation_config() -> Dict:
    """Get test validation configuration."""
    config_path = Path('.claude/hooks/config.json')
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return config.get('test_validation', {
                    'auto_run': True,
                    'block_on_failure': True,
                    'coverage_required': False
                })
        except:
            pass
    
    return {
        'auto_run': True,
        'block_on_failure': True,
        'coverage_required': False
    }

def main():
    """Main hook logic."""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # This is a post-tool-use hook
    # Only run after file writes
    if input_data['tool'] not in ['write_file', 'str_replace']:
        sys.exit(0)
        return
    
    file_path = input_data.get('path', '')
    
    # Only check Python implementation files
    if not file_path.endswith('.py') or not should_run_validation(file_path):
        sys.exit(0)
        return
    
    # Get config
    config = get_validation_config()
    if not config.get('auto_run', True):
        sys.exit(0)
        return
    
    source_file = Path(file_path)
    
    # Find related test files
    test_files = find_test_files(source_file)
    
    if not test_files:
        # No tests to run
        sys.exit(0)
        return
    
    # Run the tests
    success, results = run_specific_tests(test_files)
    
    # Check test manifest for requirements
    manifest = check_test_manifest(source_file)
    violations = validate_against_requirements(results, manifest)
    
    # Format message
    message = format_results_message(source_file, test_files, success, results, violations)
    
    # Determine action based on results and config
    if success and not violations:
        # Tests passing - just log to stdout
        print(f"✅ Tests passing for {source_file.name}")
        sys.exit(0)
    else:
        # Tests failing
        if config.get('block_on_failure', True):
            # Block with error message to stderr
            print(message, file=sys.stderr)
            sys.exit(1)
        else:
            # Warn but continue
            print(message, file=sys.stderr)
            sys.exit(2)

if __name__ == "__main__":
    main()