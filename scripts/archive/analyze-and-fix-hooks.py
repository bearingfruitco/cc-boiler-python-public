#!/usr/bin/env python3
import os
import json
import shutil
from collections import defaultdict

def analyze_hooks():
    """Analyze all hooks and identify issues"""
    hook_dirs = {
        'pre-tool-use': [],
        'post-tool-use': [],
        'notification': [],
        'stop': [],
        'sub-agent-stop': []
    }
    
    issues = {
        'duplicates': defaultdict(list),
        'unnumbered': defaultdict(list),
        'missing_from_config': defaultdict(list)
    }
    
    # Read config
    with open('.claude/hooks/config.json', 'r') as f:
        config = json.load(f)
    
    configured_hooks = {}
    for hook_type, hooks in config.get('hooks', {}).items():
        configured_hooks[hook_type] = [h['script'] for h in hooks]
    
    # Scan directories
    for hook_type in hook_dirs:
        dir_path = f'.claude/hooks/{hook_type}'
        if os.path.exists(dir_path):
            for filename in sorted(os.listdir(dir_path)):
                if filename.endswith('.py'):
                    hook_dirs[hook_type].append(filename)
                    
                    # Check for duplicate numbers
                    if filename[0:2].isdigit():
                        number = filename[0:2]
                        duplicates = [f for f in os.listdir(dir_path) 
                                    if f.startswith(number + '-') and f.endswith('.py')]
                        if len(duplicates) > 1:
                            issues['duplicates'][hook_type].extend(duplicates)
                    else:
                        # Unnumbered hook
                        issues['unnumbered'][hook_type].append(filename)
                    
                    # Check if in config
                    if hook_type in configured_hooks and filename not in configured_hooks[hook_type]:
                        issues['missing_from_config'][hook_type].append(filename)
    
    return hook_dirs, issues, config

def print_analysis(hook_dirs, issues):
    """Print analysis results"""
    print("🔍 HOOK ANALYSIS RESULTS")
    print("=" * 60)
    
    # Current state
    print("\n📂 CURRENT HOOKS BY DIRECTORY:")
    for hook_type, hooks in hook_dirs.items():
        print(f"\n{hook_type}: ({len(hooks)} hooks)")
        for hook in sorted(hooks):
            status = ""
            if hook in issues['unnumbered'][hook_type]:
                status = " ⚠️  NO NUMBER"
            elif hook in issues['duplicates'][hook_type]:
                status = " ⚠️  DUPLICATE NUMBER"
            elif hook in issues['missing_from_config'][hook_type]:
                status = " ⚠️  NOT IN CONFIG"
            print(f"  - {hook}{status}")
    
    # Issues summary
    print("\n❌ ISSUES FOUND:")
    print(f"  - Duplicate numbers: {sum(len(v) for v in issues['duplicates'].values())}")
    print(f"  - Unnumbered hooks: {sum(len(v) for v in issues['unnumbered'].values())}")
    print(f"  - Missing from config: {sum(len(v) for v in issues['missing_from_config'].values())}")

def propose_fixes(hook_dirs, issues):
    """Propose fixes for all issues"""
    fixes = {}
    
    for hook_type, hooks in hook_dirs.items():
        fixes[hook_type] = []
        
        # Sort hooks intelligently
        numbered = []
        unnumbered = []
        
        for hook in hooks:
            if hook[0:2].isdigit():
                numbered.append(hook)
            else:
                unnumbered.append(hook)
        
        # Process numbered hooks first (removing duplicates)
        seen_numbers = set()
        next_number = 0
        
        for hook in sorted(numbered):
            current_num = int(hook[0:2])
            base_name = hook[3:] if len(hook) > 3 else hook
            
            # Skip if we've seen this exact file before (duplicate)
            if hook in [f[1] for f in fixes[hook_type]]:
                continue
                
            # Assign next available number
            while next_number in seen_numbers:
                next_number += 1
            
            new_name = f"{next_number:02d}-{base_name}"
            fixes[hook_type].append((hook, new_name))
            seen_numbers.add(next_number)
            next_number += 1
        
        # Then add unnumbered hooks
        for hook in sorted(unnumbered):
            while next_number in seen_numbers:
                next_number += 1
            
            new_name = f"{next_number:02d}-{hook}"
            fixes[hook_type].append((hook, new_name))
            seen_numbers.add(next_number)
            next_number += 1
    
    return fixes

