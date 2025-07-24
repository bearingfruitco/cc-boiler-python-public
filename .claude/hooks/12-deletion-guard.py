#!/usr/bin/env python3
"""
Deletion Guard Hook - Prevents unintentional code/file deletions
Requires explicit justification for deletions
"""

import json
import sys
import re
from pathlib import Path

# Patterns that indicate deletion
DELETION_PATTERNS = [
    r'^\s*$',  # Empty replacement
    r'^[\s\n]*$'  # Only whitespace
]

# Critical files that should never be deleted
PROTECTED_FILES = [
    'package.json',
    'tsconfig.json',
    'next.config.js',
    '.env.example',
    'README.md',
    'tailwind.config.js',
    '.gitignore'
]

# Critical directories
PROTECTED_DIRS = [
    '.claude',
    '.git',
    'field-registry',
    'docs/project'
]

def count_removed_lines(old_content, new_content):
    """Count how many lines are being removed"""
    old_lines = old_content.split('\n')
    new_lines = new_content.split('\n')
    
    # Count non-empty lines being removed
    old_non_empty = [l for l in old_lines if l.strip()]
    new_non_empty = [l for l in new_lines if l.strip()]
    
    return len(old_non_empty) - len(new_non_empty)

def is_significant_deletion(old_content, new_content):
    """Check if this is a significant deletion"""
    # Check if new content is essentially empty
    if re.match(r'^[\s\n]*$', new_content) and len(old_content.strip()) > 10:
        return True
    
    # Check line count reduction
    lines_removed = count_removed_lines(old_content, new_content)
    if lines_removed > 10:
        return True
    
    # Check percentage reduction
    if len(old_content) > 100:
        reduction_percent = (len(old_content) - len(new_content)) / len(old_content)
        if reduction_percent > 0.5:  # More than 50% removed
            return True
    
    return False

def analyze_deletion(old_content, new_content):
    """Analyze what's being deleted"""
    old_lines = old_content.split('\n')
    new_lines = new_content.split('\n')
    
    # Find what's being removed
    removed_items = {
        'functions': [],
        'components': [],
        'classes': [],
        'exports': [],
        'imports': []
    }
    
    # Simple pattern matching for removed items
    for line in old_lines:
        if line not in new_lines:
            # Check for function deletions
            if re.match(r'^\s*(export\s+)?(async\s+)?function\s+(\w+)', line):
                match = re.search(r'function\s+(\w+)', line)
                if match:
                    removed_items['functions'].append(match.group(1))
            
            # Check for component deletions
            if re.match(r'^\s*export\s+(default\s+)?function\s+[A-Z]\w+', line):
                match = re.search(r'function\s+(\w+)', line)
                if match:
                    removed_items['components'].append(match.group(1))
            
            # Check for class deletions
            if re.match(r'^\s*(export\s+)?class\s+(\w+)', line):
                match = re.search(r'class\s+(\w+)', line)
                if match:
                    removed_items['classes'].append(match.group(1))
            
            # Check for export deletions
            if re.match(r'^\s*export\s+', line):
                removed_items['exports'].append(line.strip())
    
    return removed_items

def get_current_task():
    """Try to get the current task from context"""
    try:
        # Check for active task in work state
        work_state_file = Path('.claude/work-state.json')
        if work_state_file.exists():
            with open(work_state_file) as f:
                state = json.load(f)
                return state.get('current_task', 'Unknown')
    except:
        pass
    
    return 'Unknown'

def main():
    """Main hook logic"""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    tool_use = input_data.get('tool_use', {})
    operation = tool_use.get('name', '')
    
    # Check file deletion
    if operation == 'delete_file':
        file_path = tool_use.get('path', '')
        file_name = Path(file_path).name
        
        # Check if protected file
        if file_name in PROTECTED_FILES:
            print(json.dumps({
                "decision": "block",
                "message": f"🚫 Cannot delete protected file: {file_name}\nThis is a critical project file.",
                "suggestion": "Protected files cannot be deleted. Modify content instead."
            }))
            return
        
        # Check if in protected directory
        for protected_dir in PROTECTED_DIRS:
            if protected_dir in file_path:
                print(json.dumps({
                    "decision": "block",
                    "message": f"🚫 Cannot delete files in protected directory: {protected_dir}",
                    "suggestion": "This directory contains critical system files."
                }))
                return
        
        # Require justification for any deletion
        current_task = get_current_task()
        
        warning_msg = f"⚠️ File Deletion Warning\n\n"
        warning_msg += f"You're about to DELETE: {file_path}\n"
        warning_msg += f"Current task: {current_task}\n\n"
        warning_msg += "Before deleting, consider:\n"
        warning_msg += "1. Is this file truly obsolete?\n"
        warning_msg += "2. Are there any imports/references to update?\n"
        warning_msg += "3. Should this be moved/renamed instead?\n\n"
        warning_msg += "Add a comment explaining why this deletion is necessary."
        
        print(json.dumps({
            "decision": "warn",
            "message": warning_msg,
            "continue": True
        }))
        return
    
    # Check content deletion (emptying files or removing large sections)
    if operation in ['str_replace_editor', 'edit_file']:
        old_content = tool_use.get('old_str', tool_use.get('old_content', ''))
        new_content = tool_use.get('new_str', tool_use.get('content', ''))
        file_path = tool_use.get('path', '')
        
        if is_significant_deletion(old_content, new_content):
            lines_removed = count_removed_lines(old_content, new_content)
            removed_items = analyze_deletion(old_content, new_content)
            current_task = get_current_task()
            
            error_msg = f"🚨 Significant Deletion Detected\n\n"
            error_msg += f"File: {file_path}\n"
            error_msg += f"Lines being removed: {lines_removed}\n"
            error_msg += f"Current task: {current_task}\n\n"
            
            if any(removed_items.values()):
                error_msg += "Items being deleted:\n"
                for item_type, items in removed_items.items():
                    if items:
                        error_msg += f"- {item_type.capitalize()}: {', '.join(items)}\n"
                error_msg += "\n"
            
            error_msg += "❓ Key Questions:\n"
            error_msg += "1. Is this deletion related to your current task?\n"
            error_msg += "2. Are these items used elsewhere in the codebase?\n"
            error_msg += "3. Should this be refactored instead of deleted?\n\n"
            
            error_msg += "If this deletion is intentional:\n"
            error_msg += "- Add a comment explaining why\n"
            error_msg += "- Ensure all references are updated\n"
            error_msg += "- Consider git commit before major deletions"
            
            # Block if removing entire file content
            if re.match(r'^[\s\n]*$', new_content) and len(old_content.strip()) > 50:
                print(json.dumps({
                    "decision": "block",
                    "message": error_msg,
                    "suggestion": "Cannot empty entire files. Use delete_file if removal is needed."
                }))
            else:
                # Warn for significant deletions
                print(json.dumps({
                    "decision": "warn",
                    "message": error_msg,
                    "continue": True
                }))
        else:
            sys.exit(0)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
