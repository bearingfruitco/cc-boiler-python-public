---
name: check-logs
aliases: [logs, view-logs]
description: Check application and service logs
category: debugging
---

Check various application and service logs for debugging.

## Arguments:
- $SERVICE: api|agent|pipeline|all (default: all)
- $LINES: number of lines (default: 50)
- $FOLLOW: -f to follow logs (optional)

## Log Sources:

### API Logs
```bash
# FastAPI application logs
tail -n $LINES logs/api.log
# Or if using pm2/systemd
pm2 logs api --lines $LINES
```

### Agent Logs
```bash
# AI agent execution logs
tail -n $LINES logs/agents.log
# Agent memory/state logs
tail -n $LINES logs/agent-memory.log
```

### Pipeline Logs
```bash
# Prefect pipeline logs
tail -n $LINES logs/pipelines.log
# Or from Prefect UI
prefect logs --limit $LINES
```

### System Logs
```bash
# Python application logs
tail -n $LINES logs/app.log
# Error logs
tail -n $LINES logs/error.log
```

## Cloud Logs (if deployed):

### Google Cloud
```bash
gcloud logging read "resource.type=gae_app" --limit=$LINES
```

### AWS CloudWatch
```bash
aws logs tail /aws/lambda/function-name --since 1h
```

### Supabase
```bash
# Check Supabase dashboard or use API
```

## Output Format:
```
=== API Logs (last 50 lines) ===
2024-01-15 10:23:45 INFO: Request POST /api/agent/query
2024-01-15 10:23:46 INFO: Agent response in 1.2s
2024-01-15 10:23:47 ERROR: ValidationError in request body

=== Agent Logs ===
2024-01-15 10:23:45 INFO: DataAnalystAgent processing query
2024-01-15 10:23:45 DEBUG: Using tools: pandas, duckdb
2024-01-15 10:23:46 INFO: Query complete, 5 rows returned

=== Error Summary ===
- 3 validation errors in last hour
- 0 agent failures
- 1 pipeline timeout
```

## Filtering Options:
- `--error` - Show only errors
- `--level INFO|WARN|ERROR` - Filter by level
- `--service api|agent|pipeline` - Single service
- `--since 1h|1d|1w` - Time range
