#!/usr/bin/env python3
"""
Design System Enforcement Hook - Block non-compliant code before it's written
Enhanced with Suggestion Engine for educational feedback
Ensures all code follows the strict 4-size, 2-weight design system
"""

import json
import sys
import os
import re
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.suggestion_engine import SuggestionEngine
    USE_SUGGESTION_ENGINE = True
except ImportError:
    USE_SUGGESTION_ENGINE = False

def get_config():
    """Load hook configuration"""
    config_path = Path(__file__).parent.parent / 'config.json'
    with open(config_path) as f:
        return json.load(f)

def is_component_file(file_path):
    """Check if this is a component file that needs design validation"""
    component_extensions = ['.tsx', '.jsx', '.vue', '.svelte']
    ignore_paths = ['node_modules', '.next', 'dist', 'build']
    
    # Check if it's a component file
    if not any(file_path.endswith(ext) for ext in component_extensions):
        return False
    
    # Ignore certain paths
    if any(ignore in file_path for ignore in ignore_paths):
        return False
    
    return True

def find_violations_legacy(content, config):
    """Legacy violation detection (fallback when suggestion engine not available)"""
    violations = {
        'critical': [],
        'warnings': []
    }
    
    design_rules = config.get('design_system', config.get('designSystem', {}))
    
    # Check for forbidden font sizes
    forbidden_sizes = r'(?:className|class)=["\'][^"\']*\b(?:text-(?:xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl))\b'
    for match in re.finditer(forbidden_sizes, content):
        violations['critical'].append({
            'type': 'font-size',
            'line': content[:match.start()].count('\n') + 1,
            'match': match.group(),
            'fix': suggest_font_size_fix(match.group())
        })
    
    # Check for forbidden font weights
    forbidden_weights = r'(?:className|class)=["\'][^"\']*\b(?:font-(?:thin|extralight|light|normal|medium|bold|extrabold|black))\b'
    for match in re.finditer(forbidden_weights, content):
        violations['critical'].append({
            'type': 'font-weight',
            'line': content[:match.start()].count('\n') + 1,
            'match': match.group(),
            'fix': suggest_font_weight_fix(match.group())
        })
    
    # Check for non-grid spacing
    spacing_rules = design_rules.get('rules', {}).get('spacing', {})
    spacing_grid = spacing_rules.get('grid', 4)
    
    spacing_pattern = r'(?:className|class)=["\'][^"\']*\b(?:p|m|gap|space-[xy])-(\d+)\b'
    for match in re.finditer(spacing_pattern, content):
        value = int(match.group(1))
        if value % spacing_grid != 0:
            violations['critical'].append({
                'type': 'spacing',
                'line': content[:match.start()].count('\n') + 1,
                'match': match.group(),
                'value': value,
                'fix': suggest_spacing_fix(value)
            })
    
    # Check for small touch targets (buttons, links)
    mobile_rules = design_rules.get('rules', {}).get('mobile', {})
    min_touch_target = mobile_rules.get('minTouchTarget', 44)
    
    touch_pattern = r'<(?:button|a|Button|Link)[^>]*(?:className|class)=["\'][^"\']*\b(?:h|height)-(\d+)\b'
    for match in re.finditer(touch_pattern, content, re.IGNORECASE):
        height = int(match.group(1)) * 4  # Tailwind units to pixels
        if height < min_touch_target:
            violations['warnings'].append({
                'type': 'touch-target',
                'line': content[:match.start()].count('\n') + 1,
                'match': match.group(),
                'current': height,
                'minimum': min_touch_target
            })
    
    return violations

def suggest_font_size_fix(match):
    """Suggest replacement for forbidden font size"""
    size_map = {
        'text-xs': 'text-size-4',
        'text-sm': 'text-size-4',
        'text-base': 'text-size-3',
        'text-lg': 'text-size-2',
        'text-xl': 'text-size-2',
        'text-2xl': 'text-size-1',
        'text-3xl': 'text-size-1',
        'text-4xl': 'text-size-1',
        'text-5xl': 'text-size-1',
        'text-6xl': 'text-size-1'
    }
    
    for old, new in size_map.items():
        if old in match:
            return match.replace(old, new)
    
    return match

def suggest_font_weight_fix(match):
    """Suggest replacement for forbidden font weight"""
    weight_map = {
        'font-thin': 'font-regular',
        'font-extralight': 'font-regular',
        'font-light': 'font-regular',
        'font-normal': 'font-regular',
        'font-medium': 'font-semibold',
        'font-bold': 'font-semibold',
        'font-extrabold': 'font-semibold',
        'font-black': 'font-semibold'
    }
    
    for old, new in weight_map.items():
        if old in match:
            return match.replace(old, new)
    
    return match

