#!/usr/bin/env python3
"""
Auto-Persona Selection Hook
Automatically switches to the appropriate persona based on file type and keywords
Inspired by SuperClaude's intelligent persona switching
"""

import json
import sys
import re
from pathlib import Path

# File pattern to persona mapping
FILE_PATTERN_PERSONAS = {
    # Frontend patterns
    r'components/.*\.(tsx|jsx)$': 'frontend',
    r'app/\(.*\)/.*\.(tsx|jsx)$': 'frontend',
    r'styles/.*\.(css|scss)$': 'frontend',
    r'.*\.stories\.(tsx|jsx)$': 'frontend',
    
    # Backend patterns
    r'app/api/.*\.(ts|js)$': 'backend',
    r'lib/server/.*\.(ts|js)$': 'backend',
    r'lib/db/.*\.(ts|js)$': 'backend',
    r'middleware\.(ts|js)$': 'backend',
    
    # Data patterns
    r'migrations/.*\.sql$': 'data',
    r'lib/db/schema.*\.(ts|js)$': 'data',
    r'scripts/data/.*': 'data',
    
    # Security patterns
    r'lib/security/.*': 'security',
    r'.*\.env.*': 'security',
    r'security/.*': 'security',
    
    # Test patterns
    r'.*\.test\.(ts|tsx|js|jsx)$': 'qa',
    r'.*\.spec\.(ts|tsx|js|jsx)$': 'qa',
    r'tests/.*': 'qa',
    r'cypress/.*': 'qa',
    r'e2e/.*': 'qa',
    
    # Architecture patterns
    r'docs/architecture/.*': 'architect',
    r'.*ARCHITECTURE\.md$': 'architect',
    r'.*DESIGN\.md$': 'architect',
    
    # Performance patterns
    r'next\.config\.(js|ts)$': 'performance',
    r'performance/.*': 'performance',
    r'lib/cache/.*': 'performance',
    
    # Integration patterns
    r'lib/integrations/.*': 'integrator',
    r'app/api/webhooks/.*': 'integrator',
    r'lib/external/.*': 'integrator',
    
    # Documentation patterns
    r'.*README\.md$': 'mentor',
    r'docs/.*\.md$': 'mentor',
    r'.*CONTRIBUTING\.md$': 'mentor'
}

# Keyword to persona mapping
KEYWORD_PERSONAS = {
    # Frontend keywords
    'ui': 'frontend',
    'component': 'frontend',
    'responsive': 'frontend',
    'accessibility': 'frontend',
    'design system': 'frontend',
    'user interface': 'frontend',
    'style': 'frontend',
    'css': 'frontend',
    'animation': 'frontend',
    
    # Backend keywords
    'api': 'backend',
    'endpoint': 'backend',
    'database': 'backend',
    'server': 'backend',
    'authentication': 'backend',
    'authorization': 'backend',
    'middleware': 'backend',
    
    # Security keywords
    'security': 'security',
    'vulnerability': 'security',
    'audit': 'security',
    'pii': 'security',
    'encryption': 'security',
    'owasp': 'security',
    'compliance': 'security',
    
    # Performance keywords
    'performance': 'performance',
    'optimize': 'performance',
    'slow': 'performance',
    'cache': 'performance',
    'bottleneck': 'performance',
    'profiling': 'performance',
    
    # QA keywords
    'test': 'qa',
    'bug': 'qa',
    'error': 'qa',
    'coverage': 'qa',
    'e2e': 'qa',
    'validation': 'qa',
    
    # Architecture keywords
    'architecture': 'architect',
    'design': 'architect',
    'pattern': 'architect',
    'scalability': 'architect',
    'structure': 'architect',
    
    # Data keywords
    'migration': 'data',
    'schema': 'data',
    'query': 'data',
    'index': 'data',
    
    # Integration keywords
    'webhook': 'integrator',
    'integration': 'integrator',
    'third-party': 'integrator',
    'external api': 'integrator',
    
    # Refactoring keywords
    'refactor': 'refactorer',
    'cleanup': 'refactorer',
    'technical debt': 'refactorer',
    'code quality': 'refactorer',
    
    # Documentation keywords
    'explain': 'mentor',
    'document': 'mentor',
    'tutorial': 'mentor',
    'guide': 'mentor',
    'onboarding': 'mentor'
}

