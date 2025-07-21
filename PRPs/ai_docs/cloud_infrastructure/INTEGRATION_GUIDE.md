# Cloud Infrastructure Integration Guide

## What We've Added

### 1. Documentation Cache (`/PRPs/ai_docs/cloud_infrastructure/`)
- **cloud_run_deployment.md** - Comprehensive Cloud Run deployment guide
- **cloud_run_service_template.json** - Ready-to-use service configuration
- **cloud_run_instructions.json** - Machine-readable deployment instructions

### 2. New Commands
- **`/cloud-deploy`** (`/gcp-deploy`, `/deploy-service`) - Deploy to Cloud Run
- **`/chain cs`** - Complete cloud service workflow

### 3. Cloud Configuration Validator Hook
- **`18-cloud-config-validator.py`** - Pre-deployment validation
- Checks Dockerfiles for Cloud Run compatibility
- Validates service configurations
- Warns about hardcoded secrets
- Ensures proper IAM documentation

### 4. Enhanced Response Capture
- Updated to detect cloud-related AI responses
- Captures deployment plans, infrastructure designs
- Recognizes Docker, Kubernetes, BigQuery, Supabase patterns

### 5. PRP Template for Cloud Services
- **`prp_cloud_service.md`** - Specialized template for cloud deployments
- Includes all necessary context for one-pass success
- Pre-filled with common cloud patterns and gotchas

## How to Use

### Quick Cloud Service Deployment
```bash
# Method 1: Use the workflow chain
/chain cs

# Method 2: Step by step
/py-prd "Lead Tracking Service" --cloud
/cloud-deploy --check
/py-api /webhook/leadprosper POST
/cloud-deploy
```

### Create a Cloud Service PRP
```bash
/prp-create "Cloud Run Lead API" --type=cloud

# This will:
# 1. Use the cloud service template
# 2. Reference all cloud documentation
# 3. Include deployment instructions
# 4. Add validation loops
```

### Multi-Agent Cloud Deployment
```bash
/orch "Deploy lead tracking to Cloud Run with BigQuery"

# Spawns specialized agents:
# - Infrastructure: GCP setup
# - Security: IAM configuration  
# - Integration: BigQuery/Supabase
# - Monitoring: Logging setup
```

## Best Practices

1. **Always use PRPs for cloud services** - They include critical context
2. **Run `/cloud-deploy --check`** before actual deployment
3. **Use Secret Manager** - Hook will warn about hardcoded secrets
4. **Follow structured logging** - Required for Cloud Logging
5. **Test locally first** - Use Docker to verify container works

## Common Patterns

### BigQuery Integration
```python
from google.cloud import bigquery
client = bigquery.Client()  # Uses ADC

# Batch inserts for efficiency
rows = []
for item in items:
    rows.append({"field": value})
    if len(rows) >= 500:
        errors = client.insert_rows_json(table, rows)
        rows = []
```

### Structured Logging
```python
import json

def log_event(severity, message, **kwargs):
    entry = {
        "severity": severity,
        "message": message,
        **kwargs
    }
    print(json.dumps(entry))
```

### Webhook Handler
```python
@app.route('/webhook/source', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        log_event("INFO", "Webhook received", source="source")
        # Process...
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        log_event("ERROR", "Failed", error=str(e))
        return jsonify({'error': 'Internal error'}), 500
```

## Next Steps

1. **Add your BigQuery/Cloud Functions research** to `/PRPs/ai_docs/cloud_infrastructure/`
2. **Test the workflow** with a sample service
3. **Customize templates** for your specific needs
4. **Set up GitHub Actions** for CI/CD

The system is now ready for cloud-native Python development!