#!/usr/bin/env python3
"""
Debug Helper Hook - Provides detailed debugging information when things go wrong
Helps diagnose hook failures and system issues
"""

import json
import sys
import subprocess
import traceback
from pathlib import Path
from datetime import datetime

def get_system_info():
    """Gather system information for debugging"""
    info = {
        'timestamp': datetime.now().isoformat(),
        'python_version': sys.version,
        'working_directory': str(Path.cwd()),
        'hook_directory': str(Path(__file__).parent.parent),
        'user': get_current_user()
    }
    
    # Check git status
    try:
        result = subprocess.run(
            "git status --short",
            shell=True,
            capture_output=True,
            text=True
        )
        info['git_status'] = result.stdout.strip()
    except:
        info['git_status'] = 'Unable to get git status'
    
    # Check if required directories exist
    required_dirs = [
        '.claude/hooks',
        '.claude/team', 
        '.claude/commands',
        '.claude/scripts'
    ]
    
    info['directory_check'] = {}
    for dir_path in required_dirs:
        info['directory_check'][dir_path] = Path(dir_path).exists()
    
    return info

def get_current_user():
    """Get current user with fallback"""
    try:
        config_path = Path(__file__).parent.parent.parent / 'team' / 'config.json'
        if config_path.exists():
            with open(config_path) as f:
                return json.load(f).get('current_user', 'unknown')
    except:
        pass
    return 'unknown'

def diagnose_hook_failure(error_info):
    """Diagnose common hook failures"""
    diagnosis = []
    error_str = str(error_info)
    
    if 'ModuleNotFoundError' in error_str:
        diagnosis.append("Missing Python module - check requirements")
    elif 'FileNotFoundError' in error_str:
        diagnosis.append("File or directory not found - check paths")
    elif 'PermissionError' in error_str:
        diagnosis.append("Permission denied - check file permissions")
    elif 'json.decoder.JSONDecodeError' in error_str:
        diagnosis.append("Invalid JSON - check file formatting")
    elif 'git' in error_str.lower():
        diagnosis.append("Git command failed - ensure git is initialized")
    
    return diagnosis

def create_debug_report(exception_info=None):
    """Create comprehensive debug report"""
    report = {
        'system_info': get_system_info(),
        'error': None,
        'diagnosis': [],
        'suggestions': []
    }
    
    if exception_info:
        report['error'] = {
            'type': type(exception_info).__name__,
            'message': str(exception_info),
            'traceback': traceback.format_exc()
        }
        report['diagnosis'] = diagnose_hook_failure(exception_info)
    
    # Add suggestions based on diagnosis
    if report['diagnosis']:
        if 'Missing Python module' in report['diagnosis'][0]:
            report['suggestions'].append("Run: pip install -r .claude/hooks/requirements.txt")
        elif 'Permission denied' in report['diagnosis'][0]:
            report['suggestions'].append("Run: chmod +x .claude/hooks/**/*.py")
        elif 'Git command failed' in report['diagnosis'][0]:
            report['suggestions'].append("Ensure git is initialized: git init")
    
    return report

def save_debug_log(report):
    """Save debug report to file"""
    debug_dir = Path(__file__).parent.parent.parent / 'team' / 'debug'
    debug_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    debug_file = debug_dir / f'debug_{timestamp}.json'
    
    with open(debug_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    return debug_file

def main():
    """Main hook logic - wraps other hooks with error handling"""
    try:
        # This hook is meant to be used in wrapper mode
        # It should be called by other hooks when they fail
        
        # Read any error information passed via stdin
        input_data = sys.stdin.read()
        
        if input_data:
            error_data = json.loads(input_data)
            if error_data.get('error'):
                # Generate debug report
                report = create_debug_report(Exception(error_data['error']))
                
                # Save to file
                debug_file = save_debug_log(report)
                
                # Return helpful error message
                print(json.dumps({
                    "decision": "error",
                    "message": f"🔧 Hook Error Detected\n\nDiagnosis: {', '.join(report['diagnosis'])}\n\nDebug log saved: {debug_file}\n\nSuggestions:\n" + '\n'.join(f"• {s}" for s in report['suggestions']),
                    "debug_file": str(debug_file)
                }))
                return
        
        # If no error, just continue
        sys.exit(0)
        
    except Exception as e:
        # Self-diagnostic if this hook fails
        report = create_debug_report(e)
        print(json.dumps({
            "decision": "error",
            "message": f"Debug hook itself failed: {str(e)}\nThis suggests a fundamental setup issue.",
            "report": report
        }))

if __name__ == "__main__":
    main()
