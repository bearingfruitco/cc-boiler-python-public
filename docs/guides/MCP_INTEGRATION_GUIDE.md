# MCP (Model Context Protocol) Integration Guide

## 🚀 Overview

Claude Code uses MCPs to interact with external services directly through the AI interface. This guide documents all available MCPs, their capabilities, and their limitations.

## 🎯 Core Principle

**ALWAYS use MCPs when available** - they provide direct integration without leaving Claude Code. Only fall back to CLI/terminal when MCP limitations are reached.

---

## 📊 Available MCPs and Their Capabilities

### 1. Supabase MCP
**Use for**: Database operations, auth, storage, real-time
```bash
# Available functions (check exact names in your environment):
supabase:list_organizations
supabase:list_projects
supabase:get_project
supabase:create_project
supabase:execute_sql
supabase:list_tables
supabase:apply_migration
supabase:list_edge_functions
supabase:deploy_edge_function
supabase:get_logs
supabase:search_docs
```

**Limitations**:
- Cannot run local Supabase instance
- Cannot access certain admin features
- For local development, may need `npx supabase` CLI

**Example Usage**:
```typescript
// In Claude Code - use MCP
await supabase:execute_sql({
  project_id: "your-project-id",
  query: "SELECT * FROM users LIMIT 10"
})

// NOT this (unless MCP unavailable):
// shell_command: "supabase db query 'SELECT * FROM users'"
```

### 2. Upstash Redis MCP
**Use for**: Caching, rate limiting, session storage
```bash
# Available functions:
upstash:get
upstash:set
upstash:del
upstash:incr
upstash:expire
upstash:hset
upstash:hget
```

**Limitations**:
- Complex Redis scripts may need CLI
- Bulk operations might be limited
- For Redis clusters, use CLI

### 3. GitHub MCP
**Use for**: Repository operations, issues, PRs
```bash
# Available functions:
github:create_repository
github:create_issue
github:create_pull_request
github:get_file_contents
github:create_or_update_file
github:search_repositories
github:list_issues
github:update_issue
```

**Limitations**:
- Complex Git operations need CLI
- Branch management might be limited
- For rebasing, cherry-picking, use `git` CLI

### 4. Google BigQuery MCP (via Toolbox)
**Use for**: Query execution, data reading
```bash
# Available functions:
google:bigquery_query
google:bigquery_list_tables
google:bigquery_get_schema
```

**Limitations**:
- **Cannot write data** (major limitation)
- Cannot create tables/datasets
- For write operations, use `bq` CLI:

```bash
# When you need to write data, fall back to CLI:
shell_command: "bq load --source_format=CSV dataset.table gs://bucket/file.csv"
shell_command: "bq mk -t dataset.new_table schema.json"
```

### 5. Sentry MCP
**Use for**: Error tracking, performance monitoring
```bash
# Available functions:
sentry:list_issues
sentry:get_issue
sentry:resolve_issue
sentry:create_alert
sentry:get_project_stats
```

**Limitations**:
- Cannot modify DSN configurations
- Advanced settings need Sentry CLI
- For releases, use `sentry-cli`

### 6. DBT MCP
**Use for**: Data transformation workflows
```bash
# Available functions:
dbt:run_models
dbt:test_models
dbt:list_models
dbt:compile_model
dbt:get_lineage
```

**Limitations**:
- Cannot create new models via MCP
- Profile management needs CLI
- For init/debug, use `dbt` CLI

### 7. Airbyte MCP
**Use for**: Data pipeline management
```bash
# Available functions:
airbyte:list_connections
airbyte:trigger_sync
airbyte:get_sync_status
airbyte:create_connection
```

**Limitations**:
- Connector installation needs CLI
- Complex transformations limited
- For custom connectors, use Airbyte CLI

### 8. Better Auth MCP
**Use for**: Authentication flows
```bash
# Available functions:
better_auth:create_user
better_auth:verify_email
better_auth:create_session
better_auth:revoke_session
```

**Limitations**:
- Provider setup needs config files
- OAuth flow configuration limited

### 9. Playwright MCP
**Use for**: Browser automation, E2E testing
```bash
# Available functions:
playwright:navigate
playwright:click
playwright:fill
playwright:screenshot
playwright:evaluate
```

**Limitations**:
- Complex selectors might fail
- File uploads need workarounds
- For debugging, use Playwright Inspector

### 10. Browserbase MCP
**Use for**: Cloud browser automation
```bash
# Available functions:
browserbase:create_session
browserbase:navigate
browserbase:click
browserbase:screenshot
browserbase:get_text
```

**Limitations**:
- Session limits
- Cannot access local files
- For local testing, use Playwright

### 11. Bright Data MCP
**Use for**: Web scraping, data extraction
```bash
# Available functions:
brightdata:scrape_page
brightdata:search_serp
brightdata:extract_data
```

**Limitations**:
- Rate limits apply
- Complex scraping needs proxies
- For bulk operations, use their API

### 12. Stagehand MCP
**Use for**: Advanced browser automation
```bash
# Available functions:
stagehand:act
stagehand:observe
stagehand:extract
```

**Limitations**:
- Learning curve for commands
- Limited to supported sites

---

## 🔄 MCP vs CLI Decision Matrix

