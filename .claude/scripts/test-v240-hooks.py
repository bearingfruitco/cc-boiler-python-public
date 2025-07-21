#!/usr/bin/env python3
"""Test script to verify v2.4.0 hooks are working correctly."""

import json
import subprocess
import sys
from pathlib import Path

def test_creation_guard():
    """Test the Python creation guard hook."""
    print("Testing Creation Guard Hook...")
    
    # Create a test Python file that tries to create a class
    test_content = '''
class UserModel:
    """A test class."""
    pass

def test_function():
    """A test function."""
    return True
'''
    
    # Simulate hook input
    hook_input = {
        "tool": "write_file",
        "path": "test_module.py",
        "content": test_content
    }
    
    # Run the hook
    result = subprocess.run(
        ["python3", ".claude/hooks/pre-tool-use/16-python-creation-guard.py"],
        input=json.dumps(hook_input),
        capture_output=True,
        text=True
    )
    
    print(f"Exit code: {result.returncode}")
    if result.stdout:
        try:
            output = json.loads(result.stdout)
            print(f"Action: {output.get('action')}")
            if output.get('message'):
                print(f"Message preview: {output['message'][:100]}...")
        except json.JSONDecodeError as e:
            print(f"Error decoding output: {e}")
            print(f"Raw output: {result.stdout}")
    
    if result.stderr:
        print(f"Stderr: {result.stderr}")
    
    return result.returncode == 0

def test_dependency_tracker():
    """Test the dependency tracker hook."""
    print("\nTesting Dependency Tracker Hook...")
    
    # Simulate modifying a Python file
    hook_input = {
        "tool": "write_file",
        "path": "src/models/user.py",
        "content": "# Modified content"
    }
    
    result = subprocess.run(
        ["python3", ".claude/hooks/pre-tool-use/17-python-dependency-tracker.py"],
        input=json.dumps(hook_input),
        capture_output=True,
        text=True
    )
    
    print(f"Exit code: {result.returncode}")
    if result.stdout:
        try:
            output = json.loads(result.stdout)
            print(f"Action: {output.get('action')}")
        except json.JSONDecodeError as e:
            print(f"Error decoding output: {e}")
            print(f"Raw output: {result.stdout}")
    
    return result.returncode == 0

def test_response_capture():
    """Test the response capture hook."""
    print("\nTesting Response Capture Hook...")
    
    # Simulate an AI response
    ai_response = '''
    I'll create a FastAPI endpoint for user authentication.
    
    ## Implementation Plan
    
    1. Create Pydantic models for request/response
    2. Implement authentication logic
    3. Add JWT token generation
    
    ```python
    class LoginRequest(BaseModel):
        email: str
        password: str
    
    async def authenticate(request: LoginRequest):
        # Authentication logic here
        pass
    ```
    '''
    
    hook_input = {
        "tool": "some_tool",
        "ai_response": ai_response
    }
    
    result = subprocess.run(
        ["python3", ".claude/hooks/post-tool-use/04-python-response-capture.py"],
        input=json.dumps(hook_input),
        capture_output=True,
        text=True
    )
    
    print(f"Exit code: {result.returncode}")
    if result.stdout:
        try:
            output = json.loads(result.stdout)
            print(f"Action: {output.get('action')}")
            if output.get('message'):
                print(f"Capture notification: {output['message']}")
        except json.JSONDecodeError as e:
            print(f"Error decoding output: {e}")
            print(f"Raw output: {result.stdout}")
    
    return result.returncode == 0

def test_pyexists_integration():
    """Test that pyexists would work with existing components."""
    print("\nTesting PyExists Integration...")
    
    # First, let's see if UserModel exists in the project
    from pathlib import Path
    import sys
    
    # Add the project root to sys.path
    project_root = Path.cwd()
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # Import the check_exists function from the hook
    spec = __import__('importlib.util').util.spec_from_file_location(
        "creation_guard",
        ".claude/hooks/pre-tool-use/16-python-creation-guard.py"
    )
    creation_guard = __import__('importlib.util').util.module_from_spec(spec)
    spec.loader.exec_module(creation_guard)
    
    # Check if UserModel exists
    results = creation_guard.check_exists("UserModel", "class")
    
    if results['exact_matches']:
        print("✅ UserModel found!")
        for match in results['exact_matches']:
            print(f"  Type: {match['type']}")
            print(f"  Locations: {', '.join(match['locations'][:3])}")
    else:
        print("❌ UserModel not found")
    
    # Check for similar names
    if results['similar_names']:
        print(f"Similar names: {', '.join(results['similar_names'][:3])}")
    
    return True

def main():
    """Run all tests."""
    print("=== Testing v2.4.0 Hook Integration ===\n")
    
    tests = [
        test_creation_guard,
        test_dependency_tracker,
        test_response_capture,
        test_pyexists_integration
    ]
    
    results = []
    for test in tests:
        try:
            success = test()
            results.append((test.__name__, success))
        except Exception as e:
            print(f"Error in {test.__name__}: {e}")
            import traceback
            traceback.print_exc()
            results.append((test.__name__, False))
    
    print("\n=== Test Results ===")
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(success for _, success in results)
    print(f"\nOverall: {'✅ All tests passed!' if all_passed else '❌ Some tests failed'}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
