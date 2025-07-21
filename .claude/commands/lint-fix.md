---
name: lint-fix
aliases: [fix-lint, format-fix]
description: Run linters with auto-fix enabled
category: quality
---

Run Python linters and formatters with auto-fix enabled.

## Tools Used:
- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Fast Python linter (replaces flake8, pylint)
- **autopep8**: PEP8 fixes (optional)

## Default Behavior:
```bash
# Run all fixers
/lint:fix

# Equivalent to:
black src/ tests/
isort src/ tests/
ruff check --fix src/ tests/
```

## Options:
- $PATH: specific path or file (default: src/ tests/)
- $TOOL: black|isort|ruff|all (default: all)
- $CHECK: --check (dry run, no changes)

## Examples:

### Fix everything
```bash
/lint:fix
```

### Fix specific file
```bash
/lint:fix src/agents/base.py
```

### Check only (no changes)
```bash
/lint:fix --check
```

### Run specific tool
```bash
/lint:fix --tool black
/lint:fix --tool isort
```

## Configuration Files:

### pyproject.toml
```toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'

[tool.isort]
profile = "black"
line_length = 88

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]  # line too long (black handles)
```

## Pre-commit Integration:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix]
```

## Common Fixes:
- Import ordering and grouping
- Line length formatting
- Trailing whitespace
- Missing blank lines
- Quote consistency
- Unused imports
- Undefined names

## Integration:
- Used in `safe-commit` chain
- Pre-commit hook
- CI/CD pipeline
