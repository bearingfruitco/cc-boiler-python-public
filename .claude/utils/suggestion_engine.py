#!/usr/bin/env python3
"""
Suggestion Engine - Provides helpful corrections for design system violations
Tracks common mistakes and provides educational feedback
"""

import json
import re
import os
from pathlib import Path
from datetime import datetime
from collections import Counter

class SuggestionEngine:
    def __init__(self):
        self.analytics_dir = Path(".claude/analytics")
        self.analytics_dir.mkdir(parents=True, exist_ok=True)
        self.violations_file = self.analytics_dir / "design-violations.json"
        
        # Comprehensive mapping of violations to suggestions
        self.suggestions = {
            # Typography violations
            r'\btext-sm\b': {
                'suggestion': 'text-size-3',
                'explanation': 'Use text-size-3 (16px) for small text. Our design system uses only 4 font sizes.',
                'category': 'typography'
            },
            r'\btext-base\b': {
                'suggestion': 'text-size-3',
                'explanation': 'Use text-size-3 (16px) for base text size.',
                'category': 'typography'
            },
            r'\btext-lg\b': {
                'suggestion': 'text-size-2', 
                'explanation': 'Use text-size-2 (24px) for large text. Mobile automatically adjusts to 20px.',
                'category': 'typography'
            },
            r'\btext-xl\b': {
                'suggestion': 'text-size-1',
                'explanation': 'Use text-size-1 (32px) for extra large text. Mobile automatically adjusts to 28px.',
                'category': 'typography'
            },
            r'\btext-2xl\b': {
                'suggestion': 'text-size-1',
                'explanation': 'Use text-size-1 (32px) for largest headings. We only have 4 font sizes.',
                'category': 'typography'
            },
            r'\btext-xs\b': {
                'suggestion': 'text-size-4',
                'explanation': 'Use text-size-4 (12px) for extra small text like captions.',
                'category': 'typography'
            },
            r'\bfont-bold\b': {
                'suggestion': 'font-semibold',
                'explanation': 'Only font-regular (400) and font-semibold (600) are allowed. No bold (700).',
                'category': 'typography'
            },
            r'\bfont-medium\b': {
                'suggestion': 'font-semibold',
                'explanation': 'Use font-semibold (600) instead. We only have regular and semibold.',
                'category': 'typography'
            },
            r'\bfont-light\b': {
                'suggestion': 'font-regular',
                'explanation': 'Use font-regular (400) instead. We only have regular and semibold.',
                'category': 'typography'
            },
            
            # Spacing violations
            r'\bp-5\b': {
                'suggestion': 'p-4 (16px) or p-6 (24px)',
                'explanation': 'Spacing must be divisible by 4. Use p-4 for less padding or p-6 for more.',
                'category': 'spacing'
            },
            r'\bm-5\b': {
                'suggestion': 'm-4 (16px) or m-6 (24px)',
                'explanation': 'Spacing must follow 4px grid. Use m-4 or m-6 instead.',
                'category': 'spacing'
            },
            r'\bp-7\b': {
                'suggestion': 'p-6 (24px) or p-8 (32px)',
                'explanation': 'Use p-6 for 24px or p-8 for 32px. All spacing divisible by 4.',
                'category': 'spacing'
            },
            r'\bm-7\b': {
                'suggestion': 'm-6 (24px) or m-8 (32px)',
                'explanation': 'Use m-6 for 24px or m-8 for 32px. Follow the 4px grid.',
                'category': 'spacing'
            },
            r'\bgap-5\b': {
                'suggestion': 'gap-4 (16px) or gap-6 (24px)',
                'explanation': 'Gap spacing must follow 4px grid. Use gap-4 or gap-6.',
                'category': 'spacing'
            },
            r'\bspace-x-5\b': {
                'suggestion': 'space-x-4 or space-x-6',
                'explanation': 'Horizontal spacing must be divisible by 4.',
                'category': 'spacing'
            },
            r'\bspace-y-5\b': {
                'suggestion': 'space-y-4 or space-y-6',
                'explanation': 'Vertical spacing must be divisible by 4.',
                'category': 'spacing'
            },
            
            # Touch target violations
            r'<button[^>]*className="[^"]*"[^>]*>(?![^<]*h-1[12])': {
                'suggestion': 'Add h-11 (44px) or h-12 (48px) to button',
                'explanation': 'Buttons need minimum 44px height for mobile touch targets.',
                'category': 'accessibility'
            },
            r'<a[^>]*className="[^"]*"[^>]*>(?![^<]*h-1[12])': {
                'suggestion': 'Add h-11 or h-12 to interactive links',
                'explanation': 'Interactive elements need 44px minimum touch target.',
                'category': 'accessibility'
            },
            
            # Color usage
            r'\btext-black\b': {
                'suggestion': 'text-gray-900',
                'explanation': 'Use text-gray-900 instead of pure black for better readability.',
                'category': 'color'
            },
            r'\bbg-black\b': {
                'suggestion': 'bg-gray-900 or bg-gray-800',
                'explanation': 'Use gray-900/800 instead of pure black for better contrast.',
                'category': 'color'
            }
        }
    
    def find_violations(self, content, file_path=""):
        """Find all design violations in content"""
        violations = []
        
        for pattern, details in self.suggestions.items():
            try:
                matches = list(re.finditer(pattern, content, re.IGNORECASE))
                for match in matches:
                    # Get context around violation
                    start = max(0, match.start() - 50)
                    end = min(len(content), match.end() + 50)
                    context = content[start:end].strip()
                    
                    violations.append({
                        'pattern': pattern,
                        'matched_text': match.group(),
                        'suggestion': details['suggestion'],
                        'explanation': details['explanation'],
                        'category': details['category'],
                        'context': context,
                        'line_number': content[:match.start()].count('\n') + 1,
                        'file_path': file_path
                    })
            except Exception as e:
                # Skip invalid regex patterns
                continue
        
        return violations
    
    def format_violation_message(self, violation):
        """Format a helpful violation message"""
        return f"""
❌ Design System Violation: {violation['category'].title()}
📍 Line {violation['line_number']}: Found '{violation['matched_text']}'
✅ Use instead: {violation['suggestion']}
💡 Why: {violation['explanation']}
📄 Context: ...{violation['context']}...
"""
    
    def track_violation(self, violation):
        """Track violations for analytics"""
        violations = []
        if self.violations_file.exists():
            try:
                with open(self.violations_file) as f:
                    violations = json.load(f)
            except:
                violations = []
        
        violations.append({
            'timestamp': datetime.now().isoformat(),
            'matched_text': violation['matched_text'],
            'category': violation['category'],
            'file': violation['file_path'],
            'suggestion': violation['suggestion'],
            'session_id': os.environ.get('CLAUDE_SESSION_ID', 'unknown')
        })
        
        # Keep last 1000 violations
        violations = violations[-1000:]
        
        with open(self.violations_file, 'w') as f:
            json.dump(violations, f, indent=2)
    
    def get_common_mistakes(self, limit=5):
        """Get most common violations for learning"""
        if not self.violations_file.exists():
            return []
        
        try:
            with open(self.violations_file) as f:
                violations = json.load(f)
        except:
            return []
        
        # Count violations by matched text
        violation_counts = Counter(v['matched_text'] for v in violations)
        
        # Format for display
        common = []
        for text, count in violation_counts.most_common(limit):
            # Find the suggestion for this violation
            suggestion = None
            for v in violations:
                if v['matched_text'] == text:
                    suggestion = v['suggestion']
                    break
            
            common.append({
                'text': text,
                'count': count,
                'suggestion': suggestion
            })
        
        return common
    
    def get_category_stats(self):
        """Get violation statistics by category"""
        if not self.violations_file.exists():
            return {}
        
        try:
            with open(self.violations_file) as f:
                violations = json.load(f)
        except:
            return {}
        
        # Count by category
        category_counts = Counter(v['category'] for v in violations)
        return dict(category_counts)


# Make it importable
if __name__ == "__main__":
    # Test the suggestion engine
    engine = SuggestionEngine()
    test_content = """
    <button className="text-sm font-bold p-5">
        Click me
    </button>
    """
    
    violations = engine.find_violations(test_content, "test.tsx")
    for v in violations:
        print(engine.format_violation_message(v))
