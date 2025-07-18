#!/usr/bin/env python3
"""
TCPA Compliance Check Hook
Ensures lead forms have proper TCPA compliance when enabled
"""

import json
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.hook_utils import HookResult, HookViolation

def load_tcpa_config():
    """Load TCPA configuration"""
    try:
        config_path = Path(__file__).parent.parent.parent / 'tcpa.config.json'
        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)
    except Exception:
        pass
    return None

def is_lead_form_file(file_path):
    """Check if this file contains a lead form"""
    # Check if it's a form component
    if not any(file_path.endswith(ext) for ext in ['.tsx', '.jsx']):
        return False
    
    # Check for form-related paths
    form_indicators = [
        'components/forms/',
        'lead-form',
        'contact-form',
        'signup-form',
        'registration',
        'app/(public)/forms/'
    ]
    
    return any(indicator in file_path.lower() for indicator in form_indicators)

def check_tcpa_compliance(file_path, content):
    """Check if lead forms have proper TCPA compliance"""
    violations = []
    
    # Load TCPA config
    config = load_tcpa_config()
    if not config or not config.get('enabled'):
        return []  # TCPA not enabled, no checks needed
    
    if not is_lead_form_file(file_path):
        return []
    
    # Check for forms that might collect PII
    has_email_field = 'email' in content.lower() and ('input' in content or 'Input' in content)
    has_phone_field = 'phone' in content.lower() and ('input' in content or 'Input' in content)
    has_form_element = '<form' in content or 'useForm' in content or 'handleSubmit' in content
    
    if not (has_form_element and (has_email_field or has_phone_field)):
        return []  # Not a lead collection form
    
    # Check for consent field
    consent_patterns = [
        'consent_tcpa',
        'tcpaConsent',
        'consent',
        'agreeToTerms',
        'acceptTerms'
    ]
    
    has_consent = any(pattern in content for pattern in consent_patterns)
    
    if not has_consent:
        violations.append(HookViolation(
            type='error',
            message='Lead form missing TCPA consent checkbox',
            line=0,
            suggestion='Add TCPA consent checkbox with clear language about calls/texts',
            details='Forms collecting phone numbers must have TCPA consent'
        ))
    
    # Check for TrustedForm integration if enabled
    if config['providers']['trustedform']['enabled']:
        has_trustedform = any(field in content for field in [
            'xxTrustedFormCertUrl',
            'TrustedForm',
            'trustedform_cert'
        ])
        
        if not has_trustedform:
            # Check if using TCPALeadForm component
            if 'TCPALeadForm' not in content:
                violations.append(HookViolation(
                    type='warning',
                    message='TrustedForm integration missing',
                    line=0,
                    suggestion='Use TCPALeadForm component or add TrustedForm hidden fields',
                    details='TrustedForm is enabled but not integrated in this form'
                ))
    
    # Check for Jornaya integration if enabled
    if config['providers']['jornaya']['enabled']:
        has_jornaya = any(field in content for field in [
            'leadid_token',
            'LeadiD',
            'jornaya'
        ])
        
        if not has_jornaya:
            # Check if using TCPALeadForm component
            if 'TCPALeadForm' not in content:
                violations.append(HookViolation(
                    type='warning',
                    message='Jornaya LeadiD integration missing',
                    line=0,
                    suggestion='Use TCPALeadForm component or add Jornaya hidden field',
                    details='Jornaya is enabled but not integrated in this form'
                ))
    
    # Check consent language
    if has_consent and config['compliance']['requireConsent']:
        # Look for consent text
        consent_language = config['compliance']['consentLanguage']
        key_phrases = ['auto-dialer', 'consent is not required', 'message and data rates']
        
        has_proper_language = any(phrase.lower() in content.lower() for phrase in key_phrases)
        
        if not has_proper_language:
            violations.append(HookViolation(
                type='warning',
                message='TCPA consent language may be incomplete',
                line=0,
                suggestion=f'Use standard TCPA language: "{consent_language[:50]}..."',
                details='Consent language should mention auto-dialers and that consent is not required'
            ))
    
    return violations

def main():
    """Main hook entry point"""
    # This hook only runs on file write operations
    if len(sys.argv) < 3 or sys.argv[1] != 'str_replace_editor':
        return HookResult(proceed=True, violations=[]).to_json()
    
    # Get file path from arguments
    try:
        # Parse the tool use details
        tool_args = json.loads(sys.argv[2])
        command = tool_args.get('command', '')
        
        if command not in ['str_replace', 'create', 'str_replace_based_edit_tool']:
            return HookResult(proceed=True, violations=[]).to_json()
        
        file_path = tool_args.get('path', '')
        
        # For create/replace operations, check the content
        if command == 'create':
            content = tool_args.get('file_text', '')
        else:
            content = tool_args.get('new_str', '')
        
        if not content:
            return HookResult(proceed=True, violations=[]).to_json()
        
        # Check TCPA compliance
        violations = check_tcpa_compliance(file_path, content)
        
        # Warnings don't block, errors do
        proceed = not any(v.type == 'error' for v in violations)
        
        return HookResult(
            proceed=proceed,
            violations=violations,
            message="TCPA compliance check completed"
        ).to_json()
        
    except Exception as e:
        # On error, allow operation but log
        return HookResult(
            proceed=True,
            violations=[],
            message=f"TCPA check error: {str(e)}"
        ).to_json()

if __name__ == '__main__':
    print(main())