def detect_persona_from_file(file_path):
    """Detect appropriate persona based on file path"""
    for pattern, persona in FILE_PATTERN_PERSONAS.items():
        if re.search(pattern, file_path):
            return persona
    return None

def detect_persona_from_content(content):
    """Detect appropriate persona based on content keywords"""
    content_lower = content.lower()
    
    # Count keyword matches for each persona
    persona_scores = {}
    
    for keyword, persona in KEYWORD_PERSONAS.items():
        if keyword in content_lower:
            persona_scores[persona] = persona_scores.get(persona, 0) + 1
    
    # Return persona with highest score
    if persona_scores:
        return max(persona_scores.items(), key=lambda x: x[1])[0]
    
    return None

def suggest_persona_switch(current_persona, suggested_persona, reason):
    """Format message suggesting persona switch"""
    if current_persona == suggested_persona:
        return None
        
    persona_descriptions = {
        'frontend': 'Frontend Specialist (UI/UX, components, accessibility)',
        'backend': 'Backend Architect (APIs, databases, server logic)',
        'security': 'Security Analyst (vulnerabilities, compliance, PII)',
        'qa': 'QA Engineer (testing, validation, quality)',
        'architect': 'System Architect (design, patterns, scalability)',
        'performance': 'Performance Engineer (optimization, caching)',
        'integrator': 'Integration Specialist (APIs, webhooks)',
        'data': 'Data Engineer (database, migrations, queries)',
        'refactorer': 'Code Refactorer (cleanup, technical debt)',
        'mentor': 'Technical Mentor (documentation, teaching)'
    }
    
    message = f"🎭 PERSONA SUGGESTION\n\n"
    message += f"Based on {reason}, consider switching to:\n"
    message += f"**{persona_descriptions.get(suggested_persona, suggested_persona)}**\n\n"
    
    if current_persona:
        message += f"Current: {persona_descriptions.get(current_persona, current_persona)}\n\n"
    
    message += f"To switch, use: `/persona {suggested_persona}`\n"
    message += f"Or continue with current persona if more appropriate."
    
    return message

def get_current_persona():
    """Get current active persona from state file"""
    state_file = Path(__file__).parent.parent.parent / 'orchestration' / 'active-persona.json'
    
    if state_file.exists():
        try:
            with open(state_file) as f:
                data = json.load(f)
                return data.get('persona')
        except:
            pass
    
    return None

def main():
    """Main hook logic"""
    input_data = json.loads(sys.stdin.read())
    
    # Only suggest for file operations
    if input_data['tool'] not in ['write_file', 'edit_file', 'read_file']:
        sys.exit(0)
        return
    
    file_path = input_data.get('path', '')
    content = input_data.get('content', '')
    
    # Detect persona from file
    file_persona = detect_persona_from_file(file_path)
    
    # Detect persona from content (for write operations)
    content_persona = None
    if content and input_data['tool'] in ['write_file', 'edit_file']:
        content_persona = detect_persona_from_content(content)
    
    # Determine suggested persona (file takes precedence)
    suggested_persona = file_persona or content_persona
    
    if suggested_persona:
        current_persona = get_current_persona()
        
        # Determine reason for suggestion
        if file_persona:
            reason = f"file type ({Path(file_path).name})"
        else:
            reason = "content keywords"
        
        message = suggest_persona_switch(current_persona, suggested_persona, reason)
        
        if message:
            # Suggest but don't block
            print(json.dumps({
                "decision": "suggest",
                "message": message,
                "continue": True,
                "metadata": {
                    "suggested_persona": suggested_persona,
                    "reason": reason
                }
            }))
        else:
            sys.exit(0)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
