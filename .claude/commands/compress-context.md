# Compress Context

Compresses current context to save tokens when approaching limits.

## Usage

```bash
/compress-context
/compress  # alias
/ctx-compress  # alias
/token-save  # alias
```

## What It Does

When context usage exceeds 75%, this command:

1. **Summarizes Completed Work**
   - Archives finished tasks
   - Compresses verbose descriptions
   - Keeps only essential outcomes

2. **Optimizes Documentation**
   - Converts verbose text to bullet points
   - Removes redundant information
   - Preserves critical decisions

3. **Archives Old State**
   - Moves old checkpoints to archive
   - Compresses chat transcripts
   - Maintains reference links

4. **Token Reduction Strategies**
   - Uses abbreviations for common terms
   - Removes code comments in examples
   - Compresses file paths

## Auto-Activation

Automatically triggered when:
- Context usage > 75%
- Before large file operations
- When adding extensive documentation

## Token Savings

Typical compression achieves:
- 50-70% reduction in context size
- Preserves all critical information
- Maintains full traceability

## Example

```bash
# Manual compression
/compress-context

# Check current usage
/context-usage

# Compress with specific target
/cc --target=50  # Compress to 50% of current size
```

## Best Practices

1. Run before major new features
2. Use after completing task phases
3. Archive before team handoffs
4. Compress before context switches

## Preserved Information

Always keeps:
- Current task state
- Active PRD requirements
- Recent decisions
- Security configurations
- Design system rules
- Error states

## Implementation

The command:
1. Analyzes current context usage
2. Identifies compressible content
3. Creates compressed summaries
4. Archives original content
5. Updates active context
6. Reports token savings

This ensures efficient use of context window while maintaining all essential project information.
