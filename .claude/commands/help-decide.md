---
name: help-decide
aliases: [decide, when-to-use, command-guide]
description: Interactive decision guide for choosing the right command
category: help
---

Get help deciding which command to use based on your situation.

## Usage
```bash
/help-decide
/decide
```

## Interactive Decision Tree

The command will ask you questions to determine the best command:

### Question 1: What are you trying to do?
1. **Start something new** → `/init-project`, `/py-prd`, or `/prp`
2. **Capture work/ideas** → `/cti`, `/prp`, or `/mt`
3. **Break down work** → `/gi`, `/gt`, or `/think-through`
4. **Fix a bug** → `/bt`, `/mt`, or `/generate-tests`
5. **Daily development** → `/fw`, `/pt`, or `/test`

### Question 2: How well defined is it?
1. **Crystal clear** → `/cti` or `/mt`
2. **General idea** → `/py-prd` or `/think-through`
3. **Needs research** → `/prp` or `/research`
4. **Not sure** → `/think-through`

### Question 3: How big is it?
1. **< 30 minutes** → `/mt`
2. **Single feature** → `/cti` → `/gt`
3. **Multiple features** → `/py-prd` → `/gi`
4. **Entire project** → `/init-project`

## Quick Reference

### When to use CTI (Capture to Issue)
✅ Claude gave you a solution
✅ You know what to build
✅ Clear implementation path
✅ No research needed

```bash
/cti "Add validation to form inputs"
```

### When to use PRP (Progressive Research)
❓ Multiple unknowns
❓ Need to explore options
❓ Complex architecture decisions
❓ "Figure out how to..."

```bash
/prp "Lead deduplication strategy"
```

### When to use PRD (Requirements Doc)
📋 New feature/component
📋 Need formal requirements
📋 Multiple stakeholders
📋 Want issues generated

```bash
/py-prd "User notification system"
```

### When to use MT (Micro Task)
⚡ Quick fix (< 30 min)
⚡ No issue needed
⚡ Obvious solution
⚡ Small improvement

```bash
/mt "Fix typo in README"
```

### When to use BT (Bug Track)
🐛 Found a bug
🐛 Customer reported issue
🐛 Need to track fix
🐛 Requires investigation

```bash
/bt add "Import fails on empty fields"
```

## Common Scenarios

### "Claude just gave me a detailed solution"
→ Use `/cti` to capture it as an issue

### "I need to figure out how to do X"
→ Use `/prp` for research-driven development

### "I want to build a new feature"
→ Use `/py-prd` for requirements, then `/gi`

### "I found a small bug"
→ Use `/mt` if quick, `/bt` if needs tracking

### "Starting a brand new project"
→ Use `/init-project` for setup

## Workflow Examples

### Research → Implementation
```
/prp "ML lead scoring" → /prp-execute → /prp-complete → /cti
```

### Requirements → Development
```
/py-prd "Auth system" → /gi → /fw start → /gt → /pt
```

### Bug Fix Flow
```
/bt add → /generate-tests → fix → /test → /bt resolve
```

## Still Unsure?

Try: `/think-through "What's the best approach for [your task]?"`

This will analyze your specific situation and recommend the right command!
