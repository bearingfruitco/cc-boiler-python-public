#!/usr/bin/env python3
"""
PR Feedback Monitor - Checks for CodeRabbit and other PR feedback
Provides notifications when reviews are ready
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def get_current_pr():
    """Get PR number for current branch"""
    try:
        # Get current branch
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            text=True
        ).strip()
        
        # Get PR number
        result = subprocess.check_output(
            ["gh", "pr", "list", "--head", branch, "--json", "number"],
            text=True
        )
        
        prs = json.loads(result)
        if prs:
            return prs[0]['number']
    except:
        pass
    
    return None

def check_coderabbit_review(pr_number):
    """Check if CodeRabbit has reviewed"""
    try:
        # Get PR comments
        result = subprocess.check_output(
            ["gh", "api", f"repos/:owner/:repo/pulls/{pr_number}/comments"],
            text=True
        )
        
        comments = json.loads(result)
        
        # Look for CodeRabbit
        for comment in comments:
            if comment.get('user', {}).get('login') == 'coderabbitai':
                return parse_coderabbit_comment(comment['body'])
    except:
        pass
    
    return None

def parse_coderabbit_comment(body):
    """Extract key info from CodeRabbit comment"""
    issues = {
        'design_violations': [],
        'errors': [],
        'warnings': [],
        'suggestions': []
    }
    
    # Look for design system violations
    if 'text-size-' in body or 'font-regular' in body:
        issues['design_violations'].append("Design token violations found")
    
    # Look for errors
    if '🔴' in body or 'Error:' in body:
        issues['errors'].append("Critical issues found")
    
    # Look for warnings
    if '⚠️' in body or 'Warning:' in body:
        issues['warnings'].append("Warnings to address")
    
    return issues

def main():
    # This runs periodically (every 5 minutes via cron or systemd)
    pr_number = get_current_pr()
    
    if not pr_number:
        return
    
    # Check for new feedback
    feedback = check_coderabbit_review(pr_number)
    
    if feedback:
        # Check if we've already notified
        notified_file = Path(f".claude/notifications/pr-{pr_number}-notified.json")
        
        if not notified_file.exists():
            # First time seeing this feedback
            notified_file.parent.mkdir(exist_ok=True)
            
            # Create notification
            total_issues = (
                len(feedback.get('errors', [])) +
                len(feedback.get('warnings', [])) +
                len(feedback.get('design_violations', []))
            )
            
            if total_issues > 0:
                print(f"\n🐰 CodeRabbit Review Ready for PR #{pr_number}")
                print(f"Found {total_issues} issue(s) to address:")
                
                if feedback.get('errors'):
                    print(f"  - {len(feedback['errors'])} errors")
                if feedback.get('warnings'):
                    print(f"  - {len(feedback['warnings'])} warnings")
                if feedback.get('design_violations'):
                    print(f"  - {len(feedback['design_violations'])} design violations")
                
                print(f"\nRun: /pr-feedback {pr_number}")
                
                # Mark as notified
                with open(notified_file, 'w') as f:
                    json.dump({
                        'notified_at': datetime.now().isoformat(),
                        'issues': feedback
                    }, f)

    sys.exit(0)

if __name__ == "__main__":
    main()