| Task | Use MCP | Use CLI/Terminal |
|------|---------|------------------|
| Query Supabase data | ✅ `supabase:execute_sql` | ❌ |
| Create Supabase migration | ✅ `supabase:apply_migration` | ❌ |
| Run local Supabase | ❌ | ✅ `npx supabase start` |
| Redis get/set | ✅ `upstash:get/set` | ❌ |
| Redis complex Lua scripts | ❌ | ✅ `redis-cli` |
| Create GitHub issue | ✅ `github:create_issue` | ❌ |
| Git rebase/cherry-pick | ❌ | ✅ `git rebase` |
| Query BigQuery | ✅ `google:bigquery_query` | ❌ |
| **Load data to BigQuery** | ❌ | ✅ `bq load` |
| Create BigQuery table | ❌ | ✅ `bq mk` |
| Track Sentry error | ✅ `sentry:create_issue` | ❌ |
| Deploy Sentry release | ❌ | ✅ `sentry-cli` |
| Run dbt models | ✅ `dbt:run_models` | ❌ |
| Initialize dbt project | ❌ | ✅ `dbt init` |
| Trigger Airbyte sync | ✅ `airbyte:trigger_sync` | ❌ |
| Install Airbyte connector | ❌ | ✅ Airbyte CLI |

---

## 📝 Integration Patterns

### Pattern 1: MCP-First Approach
```typescript
// Always try MCP first
try {
  const result = await supabase:execute_sql({
    project_id: projectId,
    query: "INSERT INTO tasks (title) VALUES ($1)",
    params: [title]
  });
  return result;
} catch (error) {
  // Only fall back if MCP fails
  console.log("MCP failed, using CLI fallback");
  await shell_command(`npx supabase db execute "INSERT INTO tasks..."`);
}
```

### Pattern 2: Capability Check
```typescript
// Check if operation is possible with MCP
const canUseMCP = (operation: string) => {
  const mcpCapabilities = {
    'bigquery.read': true,
    'bigquery.write': false,  // Known limitation
    'supabase.query': true,
    'supabase.local': false,  // Needs CLI
  };
  return mcpCapabilities[operation] ?? false;
};

if (canUseMCP('bigquery.write')) {
  // Use MCP
} else {
  // Use CLI: bq load ...
}
```

### Pattern 3: Hybrid Workflow
```typescript
// Some workflows need both
async function deployWithData() {
  // 1. Create table structure via Supabase MCP
  await supabase:apply_migration({
    project_id: projectId,
    query: "CREATE TABLE analytics_data (...)"
  });

  // 2. Load data via BigQuery CLI (MCP can't write)
  await shell_command("bq load --source_format=CSV ...");

  // 3. Query results via BigQuery MCP
  const results = await google:bigquery_query({
    query: "SELECT COUNT(*) FROM dataset.analytics_data"
  });
}
```

---

## 🚨 Common Pitfalls to Avoid

### 1. Don't assume CLI when MCP exists
```typescript
// ❌ WRONG - Using CLI when MCP available
await shell_command("gh issue create --title 'Bug'");

// ✅ CORRECT - Use GitHub MCP
await github:create_issue({
  owner: "org",
  repo: "repo",
  title: "Bug"
});
```

### 2. Know MCP limitations
```typescript
// ❌ WRONG - Trying to write with BigQuery MCP
await google:bigquery_insert({ /* This doesn't exist! */ });

// ✅ CORRECT - Use bq CLI for writes
await shell_command("bq insert dataset.table data.json");
```

### 3. Handle MCP connection failures
```typescript
// Always have fallback strategy
const executeSql = async (query: string) => {
  try {
    return await supabase:execute_sql({ project_id, query });
  } catch (error) {
    if (error.message.includes('MCP not available')) {
      // Fallback to REST API
      return await fetch(`${SUPABASE_URL}/rest/v1/rpc/execute_sql`, {
        method: 'POST',
        headers: { 'apikey': SUPABASE_KEY },
        body: JSON.stringify({ query })
      });
    }
    throw error;
  }
};
```

---

## 🎯 Best Practices

1. **Always check MCP availability first**
   ```bash
   # In Claude Code, check available functions
   # They'll appear in autocomplete
   ```

2. **Document MCP limitations in PRDs**
   ```markdown
   ## Technical Requirements
   - Data queries: Use BigQuery MCP ✅
   - Data loading: Requires bq CLI (MCP limitation) ⚠️
   ```

3. **Create helper functions for common patterns**
   ```typescript
   // lib/mcp-helpers.ts
   export const queryOrFallback = async (service: string, operation: any) => {
     // Try MCP first, fallback to CLI
   };
   ```

4. **Keep CLI commands in constants**
   ```typescript
   // When CLI is needed, document why
   const BQ_LOAD_COMMAND = "bq load --source_format=CSV"; // MCP can't write
   ```

---

## 📚 Quick Reference

### Always Use MCP
- Supabase queries and migrations
- Redis cache operations
- GitHub issues and PRs
- Sentry error tracking
- DBT model runs
- Airbyte sync triggers
- All read operations

### Use CLI When
- Local development servers
- BigQuery data writes
- Complex Git operations
- Service initialization
- Debugging needs
- MCP connection fails
- Operation not supported

---

## 🔮 Future Considerations

As MCPs evolve, limitations may be removed. Always check:
1. Latest MCP documentation
2. Function availability in Claude Code
3. Community updates on new capabilities

Remember: MCPs are the preferred integration method. Only use CLI/terminal when you hit a known limitation or MCP is unavailable.
