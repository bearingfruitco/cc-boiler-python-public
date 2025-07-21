---
name: think-level
aliases: [tl-think, thinking-level]
description: Set or display the thinking level for complex problem solving
category: intelligence
---

Set the thinking level for Claude's problem-solving approach on the next prompt.

## Usage
```bash
/think-level [level] [--scope task|session|permanent]
```

## Thinking Levels

### standard (default)
Normal Claude reasoning - suitable for most tasks
- Token usage: Normal
- Use for: Regular development tasks

### deep
Enhanced reasoning with more exploration
- Token usage: ~2x normal
- Use for: Complex algorithms, architecture decisions
- Triggers: "think" in your next prompt

### ultra
Maximum reasoning depth
- Token usage: ~5x normal  
- Use for: Critical bugs, performance optimization, security issues
- Triggers: "think harder" or "ultra think" in your next prompt

## Options

- `--scope task`: Apply to next task only (default)
- `--scope session`: Apply to current session
- `--scope permanent`: Save to project settings

## Examples

### Set for next task
```bash
/think-level deep
# Next prompt will use enhanced thinking
```

### Set for session
```bash
/think-level ultra --scope session
# All prompts this session use maximum thinking
```

### Check current level
```bash
/think-level
# Shows: Current thinking level: standard (task scope)
```

## Integration with Commands

Some commands automatically adjust thinking level:
- `/think-through` - Uses deep by default
- `/prp-create` - Uses deep for research
- `/security-check` - Uses ultra for security analysis
- `/performance-monitor` - Uses deep for optimization

## Best Practices

1. **Start with standard** - Most tasks don't need enhanced thinking
2. **Use deep for design** - Architecture and API design benefit from deeper analysis  
3. **Reserve ultra for critical issues** - Security bugs, data loss risks
4. **Monitor token usage** - Check with `/analytics token-usage`

## Token Usage Guide

| Level | Multiplier | 1K prompt becomes | Use case |
|-------|------------|-------------------|----------|
| standard | 1x | 1K tokens | Daily development |
| deep | ~2x | 2K tokens | Complex features |
| ultra | ~5x | 5K tokens | Critical issues |

## Automatic Triggers

The system automatically increases thinking level for:
- Security-related prompts (→ deep)
- Performance optimization (→ deep)  
- Data integrity issues (→ ultra)
- Architecture decisions (→ deep)

## State Persistence

Current thinking level is stored in:
- `.claude/context/state.json` (session/task scope)
- `.claude/settings.json` (permanent scope)

This integrates with Smart Resume (`/sr`) to restore your thinking preferences.
