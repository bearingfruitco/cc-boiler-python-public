#!/usr/bin/env python3
"""
Hook Health Check - Verifies all hooks are properly configured and working
Run this to diagnose issues with the hooks system
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def check_python_version():
    """Check Python version is 3.6+"""
    version = sys.version_info
    return {
        'check': 'Python Version',
        'status': 'pass' if version >= (3, 6) else 'fail',
        'details': f"Python {version.major}.{version.minor}.{version.micro}",
        'required': 'Python 3.6+'
    }

def check_required_commands():
    """Check required commands are available"""
    commands = {
        'git': 'Git version control',
        'gh': 'GitHub CLI',
        'python3': 'Python 3 interpreter'
    }
    
    results = []
    for cmd, description in commands.items():
        try:
            subprocess.run(
                f"which {cmd}",
                shell=True,
                check=True,
                capture_output=True
            )
            status = 'pass'
            details = f"{cmd} found"
        except:
            status = 'fail'
            details = f"{cmd} not found in PATH"
        
        results.append({
            'check': f'{description} ({cmd})',
            'status': status,
            'details': details
        })
    
    return results

def check_directory_structure():
    """Check required directories exist"""
    dirs = {
        '.claude/hooks': 'Hooks directory',
        '.claude/team': 'Team collaboration',
        '.claude/commands': 'Custom commands',
        '.claude/scripts': 'Utility scripts'
    }
    
    results = []
    for dir_path, description in dirs.items():
        exists = Path(dir_path).exists()
        results.append({
            'check': description,
            'status': 'pass' if exists else 'fail',
            'details': f"{dir_path} {'exists' if exists else 'missing'}"
        })
    
    return results

def check_hook_files():
    """Check all hook files exist and are executable"""
    hook_dir = Path('.claude/hooks')
    expected_hooks = {
        'pre-tool-use': [
            '01-collab-sync.py',
            '02-design-check.py',
            '03-conflict-check.py',
            '04-actually-works.py',
            '05-code-quality.py'
        ],
        'post-tool-use': [
            '01-state-save.py',
            '02-metrics.py',
            '03-pattern-learning.py'
        ],
        'notification': [
            'team-aware.py',
            'smart-suggest.py'
        ],
        'stop': [
            'save-state.py',
            'knowledge-share.py',
            'handoff-prep.py'
        ]
    }
    
    results = []
    for hook_type, hooks in expected_hooks.items():
        for hook in hooks:
            hook_path = hook_dir / hook_type / hook
            exists = hook_path.exists()
            executable = hook_path.is_file() and hook_path.stat().st_mode & 0o111 if exists else False
            
            status = 'pass' if exists and executable else 'warn' if exists else 'fail'
            details = 'exists and executable' if exists and executable else 'exists but not executable' if exists else 'missing'
            
            results.append({
                'check': f'{hook_type}/{hook}',
                'status': status,
                'details': details
            })
    
    return results

def check_configuration():
    """Check configuration files"""
    configs = {
        '.claude/settings.json': 'Claude Code settings',
        '.claude/hooks/config.json': 'Hooks configuration',
        '.claude/team/config.json': 'Team configuration'
    }
    
    results = []
    for config_path, description in configs.items():
        path = Path(config_path)
        if path.exists():
            try:
                with open(path) as f:
                    data = json.load(f)
                
                # Check for hooks in settings.json
                if 'settings.json' in config_path:
                    has_hooks = 'hooks' in data
                    status = 'pass' if has_hooks else 'warn'
                    details = 'valid JSON, hooks configured' if has_hooks else 'valid JSON, hooks not configured'
                else:
                    status = 'pass'
                    details = 'valid JSON'
            except json.JSONDecodeError:
                status = 'fail'
                details = 'invalid JSON'
            except Exception as e:
                status = 'fail'
                details = f'error: {str(e)}'
        else:
            status = 'fail'
            details = 'file missing'
        
        results.append({
            'check': description,
            'status': status,
            'details': f"{config_path}: {details}"
        })
    
    return results

def generate_report(checks):
    """Generate health check report"""
    report = f"""
# Claude Code Hooks Health Check Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
"""
    
    total = len(checks)
    passed = sum(1 for c in checks if c['status'] == 'pass')
    warnings = sum(1 for c in checks if c['status'] == 'warn')
    failed = sum(1 for c in checks if c['status'] == 'fail')
    
    report += f"- Total checks: {total}\n"
    report += f"- ✅ Passed: {passed}\n"
    report += f"- ⚠️  Warnings: {warnings}\n"
    report += f"- ❌ Failed: {failed}\n\n"
    
    # Group by status
    if failed > 0:
        report += "## ❌ Failed Checks (Must Fix)\n"
        for check in checks:
            if check['status'] == 'fail':
                report += f"- **{check['check']}**: {check['details']}\n"
        report += "\n"
    
    if warnings > 0:
        report += "## ⚠️  Warnings (Should Fix)\n"
        for check in checks:
            if check['status'] == 'warn':
                report += f"- **{check['check']}**: {check['details']}\n"
        report += "\n"
    
    report += "## ✅ Passed Checks\n"
    for check in checks:
        if check['status'] == 'pass':
            report += f"- {check['check']}: {check['details']}\n"
    
    # Add fix instructions
    if failed > 0 or warnings > 0:
        report += "\n## 🔧 How to Fix\n\n"
        
        if any('not found in PATH' in c['details'] for c in checks if c['status'] == 'fail'):
            report += "### Missing Commands\n"
            report += "- Git: Install from https://git-scm.com\n"
            report += "- GitHub CLI: Install from https://cli.github.com\n"
            report += "- Python 3: Install from https://python.org\n\n"
        
        if any('missing' in c['details'] and 'directory' in c['details'] for c in checks if c['status'] == 'fail'):
            report += "### Missing Directories\n"
            report += "Run: `.claude/scripts/install-hooks.sh`\n\n"
        
        if any('not executable' in c['details'] for c in checks if c['status'] == 'warn'):
            report += "### Non-Executable Hooks\n"
            report += "Run: `chmod +x .claude/hooks/**/*.py`\n\n"
        
        if any('hooks not configured' in c['details'] for c in checks if c['status'] == 'warn'):
            report += "### Hooks Not Configured\n"
            report += "Run: `.claude/scripts/install-hooks.sh`\n"
    
    return report

def main():
    """Run health check"""
    all_checks = []
    
    # Run all checks
    all_checks.append(check_python_version())
    all_checks.extend(check_required_commands())
    all_checks.extend(check_directory_structure())
    all_checks.extend(check_hook_files())
    all_checks.extend(check_configuration())
    
    # Generate report
    report = generate_report(all_checks)
    
    # Save report
    report_path = Path('.claude/hooks/health-check-report.md')
    with open(report_path, 'w') as f:
        f.write(report)
    
    # Output summary
    failed = sum(1 for c in all_checks if c['status'] == 'fail')
    warnings = sum(1 for c in all_checks if c['status'] == 'warn')
    
    if failed > 0:
        print(f"❌ Health check failed: {failed} critical issues found")
        print(f"See {report_path} for details")
        sys.exit(1)
    elif warnings > 0:
        print(f"⚠️  Health check passed with warnings: {warnings} issues")
        print(f"See {report_path} for details")
        sys.exit(0)
    else:
        print("✅ All health checks passed!")
        print(f"Full report: {report_path}")
        sys.exit(0)

if __name__ == "__main__":
    main()
