#!/usr/bin/env python3
"""
Auto-Orchestration Hook
Automatically triggers multi-agent orchestration when task complexity warrants it
"""

import json
import sys
import re
from pathlib import Path
from collections import defaultdict

def analyze_task_domains(content):
    """Analyze task content to identify required domains"""
    domains = defaultdict(int)
    
    # Domain keyword patterns for Python projects
    domain_patterns = {
        'backend': r'\b(api|endpoint|database|server|auth|route|middleware|validation|schema|fastapi|sqlalchemy|redis)\b',
        'frontend': r'\b(cli|terminal|ui|ux|typer|rich|prompt|interactive|display|format)\b',
        'data': r'\b(pipeline|etl|transform|extract|load|bigquery|pandas|duckdb|prefect|airflow|data quality)\b',
        'security': r'\b(encrypt|pii|phi|audit|compliance|vulnerability|auth|owasp|jwt|hash|secret)\b',
        'testing': r'\b(test|spec|pytest|coverage|mock|fixture|unit|integration|e2e)\b',
        'performance': r'\b(optimize|slow|cache|bottleneck|profile|performance|latency|async|concurrent)\b',
        'integration': r'\b(webhook|external|third-party|integration|sync|api|client|sdk)\b',
        'devops': r'\b(deploy|docker|kubernetes|ci|cd|pipeline|monitor|helm|terraform)\b',
        'refactor': r'\b(refactor|cleanup|technical debt|simplify|extract|pattern|design)\b',
        'agent': r'\b(agent|llm|ai|pydantic|instructor|memory|orchestration)\b'
    }
    
    # Count domain mentions
    for domain, pattern in domain_patterns.items():
        matches = len(re.findall(pattern, content, re.IGNORECASE))
        if matches > 0:
            domains[domain] = matches
    
    return domains

def determine_orchestration_strategy(domains, personas_config):
    """Determine the best orchestration strategy based on domain analysis"""
    # Map domains to strategies
    domain_strategy_map = {
        ('backend', 'frontend', 'data'): 'feature_development',
        ('security', 'backend'): 'security_audit',
        ('performance', 'backend', 'data'): 'performance_optimization',
        ('refactor', 'backend'): 'code_quality',
        ('devops', 'security'): 'deployment',
        ('data', 'backend'): 'data_pipeline'
    }
    
    # Find best matching strategy
    active_domains = set(d for d, count in domains.items() if count > 1)
    
    for domain_combo, strategy in domain_strategy_map.items():
        if set(domain_combo).issubset(active_domains):
            return strategy
    
    # Default to feature development if multiple domains
    if len(active_domains) >= 3:
        return 'feature_development'
    
    return None

def main():
    """Main hook logic"""
    try:
        input_data = json.loads(sys.stdin.read())
    except:
        print(json.dumps({"action": "continue"}))
        return
    
    # Only analyze after task generation
    tool = input_data.get('tool', '')
    path = input_data.get('path', '')
    
    if tool != 'write_file' or not (path.endswith('-tasks.md') or 'tasks' in path):
        print(json.dumps({"action": "continue"}))
        return
    
    # Load personas config
    try:
        personas_path = Path(__file__).parent.parent.parent / 'personas' / 'personas.json'
        with open(personas_path) as f:
            personas_config = json.load(f)
    except:
        print(json.dumps({"action": "continue"}))
        return
    
    # Analyze the tasks
    content = input_data.get('content', '')
    domains = analyze_task_domains(content)
    
    # Determine if orchestration is beneficial
    active_domains = [d for d, count in domains.items() if count > 1]
    total_mentions = sum(domains.values())
    
    orchestration_rules = personas_config.get('auto_orchestration_rules', {})
    min_domains = orchestration_rules.get('min_domains_for_orchestration', 3)
    complexity_threshold = orchestration_rules.get('task_complexity_threshold', 15)
    
    if len(active_domains) >= min_domains or total_mentions > complexity_threshold:
        # Determine strategy
        strategy = determine_orchestration_strategy(domains, personas_config)
        
        # Extract feature name
        feature_name = Path(path).stem.replace('-tasks', '')
        
        # Build suggestion message
        message = f"🤖 AUTO-ORCHESTRATION SUGGESTED\n\n"
        message += f"Detected multi-domain work across: {', '.join(active_domains)}\n"
        message += f"Total complexity score: {total_mentions}\n\n"
        
        if strategy:
            strategy_info = personas_config['orchestration_strategies'].get(strategy, {})
            message += f"Recommended strategy: **{strategy}**\n"
            message += f"Description: {strategy_info.get('description', '')}\n"
            message += f"Agents: {', '.join(strategy_info.get('agents', []))}\n\n"
        
        message += f"Recommended command:\n"
        message += f"`/orch {feature_name} --agents={len(active_domains)}`"
        
        if strategy:
            message += f" --strategy={strategy}"
        
        message += f"\n\nThis will spawn specialized agents to work in parallel, "
        message += f"potentially saving 50-70% of development time."
        
        print(json.dumps({
            "action": "suggest",
            "message": message,
            "auto_command": f"/orch {feature_name}" + (f" --strategy={strategy}" if strategy else ""),
            "metadata": {
                "domains": active_domains,
                "feature": feature_name,
                "strategy": strategy,
                "complexity_score": total_mentions
            }
        }))
    else:
        print(json.dumps({"action": "continue"}))

if __name__ == "__main__":
    main()