def suggest_spacing_fix(value):
    """Suggest nearest valid spacing value"""
    grid = 4
    if value % grid == 0:
        return value
    
    # Find nearest multiple of 4
    lower = (value // grid) * grid
    upper = lower + grid
    
    # Return closer value
    if value - lower < upper - value:
        return lower
    return upper

def format_violations_message_legacy(violations):
    """Format violations into a readable message (legacy)"""
    if not violations['critical'] and not violations['warnings']:
        return None
    
    message = "🚨 DESIGN SYSTEM VIOLATIONS DETECTED\n\n"
    
    if violations['critical']:
        message += "❌ CRITICAL (must fix):\n"
        for v in violations['critical'][:5]:  # Show first 5
            message += f"  Line {v['line']}: {v['type']} - {v['match']}\n"
            if 'fix' in v:
                if isinstance(v['fix'], str):
                    message += f"    → Fix: {v['fix']}\n"
                elif v['type'] == 'spacing':
                    message += f"    → Use: {v['fix'] // 4} (multiple of 4)\n"
        
        if len(violations['critical']) > 5:
            message += f"  ... and {len(violations['critical']) - 5} more\n"
    
    if violations['warnings']:
        message += "\n⚠️ WARNINGS:\n"
        for v in violations['warnings'][:3]:
            if v['type'] == 'touch-target':
                message += f"  Line {v['line']}: Touch target only {v['current']}px (min: {v['minimum']}px)\n"
    
    message += "\n📚 Design Rules:\n"
    message += "  • Font sizes: text-size-1, text-size-2, text-size-3, text-size-4\n"
    message += "  • Font weights: font-regular, font-semibold\n"
    message += "  • Spacing: multiples of 4 (p-1, p-2, p-3, p-4, p-6, p-8...)\n"
    message += "  • Touch targets: minimum 44px (h-11)\n"
    
    return message

def main():
    """Main hook logic with enhanced suggestion engine"""
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    # Only process file write operations
    if input_data['tool'] not in ['write_file', 'edit_file', 'str_replace']:
        print(json.dumps({"action": "continue"}))
        return
    
    file_path = input_data.get('path', '')
    
    # Only validate component files
    if not is_component_file(file_path):
        print(json.dumps({"action": "continue"}))
        return
    
    config = get_config()
    content = input_data.get('content', '')
    
    # Use enhanced suggestion engine if available and enabled
    if USE_SUGGESTION_ENGINE and config.get('features', {}).get('suggestion_engine', True):
        engine = SuggestionEngine()
        violations = engine.find_violations(content, file_path)
        
        if violations:
            # Format message with suggestions
            message = "🚨 DESIGN SYSTEM VIOLATIONS DETECTED\n"
            message += f"\n📍 Found {len(violations)} violation(s) in {file_path}\n"
            
            # Group by category
            by_category = {}
            for v in violations:
                category = v['category']
                if category not in by_category:
                    by_category[category] = []
                by_category[category].append(v)
            
            # Show violations by category
            for category, cat_violations in by_category.items():
                message += f"\n{category.upper()} ({len(cat_violations)} issues):\n"
                for v in cat_violations[:3]:  # Show first 3 per category
                    message += engine.format_violation_message(v)
                
                if len(cat_violations) > 3:
                    message += f"\n... and {len(cat_violations) - 3} more {category} violations\n"
            
            # Track violations for analytics
            for v in violations:
                engine.track_violation(v)
            
            # Show common mistakes
            common = engine.get_common_mistakes(3)
            if common:
                message += "\n📊 Your Most Common Violations:\n"
                for mistake in common:
                    message += f"  • '{mistake['text']}' ({mistake['count']} times) → Use: {mistake['suggestion']}\n"
            
            # Get category stats
            stats = engine.get_category_stats()
            if stats:
                message += "\n📈 Violation Categories:\n"
                for category, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
                    message += f"  • {category}: {count} total violations\n"
            
            # Auto-fix suggestions
            message += "\n🔧 AUTO-FIX AVAILABLE:\n"
            message += "These violations can be automatically fixed. The suggested replacements follow our design system.\n"
            
            # Create response
            response = {
                "action": "block",
                "message": message,
                "violations_count": len(violations),
                "categories": list(by_category.keys())
            }
            
            # If config allows auto-fix, provide fixed content
            design_config = config.get('design_system', config.get('designSystem', {}))
            if design_config.get('auto_fix', False):
                # Apply fixes
                fixed_content = content
                for v in violations:
                    fixed_content = fixed_content.replace(v['matched_text'], v['suggestion'])
                
                response["action"] = "suggest_fix"
                response["fixed_content"] = fixed_content
                response["fix_description"] = f"Auto-fixed {len(violations)} design violations"
            
            print(json.dumps(response))
            return
    
    # Fallback to legacy violation detection
    violations = find_violations_legacy(content, config)
    
    if violations['critical'] or violations['warnings']:
        message = format_violations_message_legacy(violations)
        
        # Create response
        response = {
            "action": "block",
            "message": message,
            "violations": violations
        }
        
        print(json.dumps(response))
    else:
        # No violations - continue
        print(json.dumps({"action": "continue"}))

if __name__ == "__main__":
    main()
