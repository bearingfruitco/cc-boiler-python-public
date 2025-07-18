#!/usr/bin/env python3
"""
Biome Linting Hook - Run Biome checks before file changes
Ensures code quality with Biome's fast linting and formatting
"""

import json
import sys
import subprocess
from pathlib import Path

def run_biome_check(file_path):
    """Run Biome linter on the file"""
    try:
        # Run Biome check on the specific file
        result = subprocess.run(
            ["pnpm", "biome", "check", file_path],
            capture_output=True,
            text=True
        )
        
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'errors': result.stderr
        }
    except Exception as e:
        return {
            'success': False,
            'output': '',
            'errors': str(e)
        }

def run_biome_format_check(file_path):
    """Check if file needs formatting"""
    try:
        # Check format without applying
        result = subprocess.run(
            ["pnpm", "biome", "format", file_path],
            capture_output=True,
            text=True
        )
        
        return {
            'needs_format': result.returncode != 0,
            'output': result.stdout
        }
    except:
        return {'needs_format': False, 'output': ''}

def auto_fix_with_biome(file_path):
    """Attempt to auto-fix issues with Biome"""
    try:
        # Run Biome with --apply flag
        result = subprocess.run(
            ["pnpm", "biome", "check", "--apply", file_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # Read the fixed content
            with open(file_path, 'r') as f:
                fixed_content = f.read()
            return {'success': True, 'content': fixed_content}
        
        return {'success': False, 'content': None}
    except:
        return {'success': False, 'content': None}

def parse_biome_output(output):
    """Parse Biome output for specific issues"""
    issues = []
    
    if "error" in output.lower():
        # Extract error messages
        lines = output.split('\n')
        for line in lines:
            if '⚠' in line or '✖' in line:
                issues.append(line.strip())
    
    return issues

def should_check_file(file_path):
    """Determine if file should be checked by Biome"""
    # Check file extensions
    checkable_extensions = ['.js', '.jsx', '.ts', '.tsx', '.json', '.jsonc']
    
    # Skip ignored paths
    ignore_paths = ['node_modules', '.next', 'dist', 'build', '.turbo']
    
    path = Path(file_path)
    
    # Check if extension is supported
    if not any(str(path).endswith(ext) for ext in checkable_extensions):
        return False
    
    # Check if in ignored directory
    if any(ignored in str(path) for ignored in ignore_paths):
        return False
    
    return True

def format_biome_report(check_result, format_result, file_path):
    """Format Biome results into readable report"""
    report = f"🔍 Biome Check: {Path(file_path).name}\n"
    
    if not check_result['success']:
        report += "\n❌ Linting Issues Found:\n"
        issues = parse_biome_output(check_result['output'] + check_result['errors'])
        for issue in issues[:5]:  # Show first 5 issues
            report += f"  {issue}\n"
        
        if len(issues) > 5:
            report += f"\n  ... and {len(issues) - 5} more issues\n"
    
    if format_result.get('needs_format'):
        report += "\n📐 Formatting Required\n"
        report += "  File needs formatting according to Biome rules\n"
    
    report += "\n💡 To fix automatically, run:\n"
    report += f"  pnpm biome check --apply {file_path}\n"
    report += f"  pnpm format\n"
    
    return report

def main():
    """Main hook logic"""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Only check on write operations
    if input_data.get('tool') not in ['write_file', 'edit_file', 'str_replace']:
        print(json.dumps({"action": "continue"}))
        return
    
    file_path = input_data.get('path', '')
    content = input_data.get('content', '')
    
    # Check if file should be linted
    if not should_check_file(file_path):
        print(json.dumps({"action": "continue"}))
        return
    
    # Write content to temp file for checking
    temp_path = Path(f"/tmp/biome-check-{Path(file_path).name}")
    try:
        with open(temp_path, 'w') as f:
            f.write(content)
        
        # Run Biome checks
        check_result = run_biome_check(str(temp_path))
        format_result = run_biome_format_check(str(temp_path))
        
        # Clean up temp file
        temp_path.unlink()
        
        # If there are issues
        if not check_result['success'] or format_result.get('needs_format'):
            # Try auto-fix
            with open(temp_path, 'w') as f:
                f.write(content)
            
            fix_result = auto_fix_with_biome(str(temp_path))
            
            if fix_result['success']:
                # Suggest the fixed version
                response = {
                    "action": "suggest_fix",
                    "message": format_biome_report(check_result, format_result, file_path),
                    "original_content": content,
                    "fixed_content": fix_result['content'],
                    "fix_description": "Auto-fixed with Biome (linting + formatting)"
                }
            else:
                # Block if can't auto-fix
                response = {
                    "action": "warn",
                    "message": format_biome_report(check_result, format_result, file_path),
                    "continue": True  # Allow proceeding with warnings
                }
            
            temp_path.unlink(missing_ok=True)
            print(json.dumps(response))
        else:
            # No issues, continue
            print(json.dumps({"action": "continue"}))
    
    except Exception as e:
        # On error, log but don't block
        print(json.dumps({
            "action": "continue",
            "message": f"Biome check failed: {str(e)}"
        }))
    finally:
        # Ensure temp file is cleaned up
        if temp_path.exists():
            temp_path.unlink()

if __name__ == "__main__":
    main()
