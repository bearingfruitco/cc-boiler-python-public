#!/usr/bin/env python3
"""
Performance Monitor for Hooks - Tracks execution time and identifies slow hooks
"""

import json
import sys
import time
import functools
from pathlib import Path
from datetime import datetime

class HookPerformanceMonitor:
    def __init__(self):
        self.metrics_file = Path(__file__).parent.parent.parent / 'team' / 'metrics' / 'hook-performance.json'
        self.metrics_file.parent.mkdir(exist_ok=True)
        self.load_metrics()
    
    def load_metrics(self):
        """Load existing metrics"""
        if self.metrics_file.exists():
            with open(self.metrics_file) as f:
                self.metrics = json.load(f)
        else:
            self.metrics = {
                'hooks': {},
                'last_updated': None
            }
    
    def save_metrics(self):
        """Save metrics to file"""
        self.metrics['last_updated'] = datetime.now().isoformat()
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def record_execution(self, hook_name, execution_time):
        """Record hook execution time"""
        if hook_name not in self.metrics['hooks']:
            self.metrics['hooks'][hook_name] = {
                'executions': 0,
                'total_time': 0,
                'min_time': float('inf'),
                'max_time': 0,
                'avg_time': 0
            }
        
        hook_metrics = self.metrics['hooks'][hook_name]
        hook_metrics['executions'] += 1
        hook_metrics['total_time'] += execution_time
        hook_metrics['min_time'] = min(hook_metrics['min_time'], execution_time)
        hook_metrics['max_time'] = max(hook_metrics['max_time'], execution_time)
        hook_metrics['avg_time'] = hook_metrics['total_time'] / hook_metrics['executions']
        
        # Check for slow execution
        if execution_time > 1.0:  # More than 1 second is slow
            self.log_slow_execution(hook_name, execution_time)
        
        self.save_metrics()
    
    def log_slow_execution(self, hook_name, execution_time):
        """Log slow hook executions"""
        slow_log = Path(__file__).parent.parent.parent / 'team' / 'logs' / 'slow-hooks.log'
        slow_log.parent.mkdir(exist_ok=True)
        
        with open(slow_log, 'a') as f:
            f.write(f"{datetime.now().isoformat()} - {hook_name}: {execution_time:.2f}s\n")
    
    def get_performance_summary(self):
        """Get performance summary"""
        summary = []
        
        for hook_name, metrics in self.metrics['hooks'].items():
            if metrics['executions'] > 0:
                summary.append({
                    'hook': hook_name,
                    'avg_time': metrics['avg_time'],
                    'max_time': metrics['max_time'],
                    'executions': metrics['executions']
                })
        
        # Sort by average time (slowest first)
        summary.sort(key=lambda x: x['avg_time'], reverse=True)
        
        return summary

def monitor_performance(hook_name):
    """Decorator to monitor hook performance"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            monitor = HookPerformanceMonitor()
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                monitor.record_execution(hook_name, execution_time)
                
                # Add performance info to result if it's a dict
                if isinstance(result, dict):
                    result['_performance'] = {
                        'execution_time': execution_time,
                        'hook': hook_name
                    }
                
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                monitor.record_execution(f"{hook_name}_error", execution_time)
                raise
        
        return wrapper
    return decorator

def get_performance_report():
    """Generate performance report"""
    monitor = HookPerformanceMonitor()
    summary = monitor.get_performance_summary()
    
    report = "# Hook Performance Report\n\n"
    
    if not summary:
        report += "No performance data available yet.\n"
        return report
    
    report += "## Performance Summary\n\n"
    report += "| Hook | Avg Time | Max Time | Executions |\n"
    report += "|------|----------|----------|------------|\n"
    
    for item in summary[:10]:  # Top 10 slowest
        report += f"| {item['hook']} | {item['avg_time']:.3f}s | {item['max_time']:.3f}s | {item['executions']} |\n"
    
    # Identify problem hooks
    slow_hooks = [item for item in summary if item['avg_time'] > 0.5]
    
    if slow_hooks:
        report += "\n## ⚠️ Slow Hooks (>0.5s average)\n\n"
        for hook in slow_hooks:
            report += f"- **{hook['hook']}**: {hook['avg_time']:.3f}s average\n"
    
    return report

# Example usage in a hook:
# from utils.performance import monitor_performance
# 
# @monitor_performance('design-check')
# def main():
#     # Hook logic here
#     pass
