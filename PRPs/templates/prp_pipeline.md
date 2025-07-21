# PRP: Data Pipeline Development

## Metadata
- **Created**: [DATE]
- **Author**: [AUTHOR]
- **Confidence**: [1-10]
- **Complexity**: [Low/Medium/High]
- **Type**: Data-Pipeline

## Goal
[Clear description of the data pipeline to be built]

## Why
- **Business Value**: [Impact on data processing/analytics]
- **Technical Need**: [Current limitations being addressed]
- **Priority**: [Critical/High/Medium/Low]

## What
[Pipeline behavior, data flow, and transformations]

### Success Criteria
- [ ] Processes X records per minute
- [ ] Error rate < 0.1%
- [ ] Data quality checks pass
- [ ] Incremental processing supported
- [ ] Monitoring and alerting configured
- [ ] Backfill capability implemented

## All Needed Context

### Documentation & References
```yaml
# Pipeline Framework
- url: https://docs.prefect.io/latest/
  why: Prefect orchestration patterns
  sections: ["flows", "tasks", "deployments"]

- file: src/pipelines/base.py
  why: Base pipeline patterns
  pattern: Flow structure and error handling

# Data Processing
- url: https://docs.dask.org/en/stable/
  why: Parallel processing patterns
  critical: Partition strategies

- url: https://duckdb.org/docs/
  why: Analytical queries
  sections: ["data-import", "sql-features"]

# Existing Pipelines
- file: src/pipelines/etl_example.py
  why: ETL pattern to follow
  gotcha: Always use context managers

# Schema Management
- file: src/models/schemas.py
  why: Data validation schemas
  pattern: Pydantic for validation
```

### Current Pipeline Structure
```python
from prefect import flow, task
from typing import List, Dict
import pandas as pd

@task(retries=3, retry_delay_seconds=60)
def extract_data(source: str) -> pd.DataFrame:
    """Extract with automatic retries"""
    # Implementation
    pass

@task
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform with validation"""
    # Implementation
    pass

@flow(name="example-pipeline")
def pipeline_flow(config: PipelineConfig):
    """Main pipeline flow"""
    data = extract_data(config.source)
    transformed = transform_data(data)
    load_to_warehouse(transformed, config.destination)
```

### Known Gotchas & Critical Patterns
```python
# CRITICAL: Use context managers for connections
@task
def extract_from_database(query: str):
    with get_db_connection() as conn:
        return pd.read_sql(query, conn)

# PATTERN: Chunked processing for large datasets
@task
def process_large_dataset(source: str, chunk_size: int = 10000):
    for chunk in pd.read_csv(source, chunksize=chunk_size):
        yield process_chunk(chunk)

# GOTCHA: DuckDB in-memory for analytics
def analyze_with_duckdb(df: pd.DataFrame):
    import duckdb
    # Create connection with DataFrame registered
    conn = duckdb.connect(':memory:')
    conn.register('data', df)
    return conn.execute("SELECT * FROM data").fetchdf()

# WARNING: Memory management critical
# Always del large objects and gc.collect()

# PATTERN: Incremental processing
@task
def get_incremental_data(table: str, last_timestamp: datetime):
    query = f"""
    SELECT * FROM {table}
    WHERE updated_at > '{last_timestamp}'
    ORDER BY updated_at
    """
    return extract_from_database(query)
```

## Implementation Blueprint