def print_proposed_fixes(fixes):
    """Print proposed fixes"""
    print("\n\n🔧 PROPOSED FIXES:")
    print("=" * 60)
    
    for hook_type, renames in fixes.items():
        print(f"\n{hook_type}:")
        for old, new in renames:
            if old != new:
                print(f"  {old} → {new}")
            else:
                print(f"  {old} (no change)")

def apply_fixes(fixes):
    """Apply the fixes"""
    print("\n\n🚀 APPLYING FIXES...")
    
    for hook_type, renames in fixes.items():
        dir_path = f'.claude/hooks/{hook_type}'
        
        # First pass: rename to temp names to avoid conflicts
        temp_renames = []
        for old, new in renames:
            if old != new:
                old_path = os.path.join(dir_path, old)
                temp_name = f"TEMP_{old}"
                temp_path = os.path.join(dir_path, temp_name)
                
                if os.path.exists(old_path):
                    shutil.move(old_path, temp_path)
                    temp_renames.append((temp_name, new))
                    print(f"  Staged: {old} → {temp_name}")
        
        # Second pass: rename from temp to final
        for temp, new in temp_renames:
            temp_path = os.path.join(dir_path, temp)
            new_path = os.path.join(dir_path, new)
            
            if os.path.exists(temp_path):
                shutil.move(temp_path, new_path)
                print(f"  ✅ Renamed: {temp} → {new}")

def update_config(fixes, config):
    """Update config.json with all hooks"""
    print("\n\n📝 UPDATING CONFIG...")
    
    # Build new config structure
    for hook_type, renames in fixes.items():
        if hook_type not in config['hooks']:
            config['hooks'][hook_type] = []
        
        # Get current config entries by script name
        current_entries = {entry['script']: entry for entry in config['hooks'][hook_type]}
        
        # Build new list with all hooks
        new_entries = []
        for old, new in sorted(renames, key=lambda x: x[1]):
            # Check if we have existing config
            if old in current_entries:
                entry = current_entries[old].copy()
                entry['script'] = new
            else:
                # Create new entry
                entry = {
                    'script': new,
                    'enabled': True,
                    'description': f"TODO: Add description for {new}"
                }
                
                # Try to infer purpose from filename
                if 'sync' in new:
                    entry['critical'] = True
                elif 'log' in new or 'metric' in new:
                    entry['critical'] = False
                
            new_entries.append(entry)
        
        config['hooks'][hook_type] = new_entries
    
    # Write updated config
    with open('.claude/hooks/config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Config updated with all hooks")

def main():
    """Main function"""
    print("🚀 CLAUDE HOOKS ANALYZER AND FIXER")
    print("=" * 60)
    
    # Change to project directory
    os.chdir('.')
    
    # Analyze
    hook_dirs, issues, config = analyze_hooks()
    print_analysis(hook_dirs, issues)
    
    # Propose fixes
    fixes = propose_fixes(hook_dirs, issues)
    print_proposed_fixes(fixes)
    
    # Ask for confirmation
    print("\n" + "=" * 60)
    response = input("\nApply these fixes? (y/n): ")
    
    if response.lower() == 'y':
        apply_fixes(fixes)
        update_config(fixes, config)
        print("\n✅ ALL FIXES APPLIED!")
        
        # Final check
        print("\n\n📋 FINAL STATE:")
        hook_dirs, issues, _ = analyze_hooks()
        for hook_type, hooks in hook_dirs.items():
            print(f"\n{hook_type}:")
            for hook in sorted(hooks):
                print(f"  - {hook}")
    else:
        print("\n❌ Fixes cancelled")

if __name__ == "__main__":
    main()
