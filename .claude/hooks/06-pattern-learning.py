#!/usr/bin/env python3
"""
Enhanced Pattern Learning Hook
Now extracts PRD->Implementation patterns for reuse
Builds a library of successful specification patterns
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
import hashlib
import re

SPECS_DIR = Path.home() / '.claude' / 'specs'
PATTERNS_DIR = SPECS_DIR / 'patterns'
TEMPLATES_DIR = SPECS_DIR / 'templates'

def ensure_dirs():
    """Ensure spec directories exist"""
    SPECS_DIR.mkdir(exist_ok=True)
    PATTERNS_DIR.mkdir(exist_ok=True)
    TEMPLATES_DIR.mkdir(exist_ok=True)

def extract_prd_sections(file_path):
    """Extract key sections from a PRD"""
    if not file_path.exists() or not file_path.suffix == '.md':
        return None
    
    with open(file_path) as f:
        content = f.read()
    
    sections = {
        'requirements': [],
        'acceptance_criteria': [],
        'technical_approach': [],
        'api_contracts': []
    }
    
    # Extract sections using regex
    patterns = {
        'requirements': r'## Requirements\n(.*?)(?=##|\Z)',
        'acceptance_criteria': r'## Acceptance Criteria\n(.*?)(?=##|\Z)',
        'technical_approach': r'## Technical Approach\n(.*?)(?=##|\Z)',
        'api_contracts': r'## API Contracts\n(.*?)(?=##|\Z)'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, content, re.DOTALL)
        if match:
            sections[key] = match.group(1).strip().split('\n')
    
    return sections

def analyze_implementation(file_path, file_type):
    """Analyze implementation patterns"""
    patterns = {
        'file_type': file_type,
        'structure': {},
        'patterns_used': []
    }
    
    if file_type == 'component':
        # Extract component patterns
        with open(file_path) as f:
            content = f.read()
        
        # Look for common patterns
        if 'useState' in content:
            patterns['patterns_used'].append('stateful')
        if 'useForm' in content:
            patterns['patterns_used'].append('form-handling')
        if 'z.object' in content:
            patterns['patterns_used'].append('zod-validation')
        if 'useMutation' in content or 'useQuery' in content:
            patterns['patterns_used'].append('tanstack-query')
    
    elif file_type == 'api':
        with open(file_path) as f:
            content = f.read()
        
        if 'NextResponse' in content:
            patterns['patterns_used'].append('nextjs-api-route')
        if 'z.parse' in content:
            patterns['patterns_used'].append('request-validation')
        if 'try {' in content:
            patterns['patterns_used'].append('error-handling')
    
    return patterns

def create_pattern_entry(prd_path, implementation_files, metadata):
    """Create a reusable pattern from PRD and implementation"""
    pattern = {
        'id': hashlib.md5(f"{prd_path}-{datetime.now().isoformat()}".encode()).hexdigest()[:8],
        'name': prd_path.stem.replace('-PRD', '').replace('_', '-'),
        'created': datetime.now().isoformat(),
        'source': {
            'prd': str(prd_path),
            'implementations': [str(f) for f in implementation_files]
        },
        'specification': extract_prd_sections(prd_path),
        'implementation_patterns': {},
        'metrics': {
            'files_created': len(implementation_files),
            'time_to_implement': metadata.get('duration_minutes', 0),
            'bugs_found': metadata.get('bugs', 0),
            'iterations': metadata.get('iterations', 1)
        },
        'tags': [],
        'success_indicators': []
    }
    
    # Analyze each implementation file
    for file_path in implementation_files:
        if file_path.exists():
            file_type = 'component' if '/components/' in str(file_path) else 'api' if '/api/' in str(file_path) else 'other'
            pattern['implementation_patterns'][str(file_path)] = analyze_implementation(file_path, file_type)
    
    # Auto-tag based on content
    spec_text = ' '.join([' '.join(items) for items in pattern['specification'].values()])
    if 'auth' in spec_text.lower() or 'login' in spec_text.lower():
        pattern['tags'].append('authentication')
    if 'form' in spec_text.lower():
        pattern['tags'].append('forms')
    if 'api' in spec_text.lower() or 'endpoint' in spec_text.lower():
        pattern['tags'].append('api')
    if 'database' in spec_text.lower() or 'schema' in spec_text.lower():
        pattern['tags'].append('database')
    
    return pattern

def save_pattern(pattern):
    """Save pattern to library"""
    ensure_dirs()
    
    # Save to patterns directory
    pattern_file = PATTERNS_DIR / f"{pattern['name']}-{pattern['id']}.json"
    with open(pattern_file, 'w') as f:
        json.dump(pattern, f, indent=2)
    
    # Update index
    index_file = SPECS_DIR / 'index.json'
    if index_file.exists():
        with open(index_file) as f:
            index = json.load(f)
    else:
        index = {'patterns': [], 'templates': []}
    
    # Add to index
    index_entry = {
        'id': pattern['id'],
        'name': pattern['name'],
        'tags': pattern['tags'],
        'created': pattern['created'],
        'file': str(pattern_file.name)
    }
    
    # Remove duplicates
    index['patterns'] = [p for p in index['patterns'] if p['id'] != pattern['id']]
    index['patterns'].append(index_entry)
    
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=2)
    
    return pattern_file

def check_for_pattern_extraction(tool_use):
    """Check if we should extract a pattern from recent work"""
    # Look for signals that a feature is complete
    if tool_use['toolName'] == 'filesystem:write_file':
        path = Path(tool_use['parameters'].get('path', ''))
        
        # Check if we're completing tests (good signal of completion)
        if path.suffix in ['.test.tsx', '.test.ts', '.spec.tsx', '.spec.ts']:
            return check_recent_prd_work()
    
    return None

def check_recent_prd_work():
    """Check if there's recent PRD-based work to extract"""
    # Look for PRDs modified in last day
    project_root = Path.cwd()
    prd_files = list(project_root.glob('**/features/*-PRD.md'))
    
    if not prd_files:
        return None
    
    # Get most recent PRD
    recent_prd = max(prd_files, key=lambda p: p.stat().st_mtime)
    
    # Check if it's recent (last 24 hours)
    if (datetime.now().timestamp() - recent_prd.stat().st_mtime) > 86400:
        return None
    
    # Find related implementation files
    feature_name = recent_prd.stem.replace('-PRD', '')
    related_files = []
    
    # Common patterns for finding related files
    search_patterns = [
        f'**/*{feature_name}*.tsx',
        f'**/*{feature_name}*.ts',
        f'**/api/*{feature_name}*/route.ts'
    ]
    
    for pattern in search_patterns:
        related_files.extend(project_root.glob(pattern))
    
    if related_files:
        return {
            'prd': recent_prd,
            'files': related_files,
            'feature': feature_name
        }
    
    return None

def main():
    try:
        # Read hook input
        hook_input = json.loads(sys.stdin.read())
        tool_use = hook_input['toolUse']
        
        # Check if we should extract a pattern
        extraction_candidate = check_for_pattern_extraction(tool_use)
        
        if extraction_candidate:
            # Create pattern from recent work
            pattern = create_pattern_entry(
                extraction_candidate['prd'],
                extraction_candidate['files'],
                {'duration_minutes': 120}  # Estimate for now
            )
            
            # Save pattern
            pattern_file = save_pattern(pattern)
            
            print("\n✨ PATTERN EXTRACTED")
            print("=" * 50)
            print(f"Feature: {pattern['name']}")
            print(f"Files analyzed: {len(extraction_candidate['files'])}")
            print(f"Tags: {', '.join(pattern['tags'])}")
            print(f"\nPattern saved to: {pattern_file.name}")
            print("\n💡 This pattern can now be reused with:")
            print(f"   /specs apply {pattern['name']}")
            print("=" * 50)
        
        # Also do original pattern learning
        # ... (original code continues)
        
    except json.JSONDecodeError:
        pass
    except Exception as e:
        if Path('DEBUG_HOOKS').exists():
            print(f"Pattern Learning Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main()
    sys.exit(0)
