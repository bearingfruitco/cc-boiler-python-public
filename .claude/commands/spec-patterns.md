# Specification Pattern Library

Extract, store, and reuse successful specification patterns from your PRDs and implementations.

## Arguments:
- $ACTION: extract|list|apply|show|search
- $PATTERN: Pattern name or search term

## Actions:

### EXTRACT - Create pattern from recent work
```bash
/specs extract --from-feature auth-system
/specs extract --from-prd user-profile
```

Creates a reusable pattern by analyzing:
- PRD structure and requirements
- Implementation approach
- File organization
- Success metrics

### LIST - Show available patterns
```bash
/specs list
/specs list --tag authentication
/specs list --recent
```

Output:
```
=== SPECIFICATION PATTERNS ===

📦 auth-jwt (3 days ago)
   Tags: authentication, jwt, api
   Files: 12 | Success rate: 95%
   
📦 form-validated (1 week ago)
   Tags: forms, validation, zod
   Files: 8 | Success rate: 88%

📦 crud-api (2 weeks ago)
   Tags: api, database, crud
   Files: 6 | Success rate: 92%

💡 Apply with: /specs apply [pattern-name]
```

### APPLY - Use pattern for new feature
```bash
/specs apply auth-jwt --to new-feature
/specs apply form-validated --adapt
```

This will:
1. Show pattern structure
2. Adapt to your feature name
3. Generate starter files
4. Create PRD template

### SHOW - Display pattern details
```bash
/specs show auth-jwt
```

Shows:
- Original PRD sections
- File structure created
- Key implementation patterns
- Success indicators

### SEARCH - Find relevant patterns
```bash
/specs search "user authentication"
/specs search --similar-to current-prd
```

## Implementation:

```typescript
// Pattern structure
interface SpecPattern {
  id: string;
  name: string;
  created: string;
  source: {
    prd: string;
    implementations: string[];
  };
  specification: {
    requirements: string[];
    acceptance_criteria: string[];
    technical_approach: string[];
    api_contracts: string[];
  };
  implementation_patterns: {
    [file: string]: {
      file_type: string;
      patterns_used: string[];
    }
  };
  metrics: {
    files_created: number;
    time_to_implement: number;
    bugs_found: number;
    iterations: number;
  };
  tags: string[];
  success_indicators: string[];
}
```

## Pattern Evolution:

Patterns improve over time:
- Track success rate
- Update with fixes
- Merge similar patterns
- Version improvements

## Integration:

Works with existing commands:
- `/prd create --from-pattern auth-jwt`
- `/gt generate --use-pattern crud-api`
- `/orch assign --with-patterns`

## Storage:
```
.claude/specs/
  ├── patterns/
  │   ├── auth-jwt-a1b2c3d4.json
  │   ├── form-validated-e5f6g7h8.json
  │   └── crud-api-i9j0k1l2.json
  ├── templates/
  │   └── (generated templates)
  └── index.json
```

## Benefits:
- Learn from successful implementations
- Reduce time to implement similar features
- Maintain consistency across features
- Build institutional knowledge
- Accelerate onboarding
