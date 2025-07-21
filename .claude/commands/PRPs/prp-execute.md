---
name: prp-execute
aliases: [run-prp, execute-prp]
description: Execute a PRP with optional automation
category: PRPs
---

# Execute PRP: $ARGUMENTS

## Execution Mode Selection

1. **Interactive** (Default for exploration):
   ```bash
   python scripts/prp_runner.py --prp $ARGUMENTS --interactive
   ```

2. **Automated** (For known patterns):
   ```bash
   python scripts/prp_runner.py --prp $ARGUMENTS --output-format json
   ```

3. **Streaming** (For monitoring):
   ```bash
   python scripts/prp_runner.py --prp $ARGUMENTS --output-format stream-json
   ```

## Pre-Execution Checks
- [ ] PRP exists in PRPs/active/
- [ ] Validation gates are defined
- [ ] Dependencies available
- [ ] Tests are specified

## Post-Execution
- Review costs and duration
- Check success metrics
- Move to completed if done
