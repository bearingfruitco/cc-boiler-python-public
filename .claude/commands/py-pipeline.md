---
name: py-pipeline
aliases: [pyp, pipeline-create]
description: Create a data pipeline with Prefect orchestration
category: python
---

Create a data pipeline with:
- Prefect flow orchestration
- Error handling and retries
- Parallel task execution
- Monitoring and logging
- BigQuery/Cloud Storage integration

## Usage
```bash
/py-pipeline <PipelineName> [options]
```

## Options
- `--source`: Data source type (bigquery, gcs, api, file)
- `--destination`: Where to load data (bigquery, gcs, postgres)
- `--schedule`: Cron schedule (e.g., "0 9 * * *")
- `--parallel`: Enable parallel processing
- `--agents`: AI agents to use in pipeline

## Examples
```bash
# ETL pipeline from BigQuery to BigQuery
/py-pipeline DailyETL --source=bigquery --destination=bigquery --schedule="0 9 * * *"

# API ingestion pipeline
/py-pipeline APIIngestion --source=api --destination=postgres --parallel

# File processing pipeline with AI
/py-pipeline FileProcessor --source=file --agents=data_analyst
```

## What Gets Created

1. **Pipeline Module** (`src/pipelines/{name}.py`):
   ```python
   from prefect import flow, task
   from prefect.tasks import task_input_hash
   from datetime import timedelta
   
   @task(
       retries=3,
       retry_delay_seconds=60,
       cache_key_fn=task_input_hash,
       cache_expiration=timedelta(hours=1)
   )
   def extract_data(source_config: dict) -> pd.DataFrame:
       """Extract data with caching and retries"""
       pass
   
   @task
   def transform_data(df: pd.DataFrame) -> pd.DataFrame:
       """Transform with validation"""
       pass
   
   @task
   def load_data(df: pd.DataFrame, destination_config: dict) -> None:
       """Load to destination"""
       pass
   
   @flow(name="{PipelineName}")
   def {pipeline_name}_flow(config: PipelineConfig):
       """Main pipeline flow"""
       data = extract_data(config.source)
       transformed = transform_data(data)
       load_data(transformed, config.destination)
   ```

2. **Configuration** (`src/pipelines/configs/{name}_config.py`):
   - Pydantic models for configuration
   - Validation rules
   - Environment variable loading

3. **Tests** (`tests/pipelines/test_{name}.py`):
   - Unit tests for each task
   - Integration tests for full flow
   - Mock external services

4. **Deployment** (`deployments/{name}.yaml`):
   - Prefect deployment configuration
   - Schedule settings
   - Parameter defaults

## Pipeline Patterns

### Basic ETL
```python
@flow
def etl_flow():
    raw_data = extract()
    clean_data = transform(raw_data)
    load(clean_data)
```

### Parallel Processing
```python
@flow
def parallel_flow(file_list: List[str]):
    # Process files in parallel
    results = []
    for file in file_list:
        result = process_file.submit(file)
        results.append(result)
    
    # Wait for all to complete
    final_results = [r.result() for r in results]
    combine_results(final_results)
```

### AI-Enhanced Pipeline
```python
@flow
def ai_pipeline(data_source: str):
    # Extract
    data = extract_data(data_source)
    
    # Analyze with AI
    agent = DataAnalystAgent()
    insights = agent.analyze(data, "Find anomalies")
    
    # Process based on insights
    if insights.confidence > 0.8:
        processed = apply_recommendations(data, insights)
    else:
        processed = manual_review(data)
    
    # Load
    load_results(processed)
```

## Monitoring & Observability
- Automatic flow run tracking
- Task-level metrics
- Error notifications
- Performance dashboards