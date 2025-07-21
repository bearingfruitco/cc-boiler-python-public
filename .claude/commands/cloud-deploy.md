---
name: cloud-deploy
aliases: [gcp-deploy, deploy-service, cloud-run-deploy]
description: Deploy Python service to Cloud Run with BigQuery integration
category: Infrastructure
---

# Deploy to Cloud Run: $ARGUMENTS

Deploy a Python service to Google Cloud Run with proper configuration and integrations.

## Pre-deployment Checklist

- [ ] GCP project configured
- [ ] Service account created with proper IAM roles
- [ ] BigQuery dataset exists (if needed)
- [ ] Supabase credentials in Secret Manager (if used)
- [ ] Dockerfile prepared or using buildpacks
- [ ] GitHub Actions workflow configured (if using CI/CD)

## Load Configuration

Loading Cloud Run template from: PRPs/ai_docs/cloud_infrastructure/cloud_run_service_template.json

## Required IAM Roles

For the service account `$SERVICE_ACCOUNT`:
- roles/bigquery.dataEditor (on dataset)
- roles/bigquery.user (project level)
- roles/secretmanager.secretAccessor (if using secrets)
- roles/logging.logWriter (automatic)

## Deployment Steps

### 1. Build Container (if not using source deploy)
```bash
docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME:$TAG .
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:$TAG
```

### 2. Deploy Service
```bash
gcloud run deploy $SERVICE_NAME \
  --image=gcr.io/$PROJECT_ID/$SERVICE_NAME:$TAG \
  --region=$REGION \
  --platform=managed \
  --allow-unauthenticated \
  --service-account=$SERVICE_ACCOUNT \
  --set-env-vars=BIGQUERY_DATASET=$DATASET,ENV=$ENVIRONMENT \
  --cpu=1 --memory=512Mi \
  --min-instances=0 --max-instances=10 \
  --concurrency=80 \
  --timeout=60
```

### 3. Configure Webhooks (if needed)
- Endpoint will be: https://$SERVICE_NAME-$PROJECT_ID-$REGION.run.app
- Add webhook endpoints as documented in code

### 4. Set up Monitoring
```bash
# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE_NAME" --limit=50

# Set up error alerting (optional)
gcloud alpha monitoring policies create --notification-channels=$CHANNEL_ID --display-name="$SERVICE_NAME errors" --condition-display-name="Error rate" --condition="..." 
```

## Post-deployment Verification

1. Test endpoint: `curl https://$SERVICE_NAME-$PROJECT_ID-$REGION.run.app/health`
2. Check logs for startup messages
3. Verify BigQuery connectivity
4. Test webhook endpoints

## GitHub Actions Integration

If using CI/CD, ensure .github/workflows/deploy.yml includes:
- Workload identity federation setup
- Build and push steps
- Deploy to Cloud Run action

Reference: PRPs/ai_docs/cloud_infrastructure/cloud_run_instructions.json

## Common Issues

- **Permission Denied**: Check service account IAM roles
- **Cold Starts**: Consider min-instances > 0
- **Database Connections**: Implement connection pooling
- **Timeouts**: Adjust timeout setting and check external API calls