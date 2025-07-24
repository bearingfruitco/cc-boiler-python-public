#!/usr/bin/env python3
"""
Knowledge Share Hook - Extract and share learnings with team
Builds collective knowledge base from individual sessions
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime

def extract_patterns(chat_history):
    """Extract reusable patterns from session"""
    patterns = {
        'components': extract_component_patterns(chat_history),
        'solutions': extract_problem_solutions(chat_history),
        'commands': extract_useful_commands(chat_history),
        'errors': extract_error_fixes(chat_history)
    }
    
    return patterns

def extract_component_patterns(chat_history):
    """Extract new component patterns created"""
    components = []
    
    for entry in chat_history:
        if entry.get('tool') == 'write_file':
            path = entry.get('path', '')
            if 'components/' in path and path.endswith('.tsx'):
                content = entry.get('content', '')
                
                # Extract component info
                component = {
                    'name': Path(path).stem,
                    'type': classify_component_type(path),
                    'props': extract_props(content),
                    'patterns': extract_patterns_used(content),
                    'design_compliant': check_design_compliance(content)
                }
                
                if component['design_compliant']:
                    components.append(component)
    
    return components

def classify_component_type(path):
    """Classify component based on path"""
    if '/ui/' in path:
        return 'ui'
    elif '/forms/' in path:
        return 'form'
    elif '/layout/' in path:
        return 'layout'
    elif '/features/' in path:
        return 'feature'
    return 'general'

def extract_props(content):
    """Extract TypeScript props from component"""
    props_match = re.search(r'interface\s+\w+Props\s*{([^}]+)}', content, re.DOTALL)
    if props_match:
        props_content = props_match.group(1)
        props = []
        
        for line in props_content.split('\n'):
            prop_match = re.match(r'\s*(\w+)(\?)?:\s*(.+?)(?:;|$)', line.strip())
            if prop_match:
                props.append({
                    'name': prop_match.group(1),
                    'required': prop_match.group(2) != '?',
                    'type': prop_match.group(3).strip()
                })
        
        return props
    return []

def extract_patterns_used(content):
    """Extract design patterns used in component"""
    patterns = []
    
    # Check for common patterns
    if 'useState' in content:
        patterns.append('state-management')
    if 'useEffect' in content:
        patterns.append('side-effects')
    if 'Container' in content or 'max-w-md' in content:
        patterns.append('responsive-container')
    if 'h-11' in content or 'h-12' in content:
        patterns.append('proper-touch-targets')
    if 'text-size-' in content:
        patterns.append('design-system-typography')
    
    return patterns

def check_design_compliance(content):
    """Quick check for design compliance"""
    violations = []
    
    # Check for forbidden classes
    if re.search(r'text-(xs|sm|lg|xl|2xl)', content):
        violations.append('invalid-font-size')
    if re.search(r'font-(bold|medium|light)', content):
        violations.append('invalid-font-weight')
    if re.search(r'[pm]-[57]', content):
        violations.append('invalid-spacing')
    
    return len(violations) == 0

def extract_problem_solutions(chat_history):
    """Extract problems solved during session"""
    solutions = []
    
    # Look for error messages followed by fixes
    for i, entry in enumerate(chat_history):
        message = str(entry.get('message', ''))
        
        # Common problem indicators
        if any(indicator in message.lower() for indicator in ['error', 'failed', 'issue', 'problem']):
            # Look for resolution in next few entries
            for j in range(i+1, min(i+5, len(chat_history))):
                next_entry = chat_history[j]
                next_message = str(next_entry.get('message', ''))
                
                if any(indicator in next_message.lower() for indicator in ['fixed', 'resolved', 'working', 'success']):
                    solutions.append({
                        'problem': message[:200],  # Truncate
                        'solution': next_message[:200],
                        'category': categorize_problem(message)
                    })
                    break
    
    return solutions

def categorize_problem(message):
    """Categorize type of problem"""
    message_lower = message.lower()
    
    if 'typescript' in message_lower or 'type' in message_lower:
        return 'typescript'
    elif 'design' in message_lower or 'style' in message_lower:
        return 'design-system'
    elif 'git' in message_lower or 'merge' in message_lower:
        return 'version-control'
    elif 'build' in message_lower or 'compile' in message_lower:
        return 'build'
    else:
        return 'general'

def extract_useful_commands(chat_history):
    """Extract useful command sequences"""
    commands = []
    
    for entry in chat_history:
        message = entry.get('message', '')
        if isinstance(message, str) and message.startswith('/'):
            # Extract command and context
            command_parts = message.split(' ', 1)
            command = command_parts[0]
            args = command_parts[1] if len(command_parts) > 1 else ''
            
            commands.append({
                'command': command,
                'args': args,
                'context': get_command_context(chat_history, entry)
            })
    
    # Group and count usage
    command_usage = {}
    for cmd in commands:
        key = cmd['command']
        if key not in command_usage:
            command_usage[key] = {'count': 0, 'contexts': []}
        command_usage[key]['count'] += 1
        if cmd['context'] not in command_usage[key]['contexts']:
            command_usage[key]['contexts'].append(cmd['context'])
    
    return command_usage

def get_command_context(chat_history, command_entry):
    """Get context for when command was used"""
    # Simplified - would analyze surrounding entries
    return 'general'

def extract_error_fixes(chat_history):
    """Extract error messages and their fixes"""
    error_fixes = []
    
    for i, entry in enumerate(chat_history):
        if entry.get('type') == 'error' or 'error' in str(entry.get('message', '')).lower():
            error_message = str(entry.get('message', ''))
            
            # Look for fix in next entries
            for j in range(i+1, min(i+5, len(chat_history))):
                if chat_history[j].get('tool') in ['write_file', 'edit_file']:
                    error_fixes.append({
                        'error': error_message[:200],
                        'fix_type': 'code-change',
                        'file': chat_history[j].get('path', '')
                    })
                    break
    
    return error_fixes

def update_knowledge_base(patterns):
    """Update team knowledge base with new learnings"""
    kb_path = Path(__file__).parent.parent.parent / 'team' / 'knowledge-base.json'
    
    # Load existing knowledge base
    if kb_path.exists():
        with open(kb_path) as f:
            kb = json.load(f)
    else:
        kb = {
            'components': [],
            'solutions': [],
            'command_patterns': {},
            'error_fixes': []
        }
    
    # Add new components
    for component in patterns['components']:
        if not any(c['name'] == component['name'] for c in kb['components']):
            kb['components'].append({
                **component,
                'added_by': get_current_user(),
                'added_on': datetime.now().isoformat()
            })
    
    # Add new solutions
    kb['solutions'].extend([
        {
            **solution,
            'added_by': get_current_user(),
            'added_on': datetime.now().isoformat()
        }
        for solution in patterns['solutions']
    ])
    
    # Update command patterns
    for cmd, usage in patterns['commands'].items():
        if cmd not in kb['command_patterns']:
            kb['command_patterns'][cmd] = {'total_uses': 0, 'contexts': []}
        kb['command_patterns'][cmd]['total_uses'] += usage['count']
        kb['command_patterns'][cmd]['contexts'].extend(usage['contexts'])
    
    # Save updated knowledge base
    with open(kb_path, 'w') as f:
        json.dump(kb, f, indent=2)
    
    return kb

def get_current_user():
    """Get current user"""
    config_path = Path(__file__).parent.parent.parent / 'team' / 'config.json'
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f).get('current_user', 'unknown')
    return 'unknown'

def generate_learning_summary(patterns, kb):
    """Generate summary of learnings to share"""
    summary = []
    
    if patterns['components']:
        summary.append(f"Created {len(patterns['components'])} reusable components")
    
    if patterns['solutions']:
        summary.append(f"Solved {len(patterns['solutions'])} problems")
    
    if patterns['commands']:
        most_used = max(patterns['commands'].items(), key=lambda x: x[1]['count'])
        summary.append(f"Most used command: {most_used[0]} ({most_used[1]['count']} times)")
    
    return summary

def create_github_discussion(patterns, summary):
    """Create GitHub discussion for significant learnings"""
    if not patterns['components'] and not patterns['solutions']:
        return  # Nothing significant to share
    
    title = f"Session Learnings - {datetime.now().strftime('%Y-%m-%d')}"
    body = f"""
