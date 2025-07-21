#!/usr/bin/env python3
"""
Command Sequence Learner - Tracks and learns from command usage patterns
Part of the Next Command Suggestion System
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple

class CommandSequenceLearner:
    def __init__(self):
        self.data_file = Path('.claude/analytics/command-sequences.json')
        self.patterns_file = Path('.claude/analytics/learned-patterns.json')
        self.data = self.load_data()
        self.patterns = self.load_patterns()
    
    def load_data(self) -> Dict:
        """Load existing sequence data."""
        if self.data_file.exists():
            try:
                return json.loads(self.data_file.read_text())
            except:
                pass
        return {
            'sequences': [],
            'transitions': defaultdict(lambda: defaultdict(int)),
            'success_patterns': []
        }
    
    def load_patterns(self) -> Dict:
        """Load learned patterns."""
        if self.patterns_file.exists():
            try:
                return json.loads(self.patterns_file.read_text())
            except:
                pass
        return {
            'common_flows': {},
            'user_preferences': {},
            'success_sequences': []
        }
    
    def record_transition(self, from_cmd: str, to_cmd: str, context: Dict):
        """Record a command transition."""
        # Update transition counts
        if 'transitions' not in self.data:
            self.data['transitions'] = {}
        if from_cmd not in self.data['transitions']:
            self.data['transitions'][from_cmd] = {}
        if to_cmd not in self.data['transitions'][from_cmd]:
            self.data['transitions'][from_cmd][to_cmd] = 0
        
        self.data['transitions'][from_cmd][to_cmd] += 1
        
        # Record sequence
        sequence_entry = {
            'timestamp': datetime.now().isoformat(),
            'from': from_cmd,
            'to': to_cmd,
            'context': {
                'work_type': context.get('work_type'),
                'branch': context.get('branch'),
                'time_between': context.get('time_between_seconds', 0)
            }
        }
        
        if 'sequences' not in self.data:
            self.data['sequences'] = []
        self.data['sequences'].append(sequence_entry)
        
        # Keep only last 1000 sequences
        if len(self.data['sequences']) > 1000:
            self.data['sequences'] = self.data['sequences'][-1000:]
    
    def analyze_patterns(self):
        """Analyze sequences to find patterns."""
        # Find most common transitions
        common_transitions = {}
        
        for from_cmd, transitions in self.data.get('transitions', {}).items():
            if transitions:
                # Sort by frequency
                sorted_transitions = sorted(
                    transitions.items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )
                # Take top 3
                common_transitions[from_cmd] = [
                    {'command': cmd, 'frequency': count}
                    for cmd, count in sorted_transitions[:3]
                ]
        
        self.patterns['common_flows'] = common_transitions
        
        # Identify successful workflow patterns
        self.identify_success_patterns()
    
    def identify_success_patterns(self):
        """Identify patterns that lead to successful completions."""
        # Look for sequences ending in completion commands
        success_endings = ['fw complete', 'pr-feedback', 'test passed']
        success_sequences = []
        
        sequences = self.data.get('sequences', [])
        for i in range(len(sequences) - 3):
            # Check if sequence ends with success
            if any(ending in sequences[i+2].get('to', '') for ending in success_endings):
                pattern = [
                    sequences[i]['from'],
                    sequences[i]['to'],
                    sequences[i+1]['to'],
                    sequences[i+2]['to']
                ]
                success_sequences.append(pattern)
        
        # Count pattern frequencies
        pattern_counts = defaultdict(int)
        for pattern in success_sequences:
            pattern_key = ' -> '.join(pattern)
            pattern_counts[pattern_key] += 1
        
        # Store top patterns
        self.patterns['success_sequences'] = [
            {'pattern': pattern, 'count': count}
            for pattern, count in sorted(
                pattern_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        ]
    
    def get_learned_suggestions(self, current_cmd: str, context: Dict) -> List[Dict]:
        """Get suggestions based on learned patterns."""
        suggestions = []
        
        # Check common transitions
        if current_cmd in self.patterns.get('common_flows', {}):
            for transition in self.patterns['common_flows'][current_cmd]:
                suggestions.append({
                    'cmd': f"/{transition['command']}",
                    'reason': f"Frequently used after {current_cmd} ({transition['frequency']} times)",
                    'confidence': min(transition['frequency'] / 10, 1.0)
                })
        
        return suggestions
    
    def save(self):
        """Save data and patterns."""
        # Ensure directories exist
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.patterns_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save data
        self.data_file.write_text(json.dumps(self.data, indent=2, default=str))
        
        # Save patterns
        self.patterns_file.write_text(json.dumps(self.patterns, indent=2))
    
    def update_user_preference(self, cmd_sequence: List[str], chosen: str):
        """Update user preferences based on choices."""
        seq_key = ' -> '.join(cmd_sequence[-2:])
        if 'user_preferences' not in self.patterns:
            self.patterns['user_preferences'] = {}
        if seq_key not in self.patterns['user_preferences']:
            self.patterns['user_preferences'][seq_key] = {}
        if chosen not in self.patterns['user_preferences'][seq_key]:
            self.patterns['user_preferences'][seq_key][chosen] = 0
        
        self.patterns['user_preferences'][seq_key][chosen] += 1


# Utility functions for use in hooks
def track_command_sequence(from_cmd: str, to_cmd: str, context: Dict = None):
    """Track a command sequence."""
    learner = CommandSequenceLearner()
    learner.record_transition(from_cmd, to_cmd, context or {})
    learner.analyze_patterns()
    learner.save()

def get_learned_next_commands(current_cmd: str, context: Dict = None) -> List[Dict]:
    """Get learned suggestions for next commands."""
    learner = CommandSequenceLearner()
    return learner.get_learned_suggestions(current_cmd, context or {})

if __name__ == "__main__":
    # Can be run standalone to analyze patterns
    learner = CommandSequenceLearner()
    learner.analyze_patterns()
    learner.save()
    
    print("Command Sequence Analysis Complete")
    print(f"Total sequences tracked: {len(learner.data.get('sequences', []))}")
    print(f"Common patterns found: {len(learner.patterns.get('common_flows', {}))}")
    print(f"Success patterns identified: {len(learner.patterns.get('success_sequences', []))}")
