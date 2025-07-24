#!/usr/bin/env python3
"""
Metrics Hook - Track design compliance metrics
Helps identify patterns and improve the boilerplate system
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime

def get_metrics_file():
    """Get path to metrics file"""
    metrics_dir = Path(__file__).parent.parent.parent / 'team' / 'metrics'
    metrics_dir.mkdir(exist_ok=True)
    return metrics_dir / 'design-compliance.json'

def load_metrics():
    """Load existing metrics"""
    metrics_file = get_metrics_file()
    if metrics_file.exists():
        with open(metrics_file) as f:
            return json.load(f)
    return {
        'total_files_processed': 0,
        'violations_by_type': {},
        'files_with_violations': [],
        'compliance_rate': 100.0,
        'last_updated': None
    }

def save_metrics(metrics):
    """Save metrics"""
    metrics['last_updated'] = datetime.now().isoformat()
    with open(get_metrics_file(), 'w') as f:
        json.dump(metrics, f, indent=2)

def analyze_component_file(content):
    """Analyze a component file for design compliance"""
    analysis = {
        'total_classes': 0,
        'compliant_classes': 0,
        'violations': [],
        'patterns_used': {}
    }
    
    # Count font size usage
    font_sizes = {
        'text-size-1': 0,
        'text-size-2': 0,
        'text-size-3': 0,
        'text-size-4': 0
    }
    
    for size in font_sizes:
        font_sizes[size] = len(re.findall(rf'\b{size}\b', content))
        analysis['total_classes'] += font_sizes[size]
        analysis['compliant_classes'] += font_sizes[size]
    
    # Check for violations
    forbidden_sizes = re.findall(r'\b(?:text-(?:xs|sm|base|lg|xl|2xl|3xl))\b', content)
    analysis['violations'].extend([{'type': 'font-size', 'value': v} for v in forbidden_sizes])
    analysis['total_classes'] += len(forbidden_sizes)
    
    # Count font weight usage
    font_weights = {
        'font-regular': len(re.findall(r'\bfont-regular\b', content)),
        'font-semibold': len(re.findall(r'\bfont-semibold\b', content))
    }
    
    for weight, count in font_weights.items():
        analysis['total_classes'] += count
        analysis['compliant_classes'] += count
    
    # Check weight violations
    forbidden_weights = re.findall(r'\b(?:font-(?:thin|light|medium|bold|extrabold))\b', content)
    analysis['violations'].extend([{'type': 'font-weight', 'value': v} for v in forbidden_weights])
    analysis['total_classes'] += len(forbidden_weights)
    
    # Analyze patterns
    if 'Container' in content or 'max-w-md' in content:
        analysis['patterns_used']['container'] = True
    
    if 'h-11' in content or 'h-12' in content:
        analysis['patterns_used']['proper_touch_targets'] = True
    
    if 'rounded-xl' in content:
        analysis['patterns_used']['consistent_rounding'] = True
    
    # Calculate compliance rate
    if analysis['total_classes'] > 0:
        analysis['compliance_rate'] = (analysis['compliant_classes'] / analysis['total_classes']) * 100
    else:
        analysis['compliance_rate'] = 100
    
    return analysis

def update_global_metrics(analysis, file_path, metrics):
    """Update global metrics with file analysis"""
    metrics['total_files_processed'] += 1
    
    # Update violations by type
    for violation in analysis['violations']:
        vtype = violation['type']
        if vtype not in metrics['violations_by_type']:
            metrics['violations_by_type'][vtype] = 0
        metrics['violations_by_type'][vtype] += 1
    
    # Track files with violations
    if analysis['violations']:
        metrics['files_with_violations'].append({
            'file': file_path,
            'violations': len(analysis['violations']),
            'compliance_rate': analysis['compliance_rate'],
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 100 files
        metrics['files_with_violations'] = metrics['files_with_violations'][-100:]
    
    # Update overall compliance rate
    total_compliant = sum(1 for f in metrics['files_with_violations'] 
                         if f['compliance_rate'] == 100)
    if metrics['total_files_processed'] > 0:
        metrics['compliance_rate'] = (
            (metrics['total_files_processed'] - len(metrics['files_with_violations'])) / 
            metrics['total_files_processed']
        ) * 100
    
    return metrics

def generate_insights(metrics):
    """Generate insights from metrics"""
    insights = []
    
    # Most common violation
    if metrics['violations_by_type']:
        most_common = max(metrics['violations_by_type'].items(), key=lambda x: x[1])
        insights.append(f"Most common violation: {most_common[0]} ({most_common[1]} times)")
    
    # Compliance trend
    if metrics['compliance_rate'] < 90:
        insights.append(f"⚠️ Compliance rate is {metrics['compliance_rate']:.1f}% - review design rules")
    elif metrics['compliance_rate'] > 95:
        insights.append(f"✅ Excellent compliance rate: {metrics['compliance_rate']:.1f}%")
    
    # Files needing attention
    problem_files = [f for f in metrics['files_with_violations'] 
                    if f['compliance_rate'] < 80]
    if problem_files:
        insights.append(f"Files needing attention: {len(problem_files)}")
    
    return insights

def main():
    """Main hook logic"""
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    # Only process component files
    file_path = input_data.get('path', '')
    if not file_path.endswith(('.tsx', '.jsx')):
        sys.exit(0)
        return
    
    # Skip if not a write operation
    if input_data['tool'] not in ['write_file', 'edit_file']:
        sys.exit(0)
        return
    
    content = input_data.get('content', '')
    
    # Analyze the file
    analysis = analyze_component_file(content)
    
    # Load and update metrics
    metrics = load_metrics()
    metrics = update_global_metrics(analysis, file_path, metrics)
    save_metrics(metrics)
    
    # Generate insights periodically
    if metrics['total_files_processed'] % 10 == 0:
        insights = generate_insights(metrics)
        if insights:
            message = "📊 Design System Metrics Update:\n"
            for insight in insights:
                message += f"  • {insight}\n"
            
            print(json.dumps({
                "decision": "log",
                "message": message,
                "continue": True
            }))
            return
    
    # Continue silently
    sys.exit(0)

if __name__ == "__main__":
    main()
