#!/usr/bin/env python3
"""
Evidence-Based Language Enforcement Hook
Ensures all claims are backed by evidence, measurements, or documentation
Inspired by SuperClaude's evidence-based philosophy
"""

import json
import sys
import re

# Language that requires evidence
CLAIMS_REQUIRING_EVIDENCE = [
    r'\b(best|optimal|faster|slower|better|worse|superior|inferior)\b',
    r'\b(secure|insecure|vulnerable|safe|unsafe)\b',
    r'\b(performant|efficient|inefficient|optimized)\b',
    r'\b(always|never|guaranteed|definitely|certainly)\b',
    r'\b(should|must|need to|have to)\s+(?!test|verify|check|measure)'
]

# Evidence indicators
EVIDENCE_PATTERNS = [
    r'\b(test(?:ing|s|ed)?)\s+(show|confirm|indicate|prove|demonstrate)',
    r'\b(metric|measurement|benchmark|profile|analysis)\s+(show|indicate|reveal)',
    r'\b(documentation|docs?|spec(?:ification)?)\s+(state|say|specify|require)',
    r'\b(measured|verified|confirmed|validated|tested)\b',
    r'\b(\d+%?\s*(?:faster|slower|improvement|reduction|increase|decrease))\b',
    r'\b(according to|based on|as per)\s+(?:the\s+)?(?:official\s+)?(?:documentation|spec)',
    r'\b(OWASP|lighthouse|audit|scan)\s+(?:score|result|report)',
    r'\b(passes?|fails?)\s+(?:all\s+)?(?:tests?|validation|checks?)'
]

def find_unsupported_claims(content):
    """Find claims that lack evidence"""
    issues = []
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        # Skip comments and code blocks
        if line.strip().startswith('//') or line.strip().startswith('#'):
            continue
            
        # Check for claims requiring evidence
        for pattern in CLAIMS_REQUIRING_EVIDENCE:
            matches = list(re.finditer(pattern, line, re.IGNORECASE))
            if matches:
                # Check if there's evidence in the same line or nearby
                has_evidence = any(re.search(evidence, line, re.IGNORECASE) 
                                 for evidence in EVIDENCE_PATTERNS)
                
                # Also check previous and next lines for evidence
                if not has_evidence and line_num > 1:
                    has_evidence = any(re.search(evidence, lines[line_num-2], re.IGNORECASE) 
                                     for evidence in EVIDENCE_PATTERNS)
                
                if not has_evidence and line_num < len(lines):
                    has_evidence = any(re.search(evidence, lines[line_num], re.IGNORECASE) 
                                     for evidence in EVIDENCE_PATTERNS)
                
                if not has_evidence:
                    for match in matches:
                        issues.append({
                            'line': line_num,
                            'claim': match.group(),
                            'context': line.strip(),
                            'type': 'unsupported_claim'
                        })
    
    return issues

def suggest_evidence_based_alternative(claim):
    """Suggest how to rephrase claims with evidence"""
    alternatives = {
        'best': 'testing shows this approach',
        'optimal': 'benchmarks indicate this solution',
        'faster': 'measurements show X% improvement',
        'secure': 'security audit confirms',
        'better': 'metrics demonstrate improvement',
        'should': 'documentation recommends',
        'always': 'testing consistently shows',
        'never': 'no test cases have shown',
        'performant': 'performance profiling shows',
        'efficient': 'resource usage measurements indicate'
    }
    
    for trigger, replacement in alternatives.items():
        if trigger in claim.lower():
            return replacement
    
    return "testing/measurement confirms"

def format_evidence_message(issues):
    """Format issues into helpful message"""
    if not issues:
        return None
        
    message = "📊 EVIDENCE-BASED LANGUAGE CHECK\n\n"
    message += "Claims require evidence. Found unsupported statements:\n\n"
    
    for issue in issues[:5]:  # Show first 5
        message += f"Line {issue['line']}: \"{issue['claim']}\" in:\n"
        message += f"  {issue['context']}\n"
        message += f"  → Suggestion: Use '{suggest_evidence_based_alternative(issue['claim'])}...'\n\n"
    
    if len(issues) > 5:
        message += f"... and {len(issues) - 5} more\n\n"
    
    message += "✅ **Good examples**:\n"
    message += "• \"Testing shows 40% faster load times\"\n"
    message += "• \"Security scan reports 0 vulnerabilities\"\n"
    message += "• \"Documentation specifies this approach\"\n"
    message += "• \"Benchmarks demonstrate 50% memory reduction\"\n\n"
    
    message += "❌ **Avoid**:\n"
    message += "• \"This is the best approach\"\n"
    message += "• \"This is more secure\"\n"
    message += "• \"Always use this pattern\"\n"
    message += "• \"This should work better\"\n"
    
    return message

def main():
    """Main hook logic"""
    input_data = json.loads(sys.stdin.read())
    
    # Only check documentation and comments
    relevant_files = ['.md', '.mdx', '.txt', '.ts', '.tsx', '.js', '.jsx']
    file_path = input_data.get('path', '')
    
    if not any(file_path.endswith(ext) for ext in relevant_files):
        sys.exit(0)
        return
    
    # Skip checking for certain operations
    if input_data['tool'] not in ['write_file', 'edit_file', 'str_replace']:
        sys.exit(0)
        return
    
    content = input_data.get('content', '')
    
    # Find unsupported claims
    issues = find_unsupported_claims(content)
    
    if issues:
        # For documentation files, warn but don't block
        if file_path.endswith('.md') or file_path.endswith('.mdx'):
            print(json.dumps({
                "decision": "warn",
                "message": format_evidence_message(issues),
                "continue": True
            }))
        else:
            # For code comments, just warn
            print(json.dumps({
                "decision": "warn",
                "message": format_evidence_message(issues),
                "continue": True
            }))
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
