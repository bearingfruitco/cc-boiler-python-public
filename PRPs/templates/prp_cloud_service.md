# PRP: [CLOUD SERVICE NAME]

## Metadata
- **Created**: [DATE]
- **Author**: [AUTHOR]
- **Confidence**: [1-10]
- **Complexity**: [Low/Medium/High]
- **Type**: Cloud Service
- **Platform**: Google Cloud Run

## Goal
[Clear description of the cloud service to be deployed]

## Why
- **Business Value**: [Impact on system/users]
- **Technical Need**: [Problems this solves]
- **Priority**: [Critical/High/Medium/Low]

## What
[Service behavior and technical requirements]

### Success Criteria
- [ ] Service deployed and accessible via HTTPS
- [ ] All webhooks/endpoints functional
- [ ] BigQuery integration working
- [ ] Supabase connection established
- [ ] Structured logging implemented
- [ ] Error monitoring active
- [ ] Autoscaling configured
- [ ] CI/CD pipeline functional

## Cloud Infrastructure Context

### Required Documentation
```yaml
- docfile: PRPs/ai_docs/cloud_infrastructure/cloud_run_deployment.md
  why: Core deployment patterns and best practices
  sections: ["Service Configuration", "IAM & Permissions", "Logging"]

- docfile: PRPs/ai_docs/cloud_infrastructure/cloud_run_service_template.json
  why: Base service configuration template
  critical: Modify for specific service needs

- docfile: PRPs/ai_docs/cloud_infrastructure/cloud_run_instructions.json
  why: Step-by-step deployment instructions
  use: Follow tasks in order

# If using BigQuery
- url: https://cloud.google.com/bigquery/docs/python-client-migration
  why: Latest BigQuery Python client patterns
  sections: ["Streaming inserts", "Query jobs"]

# If using Supabase
- url: https://supabase.com/docs/guides/database/connecting-to-postgres
  why: Postgres connection best practices
  critical: Connection pooling section
```

### Service Configuration
```json
{
  "apiVersion": "serving.knative.dev/v1",
  "kind": "Service",
  "metadata": {
    "name": "[SERVICE_NAME]",
    "annotations": {
      "run.googleapis.com/ingress": "all"
    }
  },
  "spec": {
    "template": {
      "spec": {
        "serviceAccountName": "[SERVICE_NAME]-sa@[PROJECT_ID].iam.gserviceaccount.com",
        "containerConcurrency": 80,
        "timeoutSeconds": 60,
        "containers": [{
          "image": "gcr.io/[PROJECT_ID]/[SERVICE_NAME]:latest",
          "env": [
            { "name": "BIGQUERY_DATASET", "value": "[DATASET_NAME]" },
            { "name": "ENVIRONMENT", "value": "production" }
          ],
          "resources": {
            "limits": { "cpu": "1", "memory": "512Mi" }
          }
        }]
      }
    }
  }
}
```

### IAM Requirements
```yaml
Service Account: [SERVICE_NAME]-sa@[PROJECT_ID].iam.gserviceaccount.com
Required Roles:
  - roles/bigquery.dataEditor (on dataset: [DATASET_NAME])
  - roles/bigquery.user (project level)
  - roles/secretmanager.secretAccessor (on secrets: supabase-*)
  - roles/logging.logWriter (automatic)
  
For CI/CD Service Account: github-actions@[PROJECT_ID].iam.gserviceaccount.com
  - roles/run.admin
  - roles/iam.serviceAccountUser
  - roles/artifactregistry.writer
```

### Known Gotchas & Critical Patterns
```python
# CRITICAL: Cloud Run PORT handling
import os
port = int(os.environ.get('PORT', 8080))
app.run(host='0.0.0.0', port=port)  # Must bind to 0.0.0.0

# GOTCHA: BigQuery streaming has costs
# For high volume, batch inserts instead:
rows = []
for item in items:
    rows.append({"field": value})
    if len(rows) >= 500:  # Batch size
        errors = client.insert_rows_json(table, rows)
        rows = []

# PATTERN: Structured logging for Cloud Logging
import json
def log_event(severity, message, **kwargs):
    entry = {
        "severity": severity,
        "message": message,
        **kwargs
    }
    print(json.dumps(entry))

# WARNING: Supabase connection pooling
# Cloud Run can scale to many instances, overwhelming DB
from sqlalchemy.pool import NullPool  # No pooling per-instance
engine = create_engine(url, poolclass=NullPool)
```

## Implementation Blueprint

### Task Breakdown
```yaml
Task 1 - Prepare Service:
  CREATE Dockerfile:
    - Base image: python:3.11-slim
    - Install dependencies
    - Configure PORT usage
    
  CREATE src/main.py:
    - Flask/FastAPI app setup
    - Health check endpoint
    - Webhook endpoints
    
  CREATE requirements.txt:
    - google-cloud-bigquery>=3.0
    - psycopg2-binary
    - flask/fastapi
    - gunicorn

Task 2 - Cloud Resources:
  CREATE service account:
    gcloud iam service-accounts create [SERVICE_NAME]-sa
    
  ASSIGN IAM roles:
    - BigQuery permissions
    - Secret Manager access
    
  CREATE secrets:
    - SUPABASE_URL
    - SUPABASE_KEY

Task 3 - Deployment:
  BUILD container:
    docker build -t gcr.io/[PROJECT]/[SERVICE]:v1 .
    docker push gcr.io/[PROJECT]/[SERVICE]:v1
    
  DEPLOY service:
    gcloud run deploy [SERVICE_NAME] \
      --image=gcr.io/[PROJECT]/[SERVICE]:v1 \
      --service-account=[SERVICE_NAME]-sa@[PROJECT].iam.gserviceaccount.com

Task 4 - CI/CD:
  CREATE .github/workflows/deploy.yml:
    - Workload Identity Federation
    - Build and push image
    - Deploy to Cloud Run
    
  CONFIGURE GitHub secrets:
    - WIF_PROVIDER
    - WIF_SERVICE_ACCOUNT

Task 5 - Monitoring:
  CONFIGURE alerts:
    - Error rate > 1%
    - Response time > 2s
    - Instance count > 50
    
  CREATE dashboards:
    - Request metrics
    - Error logs
    - BigQuery usage
```

