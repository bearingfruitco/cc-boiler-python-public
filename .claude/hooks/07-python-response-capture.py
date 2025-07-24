#!/usr/bin/env python3
"""
Python Response Capture Hook - Capture AI responses for issue creation
Specifically tuned for Python development patterns
"""

import json
import sys
import os
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

def extract_python_components(content: str) -> Dict:
    """Extract Python-specific components from AI response."""
    components = {
        'classes': [],
        'functions': [],
        'models': [],
        'endpoints': [],
        'imports': [],
        'packages': [],
        'async_functions': []
    }
    
    # Extract class definitions
    class_pattern = r'class\s+(\w+)(?:\(([^)]+)\))?:'
    for match in re.finditer(class_pattern, content):
        class_name = match.group(1)
        base_classes = match.group(2) or ''
        components['classes'].append({
            'name': class_name,
            'bases': [b.strip() for b in base_classes.split(',')] if base_classes else []
        })
        
        # Check if it's a Pydantic model
        if 'BaseModel' in base_classes:
            components['models'].append(class_name)
    
    # Extract function definitions
    func_pattern = r'(?:async\s+)?def\s+(\w+)\s*\([^)]*\)(?:\s*->\s*([^:]+))?:'
    for match in re.finditer(func_pattern, content):
        func_name = match.group(1)
        return_type = match.group(2)
        
        components['functions'].append({
            'name': func_name,
            'return_type': return_type.strip() if return_type else None
        })
        
        # Check if async
        if content[match.start():match.start()+5] == 'async':
            components['async_functions'].append(func_name)
    
    # Extract FastAPI endpoints
    endpoint_pattern = r'@(?:app|router)\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']'
    for match in re.finditer(endpoint_pattern, content):
        components['endpoints'].append({
            'method': match.group(1).upper(),
            'path': match.group(2)
        })
    
    # Extract imports
    import_patterns = [
        r'import\s+([\w\.]+)',
        r'from\s+([\w\.]+)\s+import',
    ]
    for pattern in import_patterns:
        for match in re.finditer(pattern, content):
            module = match.group(1)
            if module not in components['imports']:
                components['imports'].append(module)
    
    # Extract package requirements
    package_pattern = r'(?:pip install|poetry add|requirements\.txt.*?)\s+([\w\-\[\]]+(?:==|>=|<=|~=|>|<)[\d\.]+)'
    for match in re.finditer(package_pattern, content, re.IGNORECASE):
        components['packages'].append(match.group(1))
    
    return components

def extract_sections(content: str) -> Dict[str, str]:
    """Extract structured sections from AI response."""
    sections = {}
    
    # Common section headers
    section_patterns = [
        (r'#+\s*(?:Implementation|Plan|Approach|Strategy)', 'implementation_plan'),
        (r'#+\s*(?:Summary|Overview|Description)', 'summary'),
        (r'#+\s*(?:Tasks?|Steps?|Actions?)', 'tasks'),
        (r'#+\s*(?:Dependencies|Requirements|Packages)', 'dependencies'),
        (r'#+\s*(?:Testing|Tests)', 'testing'),
        (r'#+\s*(?:API|Endpoints?)', 'api_design'),
        (r'#+\s*(?:Models?|Schema|Data)', 'data_models'),
        (r'#+\s*(?:Architecture|Design)', 'architecture'),
        # Cloud-specific sections
        (r'#+\s*(?:Deployment|Deploy|CI/CD)', 'deployment'),
        (r'#+\s*(?:Infrastructure|Cloud|GCP)', 'infrastructure'),
        (r'#+\s*(?:Security|IAM|Permissions)', 'security'),
        (r'#+\s*(?:Monitoring|Logging|Observability)', 'monitoring')
    ]
    
    for pattern, section_name in section_patterns:
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        if matches:
            for i, match in enumerate(matches):
                start = match.end()
                # Find end of section (next section or end of content)
                if i + 1 < len(matches):
                    end = matches[i + 1].start()
                else:
                    # Check for any next section
                    next_section = re.search(r'\n#+\s*\w+', content[start:])
                    end = start + next_section.start() if next_section else len(content)
                
                section_content = content[start:end].strip()
                if section_content:
                    sections[section_name] = section_content
    
    return sections

def extract_tasks(content: str) -> List[str]:
    """Extract task items from content."""
    tasks = []
    
    # Numbered tasks
    numbered_pattern = r'^\s*\d+\.\s*(.+)$'
    for match in re.finditer(numbered_pattern, content, re.MULTILINE):
        tasks.append(match.group(1).strip())
    
    # Bullet point tasks
    bullet_pattern = r'^\s*[-*]\s*(.+)$'
    for match in re.finditer(bullet_pattern, content, re.MULTILINE):
        task = match.group(1).strip()
        if task and not task.startswith('['):  # Skip markdown checkboxes
            tasks.append(task)
    
    # Checkbox tasks
    checkbox_pattern = r'^\s*-\s*\[\s*\]\s*(.+)$'
    for match in re.finditer(checkbox_pattern, content, re.MULTILINE):
        tasks.append(match.group(1).strip())
    
    return tasks[:20]  # Limit to 20 tasks

