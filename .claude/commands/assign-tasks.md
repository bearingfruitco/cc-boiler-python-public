Visualize task assignments for sub-agent orchestration: $ARGUMENTS

Steps:

1. Read task list from: docs/project/features/$ARGUMENTS-tasks.md

2. Analyze tasks and suggest agent assignments:

```
=== TASK ASSIGNMENT PLAN ===
Feature: $ARGUMENTS
Total Tasks: [count]
Suggested Agents: [number]

AGENT ASSIGNMENTS:
┌─────────────────────────────────────────────────────┐
│ FRONTEND_AGENT (5 tasks)                            │
├─────────────────────────────────────────────────────┤
│ 2.1 [ ] Create login form component                 │
│ 2.2 [ ] Create register form component              │
│ 2.3 [ ] Add form validation                         │
│ 3.1 [ ] Create dashboard layout                     │
│ 3.2 [ ] Add loading states                          │
└─────────────────────────────────────────────────────┘
     ↓ Provides: UI Components
     ↓ Depends on: API Routes (1.3, 1.4)

┌─────────────────────────────────────────────────────┐
│ BACKEND_AGENT (4 tasks)                             │
├─────────────────────────────────────────────────────┤
│ 1.1 [✓] Create user database schema                │
│ 1.2 [ ] Set up auth API routes                     │
│ 1.3 [ ] Implement JWT tokens                       │
│ 1.4 [ ] Add rate limiting                          │
└─────────────────────────────────────────────────────┘
     ↓ Provides: API Endpoints, Auth Logic
     ↓ Depends on: None (starts first)

┌─────────────────────────────────────────────────────┐
│ INTEGRATION_AGENT (3 tasks)                         │
├─────────────────────────────────────────────────────┤
│ 4.1 [ ] Connect forms to API                       │
│ 4.2 [ ] Add error handling                         │
│ 4.3 [ ] Test full auth flow                        │
└─────────────────────────────────────────────────────┘
     ↓ Provides: Working Feature
     ↓ Depends on: Frontend + Backend

DEPENDENCY GRAPH:
Backend ──┬──→ Frontend ──┬──→ Integration
  1.1 ────┘      2.1 ─────┘       4.1
  1.2            2.2              4.2
  1.3            2.3              4.3
  1.4            3.1
                 3.2

TIMELINE:
Hour 1: Backend starts (1.1, 1.2)
Hour 2: Backend (1.3) + Frontend starts (2.1)
Hour 3: Backend (1.4) + Frontend (2.2, 2.3)
Hour 4: Frontend (3.1, 3.2) + Integration starts
Hour 5: Integration completes + Testing
```

3. Generate orchestration configuration:

```json
// .claude/orchestration/config.json
{
  "feature": "$ARGUMENTS",
  "strategy": "parallel",
  "agents": {
    "backend": {
      "type": "specialized",
      "focus": "API, Database, Server Logic",
      "tasks": ["1.1", "1.2", "1.3", "1.4"],
      "file_ownership": [
        "app/api/**/*",
        "lib/db/**/*",
        "lib/server/**/*"
      ]
    },
    "frontend": {
      "type": "specialized",
      "focus": "UI Components, User Experience",
      "tasks": ["2.1", "2.2", "2.3", "3.1", "3.2"],
      "file_ownership": [
        "components/**/*",
        "app/(routes)/**/*",
        "styles/**/*"
      ],
      "dependencies": {
        "wait_for": ["1.3", "1.4"],
        "reason": "Needs API endpoints defined"
      }
    },
    "integration": {
      "type": "specialized",
      "focus": "Connecting Systems, Testing",
      "tasks": ["4.1", "4.2", "4.3"],
      "file_ownership": [
        "lib/client/**/*",
        "tests/**/*"
      ],
      "dependencies": {
        "wait_for": ["2.3", "3.1"],
        "reason": "Needs both UI and API ready"
      }
    }
  },
  "handoffs": {
    "1.3": {
      "from": "backend",
      "to": "frontend",
      "artifacts": {
        "auth_endpoints": "/api/auth/*",
        "token_format": "JWT in Authorization header"
      }
    },
    "2.3": {
      "from": "frontend",
      "to": "integration",
      "artifacts": {
        "form_components": "components/auth/*",
        "validation_schemas": "lib/validations/auth.ts"
      }
    }
  }
}
```

4. Show efficiency gains:

```
EFFICIENCY COMPARISON:
─────────────────────────────────────
Sequential (1 agent):  ~5 hours
Parallel (3 agents):   ~2 hours
Speedup:              2.5x
─────────────────────────────────────

BENEFITS:
✓ No context switching between frontend/backend
✓ Parallel development of independent tasks
✓ Clear ownership prevents conflicts
✓ Natural documentation from handoffs
✓ Each agent maintains deep context
```

5. Suggest optimization:

Based on task analysis, recommend:
- Number of agents (2-5)
- Task groupings
- Dependency order
- Potential bottlenecks
- Critical path highlights

6. Interactive options:

```
Would you like to:
1. Start orchestration with this plan → /orchestrate $ARGUMENTS
2. Modify assignments manually → /edit-assignments
3. View different strategy → /assign-tasks $ARGUMENTS --strategy=sequential
4. Cancel → /cancel
```

Save visualization to: .claude/orchestration/plans/$ARGUMENTS-assignment.md
