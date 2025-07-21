#!/usr/bin/env python3
"""
Hook Testing Framework - Test your hooks work correctly
"""

import json
import subprocess
import sys
from pathlib import Path
import tempfile
import shutil

class HookTester:
    def __init__(self):
        self.results = []
        self.hooks_dir = Path('.claude/hooks')
    
    def test_hook(self, hook_path, test_input, expected_action=None):
        """Test a single hook"""
        try:
            # Run hook with test input
            result = subprocess.run(
                [sys.executable, hook_path],
                input=json.dumps(test_input),
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return {
                    'hook': hook_path.name,
                    'status': 'error',
                    'error': result.stderr
                }
            
            # Parse output
            try:
                output = json.loads(result.stdout)
                
                # Check expected action if provided
                if expected_action and output.get('action') != expected_action:
                    return {
                        'hook': hook_path.name,
                        'status': 'fail',
                        'expected': expected_action,
                        'actual': output.get('action'),
                        'message': output.get('message', '')
                    }
                
                return {
                    'hook': hook_path.name,
                    'status': 'pass',
                    'action': output.get('action'),
                    'message': output.get('message', '')
                }
            
            except json.JSONDecodeError:
                return {
                    'hook': hook_path.name,
                    'status': 'error',
                    'error': 'Invalid JSON output',
                    'output': result.stdout
                }
        
        except Exception as e:
            return {
                'hook': hook_path.name,
                'status': 'error',
                'error': str(e)
            }
    
    def run_tests(self):
        """Run all hook tests"""
        print("🧪 Running Hook Tests")
        print("====================\n")
        
        # Test design enforcement
        self.test_design_enforcement()
        
        # Test actually works protocol
        self.test_actually_works()
        
        # Test code quality
        self.test_code_quality()
        
        # Test collaboration sync
        self.test_collab_sync()
        
        # Generate report
        self.generate_report()
    
    def test_design_enforcement(self):
        """Test design system enforcement"""
        print("Testing design enforcement...")
        
        hook_path = self.hooks_dir / 'pre-tool-use' / '02-design-check.py'
        
        # Test 1: Valid design
        test_input = {
            'tool': 'write_file',
            'path': 'test.tsx',
            'content': '<div className="text-size-2 font-semibold p-4">Valid</div>'
        }
        result = self.test_hook(hook_path, test_input, 'continue')
        self.results.append(('Design: Valid classes', result))
        
        # Test 2: Invalid font size
        test_input['content'] = '<div className="text-sm font-bold">Invalid</div>'
        result = self.test_hook(hook_path, test_input)
        self.results.append(('Design: Invalid font size', result))
        
        # Test 3: Invalid spacing
        test_input['content'] = '<div className="p-5 m-7">Invalid spacing</div>'
        result = self.test_hook(hook_path, test_input)
        self.results.append(('Design: Invalid spacing', result))
    
    def test_actually_works(self):
        """Test actually works protocol"""
        print("Testing actually works protocol...")
        
        hook_path = self.hooks_dir / 'pre-tool-use' / '04-actually-works.py'
        
        # Test 1: Untested claim
        test_input = {
            'tool': 'write_file',
            'path': 'fix.ts',
            'content': '// Fixed the issue\n// This should work now'
        }
        result = self.test_hook(hook_path, test_input)
        self.results.append(('Actually Works: Untested claim', result))
        
        # Test 2: Tested claim
        test_input['content'] = '// I tested this and it works\n// Test output: success'
        result = self.test_hook(hook_path, test_input, 'continue')
        self.results.append(('Actually Works: Tested claim', result))
    
    def test_code_quality(self):
        """Test code quality checks"""
        print("Testing code quality...")
        
        hook_path = self.hooks_dir / 'pre-tool-use' / '05-code-quality.py'
        
        # Test 1: Console.log in production
        test_input = {
            'tool': 'write_file',
            'path': 'component.tsx',
            'content': 'console.log("debug"); function Component() {}'
        }
        result = self.test_hook(hook_path, test_input)
        self.results.append(('Quality: Console.log', result))
        
        # Test 2: Any type
        test_input['content'] = 'const data: any = {}; function process(input: any) {}'
        result = self.test_hook(hook_path, test_input)
        self.results.append(('Quality: Any type', result))
    
    def test_collab_sync(self):
        """Test collaboration sync"""
        print("Testing collaboration sync...")
        
        hook_path = self.hooks_dir / 'pre-tool-use' / '01-collab-sync.py'
        
        # Create a test git repo
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save current dir
            original_dir = Path.cwd()
            
            try:
                # Setup test repo
                Path(tmpdir).mkdir(exist_ok=True)
                shutil.copytree('.claude', Path(tmpdir) / '.claude')
                
                # Change to test dir
                import os
                os.chdir(tmpdir)
                
                # Initialize git
                subprocess.run(['git', 'init'], capture_output=True)
                subprocess.run(['git', 'add', '.'], capture_output=True)
                subprocess.run(['git', 'commit', '-m', 'test'], capture_output=True)
                
                # Test sync
                test_input = {
                    'tool': 'write_file',
                    'path': 'test.ts',
                    'content': 'test'
                }
                result = self.test_hook(hook_path, test_input)
                self.results.append(('Collab: Git sync', result))
                
            finally:
                # Restore directory
                import os
                os.chdir(original_dir)
    
    def generate_report(self):
        """Generate test report"""
        print("\n📊 Test Results")
        print("===============\n")
        
        passed = sum(1 for _, r in self.results if r['status'] == 'pass')
        failed = sum(1 for _, r in self.results if r['status'] == 'fail')
        errors = sum(1 for _, r in self.results if r['status'] == 'error')
        
        print(f"Total: {len(self.results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"🔥 Errors: {errors}")
        print()
        
        # Show details
        for test_name, result in self.results:
            status_emoji = {
                'pass': '✅',
                'fail': '❌',
                'error': '🔥'
            }.get(result['status'], '❓')
            
            print(f"{status_emoji} {test_name}")
            
            if result['status'] != 'pass':
                if 'error' in result:
                    print(f"   Error: {result['error']}")
                elif 'expected' in result:
                    print(f"   Expected: {result['expected']}, Got: {result['actual']}")
                if 'message' in result and result['message']:
                    print(f"   Message: {result['message'][:100]}...")
            print()
        
        # Save detailed report
        report_path = Path('.claude/hooks/test-report.json')
        with open(report_path, 'w') as f:
            json.dump({
                'timestamp': str(Path.cwd()),
                'summary': {
                    'total': len(self.results),
                    'passed': passed,
                    'failed': failed,
                    'errors': errors
                },
                'results': [
                    {'test': name, **result}
                    for name, result in self.results
                ]
            }, f, indent=2)
        
        print(f"📄 Detailed report saved to: {report_path}")

if __name__ == "__main__":
    tester = HookTester()
    tester.run_tests()