def should_capture(content: str) -> bool:
    """Determine if content should be captured."""
    # Minimum length
    if len(content) < 200:
        return False
    
    # Keywords that indicate valuable content
    valuable_keywords = [
        'implement', 'plan', 'approach', 'strategy', 'architecture',
        'design', 'create', 'build', 'develop', 'setup',
        'class', 'function', 'api', 'endpoint', 'model',
        'async', 'await', 'fastapi', 'pydantic', 'prefect',
        # Cloud-specific keywords
        'cloud run', 'gcloud', 'docker', 'container',
        'bigquery', 'supabase', 'webhook', 'deployment',
        'service account', 'iam', 'kubernetes', 'eventarc'
    ]
    
    content_lower = content.lower()
    keyword_count = sum(1 for keyword in valuable_keywords if keyword in content_lower)
    
    # Need at least 3 keywords
    return keyword_count >= 3

def save_capture(capture_data: Dict) -> str:
    """Save capture to file system."""
    captures_dir = Path('.claude/captures')
    captures_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    content_hash = hashlib.md5(capture_data['content'].encode()).hexdigest()[:8]
    filename = f"capture_{timestamp}_{content_hash}.json"
    
    filepath = captures_dir / filename
    
    # Save capture
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(capture_data, f, indent=2, ensure_ascii=False)
    
    # Update index
    index_file = captures_dir / 'index.json'
    if index_file.exists():
        with open(index_file, 'r') as f:
            index = json.load(f)
    else:
        index = {"captures": []}
    
    index_entry = {
        "id": capture_data['id'],
        "timestamp": capture_data['timestamp'],
        "filename": filename,
        "summary": capture_data['sections'].get('summary', '')[:100],
        "components": len(capture_data['components'].get('classes', [])) + 
                     len(capture_data['components'].get('functions', [])),
        "has_tasks": bool(capture_data['sections'].get('tasks')),
        "converted_to_issue": False
    }
    
    index['captures'].insert(0, index_entry)
    
    # Keep only last 50 captures in index
    index['captures'] = index['captures'][:50]
    
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=2)
    
    return capture_data['id']

def get_current_context() -> Dict:
    """Get current session context."""
    context = {
        'branch': 'main',
        'session': None,
        'files_modified': []
    }
    
    # Try to get git branch
    try:
        import subprocess
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            context['branch'] = result.stdout.strip()
    except:
        pass
    
    # Get session from context file
    context_file = Path('.claude/context/state.json')
    if context_file.exists():
        try:
            with open(context_file, 'r') as f:
                state = json.load(f)
                context['session'] = state.get('session_id')
                context['files_modified'] = state.get('recent_files', [])
        except:
            pass
    
    return context

def main():
    """Main hook logic."""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # This is a post-tool-use hook, check if we should capture
    if 'ai_response' not in input_data:
        sys.exit(0)
        return
    
    content = input_data.get('ai_response', '')
    
    # Check if content is worth capturing
    if not should_capture(content):
        sys.exit(0)
        return
    
    # Extract components and sections
    components = extract_python_components(content)
    sections = extract_sections(content)
    
    # Extract tasks if present
    if 'tasks' in sections:
        task_list = extract_tasks(sections['tasks'])
    else:
        task_list = extract_tasks(content)
    
    # Get current context
    context = get_current_context()
    
    # Create capture data
    capture_data = {
        'id': f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(content.encode()).hexdigest()[:8]}",
        'timestamp': datetime.now().isoformat(),
        'content': content,
        'sections': sections,
        'tasks': task_list,
        'components': components,
        'metadata': {
            'branch': context['branch'],
            'session': context['session'],
            'files_modified': context['files_modified'],
            'tool': input_data.get('tool'),
            'capture_type': 'python_development'
        },
        'converted_to_issue': False
    }
    
    # Save capture
    capture_id = save_capture(capture_data)
    
    # Notify user if significant content captured
    if components['classes'] or components['functions'] or task_list:
        message = f"📸 Captured AI response: {capture_id}\n"
        
        if components['classes']:
            message += f"  • {len(components['classes'])} classes\n"
        if components['functions']:
            message += f"  • {len(components['functions'])} functions\n"
        if task_list:
            message += f"  • {len(task_list)} tasks\n"
        
        message += "\nUse /capture-to-issue to convert to GitHub issue"
        
        print(json.dumps({
            "decision": "notify",
            "message": message,
            "capture_id": capture_id
        }))
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
