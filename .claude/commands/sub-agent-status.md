Check the status of sub-agent orchestration

Show current orchestration status including:
- Active agents and their progress
- Current tasks being worked on
- Completed tasks
- Pending handoffs
- Time estimates

Read from: .claude/orchestration/state.json and progress files

Display format:

```
=== SUB-AGENT ORCHESTRATION STATUS ===
Feature: user-authentication
Started: 2024-01-15 10:00 AM
Elapsed: 1h 23m

AGENT STATUS:
┌────────────────┬──────────┬───────────────────────┬──────────┐
│ Agent          │ Progress │ Current Task          │ Status   │
├────────────────┼──────────┼───────────────────────┼──────────┤
│ BACKEND_AGENT  │ ███░░ 60%│ 1.3 JWT tokens        │ Active   │
│ FRONTEND_AGENT │ █░░░░ 20%│ Waiting for API       │ Blocked  │
│ SECURITY_AGENT │ ░░░░░  0%│ Not started           │ Pending  │
└────────────────┴──────────┴───────────────────────┴──────────┘

COMPLETED TASKS:
✓ 1.1 Create user database schema (backend)
✓ 1.2 Set up auth API routes (backend)

IN PROGRESS:
⚡ 1.3 Implement JWT tokens (backend) - 45% complete

BLOCKED:
⏸ 2.1 Create login form (frontend) - Waiting for: API endpoints

HANDOFF QUEUE:
1. [PENDING] Backend → Frontend: Auth endpoint specs
2. [PENDING] Frontend → Security: Component audit

MESSAGES (Last 3):
• [11:15] BACKEND: Database schema created successfully
• [11:45] BACKEND: Auth routes /api/auth/login and /api/auth/register ready
• [12:23] SYSTEM: Frontend agent waiting for task 1.3 completion

TIMELINE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         ▼ (You are here)
[====|====|====|····|····] 60% Complete
10am  11am  12pm  1pm   2pm

Estimated completion: 2:00 PM (40 minutes remaining)

OPTIONS:
- View detailed agent log: /agent-log [agent-name]
- Send message to agent: /agent-message [agent] [message]
- Modify assignments: /reassign-task [task-id] [new-agent]
- Pause orchestration: /orch pause
```

If no orchestration is active, show:
```
No active orchestration.

Recent orchestrations:
- user-authentication (Completed 2h ago) → /orch-history 1
- payment-integration (Completed yesterday) → /orch-history 2

Start new orchestration: /orch [feature-name]
```
