---
name: compress-context
aliases: [compress, ctx-compress, token-save, cc]
description: Compress context with focus options to preserve specific information
category: workflow
---

Intelligently compress the current context to save tokens while preserving critical information.

## Usage
```bash
/compress-context [options]
/compress [options]
/cc [options]
```

## Options

### --focus
Specify areas to preserve in full detail during compression:
```bash
/compress --focus="api design decisions, security choices"
/compress --focus="database schema, authentication flow"
```

### --exclude  
Explicitly exclude topics from compressed output:
```bash
/compress --exclude="debugging logs, test failures"
/compress --exclude="old feature discussions"
```

### --target
Target compression percentage:
```bash
/compress --target=50  # Compress to 50% of current size
/compress --target=30  # Aggressive compression to 30%
```

### --preserve
Force preservation of specific elements:
```bash
/compress --preserve="task-ledger, current-prd"
/compress --preserve="error-states, security-config"
```

## Compression Strategies

### 1. Smart Summarization
- Completed work → outcome summaries
- Long discussions → key decisions
- Code examples → essential snippets
- Error logs → root causes only

### 2. Contextual Preservation
Based on your focus areas:
- **API Design**: Keeps endpoints, schemas, contracts
- **Security**: Preserves auth flows, encryption decisions
- **Database**: Maintains schema, migrations, indexes
- **Testing**: Keeps coverage metrics, critical test cases

### 3. Automatic Preservation
Always keeps:
- Active Task Ledger entries
- Current PRD requirements
- Last 5 critical decisions
- Security configurations
- Design system rules
- Active error states
- Team coordination info

## Token Savings Analysis

The command provides detailed metrics:
```
📊 Compression Results:
- Original: 145,230 tokens
- Compressed: 42,350 tokens
- Savings: 70.8% (102,880 tokens)
- Preserved: API contracts, auth flow, current tasks
- Excluded: 47 debug sessions, 23 resolved errors
```

## Integration with Workflow

### Auto-Triggers
Compression automatically runs when:
- Context usage > 75%
- Before `/orch` multi-agent tasks
- Starting new feature with `/fw`
- Switching branches with `/bsw`

### Task Ledger Integration
- Completed tasks are summarized
- Active tasks remain detailed
- Links to issues preserved
- Progress metrics maintained

### Smart Resume Compatible
Compressed state fully supports `/sr`:
- Restoration points created
- Critical context preserved
- Work history maintained
- Decision rationale kept

## Examples

### Focused API Development
```bash
/compress --focus="api endpoints, request/response schemas" --exclude="ui discussions"
```

### Security Review Preparation  
```bash
/compress --focus="authentication, authorization, encryption" --target=40
```

### Multi-Agent Prep
```bash
/compress --preserve="task-distribution, agent-roles" --exclude="implementation-details"
```

### Branch Switch Optimization
```bash
/compress --focus="current-branch-work" --exclude="other-features"
```

## Best Practices

1. **Before Major Features**
   ```bash
   /compress --focus="architecture-decisions"
   ```

2. **After Debug Sessions**
   ```bash
   /compress --exclude="debug-logs, stack-traces"
   ```

3. **Team Handoffs**
   ```bash
   /compress --focus="decisions, blockers" --preserve="task-ledger"
   ```

4. **Context Switches**
   ```bash
   /compress --focus="next-feature" --exclude="completed-work"
   ```

## Advanced Features

### Compression Profiles
Save common compression patterns:
```bash
/compress --save-profile="api-work"
/compress --use-profile="api-work"
```

### Incremental Compression
Compress in stages:
```bash
/compress --incremental --target=70  # First pass
/compress --incremental --target=50  # If needed
```

### Compression History
View what was compressed:
```bash
/compress --history
# Shows last 10 compressions with savings
```

## State Storage

Compression artifacts stored in:
- `.claude/compressions/` - Compressed summaries
- `.claude/archives/` - Original content
- `.claude/compression-log.json` - Compression history

All compression is reversible through archives.
