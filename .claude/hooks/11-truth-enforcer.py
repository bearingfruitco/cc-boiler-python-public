#!/usr/bin/env python3
"""
Truth Enforcer Hook - Prevents ACCIDENTAL changes to established project facts
Allows intentional changes when explicitly requested
"""

import json
import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

class ProjectTruthExtractor:
    """Extracts established facts from the codebase"""
    
    def __init__(self):
        self.truths = {
            'project': {},
            'api_routes': {},
            'components': {},
            'env_vars': {},
            'database': {},
            'types': {}
        }
    
    def extract_all(self):
        """Extract all established truths"""
        self.extract_project_info()
        self.extract_api_routes()
        self.extract_components()
        self.extract_env_vars()
        self.extract_database_schema()
        self.extract_type_definitions()
        return self.truths
    
    def extract_project_info(self):
        """Extract from package.json and project files"""
        try:
            with open('package.json', 'r') as f:
                pkg = json.load(f)
                self.truths['project']['name'] = pkg.get('name', '')
                self.truths['project']['version'] = pkg.get('version', '')
        except:
            pass
        
        # Extract from PROJECT_PRD.md
        try:
            prd_files = Path('docs/project').glob('*PRD.md')
            for prd in prd_files:
                content = prd.read_text()
                # Extract project name from PRD
                name_match = re.search(r'(?:Project|App|Application):\s*([^\n]+)', content)
                if name_match:
                    self.truths['project']['display_name'] = name_match.group(1).strip()
        except:
            pass
    
    def extract_api_routes(self):
        """Extract API routes from app/api directory"""
        try:
            api_dir = Path('app/api')
            if api_dir.exists():
                for route_file in api_dir.rglob('route.ts'):
                    # Get route path from file location
                    route_path = str(route_file.parent).replace('app/api', '/api')
                    route_path = route_path.replace('\\', '/')
                    
                    # Extract HTTP methods
                    content = route_file.read_text()
                    methods = []
                    for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                        if f'export async function {method}' in content:
                            methods.append(method)
                    
                    if methods:
                        self.truths['api_routes'][route_path] = {
                            'methods': methods,
                            'file': str(route_file)
                        }
        except:
            pass
    
    def extract_components(self):
        """Extract component props and exports"""
        try:
            components_dir = Path('components')
            if components_dir.exists():
                for comp_file in components_dir.rglob('*.tsx'):
                    if '.test.' not in str(comp_file):
                        content = comp_file.read_text()
                        comp_name = comp_file.stem
                        
                        # Extract props interface
                        props_match = re.search(rf'interface\s+{comp_name}Props\s*{{([^}}]+)}}', content, re.DOTALL)
                        if props_match:
                            self.truths['components'][comp_name] = {
                                'file': str(comp_file),
                                'has_props': True
                            }
                            
                            # Extract prop types for important components
                            if comp_name in ['Button', 'Card', 'Input', 'Form']:
                                prop_content = props_match.group(1)
                                # Extract variant/size/type enums
                                variant_match = re.search(r'variant\??\s*:\s*["\']([^"\']+)["\']', prop_content)
                                if variant_match:
                                    self.truths['components'][comp_name]['variants'] = variant_match.group(1).split('|')
        except:
            pass
    
    def extract_env_vars(self):
        """Extract from .env.example"""
        try:
            env_file = Path('.env.example')
            if env_file.exists():
                content = env_file.read_text()
                for line in content.split('\n'):
                    if '=' in line and not line.strip().startswith('#'):
                        key = line.split('=')[0].strip()
                        if key:
                            self.truths['env_vars'][key] = True
        except:
            pass
    
    def extract_database_schema(self):
        """Extract from Prisma schema or Drizzle schema"""
        try:
            # Check Prisma
            prisma_file = Path('prisma/schema.prisma')
            if prisma_file.exists():
                content = prisma_file.read_text()
                # Extract model names
                models = re.findall(r'model\s+(\w+)\s*{', content)
                for model in models:
                    self.truths['database'][model.lower()] = {'type': 'table'}
            
            # Check Drizzle schemas
            schema_files = Path('lib/db').glob('**/schema.ts')
            for schema_file in schema_files:
                content = schema_file.read_text()
                # Extract table names
                tables = re.findall(r'export\s+const\s+(\w+)\s*=\s*(?:pg|mysql|sqlite)Table', content)
                for table in tables:
                    self.truths['database'][table] = {'type': 'table'}
        except:
            pass
    
    def extract_type_definitions(self):
        """Extract key type definitions"""
        try:
            types_dir = Path('types')
            if types_dir.exists():
                for type_file in types_dir.glob('*.ts'):
                    content = type_file.read_text()
                    # Extract type names
                    types = re.findall(r'export\s+(?:type|interface)\s+(\w+)', content)
                    for type_name in types:
                        self.truths['types'][type_name] = {'file': str(type_file)}
        except:
            pass

