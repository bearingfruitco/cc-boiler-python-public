#!/usr/bin/env python3
"""
Next Command Suggester - Provides contextual next step suggestions after every command
Enhances workflow by guiding users to the logical next action
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Command flow mappings
COMMAND_FLOWS = {
    # Task Ledger Management
    'task-ledger': {
        'view': [
            {'cmd': '/pt {feature}', 'reason': 'Process tasks for active feature'},
            {'cmd': '/fw start {issue}', 'reason': 'Start work on pending feature'},
            {'cmd': '/ws', 'reason': 'See detailed work status'}
        ],
        'empty': [
            {'cmd': '/tl generate', 'reason': 'Generate ledger from existing tasks'},
            {'cmd': '/gt {feature}', 'reason': 'Create new tasks for tracking'}
        ]
    },
    
    # Project Initialization
    'init-project': [
        {'cmd': '/py-prd {project}', 'reason': 'Define project requirements'},
        {'cmd': '/gi PROJECT', 'reason': 'Generate initial issues'},
        {'cmd': '/checkpoint', 'reason': 'Save initial setup'}
    ],
    
    # Issue & Task Creation Flow
    'capture-to-issue': {
        'complex': [
            {'cmd': '/prp {feature}', 'reason': 'Complex feature - research recommended'},
            {'cmd': '/think-through "{title}"', 'reason': 'Explore architecture options'}
        ],
        'standard': [
            {'cmd': '/gt {feature}', 'reason': 'Generate detailed task breakdown'},
            {'cmd': '/fw start {issue}', 'reason': 'Start working immediately'}
        ]
    },
    'generate-tasks': {
        'orchestratable': [
            {'cmd': '/tl view {feature}', 'reason': 'View task tracking in ledger'},
            {'cmd': '/orch {feature} --agents={count}', 'reason': 'Save {time} with parallel execution'},
            {'cmd': '/fw start {issue}', 'reason': 'Process tasks sequentially'}
        ],
        'simple': [
            {'cmd': '/tl view {feature}', 'reason': 'View task tracking in ledger'},
            {'cmd': '/fw start {issue}', 'reason': 'Begin implementation'},
            {'cmd': '/pt {feature}', 'reason': 'Process tasks immediately'}
        ]
    },
    'feature-workflow': {
        'start': {
            'no_tasks': [
                {'cmd': '/gt {feature}', 'reason': 'No tasks found - generate them first'},
                {'cmd': '/cti "{title}" --tests', 'reason': 'Capture requirements to issue'}
            ],
            'has_tasks': [
                {'cmd': '/pt {feature}', 'reason': 'Process {count} tasks systematically'},
                {'cmd': '/orch {feature}', 'reason': 'Use multi-agent for faster completion'}
            ]
        },
        'complete': [
            {'cmd': '/test', 'reason': 'Verify all tests pass'},
            {'cmd': '/pr-feedback', 'reason': 'Create pull request'},
            {'cmd': '/ws', 'reason': 'Check for other work'}
        ]
    },
    'process-tasks': {
        'completed': [
            {'cmd': '/test', 'reason': 'Run test suite'},
            {'cmd': '/grade', 'reason': 'Check implementation quality'},
            {'cmd': '/fw complete {issue}', 'reason': 'Mark feature complete'}
        ],
        'blocked': [
            {'cmd': '/mt "{blocker}"', 'reason': 'Create micro-task for blocker'},
            {'cmd': '/think-through "{problem}"', 'reason': 'Get AI help with the issue'},
            {'cmd': '/research "{topic}"', 'reason': 'Research the blocking topic'}
        ],
        'in_progress': [
            {'cmd': '/pt --continue', 'reason': 'Continue with next task'},
            {'cmd': '/checkpoint', 'reason': 'Save progress'},
            {'cmd': '/ts', 'reason': 'Check task status'}
        ],
        'verification_failed': [
            {'cmd': '/verify --verbose', 'reason': 'See detailed verification output'},
            {'cmd': '/test', 'reason': 'Run tests to see failures'},
            {'cmd': '/debug', 'reason': 'Debug the implementation'}
        ]
    },
    'test-runner': {
        'passed': [
            {'cmd': '/verify', 'reason': 'Verify complete implementation'},
            {'cmd': '/fw complete {issue}', 'reason': 'All tests passing - complete feature'},
            {'cmd': '/coverage', 'reason': 'Check test coverage'},
            {'cmd': '/lint', 'reason': 'Run code quality checks'}
        ],
        'failed': [
            {'cmd': '/bt add "{test_failure}"', 'reason': 'Track test failure'},
            {'cmd': '/debug "{failing_test}"', 'reason': 'Debug the failure'},
            {'cmd': '/generate-tests --fix', 'reason': 'Update test expectations'}
        ]
    },
    'verify': {
        'passed': [
            {'cmd': '/fw complete {issue}', 'reason': 'Verification passed - complete feature'},
            {'cmd': '/pt --continue', 'reason': 'Continue with next task'},
            {'cmd': '/checkpoint', 'reason': 'Save verified state'}
        ],
        'failed': [
            {'cmd': '/test --verbose', 'reason': 'See detailed test output'},
            {'cmd': '/verify --step {failed_step}', 'reason': 'Re-run failed verification step'},
            {'cmd': '/debug', 'reason': 'Debug the failures'}
        ]
    },
    'py-prd': [
        {'cmd': '/gi {feature}', 'reason': 'Create GitHub issues from PRD'},
        {'cmd': '/think-through architecture', 'reason': 'Design system architecture'},
        {'cmd': '/cti "{title}" --prd={name}', 'reason': 'Capture implementation plan'}
    ],
    'generate-issues': [
        {'cmd': '/fw start {first_issue}', 'reason': 'Start with first issue'},
        {'cmd': '/task-board', 'reason': 'View all generated issues'},
        {'cmd': '/gt {first_feature}', 'reason': 'Generate tasks for first feature'}
    ],
    'micro-task': [
        {'cmd': '/test', 'reason': 'Verify the fix works'},
        {'cmd': '/commit-review', 'reason': 'Review before committing'},
        {'cmd': '/checkpoint', 'reason': 'Save quick fix'}
    ],
    'bug-track': {
        'add': [
            {'cmd': '/generate-tests {bug_name}', 'reason': 'Create test to reproduce bug'},
            {'cmd': '/bt assign {id}', 'reason': 'Assign bug to yourself'},
            {'cmd': '/fw start bug-{id}', 'reason': 'Start bug fix workflow'}
        ],
        'resolve': [
            {'cmd': '/test', 'reason': 'Verify bug is fixed'},
            {'cmd': '/bt close {id}', 'reason': 'Close the bug'},
            {'cmd': '/ws', 'reason': 'Check for other work'}
        ]
    },
    'think-through': [
        {'cmd': '/cti "{solution}"', 'reason': 'Capture the solution as issue'},
        {'cmd': '/prp {topic}', 'reason': 'Need deeper research'},
        {'cmd': '/py-prd {feature}', 'reason': 'Create formal requirements'}
    ],
    'prp-create': [
        {'cmd': '/prp-execute', 'reason': 'Begin research phase'},
        {'cmd': '/research-docs {topic}', 'reason': 'Find relevant documentation'},
        {'cmd': '/checkpoint', 'reason': 'Save research plan'}
    ],
    'prp-execute': [
        {'cmd': '/prp-status', 'reason': 'Check progress (wait 20 min)'},
        {'cmd': '/think-through "{question}"', 'reason': 'Explore specific aspect'},
        {'cmd': '/checkpoint', 'reason': 'Save research progress'}
    ],
    'prp-complete': [
        {'cmd': '/cti "{solution}"', 'reason': 'Create implementation issue'},
        {'cmd': '/py-prd {feature}', 'reason': 'Formalize requirements'},
        {'cmd': '/gt {feature}', 'reason': 'Break down into tasks'}
    ],
    'orchestrate-agents': [
        {'cmd': '/sas', 'reason': 'Check agent status'},
        {'cmd': '/ov', 'reason': 'View orchestration progress'},
        {'cmd': '/assign-tasks', 'reason': 'Distribute work to agents'}
    ],
    'py-agent': [
        {'cmd': '/generate-tests {agent_name}', 'reason': 'Create agent tests'},
        {'cmd': '/py-api /{agent_name}/query', 'reason': 'Create API endpoint for agent'},
        {'cmd': '/test agents/test_{agent_name}', 'reason': 'Run agent tests'}
    ],
    'sync-main': {
        'success': [
            {'cmd': '/test', 'reason': 'Verify tests still pass after merge'},
            {'cmd': '/pt --continue', 'reason': 'Continue current work'},
            {'cmd': '/bs', 'reason': 'Check branch status'}
        ],
        'conflict': [
            {'cmd': '/conflict-resolve', 'reason': 'Resolve merge conflicts'},
            {'cmd': '/think-through "merge strategy"', 'reason': 'Get help with conflicts'}
        ]
    },
    'checkpoint': [
        {'cmd': '/bs', 'reason': 'Review branch status'},
        {'cmd': '/handoff-prep', 'reason': 'Prepare handoff notes'},
        {'cmd': '/todo list', 'reason': 'Review remaining tasks'}
    ],
    'work-status': [
        {'cmd': '/tl', 'reason': 'View task ledger for all features'},
        {'cmd': '/pt {feature}', 'reason': 'Continue current feature tasks'},
        {'cmd': '/checkpoint', 'reason': 'Save current progress'}
    ],
    'smart-resume': [
        {'cmd': '/tl', 'reason': 'View all active tasks'},
        {'cmd': '/ws', 'reason': 'Check detailed work status'},
        {'cmd': '/pt {feature}', 'reason': 'Continue where you left off'}
    ]
}

# Decision context suggestions - when user might be unsure
DECISION_CONTEXTS = {
    'starting_new': [
        {'cmd': '/init-project', 'reason': 'Brand new project/repository'},
        {'cmd': '/py-prd {feature}', 'reason': 'New feature with requirements'},
        {'cmd': '/prp {topic}', 'reason': 'Complex problem needing research'}
    ],
    'have_ai_suggestion': [
        {'cmd': '/cti "{title}"', 'reason': 'Capture AI solution to issue'},
        {'cmd': '/think-through', 'reason': 'Need more analysis'},
        {'cmd': '/prp {topic}', 'reason': 'Requires research'}
    ],
    'found_bug': [
        {'cmd': '/bt add "{description}"', 'reason': 'Track the bug'},
        {'cmd': '/mt "{quick_fix}"', 'reason': 'Fix immediately (< 30 min)'},
        {'cmd': '/generate-tests', 'reason': 'Create test to reproduce'}
    ],
    'need_breakdown': [
        {'cmd': '/gt {feature}', 'reason': 'Generate detailed tasks'},
        {'cmd': '/gi {project}', 'reason': 'Create GitHub issues from PRD'},
        {'cmd': '/think-through', 'reason': 'Analyze complexity first'}
    ]
}

# Time-based suggestions
TIME_BASED_SUGGESTIONS = {
    'morning': [
        {'cmd': '/sr', 'reason': 'Resume yesterday\'s work'},
        {'cmd': '/ws', 'reason': 'Check work status'},
        {'cmd': '/sync-main', 'reason': 'Get latest changes'}
    ],
    'evening': [
        {'cmd': '/checkpoint', 'reason': 'Save progress before leaving'},
        {'cmd': '/todo add "Continue {current_task}"', 'reason': 'Note for tomorrow'},
        {'cmd': '/handoff-prep', 'reason': 'Prepare handoff if needed'}
    ],
    'long_session': [
        {'cmd': '/checkpoint', 'reason': 'You\'ve been working for {hours}h - save progress'},
        {'cmd': '/test', 'reason': 'Good time to run tests'},
        {'cmd': '/bs', 'reason': 'Review branch health'}
    ]
}

def load_context() -> Dict:
    """Load current context from various sources."""
    context = {
        'workflow_state': {},
        'branch_registry': {},
        'current_issue': None,
        'current_feature': None,
        'session_start': None
    }
    
    # Load workflow state
    workflow_file = Path('.claude/context/workflow_state.json')
    if workflow_file.exists():
        try:
            context['workflow_state'] = json.loads(workflow_file.read_text())
            context['current_issue'] = context['workflow_state'].get('current_issue')
            context['current_feature'] = context['workflow_state'].get('current_task')
        except:
            pass
    
    # Load branch registry
    branch_file = Path('.claude/branch-registry.json')
    if branch_file.exists():
        try:
            context['branch_registry'] = json.loads(branch_file.read_text())
        except:
            pass
    
    # Get session duration
    try:
        # This would need to track when session started
        context['session_duration_hours'] = 0  # Placeholder
    except:
        pass
    
    return context

def extract_command_result(input_data: Dict) -> Tuple[str, Dict]:
    """Extract command name and result from input data."""
    tool = input_data.get('tool', '')
    args = input_data.get('args', {})
    result = input_data.get('result', {})
    
    # Map tool names to command names
    if tool == 'str_replace_editor':
        # Check if it's a command file being edited
        path = args.get('path', '')
        if '.claude/commands/' in path:
            return 'command_edit', result
    
    # Extract command from execute_command
    if 'command' in args:
        cmd_line = args['command']
        if cmd_line.startswith('/'):
            parts = cmd_line.split()
            cmd_name = parts[0][1:]  # Remove leading /
            return cmd_name, result
    
    return tool, result

def analyze_command_result(cmd_name: str, result: Dict, context: Dict) -> str:
    """Analyze command result to determine suggestion context."""
    # Check for specific patterns in output
    output = str(result.get('output', ''))
    
    # Check for decision contexts in output
    output_lower = output.lower()
    
    # New project/feature indicators
    if any(word in output_lower for word in ['new project', 'new feature', 'starting', 'initialize']):
        return 'starting_new'
    
    # AI suggestion indicators
    if any(word in output_lower for word in ['implementation plan', 'solution:', 'approach:', 'claude suggests']):
        return 'have_ai_suggestion'
    
    # Bug indicators
    if any(word in output_lower for word in ['bug', 'error', 'broken', 'failing', 'exception']):
        return 'found_bug'
    
    # Complexity indicators
    if any(word in output_lower for word in ['complex', 'research', 'figure out', 'investigate', 'unknown']):
        return 'complex'
    
    # Task generation
    if cmd_name == 'generate-tasks':
        if 'orchestration recommended' in output_lower:
            return 'orchestratable'
        return 'simple'
    
    # Feature workflow
    if cmd_name == 'feature-workflow':
        if 'start' in str(result):
            if 'no tasks found' in output.lower():
                return 'start.no_tasks'
            return 'start.has_tasks'
        if 'complete' in str(result):
            return 'complete'
    
    # Process tasks
    if cmd_name == 'process-tasks':
        if 'completed' in output.lower() or 'all tasks done' in output.lower():
            return 'completed'
        if 'blocked' in output.lower():
            return 'blocked'
        if 'verification failed' in output.lower():
            return 'verification_failed'
        return 'in_progress'
    
    # Test runner
    if cmd_name in ['test-runner', 'test']:
        if 'passed' in output.lower() and 'failed: 0' in output.lower():
            return 'passed'
        if 'failed' in output.lower():
            return 'failed'
    
    # Verification
    if cmd_name == 'verify':
        if 'verification complete' in output.lower() and 'all checks passed' in output.lower():
            return 'passed'
        if 'verification failed' in output.lower() or 'checks did not pass' in output.lower():
            return 'failed'
    
    # Sync main
    if cmd_name == 'sync-main':
        if 'conflict' in output.lower():
            return 'conflict'
        return 'success'
    
    # Capture to issue
    if cmd_name == 'capture-to-issue':
        if any(word in output.lower() for word in ['complex', 'research', 'investigate']):
            return 'complex'
        return 'standard'
    
    return 'default'

def extract_variables_from_output(output: str, context: Dict) -> Dict:
    """Extract variables from command output for suggestion formatting."""
    variables = {
        'issue': context.get('current_issue', 'ISSUE'),
        'feature': context.get('current_feature', 'FEATURE'),
        'title': 'TITLE',
        'count': '?',
        'time': '?h',
        'hours': '?'
    }
    
    # Extract issue number
    issue_match = re.search(r'#(\d+)', output)
    if issue_match:
        variables['issue'] = issue_match.group(1)
    
    # Extract feature name
    feature_match = re.search(r'feature[:/]([^\s]+)', output)
    if feature_match:
        variables['feature'] = feature_match.group(1)
    
    # Extract counts
    count_match = re.search(r'(\d+)\s+tasks?', output)
    if count_match:
        variables['count'] = count_match.group(1)
    
    # Extract agent count for orchestration
    agent_match = re.search(r'(\d+)\s+agents?', output)
    if agent_match:
        variables['count'] = agent_match.group(1)
    
    # Time estimates
    time_match = re.search(r'save\s+(\d+\.?\d*)\s*hours?', output)
    if time_match:
        variables['time'] = f"{time_match.group(1)}h"
    
    return variables

def get_time_based_suggestions(context: Dict) -> List[Dict]:
    """Get suggestions based on time of day and session duration."""
    suggestions = []
    current_hour = datetime.now().hour
    
    if current_hour < 10:
        return TIME_BASED_SUGGESTIONS.get('morning', [])
    elif current_hour > 17:
        return TIME_BASED_SUGGESTIONS.get('evening', [])
    
    # Long session check
    session_hours = context.get('session_duration_hours', 0)
    if session_hours > 3:
        return TIME_BASED_SUGGESTIONS.get('long_session', [])
    
    return []

def format_suggestions(suggestions: List[Dict], variables: Dict, limit: int = 3, context_type: str = None) -> str:
    """Format suggestions for display."""
    if not suggestions:
        return ""
    
    output = "\n💡 **Next steps:**\n"
    
    # Add decision helper if in decision context
    if context_type in DECISION_CONTEXTS:
        output = "\n🎯 **Decision Guide:**\n"
        if context_type == 'starting_new':
            output += "Starting something new? Choose based on:\n"
        elif context_type == 'have_ai_suggestion':
            output += "AI gave you a solution? Choose based on:\n"
        elif context_type == 'found_bug':
            output += "Found a bug? Choose based on:\n"
        elif context_type == 'complex':
            output += "Complex problem? Choose based on:\n"
    
    # Take top suggestions
    for i, suggestion in enumerate(suggestions[:limit], 1):
        cmd = suggestion['cmd']
        reason = suggestion['reason']
        
        # Replace variables
        for var, value in variables.items():
            cmd = cmd.replace(f'{{{var}}}', str(value))
            reason = reason.replace(f'{{{var}}}', str(value))
        
        output += f"  {i}. `{cmd}` - {reason}\n"
    
    # Add help section if user might be stuck
    if len(suggestions) > limit:
        output += f"\n📚 More options: ({len(suggestions) - limit} additional suggestions available)\n"
    
    # Enhanced help section with decision guide
    output += "\n🤔 Need help deciding?\n"
    output += "  • `/help decide` - When to use what command\n"
    output += "  • `/workflow-guide` - See complete workflows\n"
    output += "  • `/think-through "what should I do?"` - Get AI guidance\n"
    
    return output

def load_suggestion_config() -> Dict:
    """Load suggestion configuration."""
    config_file = Path('.claude/suggestions-config.json')
    if config_file.exists():
        try:
            return json.loads(config_file.read_text())
        except:
            pass
    return {
        'enabled': True,
        'suggestion_limit': 3,
        'show_help_section': True,
        'skip_commands': []
    }

def should_show_suggestions(cmd_name: str, result: Dict, config: Dict) -> bool:
    """Determine if suggestions should be shown for this command."""
    # Check if enabled
    if not config.get('enabled', True):
        return False
    
    # Check skip list from config
    skip_commands = config.get('skip_commands', [])
    if cmd_name in skip_commands:
        return False
    
    # Don't show if command failed
    if result.get('exit_code', 0) != 0:
        return False
    
    return True

def main():
    """Main hook logic."""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Load config
    config = load_suggestion_config()
    
    # Extract command and result
    cmd_name, result = extract_command_result(input_data)
    
    # Check if we should show suggestions
    if not should_show_suggestions(cmd_name, result, config):
        sys.exit(0)
        return
    
    # Load context
    context = load_context()
    
    # Analyze command result
    result_type = analyze_command_result(cmd_name, result, context)
    
    # Get base suggestions
    suggestions = []
    
    # Check for specific command flows
    if cmd_name in COMMAND_FLOWS:
        flow = COMMAND_FLOWS[cmd_name]
        if isinstance(flow, dict) and result_type in flow:
            suggestions = flow[result_type]
        elif isinstance(flow, list):
            suggestions = flow
    
    # Check for decision contexts if no specific suggestions
    if not suggestions and result_type in DECISION_CONTEXTS:
        suggestions = DECISION_CONTEXTS[result_type]
    
    # Add time-based suggestions if enabled and no specific suggestions
    if not suggestions and config.get('time_based_suggestions', True):
        suggestions = get_time_based_suggestions(context)
    
    # Extract variables from output
    output = str(result.get('output', ''))
    variables = extract_variables_from_output(output, context)
    
    # Format and display suggestions
    if suggestions:
        limit = config.get('suggestion_limit', 3)
        # Pass context type for decision guide formatting
        context_type = result_type if result_type in DECISION_CONTEXTS else None
        suggestion_text = format_suggestions(suggestions, variables, limit, context_type)
        if suggestion_text:
            print(suggestion_text, file=sys.stderr)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
