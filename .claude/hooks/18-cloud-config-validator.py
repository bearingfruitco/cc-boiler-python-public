#!/usr/bin/env python3
"""
Cloud Configuration Validator - Ensures proper GCP setup before deployment
Validates Cloud Run configs, IAM roles, and environment variables
"""

import json
import sys
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

def load_cloud_templates() -> Dict:
    """Load Cloud Run templates from documentation."""
    templates = {}
    try:
        # Load service template
        template_path = Path(".claude/PRPs/ai_docs/cloud_infrastructure/cloud_run_service_template.json")
        if template_path.exists():
            with open(template_path) as f:
                templates['service'] = json.load(f)
        
        # Load instructions
        instructions_path = Path(".claude/PRPs/ai_docs/cloud_infrastructure/cloud_run_instructions.json")
        if instructions_path.exists():
            with open(instructions_path) as f:
                templates['instructions'] = json.load(f)
    except Exception as e:
        print(f"Warning: Could not load cloud templates: {e}", file=sys.stderr)
    
    return templates

def validate_dockerfile(content: str) -> List[str]:
    """Validate Dockerfile for Cloud Run compatibility."""
    issues = []
    
    # Check for PORT environment variable usage
    if '$PORT' not in content and '${PORT}' not in content and 'os.environ.get("PORT"' not in content:
        issues.append("Dockerfile should use $PORT environment variable for Cloud Run")
    
    # Check for proper base image
    if 'FROM python:' in content:
        # Extract Python version
        match = re.search(r'FROM python:(\d+\.\d+)', content)
        if match:
            version = float(match.group(1))
            if version < 3.8:
                issues.append(f"Python {version} is outdated. Use Python 3.8+ for Cloud Run")
    
    # Check for proper command
    if 'CMD' not in content and 'ENTRYPOINT' not in content:
        issues.append("Dockerfile must have CMD or ENTRYPOINT to start the service")
    
    return issues

def validate_service_config(config: Dict) -> List[str]:
    """Validate Cloud Run service configuration."""
    issues = []
    
    # Check memory allocation
    if 'resources' in config:
        memory = config['resources'].get('limits', {}).get('memory', '')
        if memory:
            # Extract number from format like "512Mi"
            match = re.match(r'(\d+)', memory)
            if match:
                mem_mb = int(match.group(1))
                if mem_mb < 256:
                    issues.append("Memory should be at least 256Mi for Python services")
    
    # Check timeout
    timeout = config.get('timeoutSeconds', 300)
    if timeout > 3600:
        issues.append("Timeout cannot exceed 3600 seconds (60 minutes)")
    
    # Check concurrency
    concurrency = config.get('containerConcurrency', 80)
    if concurrency > 1000:
        issues.append("Concurrency cannot exceed 1000")
    
    return issues

def validate_iam_setup(content: str) -> List[str]:
    """Check for proper IAM role assignments."""
    issues = []
    required_roles = [
        'bigquery.user',
        'bigquery.dataEditor',
        'run.invoker',
        'secretmanager.secretAccessor'
    ]
    
    mentioned_roles = []
    for role in required_roles:
        if role in content:
            mentioned_roles.append(role)
    
    missing_roles = set(required_roles) - set(mentioned_roles)
    if missing_roles and ('bigquery' in content.lower() or 'secret' in content.lower()):
        issues.append(f"Missing IAM roles documentation: {', '.join(missing_roles)}")
    
    return issues

def validate_env_vars(content: str) -> List[str]:
    """Check for hardcoded secrets."""
    issues = []
    
    # Common patterns for secrets
    secret_patterns = [
        r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
        r'password\s*=\s*["\'][^"\']+["\']',
        r'secret\s*=\s*["\'][^"\']+["\']',
        r'token\s*=\s*["\'][^"\']+["\']',
    ]
    
    for pattern in secret_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append("Potential hardcoded secret detected. Use Secret Manager or environment variables")
            break
    
    return issues

def format_alert_message(issues: List[str], file_type: str) -> str:
    """Format validation issues as an alert message."""
    if not issues:
        return None
    
    msg = f"⚠️ Cloud Run Configuration Issues Detected ({file_type})\n\n"
    for i, issue in enumerate(issues, 1):
        msg += f"{i}. {issue}\n"
    
    msg += "\n📚 References:\n"
    msg += "• Cloud Run deployment guide: PRPs/ai_docs/cloud_infrastructure/cloud_run_deployment.md\n"
    msg += "• Service template: PRPs/ai_docs/cloud_infrastructure/cloud_run_service_template.json\n"
    msg += "• Instructions: PRPs/ai_docs/cloud_infrastructure/cloud_run_instructions.json\n"
    
    return msg

def main():
    """Main hook logic."""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Only check on relevant operations
    if input_data['tool'] not in ['write_file', 'str_replace']:
        sys.exit(0)
        return
    
    file_path = input_data.get('path', '')
    content = input_data.get('content', '')
    
    issues = []
    file_type = None
    
    # Check different file types
    if file_path.endswith('Dockerfile'):
        file_type = 'Dockerfile'
        issues = validate_dockerfile(content)
    
    elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
        if 'apiVersion' in content and 'serving.knative.dev' in content:
            file_type = 'Cloud Run Service Config'
            # Would need to parse YAML to dict for validation
            # For now, check basic patterns
            issues = validate_iam_setup(content)
    
    elif file_path.endswith('.json'):
        if 'serving.knative.dev' in content:
            try:
                config = json.loads(content)
                file_type = 'Cloud Run Service Config'
                if 'spec' in config:
                    spec = config['spec']['template']['spec']
                    issues = validate_service_config(spec)
            except:
                pass
    
    elif file_path.endswith('.py'):
        # Check Python files for cloud-related issues
        if any(term in content for term in ['cloud_run', 'bigquery', 'SECRET', 'API_KEY']):
            file_type = 'Python Cloud Integration'
            issues.extend(validate_env_vars(content))
            
            # Check for proper imports
            if 'bigquery' in content and 'from google.cloud import bigquery' not in content:
                issues.append("Missing 'from google.cloud import bigquery' import")
    
    elif 'deploy' in file_path and ('.yml' in file_path or '.yaml' in file_path):
        # GitHub Actions deployment files
        file_type = 'GitHub Actions Deploy'
        if 'workload_identity_provider' not in content and 'service_account' in content:
            issues.append("Consider using Workload Identity Federation instead of service account keys")
    
    # Alert if issues found
    if issues:
        alert_msg = format_alert_message(issues, file_type)
        if alert_msg:
            print(json.dumps({
                "action": "warn",
                "message": alert_msg,
                "severity": "warning"
            }))
    
    sys.exit(0)

if __name__ == "__main__":
    main()