def is_intentional_change():
    """Check if this change is intentional based on context"""
    # Check for override file
    override_file = Path('.claude/truth-override.json')
    if override_file.exists():
        try:
            with open(override_file) as f:
                overrides = json.load(f)
                # Check if override is recent (within last hour)
                if 'timestamp' in overrides:
                    override_time = datetime.fromisoformat(overrides['timestamp'])
                    if datetime.now() - override_time < timedelta(hours=1):
                        return True, overrides.get('reason', 'Explicit override requested')
        except:
            pass
    
    # Check current task for refactoring keywords
    try:
        work_state = Path('.claude/work-state.json')
        if work_state.exists():
            with open(work_state) as f:
                state = json.load(f)
                current_task = state.get('current_task', '').lower()
                
                # Keywords that indicate intentional changes
                refactor_keywords = [
                    'refactor', 'rename', 'update api', 'change route',
                    'migrate', 'restructure', 'redesign', 'breaking change',
                    'api v2', 'new version', 'deprecate', 'replace'
                ]
                
                for keyword in refactor_keywords:
                    if keyword in current_task:
                        return True, f"Current task involves: {keyword}"
    except:
        pass
    
    # Check git commit messages for refactoring intent
    try:
        result = subprocess.run(
            "git log -1 --pretty=%B",
            shell=True,
            capture_output=True,
            text=True
        )
        last_commit = result.stdout.lower()
        if any(word in last_commit for word in ['refactor', 'breaking', 'migrate']):
            return True, "Recent commit indicates refactoring"
    except:
        pass
    
    return False, None

def check_truth_violations(tool_use, truths):
    """Check if the change violates established truths"""
    violations = []
    
    # Get the operation details
    operation = tool_use.get('name', '')
    path = tool_use.get('path', '')
    
    if operation in ['str_replace_editor', 'edit_file']:
        old_content = tool_use.get('old_str', '')
        new_content = tool_use.get('new_str', tool_use.get('content', ''))
        
        # Check for API route changes
        if '/api/' in path:
            # Check if changing established routes
            for route, details in truths['api_routes'].items():
                if route in old_content and route not in new_content:
                    violations.append({
                        'type': 'api_route_change',
                        'message': f"Changing established API route: {route}",
                        'established': route,
                        'source': details['file'],
                        'severity': 'high'
                    })
        
        # Check for environment variable changes
        if '.env' in path:
            for env_var in truths['env_vars']:
                if env_var in old_content and env_var not in new_content:
                    violations.append({
                        'type': 'env_var_removal',
                        'message': f"Removing established env var: {env_var}",
                        'established': env_var,
                        'source': '.env.example',
                        'severity': 'medium'
                    })
        
        # Check for component prop changes
        for comp_name, details in truths['components'].items():
            if comp_name in path:
                # Check if changing variant values
                if 'variants' in details:
                    for variant in details['variants']:
                        if f"'{variant}'" in old_content and f"'{variant}'" not in new_content:
                            violations.append({
                                'type': 'component_variant_change',
                                'message': f"Changing established variant: {variant} in {comp_name}",
                                'established': variant,
                                'source': details['file'],
                                'severity': 'low'
                            })
    
    return violations

def main():
    """Main hook logic"""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Only check file modifications
    tool_use = input_data.get('tool_use', {})
    if tool_use.get('name') not in ['str_replace_editor', 'edit_file', 'create_file']:
        sys.exit(0)
        return
    
    # Check if this is an intentional change
    is_intentional, reason = is_intentional_change()
    
    # Extract current truths
    extractor = ProjectTruthExtractor()
    truths = extractor.extract_all()
    
    # Check for violations
    violations = check_truth_violations(tool_use, truths)
    
    if violations:
        # If intentional, just warn
        if is_intentional:
            warning_msg = "⚠️ Truth Enforcement: Changing established values\n\n"
            warning_msg += f"Reason: {reason}\n\n"
            
            for v in violations:
                warning_msg += f"📝 {v['message']}\n"
                warning_msg += f"   Current: {v['established']}\n"
                warning_msg += f"   Location: {v['source']}\n\n"
            
            warning_msg += "✅ Proceeding with intentional change.\n"
            warning_msg += "Remember to update all references!"
            
            print(json.dumps({
                "decision": "warn",
                "message": warning_msg,
                "continue": True
            }))
        else:
            # Not intentional - format error message
            error_msg = "🚫 Truth Enforcement: Cannot change established facts\n\n"
            
            # Check severity
            high_severity = any(v['severity'] == 'high' for v in violations)
            
            for v in violations:
                emoji = "🔴" if v['severity'] == 'high' else "⚠️"
                error_msg += f"{emoji} {v['message']}\n"
                error_msg += f"   Established in: {v['source']}\n"
                error_msg += f"   Value: {v['established']}\n\n"
            
            error_msg += "These are established project facts.\n\n"
            error_msg += "To make intentional changes:\n"
            error_msg += "1. Add 'refactor' or 'update api' to your task description\n"
            error_msg += "2. Create override file: echo '{\"timestamp\":\"" + datetime.now().isoformat() + "\",\"reason\":\"Refactoring API v2\"}' > .claude/truth-override.json\n"
            error_msg += "3. Update ALL references across the codebase\n"
            error_msg += "4. Run /facts to see all established values"
            
            # Only block for high severity violations
            if high_severity:
                print(json.dumps({
                    "decision": "block",
                    "message": error_msg,
                    "suggestion": "This appears unintentional. Use override if this is deliberate."
                }))
            else:
                # Warn for low severity
                print(json.dumps({
                    "decision": "warn",
                    "message": error_msg,
                    "continue": True
                }))
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
