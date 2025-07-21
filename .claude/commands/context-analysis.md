# Context Analysis Command

Analyze the completeness and quality of context for the current project.

## Steps:

1. **Check for PRD**
   ```bash
   # Look for PRDs in project features
   ls -la docs/project/features/*.md
   ```
   - Score: 20 points if PRD exists, 0 if not

2. **Check for Examples**
   ```bash
   # Count pattern examples
   ls -la docs/examples/patterns/*.md | wc -l
   
   # Count anti-pattern docs
   ls -la docs/examples/anti-patterns/*.md | wc -l
   ```
   - Score: 5 points per pattern example (max 20)
   - Score: 5 points per anti-pattern doc (max 10)

3. **Check MCP Connections**
   ```bash
   # List available MCP functions
   # Check for Supabase, GitHub, etc.
   ```
   - Score: 5 points per connected MCP (max 20)

4. **Review Learned Patterns**
   ```bash
   # Check context state
   cat .claude/context/state.json | jq '.learned_patterns | length'
   ```
   - Score: 3 points per learned pattern (max 15)

5. **Check Task Decomposition**
   ```bash
   # Look for task files
   ls -la docs/project/features/*-tasks.md
   ```
   - Score: 15 points if tasks exist

6. **Context Quality Report**
   ```
   ===== CONTEXT QUALITY SCORE =====
   
   Documentation:     [X]/20
   - PRD:            [✓/✗]
   - Business Logic: [✓/✗]
   
   Examples:          [X]/30  
   - Patterns:       [count]
   - Anti-patterns:  [count]
   
   Integration:       [X]/20
   - MCPs Connected: [list]
   
   Memory:           [X]/15
   - Learned:       [count]
   - Decisions:     [count]
   
   Structure:        [X]/15
   - Tasks:         [✓/✗]
   - Organization:  [✓/✗]
   
   --------------------------------
   TOTAL SCORE:      [X]/100
   
   Grade: [A-F]
   Status: [Excellent/Good/Needs Work]
   ```

7. **Recommendations**
   Based on score, suggest improvements:
   
   If Documentation < 15:
   - "Create PRD using /prd command"
   - "Add business logic documentation"
   
   If Examples < 20:
   - "Add more pattern examples in docs/examples/patterns/"
   - "Document common mistakes in anti-patterns/"
   
   If Integration < 15:
   - "Connect more MCP servers for better context"
   - "Enable Supabase MCP for database context"
   
   If Memory < 10:
   - "Run more features to build pattern library"
   - "Document project decisions in state.json"

## Scoring Guide:
- **90-100**: A - Excellent context, minimal hallucination risk
- **80-89**: B - Good context, low hallucination risk  
- **70-79**: C - Adequate context, some gaps
- **60-69**: D - Weak context, high hallucination risk
- **< 60**: F - Insufficient context, expect issues

## Usage:
```bash
/context-analysis
```

This helps ensure you have sufficient context before starting implementation, following the "sharpen the axe" principle.
