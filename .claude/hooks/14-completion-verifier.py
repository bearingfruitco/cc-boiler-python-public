#!/usr/bin/env python3
"""
Completion Verifier - Ensures completion claims are verified before proceeding
Works with existing test infrastructure to validate "done" claims
"""

import json
import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Phrases that indicate completion claims
COMPLETION_PHRASES = [
    "implementation complete",
    "feature is now complete",
    "successfully implemented",
    "done implementing",
    "finished implementing",
    "completed successfully",
    "task completed",
    "✅ completed",
    "✅ done",
    "all set",
    "ready to go",
    "should now work",
    "is now working"
]

def load_verification_config() -> Dict:
    """Load verification configuration from config.json."""
    config_path = Path(".claude/hooks/config.json")
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return config.get('verification', {
                    'enabled': True,
                    'strict_mode': False,  # Start with warnings only
                    'block_on_failure': False,
                    'require_integration_tests': False,
                    'require_regression_check': False,
                    'completion_phrases': COMPLETION_PHRASES
                })
        except:
            pass
    
    return {
        'enabled': True,
        'strict_mode': False,
        'block_on_failure': False,
        'completion_phrases': COMPLETION_PHRASES
    }

def detect_completion_claim(output: str, phrases: List[str]) -> bool:
    """Check if output contains completion claims."""
    if not output:
        return False
    
    output_lower = output.lower()
    return any(phrase.lower() in output_lower for phrase in phrases)

def extract_context(input_data: Dict) -> Dict:
    """Extract context about what's being claimed complete."""
    context = {
        'tool': input_data.get('tool', ''),
        'timestamp': datetime.now().isoformat(),
        'feature': None,
        'issue': None,
        'task': None
    }
    
    # Try to extract from command or path
    if 'command' in input_data:
        cmd = input_data['command']
        # Look for issue numbers
        issue_match = re.search(r'#(\d+)|issue[:\s]+(\d+)', cmd)
        if issue_match:
            context['issue'] = issue_match.group(1) or issue_match.group(2)
        
        # Look for feature names
        if '/pt' in cmd or 'process-tasks' in cmd:
            parts = cmd.split()
            if len(parts) > 1:
                context['task'] = parts[1]
    
    # Extract from workflow state
    workflow_file = Path('.claude/context/workflow_state.json')
    if workflow_file.exists():
        try:
            workflow = json.loads(workflow_file.read_text())
            context['feature'] = workflow.get('current_task')
            context['issue'] = workflow.get('current_issue')
        except:
            pass
    
    return context

def load_verification_manifest() -> Dict:
    """Load existing verification manifest."""
    manifest_path = Path('.claude/verification-manifest.json')
    if manifest_path.exists():
        try:
            return json.loads(manifest_path.read_text())
        except:
            pass
    
    return {
        'verification_rules': {
            'require_execution_proof': True,
            'require_test_results': True
        },
        'feature_verifications': {},
        'last_updated': datetime.now().isoformat()
    }

def save_verification_manifest(manifest: Dict):
    """Save verification manifest."""
    manifest_path = Path('.claude/verification-manifest.json')
    manifest['last_updated'] = datetime.now().isoformat()
    manifest_path.write_text(json.dumps(manifest, indent=2))

def run_verification_checks(context: Dict, config: Dict) -> Dict:
    """Run verification checks based on context."""
    results = {
        'timestamp': datetime.now().isoformat(),
        'context': context,
        'all_passed': True,
        'checks': []
    }
    
    # 1. Check for test files
    test_check = check_tests_exist(context)
    results['checks'].append(test_check)
    if not test_check['passed']:
        results['all_passed'] = False
    
    # 2. Run unit tests if they exist
    if test_check['passed']:
        unit_result = run_unit_tests(context)
        results['checks'].append(unit_result)
        if not unit_result['passed']:
            results['all_passed'] = False
    
    # 3. Check for recent test runs
    recent_test = check_recent_test_run(context)
    results['checks'].append(recent_test)
    if not recent_test['passed']:
        results['all_passed'] = False
    
    # 4. Integration tests if configured
    if config.get('require_integration_tests', False):
        integration_result = check_integration_tests(context)
        results['checks'].append(integration_result)
        if not integration_result['passed']:
            results['all_passed'] = False
    
    return results

def check_tests_exist(context: Dict) -> Dict:
    """Check if tests exist for the feature."""
    feature = context.get('feature') or context.get('task') or 'unknown'
    
    # Look for test files
    test_patterns = [
        f"tests/test_{feature}.py",
        f"tests/unit/test_{feature}.py",
        f"tests/integration/test_{feature}.py",
        f"tests/**/test_{feature}_*.py"
    ]
    
    test_files = []
    for pattern in test_patterns:
        test_files.extend(Path('.').glob(pattern))
    
    return {
        'check': 'tests_exist',
        'passed': len(test_files) > 0,
        'test_files': [str(f) for f in test_files],
        'message': f"Found {len(test_files)} test file(s)" if test_files else "No test files found"
    }

