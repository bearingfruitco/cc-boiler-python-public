---
name: feature-workflow
aliases: [fw]
description: Python issue-based development workflow with TDD automation
category: workflow
---

Orchestrates Python issue-based development with automatic test generation and TDD enforcement.

## Arguments:
- $ACTION: start|validate|complete|test-status
- $ISSUE_NUMBER: GitHub issue number

## Enhanced with TDD Automation

This command now automatically generates tests when starting work on an issue, ensuring TDD compliance.

## Steps:

### Action: START
1. **Get Issue Details**
   ```python
   # Fetch issue from GitHub
   issue = github.get_issue(ISSUE_NUMBER)
   feature_name = slugify(issue.title)
   ```

2. **Auto-Generate Tests** (NEW!)
   ```python
   # Check if tests exist
   if not tests_exist(feature_name, ISSUE_NUMBER):
       # Generate tests from issue
       /generate-tests $feature_name --source issue --issue $ISSUE_NUMBER
       
       # Update issue
       github.add_comment(ISSUE_NUMBER, "✅ Tests auto-generated")
   ```

3. **Create Development Branch**
   ```bash
   BRANCH_NAME="feature/${ISSUE_NUMBER}-${feature_name}"
   git checkout -b $BRANCH_NAME
   ```

4. **Generate Implementation Plan**
   ```markdown
   # Feature: ${issue.title}
   
   ## TDD Status:
   - [x] Tests Generated: tests/test_${feature_name}.py
   - [ ] Tests Reviewed
   - [ ] Tests Running (Red)
   - [ ] Implementation Complete (Green)
   - [ ] Refactoring Done
   
   ## Components from Issue:
   ${parse_python_components(issue.body)}
   
   ## Implementation Checklist:
   - [ ] Run tests first (see them fail)
   - [ ] Implement minimal code to pass
   - [ ] Refactor for quality
   - [ ] Update documentation
   ```

5. **Open Test File** (NEW!)
   ```bash
   # Open the generated test file in editor
   ${EDITOR} tests/test_${feature_name}.py
   
   # Run tests to see them fail
   pytest tests/test_${feature_name}.py -v
   ```

### Action: TEST-STATUS (NEW!)
Check TDD progress for the feature:
```bash
/fw test-status 23

Output:
Feature #23: User Authentication
├── Tests: ✅ Generated (tests/test_user_auth.py)
├── Coverage: 0% (no implementation yet)
├── Status: 🔴 Red (5 tests, 0 passing)
└── Next: Implement auth.py to make tests pass
```

### Action: VALIDATE
1. **TDD Compliance Check** (NEW!)
   ```python
   # Ensure tests exist and pass
   if not run_tests(feature_name):
       print("❌ Tests must pass before committing")
       exit(1)
   
   # Check test coverage
   coverage = get_coverage(feature_name)
   if coverage < 80:
       print(f"⚠️ Low coverage: {coverage}% (minimum: 80%)")
   ```

2. **Pre-Commit Validation**
   ```bash
   # Python quality checks
   ruff check src/
   mypy src/
   pytest tests/test_${feature_name}.py
   ```

3. **Generate Commit Message**
   ```python
   # TDD-aware commit message
   message = f"feat: {issue.title} (#${ISSUE_NUMBER})\n\n"
   message += f"- Tests: {test_count} passing\n"
   message += f"- Coverage: {coverage}%\n"
   message += f"- Components: {', '.join(components)}"
   ```

### Action: COMPLETE
1. **Final TDD Validation & Verification**
   ```bash
   # All tests must pass
   pytest tests/
   
   # Coverage check
   pytest --cov=src --cov-report=term-missing
   
   # Type checking
   mypy src/
   
   # Run completion verification (NEW!)
   /verify ${feature_name} --level comprehensive
   ```
   
   ```python
   # Verification must pass before completion
   verification_result = run_verification(feature_name, 'comprehensive')
   if not verification_result.passed:
       print("❌ Cannot complete - verification failed!")
       print("Fix the following issues:")
       show_verification_failures(verification_result)
       exit(1)
   ```

2. **Generate PR Body**
   ```markdown
   Closes #${ISSUE_NUMBER}
   
   ## 🧪 TDD Compliance
   - ✅ Tests written first
   - ✅ All tests passing (${test_count} tests)
   - ✅ Coverage: ${coverage}%
   - ✅ Type hints: 100%
   
   ## 📋 Implementation
   ${list_implemented_components()}
   
   ## 🔍 Test Summary
   ```python
   # Example test
   def test_user_authentication():
       user = authenticate("user@example.com", "password")
       assert user.is_authenticated
       assert user.email == "user@example.com"
   ```
   ```

3. **Create PR with Test Results**
   ```python
   # Include test output in PR
   pr_body += "\n## Test Results\n"
   pr_body += "```\n"
   pr_body += run_pytest_with_output()
   pr_body += "```\n"
   
   github.create_pull_request(title, pr_body)
   ```

## What's New with TDD Integration:

1. **Automatic Test Generation** - Tests created from issue description
2. **TDD Enforcement** - Can't commit without passing tests  
3. **Test-First Workflow** - Opens test file before implementation
4. **Coverage Tracking** - Monitors test coverage throughout
5. **Test Status Command** - Check TDD progress anytime

## Workflow Example:

```bash
# 1. Start feature (auto-generates tests)
/fw start 23
# Output: 
# ✅ Tests generated: tests/test_user_auth.py
# 🔴 Running tests... 5 failed (expected)
# 📝 Ready to implement!

# 2. Check test status
/fw test-status 23
# Shows which tests are failing

# 3. Implement features to make tests pass
/py-api /auth/login POST
/py-agent AuthValidator

# 4. Validate (ensures tests pass)
/fw validate 23

# 5. Complete with full test report
/fw complete 23
```

## Integration with Other Commands:

- **/process-tasks** - Now checks for tests before allowing work
- **/py-prd** - Includes test specifications
- **/capture-to-issue** - Can trigger test generation with `--tests`
- **/generate-tests** - Called automatically by this workflow

## Configuration:

Set TDD preferences in `.claude/settings.json`:
```json
{
  "tdd": {
    "auto_generate_tests": true,
    "enforce_tests_first": true,
    "minimum_coverage": 80,
    "open_tests_in_editor": true
  }
}
```
