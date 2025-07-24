#!/usr/bin/env python3
"""
Implementation Guide - Intelligent pre-implementation analysis
Prevents duplicates, identifies overlaps, suggests better approaches
Embodies the "analyze, recommend, revise" pattern
"""

import json
import sys
import os
from pathlib import Path
import re
from difflib import SequenceMatcher

class ImplementationGuide:
    def __init__(self):
        self.project_root = Path.cwd()
        self.claude_dir = self.project_root / '.claude'
        
        # What NOT to duplicate (existing systems)
        self.existing_systems = {
            'state_tracking': {
                'handled_by': ['01-state-save.py', '/checkpoint', 'GitHub gists'],
                'files': ['.claude/context/state.json', '.claude/checkpoints/'],
                'avoid': ['session tracking', 'state files', 'context persistence']
            },
            'change_tracking': {
                'handled_by': ['/change-log', 'git integration'],
                'files': ['.claude/commands/change-log.md'],
                'avoid': ['change detection', 'modification tracking', 'diff logging']
            },
            'documentation_sync': {
                'handled_by': ['/change-log sync-docs', 'auto-updates'],
                'files': ['docs/', 'CHANGELOG.md'],
                'avoid': ['doc sync checking', 'automated doc updates']
            },
            'design_enforcement': {
                'handled_by': ['02-design-check.py', 'suggestion_engine.py'],
                'files': ['.claude/hooks/pre-tool-use/02-design-check.py'],
                'avoid': ['design validation', 'CSS checking']
            },
            'quality_checks': {
                'handled_by': ['various hooks', '/validate-design'],
                'files': ['.claude/hooks/'],
                'avoid': ['general quality validation']
            }
        }
        
        # Common implementation patterns
        self.patterns = {
            'enhanced_duplicate': r'(.+)[-_](?:enhanced|improved|new|v2|updated|better)(\.\w+)$',
            'numbered_duplicate': r'(.+?)[-_]?(\d+)(\.\w+)$',
            'backup_file': r'(.+)\.(?:backup|old|orig|original)$',
            'temporary_file': r'(.+)\.(?:tmp|temp|draft)$'
        }
        
        # Files that should be updated together
        self.update_groups = {
            'version_bump': [
                '.claude/config.json',
                'package.json',
                'NEW_CHAT_CONTEXT.md'
            ],
            'new_hook': [
                'CHANGELOG.md',
                '.claude/hooks/README.md'
            ],
            'new_command': [
                'QUICK_REFERENCE.md',
                'CHANGELOG.md'
            ]
        }
    
    def analyze_implementation(self, tool_data):
        """Main analysis - the "check your work before you work" approach"""
        tool = tool_data.get('tool', '')
        path = tool_data.get('path', '')
        content = tool_data.get('content', '')
        
        analysis = {
            'recommendations': [],
            'warnings': [],
            'existing_solutions': [],
            'better_approaches': []
        }
        
        if not path or tool not in ['write_file', 'edit_file', 'str_replace']:
            return analysis
        
        # 1. Check for potential duplicates
        self._check_duplicates(path, analysis)
        
        # 2. Check for overlapping functionality
        self._check_overlaps(path, content, analysis)
        
        # 3. Suggest better approaches
        self._suggest_improvements(path, content, analysis)
        
        # 4. Identify required updates
        self._identify_updates(path, content, analysis)
        
        # 5. Prevent over-engineering
        self._check_complexity(path, content, analysis)
        
        return analysis
    
    def _check_duplicates(self, path, analysis):
        """Check if this might be a duplicate of an existing file"""
        target = Path(path)
        target_name = target.stem
        target_dir = target.parent
        
        # Check for enhanced/numbered patterns
        for pattern_name, pattern in self.patterns.items():
            match = re.match(pattern, target.name)
            if match and pattern_name in ['enhanced_duplicate', 'numbered_duplicate']:
                base_name = match.group(1)
                extension = match.group(2) if pattern_name == 'enhanced_duplicate' else match.group(3)
                
                # Look for the original
                original = target_dir / f"{base_name}{extension}"
                if original.exists():
                    analysis['warnings'].append({
                        'type': 'potential_duplicate',
                        'severity': 'high',
                        'message': f"This looks like a duplicate of {original}",
                        'suggestion': f"Update {original} instead of creating {target.name}",
                        'example': "Use edit_file or str_replace to modify the existing file"
                    })
                    return
        
        # Check for similar files
        if target_dir.exists():
            for existing in target_dir.iterdir():
                if existing.is_file() and existing != target:
                    similarity = SequenceMatcher(None, target_name, existing.stem).ratio()
                    if similarity > 0.8:
                        analysis['warnings'].append({
                            'type': 'similar_file',
                            'severity': 'medium',
                            'message': f"Similar file exists: {existing.name}",
                            'suggestion': "Consider if this functionality belongs there",
                            'similarity': f"{similarity*100:.0f}%"
                        })
    
    def _check_overlaps(self, path, content, analysis):
        """Check if this functionality already exists elsewhere"""
        # Analyze content for keywords
        content_lower = content.lower()
        
        for system, info in self.existing_systems.items():
            # Check if content suggests overlapping functionality
            for avoid_term in info['avoid']:
                if avoid_term in content_lower:
                    analysis['existing_solutions'].append({
                        'functionality': avoid_term,
                        'already_handled_by': info['handled_by'],
                        'message': f"We already have {system} handled by {info['handled_by'][0]}",
                        'suggestion': f"Use existing {info['handled_by'][0]} instead"
                    })
        
        # Check for specific patterns
        if 'session' in content_lower and 'track' in content_lower:
            analysis['existing_solutions'].append({
                'functionality': 'session tracking',
                'already_handled_by': ['GitHub gists', '01-state-save.py'],
                'message': "Session state is saved to GitHub every 60 seconds",
                'suggestion': "Use /checkpoint or rely on auto-save instead"
            })
    
    def _suggest_improvements(self, path, content, analysis):
        """Suggest better approaches based on the implementation"""
        # If creating a hook, check ordering
        if '/hooks/' in path and path.endswith('.py'):
            # Extract number prefix
            filename = Path(path).name
            match = re.match(r'^(\d+)-', filename)
            
            if match:
                number = int(match.group(1))
                hook_dir = Path(path).parent
                
                # Check for conflicts
                if hook_dir.exists():
                    existing_numbers = []
                    for hook in hook_dir.glob('*.py'):
                        hook_match = re.match(r'^(\d+)-', hook.name)
                        if hook_match:
                            existing_numbers.append(int(hook_match.group(1)))
                    
                    if number in existing_numbers:
                        # Suggest next available number
                        next_num = max(existing_numbers) + 1
                        analysis['better_approaches'].append({
                            'issue': f"Hook number {number} already exists",
                            'suggestion': f"Use {next_num:02d}- prefix instead",
                            'reason': "Prevents execution order conflicts"
                        })
        
        # If modifying core system files, suggest creating extension instead
        core_files = ['tailwind.config.js', 'next.config.js', 'tsconfig.json']
        if any(path.endswith(f) for f in core_files):
            analysis['better_approaches'].append({
                'issue': "Modifying core configuration",
                'suggestion': "Consider using extending pattern instead",
                'example': "Create tailwind.config.custom.js and import in main config"
            })
    
    def _identify_updates(self, path, content, analysis):
        """Identify other files that should be updated"""
        updates_needed = []
        
        # Check for version changes
        if '"version"' in content:
            updates_needed.extend(self.update_groups['version_bump'])
        
        # Check for new hooks
        if '/hooks/' in path and path.endswith('.py'):
            updates_needed.extend(self.update_groups['new_hook'])
        
        # Check for new commands
        if '/commands/' in path:
            updates_needed.extend(self.update_groups['new_command'])
        
        if updates_needed:
            # Filter to only existing files
            existing_updates = [f for f in set(updates_needed) if Path(f).exists()]
            
            if existing_updates:
                analysis['recommendations'].append({
                    'type': 'required_updates',
                    'message': "Remember to update these files:",
                    'files': existing_updates,
                    'reason': "Keeps documentation and configs in sync"
                })
    
    def _check_complexity(self, path, content, analysis):
        """Prevent over-engineering"""
        # Count complexity indicators
        complexity_indicators = {
            'class_definitions': len(re.findall(r'^class\s+\w+', content, re.MULTILINE)),
            'functions': len(re.findall(r'^def\s+\w+', content, re.MULTILINE)),
            'imports': len(re.findall(r'^import\s+|^from\s+', content, re.MULTILINE)),
            'lines': len(content.splitlines())
        }
        
        # Check for over-engineering
        if complexity_indicators['class_definitions'] > 3:
            analysis['warnings'].append({
                'type': 'complexity',
                'severity': 'low',
                'message': "This implementation might be over-engineered",
                'suggestion': "Consider splitting into smaller, focused modules",
                'metrics': complexity_indicators
            })
        
        # Check for reimplementing existing functionality
        if 'subprocess' in content and 'git' in content:
            analysis['existing_solutions'].append({
                'functionality': 'git operations',
                'already_handled_by': ['git integration in change-log'],
                'message': "Git operations are already abstracted",
                'suggestion': "Use existing git utilities instead"
            })