def run_unit_tests(context: Dict) -> Dict:
    """Run unit tests for the feature."""
    feature = context.get('feature') or context.get('task') or 'unknown'
    
    # Find test file
    test_file = None
    for pattern in [f"tests/test_{feature}.py", f"tests/unit/test_{feature}.py"]:
        if Path(pattern).exists():
            test_file = pattern
            break
    
    if not test_file:
        return {
            'check': 'unit_tests',
            'passed': False,
            'message': 'No unit test file found'
        }
    
    try:
        # Run pytest
        result = subprocess.run(
            ['pytest', test_file, '-v', '--tb=short'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Parse results
        passed = result.returncode == 0
        output = result.stdout + result.stderr
        
        # Extract test counts
        test_count = 0
        failed_count = 0
        for line in output.split('\n'):
            if ' passed' in line and ' failed' not in line:
                match = re.search(r'(\d+) passed', line)
                if match:
                    test_count = int(match.group(1))
            if ' failed' in line:
                match = re.search(r'(\d+) failed', line)
                if match:
                    failed_count = int(match.group(1))
        
        return {
            'check': 'unit_tests',
            'passed': passed,
            'test_file': test_file,
            'tests_run': test_count,
            'tests_failed': failed_count,
            'message': f"{test_count} tests passed" if passed else f"{failed_count} tests failed"
        }
        
    except Exception as e:
        return {
            'check': 'unit_tests',
            'passed': False,
            'error': str(e),
            'message': 'Failed to run tests'
        }

def check_recent_test_run(context: Dict) -> Dict:
    """Check if tests were run recently."""
    # Look for pytest cache
    pytest_cache = Path('.pytest_cache/v/cache/lastfailed')
    if pytest_cache.exists():
        # Check modification time
        import time
        mtime = pytest_cache.stat().st_mtime
        age_minutes = (time.time() - mtime) / 60
        
        if age_minutes < 5:  # Tests run in last 5 minutes
            return {
                'check': 'recent_test_run',
                'passed': True,
                'age_minutes': round(age_minutes, 1),
                'message': f'Tests run {round(age_minutes, 1)} minutes ago'
            }
    
    return {
        'check': 'recent_test_run',
        'passed': False,
        'message': 'No recent test run detected'
    }

def check_integration_tests(context: Dict) -> Dict:
    """Check for integration tests."""
    feature = context.get('feature') or context.get('task') or 'unknown'
    
    integration_test = Path(f'tests/integration/test_{feature}_integration.py')
    if integration_test.exists():
        # Could run the test here
        return {
            'check': 'integration_tests',
            'passed': True,
            'test_file': str(integration_test),
            'message': 'Integration test file exists'
        }
    
    return {
        'check': 'integration_tests',
        'passed': False,
        'message': 'No integration test found'
    }

def format_verification_message(results: Dict, config: Dict) -> str:
    """Format verification results message."""
    if results['all_passed']:
        msg = "✅ **Completion Verified!**\n\n"
        msg += "All verification checks passed:\n"
        for check in results['checks']:
            msg += f"  ✅ {check['check']}: {check['message']}\n"
        
        msg += "\n✅ Safe to proceed with next task!\n"
        return msg
    
    # Format failure/warning message
    if config.get('strict_mode', False):
        msg = "❌ **COMPLETION NOT VERIFIED!**\n\n"
    else:
        msg = "⚠️ **Completion Verification Warning**\n\n"
    
    msg += "The following checks did not pass:\n"
    
    for check in results['checks']:
        if check['passed']:
            msg += f"  ✅ {check['check']}: {check['message']}\n"
        else:
            msg += f"  ❌ {check['check']}: {check['message']}\n"
    
    msg += "\n**Required Actions:**\n"
    
    # Suggest actions based on failures
    for check in results['checks']:
        if not check['passed']:
            if check['check'] == 'tests_exist':
                msg += "1. Generate tests: `/generate-tests " + str(results['context'].get('feature', 'feature')) + "`\n"
            elif check['check'] == 'unit_tests':
                msg += "1. Fix failing tests or implementation\n"
                msg += "2. Run tests: `/test`\n"
            elif check['check'] == 'recent_test_run':
                msg += "1. Run tests to verify: `/test`\n"
    
    if config.get('strict_mode', False):
        msg += "\n🚫 **Cannot proceed until verification passes!**\n"
    else:
        msg += "\n⚠️ **Proceeding without verification is risky!**\n"
        msg += "Enable strict mode to enforce verification.\n"
    
    return msg

def record_verification(context: Dict, results: Dict):
    """Record verification results in manifest."""
    manifest = load_verification_manifest()
    
    feature = context.get('feature') or context.get('task') or 'unknown'
    
    if 'feature_verifications' not in manifest:
        manifest['feature_verifications'] = {}
    
    manifest['feature_verifications'][feature] = {
        'last_verified': results['timestamp'],
        'verification_passed': results['all_passed'],
        'checks': results['checks'],
        'context': context
    }
    
    save_verification_manifest(manifest)

def main():
    """Main hook logic."""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Load config
    config = load_verification_config()
    
    if not config.get('enabled', True):
        sys.exit(0)
        return
    
    # Check for completion claims
    output = str(input_data.get('output', ''))
    
    if not detect_completion_claim(output, config.get('completion_phrases', COMPLETION_PHRASES)):
        sys.exit(0)
        return
    
    # Extract context
    context = extract_context(input_data)
    
    # Run verification checks
    results = run_verification_checks(context, config)
    
    # Record results
    record_verification(context, results)
    
    # Format message
    message = format_verification_message(results, config)
    
    # Output message
    print(message, file=sys.stderr)
    
    # Determine exit code
    if results['all_passed']:
        sys.exit(0)  # Success
    elif config.get('block_on_failure', False) and config.get('strict_mode', False):
        sys.exit(1)  # Block progression
    else:
        sys.exit(2)  # Warning but continue

if __name__ == "__main__":
    main()
