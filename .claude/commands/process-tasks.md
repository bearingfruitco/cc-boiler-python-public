---
name: process-tasks
aliases: [pt]
description: Process tasks with TDD enforcement
category: workflow
---

Process tasks for feature: $ARGUMENTS

## Enhanced with TDD Checks

This command now ensures tests exist before allowing implementation work.

## Workflow:

### 1. Pre-Implementation Check (NEW!)
```python
# Before starting any implementation task
feature_name = $ARGUMENTS
if not tests_exist(feature_name):
    print("🧪 No tests found! Generating tests first...")
    
    # Look for PRD/PRP/Issue
    source = find_best_source(feature_name)
    /generate-tests $feature_name --source $source
    
    print("✅ Tests generated. Please review before proceeding.")
    print("📝 Run: pytest tests/test_${feature_name}.py -v")
```

### 2. Load Task List
```python
task_file = f"docs/project/features/{feature_name}-tasks.md"
tasks = load_tasks(task_file)
```

### 3. TDD Task Processing
For each task:

#### a. Check Task Type
```python
if task.requires_code:
    # Ensure specific test exists
    test_name = f"test_{task.component}_{task.function}"
    if not test_exists(test_name):
        print(f"⚠️ Missing test for: {test_name}")
        print("Add test case before implementing")
```

#### b. Show Test Status
```bash
Working on task X.Y: [description]

📋 TDD Status:
- Tests: tests/test_${feature_name}.py
- Related test: test_${component}_${function}
- Status: 🔴 Failing (expected)

Run tests: pytest tests/test_${feature_name}.py::${test_name} -v
```

#### c. Implementation Guidance
```python
# Show what needs to be implemented
print("To make test pass, implement:")
print(f"- Module: src/{module}.py")
print(f"- Function: {function_signature}")
print(f"- Expected behavior: {test_description}")
```

### 4. Post-Implementation Validation (ENHANCED!)
After implementing each task:
```python
# Auto-run related tests
test_result = run_specific_test(test_name)

if test_result.passed:
    print("✅ Test passing! Task implementation complete.")
    
    # Trigger verification if claiming completion
    if task.is_final or "complete" in task.description:
        print("🔍 Running completion verification...")
        verification = run_verification(feature_name, level='standard')
        
        if verification.passed:
            mark_task_complete(task)
        else:
            print("❌ Verification failed - fix issues before marking complete")
            show_verification_failures(verification)
    else:
        mark_task_complete(task)
else:
    print("🔴 Test still failing. Review implementation:")
    print(test_result.failure_message)
```

### 5. Progress Tracking
```markdown
## Task Progress
- [✓] 1.1 Create User model - ✅ test_user_model_creation passing
- [✓] 1.2 Add validation - ✅ test_user_validation passing  
- [ ] 1.3 Create repository - 🔴 test_user_repository failing
- [ ] 1.4 Add authentication - ⚪ test not yet run
```

## Important TDD Rules:

1. **No Implementation Without Tests**
   - Every code task must have a corresponding test
   - Tests must exist before implementation

2. **Incremental Development**
   - Implement minimum code to pass test
   - Refactor only after test passes

3. **Test Status Visibility**
   - Always show which test relates to current task
   - Display test status (red/green)

4. **Automatic Test Runs**
   - Tests run automatically after each implementation
   - Must pass before marking task complete

## Task Format:
```markdown
Working on task X.Y: [description]
Test: test_${component}_${function} (🔴 failing)
Location: src/${module}.py
Next: Implement ${function} to make test pass
```

## Configuration:
Control TDD behavior in `.claude/settings.json`:
```json
{
  "tdd": {
    "require_tests_before_tasks": true,
    "auto_run_tests": true,
    "show_test_hints": true
  }
}
```

## Example Session:
```bash
/pt user-authentication

# Output:
🧪 Checking tests... Found: tests/test_user_authentication.py
📋 Loading tasks from: docs/project/features/user-authentication-tasks.md

Working on task 1.1: Create User model
Test: test_user_model_creation (🔴 failing)

To make test pass:
- Create: src/models/user.py
- Define: class User(BaseModel) with email, hashed_password
- Include: password validation and hashing

[After implementation]
🧪 Running test... ✅ PASSED!
Task 1.1 marked complete.

Moving to task 1.2...
```
