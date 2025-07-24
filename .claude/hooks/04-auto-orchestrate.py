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

def check_for_prp(feature_name):
    """Check if a PRP exists for this feature"""
    prp_paths = [
        Path(f"PRPs/active/{feature_name}.md"),
        Path(f"PRPs/active/{feature_name}-prp.md"),
        Path(f"PRPs/{feature_name}.md")
    ]
    
    for path in prp_paths:
        if path.exists():
            return path
    return None

def extract_prp_orchestration_hints(prp_path):
    """Extract orchestration hints from PRP"""
    try:
        prp_content = prp_path.read_text()
        
        # Extract task breakdown section
        task_section = re.search(r'### Task Breakdown(.*?)##', prp_content, re.DOTALL)
        if not task_section:
            return None
            
        hints = {
            'domains': [],
            'validation_levels': [],
            'dependencies': []
        }
        
        # Extract domain hints from tasks
        domain_patterns = {
            'backend': r'(models?|api|endpoint|database|schema)',
            'frontend': r'(cli|ui|interface|display)',
            'data': r'(pipeline|etl|transform|data)',
            'testing': r'(test|coverage|validation)',
            'agent': r'(agent|llm|ai|pydantic)'
        }
        
        task_content = task_section.group(1)
        for domain, pattern in domain_patterns.items():
            if re.search(pattern, task_content, re.IGNORECASE):
                hints['domains'].append(domain)
        
        # Extract validation requirements
        validation_section = re.search(r'## Validation Loops(.*?)##', prp_content, re.DOTALL)
        if validation_section:
            hints['validation_levels'] = re.findall(r'Level (\d+):', validation_section.group(1))
        
        return hints
        
    except Exception as e:
        print(f"Error reading PRP: {e}")
        return None

def determine_orchestration_strategy(domains, personas_config, prp_hints=None):
    """Determine the best orchestration strategy based on domain analysis and PRP hints"""
    # If PRP hints available, use them to enhance strategy selection
    if prp_hints and prp_hints.get('domains'):
        for domain in prp_hints['domains']:
            domains[domain] = domains.get(domain, 0) + 5  # Boost PRP-mentioned domains
    
    # Map domains to strategies
    domain_strategy_map = {
        ('backend', 'frontend', 'data'): 'feature_development',
        ('security', 'backend'): 'security_audit',
        ('performance', 'backend', 'data'): 'performance_optimization',
        ('refactor', 'backend'): 'code_quality',
        ('devops', 'security'): 'deployment',
        ('data', 'backend'): 'data_pipeline',
        ('agent', 'backend'): 'agent_development'
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
        sys.exit(0)
        return
    
    # Only analyze after task generation
    tool = input_data.get('tool', '')
    path = input_data.get('path', '')
    
    if tool != 'write_file' or not (path.endswith('-tasks.md') or 'tasks' in path):
        sys.exit(0)
        return
    
    # Load personas config
    try:
        personas_path = Path(__file__).parent.parent.parent / 'personas' / 'personas.json'
        with open(personas_path) as f:
            personas_config = json.load(f)
    except:
        sys.exit(0)
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
            "decision": "suggest",
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
        sys.exit(0)

if __name__ == "__main__":
    main()