### Task Breakdown
```yaml
Task 1 - Pipeline Configuration:
  CREATE src/pipelines/config/{pipeline_name}_config.py:
    - Source configurations
    - Destination settings
    - Transformation rules
    - Schedule definition
    
  CREATE config/{pipeline_name}.yaml:
    - Environment-specific settings
    - Connection strings
    - Resource limits

Task 2 - Data Models:
  CREATE src/models/{pipeline_name}_schemas.py:
    - Input schema validation
    - Output schema definition
    - Intermediate schemas
    
  TESTS tests/models/test_{pipeline_name}_schemas.py:
    - Schema validation tests
    - Edge case handling

Task 3 - Extract Tasks:
  CREATE src/pipelines/{pipeline_name}/extract.py:
    - Source connectors
    - Incremental logic
    - Error handling
    - Retry configuration
    
  IMPLEMENT extraction patterns:
    - Database queries
    - API calls
    - File reading
    - Stream processing

Task 4 - Transform Tasks:
  CREATE src/pipelines/{pipeline_name}/transform.py:
    - Data cleaning
    - Enrichment logic
    - Aggregations
    - Validation checks
    
  OPTIMIZE for performance:
    - Vectorized operations
    - Parallel processing
    - Memory efficiency

Task 5 - Load Tasks:
  CREATE src/pipelines/{pipeline_name}/load.py:
    - Destination connectors
    - Upsert logic
    - Transaction handling
    - Post-load validation
    
  IMPLEMENT patterns:
    - Batch loading
    - Streaming writes
    - Error recovery

Task 6 - Orchestration:
  CREATE src/pipelines/{pipeline_name}/flow.py:
    - Main pipeline flow
    - Task dependencies
    - Error handling
    - Monitoring hooks
    
  CONFIGURE deployment:
    - Schedule settings
    - Resource allocation
    - Alerting rules

Task 7 - Testing:
  CREATE tests/pipelines/test_{pipeline_name}_flow.py:
    - Unit tests for each task
    - Integration tests
    - Data quality tests
    - Performance tests
    
  CREATE tests/pipelines/test_{pipeline_name}_e2e.py:
    - End-to-end testing
    - Sample data fixtures
```

### Implementation Patterns

```python
# Pattern 1: Robust Pipeline Structure
from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner
from typing import List, Optional
import pandas as pd
from datetime import datetime

@task(
    name="extract-source-data",
    retries=3,
    retry_delay_seconds=60,
    cache_key_fn=lambda *args, **kwargs: f"extract-{kwargs.get('date')}"
)
async def extract_data(
    source: str,
    date: datetime,
    filters: Optional[Dict] = None
) -> pd.DataFrame:
    """Extract data with caching and retries"""
    logger = get_run_logger()
    logger.info(f"Extracting data from {source} for {date}")
    
    try:
        # Connection pooling
        async with get_connection_pool(source) as pool:
            query = build_extraction_query(date, filters)
            df = await pool.fetch_dataframe(query)
            
        # Validate extraction
        assert not df.empty, "No data extracted"
        logger.info(f"Extracted {len(df)} records")
        
        return df
        
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise

# Pattern 2: Efficient Transformation
@task(name="transform-data")
def transform_data(
    df: pd.DataFrame,
    rules: TransformationRules
) -> pd.DataFrame:
    """Transform with validation and monitoring"""
    logger = get_run_logger()
    
    # Data quality checks
    quality_report = validate_input_data(df, rules.input_schema)
    if not quality_report.is_valid:
        raise DataQualityError(quality_report.errors)
    
    # Transformations with progress tracking
    with transformation_context() as ctx:
        # Clean
        df_clean = clean_data(df, rules.cleaning_rules)
        ctx.log_step("cleaning", len(df_clean))
        
        # Enrich
        df_enriched = enrich_data(df_clean, rules.enrichment_rules)
        ctx.log_step("enrichment", len(df_enriched))
        
        # Aggregate
        if rules.aggregation_rules:
            df_final = aggregate_data(df_enriched, rules.aggregation_rules)
        else:
            df_final = df_enriched
        ctx.log_step("aggregation", len(df_final))
    
    # Output validation
    validate_output_data(df_final, rules.output_schema)
    
    return df_final

# Pattern 3: Parallel Processing
@flow(
    name="parallel-pipeline",
    task_runner=DaskTaskRunner(
        cluster_kwargs={"n_workers": 4, "threads_per_worker": 2}
    )
)
def parallel_pipeline_flow(
    sources: List[str],
    date: datetime,
    config: PipelineConfig
):
    """Process multiple sources in parallel"""
    logger = get_run_logger()
    
    # Extract in parallel
    extraction_futures = []
    for source in sources:
        future = extract_data.submit(source, date)
        extraction_futures.append(future)
    
    # Wait for all extractions
    extracted_data = [future.result() for future in extraction_futures]
    
    # Combine and transform
    combined_df = pd.concat(extracted_data, ignore_index=True)
    transformed_df = transform_data(combined_df, config.transformation_rules)
    
    # Load with partitioning
    load_with_partitions(
        transformed_df,
        config.destination,
        partition_cols=["date", "source"]
    )

# Pattern 4: Incremental Processing
class IncrementalPipeline:
    """Incremental processing with state management"""
    
    def __init__(self, pipeline_name: str):
        self.pipeline_name = pipeline_name
        self.state_manager = StateManager(pipeline_name)
    
    @flow(name="incremental-pipeline")
    async def run(self, config: IncrementalConfig):
        # Get last successful run
        last_run = await self.state_manager.get_last_successful_run()
        
        # Determine processing window
        start_time = last_run.end_time if last_run else config.initial_start
        end_time = datetime.now()
        
        # Process incrementally
        logger.info(f"Processing from {start_time} to {end_time}")
        
        try:
            # Extract incremental data
            data = await extract_incremental(
                config.source,
                start_time,
                end_time
            )
            
            # Transform
            transformed = transform_data(data, config.rules)
            
            # Load
            await load_incremental(
                transformed,
                config.destination,
                mode="append"
            )
            
            # Update state
            await self.state_manager.mark_successful(
                start_time,
                end_time,
                records_processed=len(data)
            )
            
        except Exception as e:
            await self.state_manager.mark_failed(start_time, end_time, str(e))
            raise
```

