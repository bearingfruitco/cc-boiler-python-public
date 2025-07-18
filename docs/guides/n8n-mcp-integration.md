# n8n MCP Integration Guide

## Overview
n8n MCP enables workflow automation and orchestration directly from Claude Code. Use this when you need complex multi-service integrations or background job processing.

## When to Use

### ✅ Good Use Cases
- Complex notification workflows (email → Slack → SMS)
- ETL pipelines with multiple data sources
- Scheduled automation tasks
- Multi-step approval processes
- Integration with services not available as MCPs

### ❌ When NOT to Use
- Simple API calls (use direct MCPs)
- Basic CRUD operations (use Supabase)
- One-off scripts (write directly)
- Real-time processing (use Edge Functions)

## Available Functions

```typescript
// Workflow Management
n8n:list_workflows()
n8n:get_workflow(id: string)
n8n:create_workflow(workflow: WorkflowDefinition)
n8n:update_workflow(id: string, updates: Partial<WorkflowDefinition>)
n8n:delete_workflow(id: string)

// Execution
n8n:execute_workflow(id: string, data?: any)
n8n:get_executions(workflowId?: string)
n8n:get_execution(id: string)

// Monitoring
n8n:get_workflow_stats(id: string)
n8n:get_failed_executions()
```

## Integration Patterns

### 1. Deployment Notifications
```typescript
// After successful deployment
await n8n:execute_workflow({
  workflow_id: "deployment-notification",
  data: {
    version: "1.2.3",
    environment: "production",
    deployer: user.email,
    changes: commitMessages
  }
})
```

### 2. Data Processing Pipeline
```typescript
// Process uploaded CSV through n8n
const { execution_id } = await n8n:execute_workflow({
  workflow_id: "csv-processing",
  data: {
    file_url: uploadedFileUrl,
    user_id: user.id,
    processing_options: {
      deduplicate: true,
      validate_emails: true
    }
  }
})

// Poll for completion
const result = await waitForExecution(execution_id)
```

### 3. Scheduled Reports
```typescript
// Create workflow for weekly reports
await n8n:create_workflow({
  name: "weekly-analytics-report",
  nodes: [
    {
      type: "n8n-nodes-base.cron",
      parameters: {
        triggerTimes: {
          item: [{
            mode: "everyWeek",
            hour: 9,
            minute: 0,
            weekday: 1 // Monday
          }]
        }
      }
    },
    {
      type: "n8n-nodes-base.supabase",
      parameters: {
        operation: "getAll",
        table: "analytics_events",
        filters: {
          created_at: "gte.{{$fromDate}}"
        }
      }
    },
    // ... more nodes
  ]
})
```

### 4. Error Recovery Workflow
```typescript
// Trigger error recovery workflow
try {
  await riskyOperation()
} catch (error) {
  await n8n:execute_workflow({
    workflow_id: "error-recovery",
    data: {
      error_type: error.name,
      error_message: error.message,
      context: {
        user_id: user.id,
        operation: "riskyOperation",
        timestamp: new Date().toISOString()
      }
    }
  })
}
```

## Best Practices

1. **Keep Workflows Simple** - Complex logic belongs in code
2. **Use for Integration** - n8n excels at connecting services
3. **Handle Failures** - Always check execution status
4. **Version Control** - Export workflows to JSON and commit
5. **Monitor Performance** - Track execution times
6. **Test Workflows** - Have test versions of critical workflows

## Common Patterns

### Polling for Completion
```typescript
async function waitForExecution(executionId: string, maxWait = 60000) {
  const start = Date.now()
  
  while (Date.now() - start < maxWait) {
    const execution = await n8n:get_execution(executionId)
    
    if (execution.finished) {
      if (execution.data.resultData.error) {
        throw new Error(execution.data.resultData.error.message)
      }
      return execution.data.resultData.runData
    }
    
    await new Promise(resolve => setTimeout(resolve, 1000))
  }
  
  throw new Error('Workflow execution timeout')
}
```

### Error Handling
```typescript
try {
  const result = await n8n:execute_workflow({
    workflow_id: "data-import",
    data: { source: "csv" }
  })
  
  if (!result.success) {
    // Handle workflow-level errors
    console.error('Workflow failed:', result.error)
  }
} catch (error) {
  // Handle MCP-level errors
  if (error.message.includes('Workflow not found')) {
    // Create workflow first
  }
}
```

## Limitations

1. **No Visual Builder** - Can't see/edit workflows visually through MCP
2. **Async Execution** - Most workflows run async, need polling
3. **Rate Limits** - Respect n8n instance limits
4. **No Debugging** - Can't step through workflow execution
5. **Limited Node Types** - Some nodes may not work via API

## Alternatives to Consider

Before using n8n, consider if these are sufficient:

| Need | Alternative |
|------|------------|
| Background jobs | Supabase Edge Functions |
| Scheduled tasks | GitHub Actions |
| Simple integrations | Direct API calls |
| Queue processing | BullMQ or similar |
| ETL | Airbyte MCP |

## Remember

n8n MCP is powerful but adds complexity. Only use when:
- You need multi-service orchestration
- Workflows change frequently
- Non-developers need to modify flows
- Built-in integrations save significant time
