# Completion Verification System - Migration Plan

## Overview
This migration plan introduces the Completion Verification System gradually to avoid disrupting existing workflows while improving reliability.

## Phase 1: Detection & Warning (Week 1) ✅ CURRENT
**Status: Implemented**

### What's Active:
- Completion detection in hook 14
- Warning messages when verification fails
- Verification manifest tracking
- `/verify` command available

### Configuration:
```json
{
  "verification": {
    "enabled": true,
    "strict_mode": false,      // Just warnings
    "block_on_failure": false   // Don't block yet
  }
}
```

### User Experience:
- See warnings when claiming completion without verification
- Can still proceed with workflow
- Start learning verification patterns

## Phase 2: Soft Enforcement (Week 2-3)

### Changes:
- Enable `strict_mode` but keep `block_on_failure` false
- Add verification status to PR templates
- Track verification metrics

### Configuration Update:
```json
{
  "verification": {
    "enabled": true,
    "strict_mode": true,        // Stronger warnings
    "block_on_failure": false    // Still don't block
  }
}
```

### Metrics to Track:
- How often verification passes/fails
- Common failure patterns
- Time added to workflow

## Phase 3: Full Enforcement (Week 4+)

### Changes:
- Enable `block_on_failure` for production features
- Require verification for `/fw complete`
- Integration tests become required

### Configuration Update:
```json
{
  "verification": {
    "enabled": true,
    "strict_mode": true,
    "block_on_failure": true,    // Now blocking
    "require_integration_tests": true
  }
}
```

### Exemptions:
- Micro-tasks (`/mt`) skip verification
- Documentation changes skip
- Test-only changes skip

## Rollout Communication

### Week 1 Message:
```
🎉 New Feature: Completion Verification

We're introducing verification to ensure "done" actually means done!

Currently in WARNING mode:
- You'll see verification warnings when claiming completion
- No workflow changes required yet
- Try `/verify` to see how it works

This will help catch issues before they reach production!
```

### Week 2 Message:
```
📈 Verification Update

Based on Week 1 data:
- X% of "complete" claims had failing tests
- Y% had missing dependencies

Moving to SOFT ENFORCEMENT:
- Stronger warnings for verification failures
- PR templates now show verification status
- Still not blocking - just more visible

Use `/verify` before marking tasks complete!
```

### Week 4 Message:
```
✅ Full Verification Enforcement

Starting today:
- Verification required for feature completion
- `/fw complete` blocked if verification fails
- Integration tests now required

Benefits we've seen:
- Z% reduction in post-merge failures
- Faster PR reviews
- Higher confidence in deployments

Questions? See docs/verification/README.md
```

## Quick Enable/Disable

### To Enable Strict Mode Now:
```bash
# Edit .claude/hooks/config.json
{
  "verification": {
    "strict_mode": true,
    "block_on_failure": true
  }
}
```

### To Disable Temporarily:
```bash
# For emergency bypass
{
  "verification": {
    "enabled": false
  }
}
```

### Per-Feature Control:
```bash
# In task files, add:
<!-- verification: skip -->
# or
<!-- verification: comprehensive -->
```

## Success Metrics

### Week 1:
- [ ] Detection working (0 false positives)
- [ ] Warnings shown appropriately
- [ ] `/verify` command used X times

### Week 2-3:
- [ ] 50% of completions run verification
- [ ] Average verification time < 30s
- [ ] No workflow disruption reports

### Week 4+:
- [ ] 90%+ features verified before merge
- [ ] 50% reduction in "it worked on my machine"
- [ ] Team confidence in "done" increased

## Troubleshooting

### Common Issues:

1. **"Verification takes too long"**
   - Use `--level quick` for fast checks
   - Skip integration tests initially
   - Run async in background

2. **"Too many false positives"**
   - Tune completion phrases
   - Add context detection
   - Allow task-specific overrides

3. **"Breaks my workflow"**
   - Start with warnings only
   - Add to specific commands gradually
   - Provide easy bypass options

## Next Steps

1. Monitor Week 1 adoption
2. Gather feedback on friction points
3. Tune detection patterns
4. Add verification dashboard
5. Integrate with CI/CD

This gradual rollout ensures teams adopt verification without disruption while building confidence in the system.