### Webhook Endpoints
```python
@app.route('/webhook/leadprosper', methods=['POST'])
def leadprosper_webhook():
    """Handle LeadProsper webhook events."""
    try:
        # Verify signature if provided
        signature = request.headers.get('X-Signature')
        if not verify_signature(request.data, signature):
            return jsonify({'error': 'Invalid signature'}), 401
        
        # Process payload
        data = request.get_json()
        log_event("INFO", "LeadProsper webhook received", 
                 lead_id=data.get('lead_id'))
        
        # Insert to BigQuery
        table = bigquery_client.dataset(DATASET).table('leads')
        errors = bigquery_client.insert_rows_json(table, [data])
        
        if errors:
            log_event("ERROR", "BigQuery insert failed", errors=errors)
            return jsonify({'error': 'Storage failed'}), 500
            
        return jsonify({'status': 'ok'}), 200
        
    except Exception as e:
        log_event("ERROR", "Webhook processing failed", error=str(e))
        return jsonify({'error': 'Internal error'}), 500
```

## Validation Loops

### Level 1: Local Testing
```bash
# Build and run locally
docker build -t test-service .
docker run -p 8080:8080 -e PORT=8080 test-service

# Test endpoints
curl http://localhost:8080/health
curl -X POST http://localhost:8080/webhook/test -d '{"test": "data"}'
```

### Level 2: Cloud Run Staging
```bash
# Deploy to staging
gcloud run deploy [SERVICE]-staging --tag=staging

# Test staging endpoints
STAGING_URL=$(gcloud run services describe [SERVICE]-staging --format='value(status.url)')
curl $STAGING_URL/health
```

### Level 3: Integration Tests
```python
# tests/test_integration.py
def test_bigquery_connection():
    """Verify BigQuery connectivity."""
    client = bigquery.Client()
    query = "SELECT 1 as test"
    result = list(client.query(query))
    assert result[0].test == 1

def test_supabase_connection():
    """Verify Supabase connectivity."""
    conn = psycopg2.connect(os.environ['SUPABASE_URL'])
    cur = conn.cursor()
    cur.execute("SELECT 1")
    assert cur.fetchone()[0] == 1
    conn.close()

def test_webhook_processing():
    """Test webhook with real services."""
    response = requests.post(
        f"{STAGING_URL}/webhook/test",
        json={"test_id": "123", "value": 100}
    )
    assert response.status_code == 200
    
    # Verify in BigQuery
    query = f"SELECT * FROM `{DATASET}.test_events` WHERE test_id = '123'"
    results = list(bigquery_client.query(query))
    assert len(results) == 1
```

### Level 4: Production Validation
```bash
# Smoke tests after deployment
./scripts/smoke_test_production.sh

# Monitor for 15 minutes
gcloud logging read "resource.type=cloud_run_revision AND severity>=ERROR" \
  --format=json --freshness=15m

# Check metrics
gcloud monitoring time-series list \
  --filter='metric.type="run.googleapis.com/request_count"'
```

## Deployment Checklist
- [ ] Dockerfile tested locally
- [ ] Service account created with correct permissions
- [ ] Secrets stored in Secret Manager
- [ ] BigQuery dataset exists and accessible
- [ ] Supabase connection string valid
- [ ] GitHub Actions workflow committed
- [ ] Staging deployment successful
- [ ] Integration tests passing
- [ ] Monitoring alerts configured
- [ ] Documentation updated

## Anti-Patterns to Avoid
- ❌ Don't hardcode credentials - use Secret Manager
- ❌ Don't use synchronous BigQuery loads for real-time data
- ❌ Don't create new DB connections per request
- ❌ Don't ignore structured logging format
- ❌ Don't set CPU always-on unless needed
- ❌ Don't skip health check endpoint
- ❌ Don't deploy without CI/CD pipeline

## Rollback Plan
```bash
# List all revisions
gcloud run revisions list --service=[SERVICE_NAME]

# Route traffic to previous revision
gcloud run services update-traffic [SERVICE_NAME] \
  --to-revisions=[PREVIOUS_REVISION]=100

# Or use tagged revision
gcloud run services update-traffic [SERVICE_NAME] \
  --to-tags=stable=100
```

## Performance Optimization
- Use connection pooling for Supabase
- Batch BigQuery inserts when possible
- Enable Cloud CDN for static assets
- Set appropriate concurrency limits
- Use async handlers for I/O operations
- Implement caching where appropriate

## Security Considerations
- All endpoints use HTTPS (Cloud Run default)
- Webhook signatures verified
- Secrets never logged
- Service account has minimal permissions
- VPC connector for fixed egress IP (if needed)
- Regular security scans on container images

## Confidence Score: [X]/10

### Scoring Rationale:
- Documentation completeness: [X]/2
- Pattern examples: [X]/2
- Cloud gotchas identified: [X]/2
- Test coverage: [X]/2
- Automation readiness: [X]/2