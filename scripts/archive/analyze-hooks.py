#!/usr/bin/env python3
"""
Hook Analysis Tool - Analyze all hooks for conflicts and overlaps
"""

import os
import json
from pathlib import Path
from collections import defaultdict

def analyze_hooks():
    hooks_dir = Path(".claude/hooks")
    hook_analysis = defaultdict(list)
    
    # Scan all hook directories
    for hook_type in ["pre-tool-use", "post-tool-use", "notification", "stop", "sub-agent-stop"]:
        dir_path = hooks_dir / hook_type
        if dir_path.exists():
            for hook_file in sorted(dir_path.glob("*.py")):
                # Read first 50 lines to understand purpose
                with open(hook_file, 'r') as f:
                    lines = f.readlines()[:50]
                    content = ''.join(lines)
                    
                    # Extract purpose from docstring
                    purpose = "Unknown"
                    if '"""' in content:
                        start = content.find('"""') + 3
                        end = content.find('"""', start)
                        if end > start:
                            purpose = content[start:end].strip().split('\n')[0]
                    
                    # Look for key patterns
                    patterns = {
                        'file_operations': bool(re.search(r'(write_file|edit_file|create_file)', content)),
                        'validation': bool(re.search(r'(validate|check|enforce)', content)),
                        'logging': bool(re.search(r'(log|record|track)', content)),
                        'state_management': bool(re.search(r'(state|save|persist)', content)),
                        'python_specific': bool(re.search(r'(python|py|import|module)', content, re.I)),
                        'design_system': bool(re.search(r'(design|typography|spacing)', content)),
                        'safety': bool(re.search(r'(dangerous|protect|guard|block)', content)),
                    }
                    
                    hook_analysis[hook_type].append({
                        'file': hook_file.name,
                        'purpose': purpose,
                        'patterns': patterns
                    })
    
    return hook_analysis

def find_conflicts(analysis):
    """Find potential conflicts between hooks"""
    conflicts = []
    
    # Check within each hook type
    for hook_type, hooks in analysis.items():
        for i, hook1 in enumerate(hooks):
            for hook2 in hooks[i+1:]:
                # Check for overlapping patterns
                overlap_count = sum(
                    1 for k in hook1['patterns'] 
                    if hook1['patterns'][k] and hook2['patterns'][k]
                )
                
                if overlap_count >= 2:  # Significant overlap
                    conflicts.append({
                        'type': hook_type,
                        'hook1': hook1['file'],
                        'hook2': hook2['file'],
                        'overlap_patterns': [
                            k for k in hook1['patterns'] 
                            if hook1['patterns'][k] and hook2['patterns'][k]
                        ]
                    })
    
    return conflicts

# Run analysis
import re
analysis = analyze_hooks()
conflicts = find_conflicts(analysis)

print("🔍 HOOK ANALYSIS RESULTS")
print("=" * 60)

# Summary
total_hooks = sum(len(hooks) for hooks in analysis.values())
print(f"\nTotal hooks: {total_hooks}")

# By type
print("\nHooks by type:")
for hook_type, hooks in analysis.items():
    print(f"  {hook_type}: {len(hooks)} hooks")

# Potential conflicts
if conflicts:
    print(f"\n⚠️  POTENTIAL CONFLICTS FOUND: {len(conflicts)}")
    for conflict in conflicts:
        print(f"\n  In {conflict['type']}:")
        print(f"    {conflict['hook1']} ↔ {conflict['hook2']}")
        print(f"    Overlapping: {', '.join(conflict['overlap_patterns'])}")
else:
    print("\n✅ No significant conflicts found")

# Pattern distribution
print("\n📊 PATTERN DISTRIBUTION:")
pattern_counts = defaultdict(int)
for hook_type, hooks in analysis.items():
    for hook in hooks:
        for pattern, present in hook['patterns'].items():
            if present:
                pattern_counts[pattern] += 1

for pattern, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {pattern}: {count} hooks")

# Detailed analysis
print("\n\n📋 DETAILED HOOK PURPOSES:")
for hook_type, hooks in analysis.items():
    print(f"\n{hook_type.upper()}:")
    for hook in hooks:
        print(f"  {hook['file']}: {hook['purpose']}")
