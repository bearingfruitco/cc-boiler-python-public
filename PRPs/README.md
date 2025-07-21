# PRP (Product Requirement Prompt) System

## Overview
PRPs are enhanced PRDs optimized for AI agents to achieve one-pass implementation success.

## Directory Structure
- `templates/` - PRP templates for different use cases
- `ai_docs/` - Cached documentation for offline AI context
- `active/` - Current PRPs being worked on
- `completed/` - Finished PRPs for reference
- `execution_logs/` - Execution tracking and metrics

## Workflow
1. Create PRP: `/prp-create [feature]` or `/py-prd [feature] --prp`
2. Execute: `python scripts/prp_runner.py --prp [feature]`
3. Track: `/prp-status [feature]`
4. Complete: `/prp-complete [feature]`

## Key Differences from PRDs
- **Context-Rich**: Includes specific file paths, URLs, and gotchas
- **Validation Loops**: 4-level automated validation
- **Automation Ready**: Can be executed with prp_runner.py
- **Pattern-Focused**: Emphasizes existing code patterns

## Integration with Existing Workflow
- Use `/py-prd` for quick planning (traditional PRDs)
- Use `/prp-create` for complex features needing automation
- Both workflows integrate with `/gt` and `/pt` task management
- PRPs enhance but don't replace existing commands
