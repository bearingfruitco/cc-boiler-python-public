---
name: roadmap-view
aliases: [roadmap, view-roadmap]
description: Visual roadmap view from task ledger data
category: planning
---

Generate visual roadmap from task ledger data.

## Roadmap Overview

Read `.task-ledger.md` and visualize as roadmap:

```
=== ROADMAP VIEW ===

Phase 1: Foundation
Status: ████████░░ 80% (8/10 tasks)
├─ ✓ User Authentication System
├─ ✓ Base Agent Framework  
├─ ✓ Database Schema
├─ ⧗ API Structure (in progress - 2/3 tasks)
└─ ○ Memory System (not started)

Phase 2: Core Features
Status: ██░░░░░░░░ 20% (2/10 tasks)  
├─ ✓ Basic CRUD Operations
├─ ⧗ Agent Communication (1/4 tasks)
├─ ○ Event Queue System
└─ ○ Pipeline Integration

Phase 3: Polish & Deploy
Status: ░░░░░░░░░░ 0% (0/8 tasks)
└─ (Waiting on Phase 2 completion)

=== METRICS ===
Overall Progress: 33% (10/30 tasks)
Time Elapsed: 3 days
Est. Completion: 6 days
Velocity: 3.3 tasks/day

=== BLOCKERS ===
⚠ API Structure: Waiting on security review
⚠ Memory System: Redis setup required

=== RECENT DECISIONS ===
• 2024-01-20: Switched to event-driven architecture
• 2024-01-18: Adopted BaseAgent pattern
```

## Integration Points

1. Pulls data from `.task-ledger.md`
2. Groups by feature/phase from PRDs
3. Shows completion percentage
4. Highlights blockers
5. Links to recent architectural decisions

## Usage

```bash
/roadmap              # Full roadmap view
/roadmap --phase=2    # Focus on specific phase
/roadmap --metrics    # Detailed metrics only
```

This complements `/tl` by providing high-level visualization.