## Validation Loops

### Level 1: Syntax & Code Quality
```bash
# Style checks
ruff check src/pipelines/ --fix
black src/pipelines/
mypy src/pipelines/ --strict

# Complexity check
radon cc src/pipelines/ -s
# Ensure cyclomatic complexity < 10
```

### Level 2: Unit Tests
```bash
# Test individual tasks
pytest tests/pipelines/test_{pipeline_name}_tasks.py -v

# Test transformations
pytest tests/pipelines/test_{pipeline_name}_transforms.py -v

# Coverage check
pytest tests/pipelines/ --cov=src/pipelines/{pipeline_name} --cov-report=term-missing
# Required: >85% coverage
```

### Level 3: Integration Tests
```bash
# Test with sample data
pytest tests/pipelines/test_{pipeline_name}_integration.py -v

# Test error scenarios
pytest tests/pipelines/test_{pipeline_name}_errors.py -v

# Test incremental processing
pytest tests/pipelines/test_{pipeline_name}_incremental.py -v
```

### Level 4: Performance & Data Quality
```bash
# Performance test
python tests/pipelines/perf_{pipeline_name}.py
# Requirement: Process 1M records in < 5 minutes

# Data quality validation
python tests/pipelines/quality_{pipeline_name}.py
# All quality checks must pass

# Memory profiling
mprof run python tests/pipelines/profile_{pipeline_name}.py
# Memory usage must stay under 4GB

# Load testing
python tests/pipelines/load_{pipeline_name}.py
# Handle 10 concurrent runs
```

## Deployment Checklist
- [ ] Pipeline registered in Prefect
- [ ] Schedule configured
- [ ] Monitoring alerts set up
- [ ] Data quality checks in place
- [ ] Backfill procedure documented
- [ ] Resource limits configured
- [ ] Failure recovery tested
- [ ] Documentation updated

## Anti-Patterns to Avoid
- ❌ Don't load entire dataset into memory
- ❌ Don't use pandas for > 10M records (use Dask/DuckDB)
- ❌ Don't skip data validation
- ❌ Don't hardcode connection strings
- ❌ Don't ignore failed records
- ❌ Don't process without checkpointing
- ❌ Don't forget cleanup (temp files, connections)

## Confidence Score: [X]/10

### Scoring Rationale:
- Pipeline patterns followed: [X]/2
- Error handling complete: [X]/2
- Performance optimized: [X]/2
- Testing comprehensive: [X]/2
- Monitoring configured: [X]/2
