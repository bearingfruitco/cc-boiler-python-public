# Think Through - Sequential Analysis Command

## Command: think-through
**Aliases:** `tt`, `seq`, `analyze-deep`

## Description
Uses the sequential thinking MCP for systematic, multi-step problem solving and analysis. Perfect for complex architectural decisions, debugging challenging issues, or planning system designs.

## Usage
```bash
/think-through "How should we architect the payment processing system?"
/tt "Debug why form submissions are failing intermittently"
/seq "Plan migration from REST to GraphQL"
```

## Options
- `--steps [number]` - Specify number of thinking steps (default: auto)
- `--branch` - Allow branching/exploring multiple solutions
- `--verify` - Include hypothesis verification steps

## When to Use
- **Complex Problems**: Multi-faceted issues requiring systematic analysis
- **Architecture Decisions**: System design with trade-offs
- **Root Cause Analysis**: Debugging non-obvious problems
- **Planning**: Breaking down large features into implementation steps
- **Performance Issues**: Systematic performance investigation

## Examples

### Architecture Planning
```bash
/tt "Design a real-time notification system supporting 100k concurrent users"
# Will analyze: infrastructure, scaling, protocols, fallbacks, costs
```

### Debugging Complex Issues
```bash
/think-through "Users report data loss but logs show successful saves"
# Will investigate: race conditions, caching, UI state, database transactions
```

### Feature Planning
```bash
/seq "Implement multi-tenant architecture" --steps 10
# Will break down: isolation strategies, routing, security, migration plan
```

## Integration with Personas
Works especially well with:
- `--persona-architect`: System design thinking
- `--persona-analyzer`: Root cause investigation
- `--persona-performance`: Optimization analysis

## Output Format
1. **Initial Analysis**: Problem decomposition
2. **Step-by-Step Thinking**: Each consideration explained
3. **Hypothesis Generation**: Potential solutions/causes
4. **Verification Steps**: How to validate conclusions
5. **Final Recommendation**: Evidence-based conclusion

## Notes
- Automatically adjusts depth based on problem complexity
- Can revise earlier thoughts as new insights emerge
- Includes uncertainty when present ("might be", "possibly")
- Always ends with actionable next steps