def format_analysis(analysis):
    """Format the analysis into helpful guidance"""
    if not any(analysis.values()):
        return None
    
    message = "🤔 IMPLEMENTATION ANALYSIS\n\n"
    
    # Warnings (most important)
    if analysis['warnings']:
        message += "⚠️  WARNINGS:\n"
        for warning in analysis['warnings']:
            message += f"• {warning['message']}\n"
            message += f"  → {warning['suggestion']}\n"
            if 'example' in warning:
                message += f"  Example: {warning['example']}\n"
            message += "\n"
    
    # Existing solutions
    if analysis['existing_solutions']:
        message += "🔄 EXISTING SOLUTIONS:\n"
        for solution in analysis['existing_solutions']:
            message += f"• {solution['functionality'].title()}: {solution['message']}\n"
            message += f"  → {solution['suggestion']}\n\n"
    
    # Better approaches
    if analysis['better_approaches']:
        message += "💡 BETTER APPROACHES:\n"
        for approach in analysis['better_approaches']:
            message += f"• {approach['issue']}\n"
            message += f"  → {approach['suggestion']}\n"
            if 'example' in approach:
                message += f"  Example: {approach['example']}\n"
            message += "\n"
    
    # Recommendations
    if analysis['recommendations']:
        message += "📝 RECOMMENDATIONS:\n"
        for rec in analysis['recommendations']:
            message += f"• {rec['message']}\n"
            if 'files' in rec:
                for file in rec['files']:
                    message += f"  - {file}\n"
            if 'reason' in rec:
                message += f"  Reason: {rec['reason']}\n"
            message += "\n"
    
    # Add philosophy reminder
    message += "💭 Remember: "
    message += "Revise your approach based on this analysis. "
    message += "The best implementation often updates existing code rather than adding new files.\n"
    
    return message


def main():
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Only analyze write operations
    if input_data['tool'] not in ['write_file', 'edit_file', 'str_replace']:
        sys.exit(0)
        return
    
    guide = ImplementationGuide()
    analysis = guide.analyze_implementation(input_data)
    
    message = format_analysis(analysis)
    
    if message:
        # Check severity
        has_high_warnings = any(
            w.get('severity') == 'high' 
            for w in analysis.get('warnings', [])
        )
        
        if has_high_warnings:
            # Block with recommendations
            response = {
                "decision": "block",
                "message": message,
                "analysis": analysis
            }
        else:
            # Warn but continue
            sys.exit(0)  # Continue normally
        
        print(json.dumps(response))
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