## 🧠 Session Learnings

**Engineer**: {get_current_user()}
**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

### Summary
{' | '.join(summary)}

### New Components
"""
    
    for component in patterns['components'][:3]:  # Top 3
        body += f"""
#### `{component['name']}` ({component['type']})
- Props: {', '.join(p['name'] for p in component['props'])}
- Patterns: {', '.join(component['patterns'])}
"""
    
    if patterns['solutions']:
        body += "\n### Problems Solved\n"
        for solution in patterns['solutions'][:3]:
            body += f"""
**Problem**: {solution['problem']}
**Solution**: {solution['solution']}
**Category**: {solution['category']}

"""
    
    # Create discussion via GitHub CLI
    try:
        subprocess.run(
            f"gh discussion create --title '{title}' --body '{body}' --category 'Learnings'",
            shell=True,
            capture_output=True,
            text=True
        )
    except:
        pass  # Fail silently

def main():
    """Main hook logic"""
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    # Get chat history
    chat_history = input_data.get('history', [])
    
    # Extract patterns and learnings
    patterns = extract_patterns(chat_history)
    
    # Update knowledge base
    kb = update_knowledge_base(patterns)
    
    # Generate summary
    summary = generate_learning_summary(patterns, kb)
    
    # Create GitHub discussion for significant learnings
    create_github_discussion(patterns, summary)
    
    # Return response
    response = {
        "decision": "log",
        "message": f"📚 Knowledge shared: {' | '.join(summary) if summary else 'No new patterns detected'}"
    }
    
    print(json.dumps(response))

    sys.exit(0)

if __name__ == "__main__":
    main()
