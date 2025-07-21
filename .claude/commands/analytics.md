# Analytics

Track command usage and identify workflow improvements.

## Arguments:
- $ACTION: track|report|insights|export

## Why This Command:
- Understand usage patterns
- Identify pain points
- Improve workflows
- Track productivity

## Implementation:

### Usage Tracking
Automatically track in `.claude/analytics/usage.json`:

```json
{
  "sessions": [
    {
      "id": "session-1234",
      "start": "2024-01-15T09:00:00Z",
      "end": "2024-01-15T17:30:00Z",
      "commands": [
        {
          "command": "smart-resume",
          "timestamp": "2024-01-15T09:00:15Z",
          "duration": 2.3,
          "success": true
        },
        {
          "command": "create-component",
          "args": ["ui", "Button"],
          "timestamp": "2024-01-15T09:05:00Z",
          "duration": 5.1,
          "success": true
        },
        {
          "command": "validate-design",
          "timestamp": "2024-01-15T09:10:00Z",
          "duration": 3.2,
          "success": false,
          "error": "3 violations found"
        }
      ]
    }
  ],
  "aggregates": {
    "totalCommands": 1247,
    "uniqueCommands": 18,
    "successRate": 0.94,
    "avgSessionLength": 465,
    "mostUsed": [
      {"command": "validate-design", "count": 234},
      {"command": "smart-resume", "count": 189},
      {"command": "create-component", "count": 156}
    ],
    "errorPatterns": [
      {"pattern": "design violations", "count": 45},
      {"pattern": "missing tests", "count": 23}
    ]
  }
}
```

### Action: REPORT
Generate usage report:

```markdown
## 📊 Claude Code Analytics Report

### Period: Last 7 Days

#### Usage Summary
- Total Commands: 487
- Unique Commands: 15/22 (68%)
- Success Rate: 94%
- Avg Commands/Day: 69

#### Top Commands
1. `/validate-design` - 89 uses (18%)
2. `/smart-resume` - 67 uses (14%)
3. `/create-component` - 45 uses (9%)
4. `/test-runner` - 38 uses (8%)
5. `/checkpoint` - 34 uses (7%)

#### Workflow Patterns
- Morning: 78% start with `/smart-resume`
- Pre-commit: 92% run `/validate-design`
- Feature complete: Average 23 commands

#### Error Analysis
- Design violations: 34 occurrences
  - Font issues: 18 (53%)
  - Spacing issues: 12 (35%)
  - Color issues: 4 (12%)

#### Time Analysis
- Avg session: 2.5 hours
- Peak hours: 10am-12pm, 2pm-4pm
- Commands/hour: 28

#### Productivity Metrics
- Components created: 23
- Features completed: 4
- PRs created: 6
- Tests written: 67
```

### Action: INSIGHTS
AI-powered insights:

```markdown
## 🧠 Workflow Insights

### Observations
1. **High validation failure rate (38%) for first attempts**
   - Suggestion: Run validation in watch mode
   - Command: `/validate-design --watch`

2. **Test creation lags component creation**
   - 23 components created
   - Only 14 have tests
   - Suggestion: Use `--with-tests` flag

3. **Context loss after lunch**
   - 3pm resume takes 2x longer
   - Suggestion: Create pre-lunch checkpoint

### Recommended Workflow Improvements

#### 1. Morning Routine
Instead of:
```
/smart-resume
/validate-design
/test-runner
```

Try:
```
/morning-setup  # New composite command
```

#### 2. Component Creation
Current: 45% need design fixes after creation

Improved:
```
/cc ui Button --validate --with-tests
```

#### 3. Pre-PR Checklist
Create command: `/pre-pr-check` that runs:
- Validation
- Tests
- Performance
- Security
- Documentation check
```

### Action: TRACK
Real-time tracking:

```typescript
// Automatically added to each command
export function trackCommand(command: string, args: any[]) {
  const start = Date.now();
  
  try {
    const result = executeCommand(command, args);
    
    analytics.track({
      command,
      args,
      duration: Date.now() - start,
      success: true,
      context: getCurrentContext()
    });
    
    return result;
  } catch (error) {
    analytics.track({
      command,
      args,
      duration: Date.now() - start,
      success: false,
      error: error.message
    });
    
    throw error;
  }
}
```

### Privacy & Settings

```json
{
  "analytics": {
    "enabled": true,
    "trackErrors": true,
    "trackTiming": true,
    "trackArgs": false,  // Privacy: don't track component names
    "retention": 30,     // Days to keep data
    "share": false       // Share anonymized data to improve commands
  }
}
```

This helps identify which commands need improvement and how to optimize workflows!
