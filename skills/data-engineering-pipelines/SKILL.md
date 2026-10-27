---
name: data-engineering-pipelines
description: Scalable data pipeline architecture, dbt transformations, Apache Iceberg & Delta Lake open table formats, Spark, Flink streaming, Kafka event buses, data contracts, and data mesh governance.
---

# Data Engineering, Lakehouses & Streaming Pipelines

## 1. Intended Role & Domain
- **Primary Domain**: Backend, APIs & Data Platforms
- **Target Roles**: Senior Data Engineer, Analytics Engineer, Data Platform Architect
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "data pipeline", "dbt transformation", "apache iceberg", "delta lake", "spark streaming", "flink pipeline", "kafka event stream", "data contract", "data mesh", "lakehouse architecture".
- **Contextual Inferences**: Building batch or real-time ETL/ELT pipelines, designing medallion lakehouse architectures (Bronze/Silver/Gold), implementing schema governance across data producers and consumers.
- **Chained Predecessors**: `data-architecture-system-design`, `reproducible-data-science`, `database-postgresql-performance-optimization`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Performing basic CRUD operations on a single transactional database -> use `/fastapi-pro` or `/database-postgresql-performance-optimization`.
  - Simple ad-hoc Jupyter notebook exploratory analysis -> use `/reproducible-data-science`.

## 4. Required Inputs & Context
- Source data feeds (Postgres CDC, Kafka events, REST webhooks, S3/GCS raw logs).
- Processing engine (Apache Spark, PySpark, DuckDB, Flink, dbt-core).
- Target storage & table format (Apache Iceberg, Delta Lake, Snowflake, BigQuery, ClickHouse).
- SLA requirements (batch hourly/daily vs real-time sub-second streaming).

## 5. Expected Outputs & Artifacts
- Medallion architecture transformations (`models/bronze/`, `models/silver/`, `models/gold/` in dbt).
- Data contract specifications (`schema.yaml` with Great Expectations or Pydantic validation).
- Streaming pipeline scripts (`kafka_stream_processor.py` or PySpark jobs).
- CI/CD automated pipeline verification harness with zero-breakage schema evolution.

## 6. Step-by-Step Operating Procedure
1. **Medallion Lakehouse Architecture**:
   - Bronze: Raw immutable ingestion logs with metadata (`_ingested_at`, `_source_file`).
   - Silver: Cleaned, deduplicated, schema-validated, normalized dimension and fact tables.
   - Gold: High-performance business aggregates, metrics mart, and feature store tables.
2. **Open Table Format Configuration**:
   - Configure Apache Iceberg or Delta Lake table properties: compaction policies, Z-Order clustering, time-travel retention (e.g. 7 days).
3. **Data Contract & Schema Governance**:
   - Enforce schema contracts at producer boundaries (JSON Schema / Protobuf / Avro) to prevent downstream breaking changes.
4. **dbt Transformation & Lineage**:
   - Write modular SQL models with explicit dependency DAGs (`ref()` and `source()`).
   - Add data quality tests: `not_null`, `unique`, `relationships`, and custom freshness tests.
5. **Streaming & CDC Ingestion**:
   - Build exactly-once or at-least-once streaming consumers with checkpointing and dead-letter queues (DLQ).

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection of data models and pipeline definitions:
  ```bash
  find . -name "dbt_project.yml" -o -name "*iceberg*" -o -name "*pipeline*.py" 2>/dev/null
  ```
- Preservation rule: Never delete raw Bronze partition data; maintain deterministic auditability.

## 8. Tool & Dependency Requirements
- dbt 1.8+, Apache Iceberg / Delta Lake, PySpark / DuckDB, Apache Kafka, Pydantic V2, Great Expectations.

## 9. Implementation Guidelines & Best Practices
- Production-grade dbt Silver transformation model with schema tests and Iceberg optimization:

```sql
{{ config(
    materialized='incremental',
    table_type='iceberg',
    unique_key='transaction_id',
    incremental_strategy='merge',
    cluster_by=['customer_id', 'transaction_date']
) }}

WITH raw_source AS (
    SELECT
        CAST(json_extract_scalar(raw_payload, '$.id') AS VARCHAR) AS transaction_id,
        CAST(json_extract_scalar(raw_payload, '$.customer_id') AS VARCHAR) AS customer_id,
        CAST(json_extract_scalar(raw_payload, '$.amount') AS DECIMAL(12, 2)) AS amount,
        CAST(json_extract_scalar(raw_payload, '$.currency') AS VARCHAR) AS currency,
        FROM_ISO8601_TIMESTAMP(json_extract_scalar(raw_payload, '$.timestamp')) AS transaction_timestamp,
        _ingested_at
    FROM {{ source('bronze', 'raw_transactions') }}
    {% if is_incremental() %}
    WHERE _ingested_at > (SELECT MAX(_ingested_at) FROM {{ this }})
    {% endif %}
),

validated AS (
    SELECT
        transaction_id,
        customer_id,
        amount,
        UPPER(currency) AS currency,
        transaction_timestamp,
        DATE(transaction_timestamp) AS transaction_date,
        _ingested_at
    FROM raw_source
    WHERE transaction_id IS NOT NULL
      AND amount > 0
)

SELECT * FROM validated
```

## 10. Error Handling & Recovery Procedures
- Upstream schema drift: Implement dead-letter routing for malformed payloads rather than failing the entire batch.
- Out-of-memory in Spark transformations: Optimize partition sizing (aim for 128MB-256MB per partition); avoid full shuffles and Cartesian joins.

## 11. Security & Privacy Constraints
- Mask PII columns (emails, phone numbers, credit cards) at the Silver tier using cryptographic hashing or tokenization.
- Implement column-level and row-level access control on Gold analytical tables.

## 12. Verification & Testing Requirements
- Run dbt test suite (`dbt test`) to verify primary keys, foreign keys, and zero null regressions.
- Verify pipeline idempotency: running the same pipeline twice on identical input produces identical downstream state.

## 13. Completion Criteria
- Pipeline completes with 100% data freshness compliance.
- Lineage DAG documented and visible in catalog.
- Zero silent data corruption or schema contract violations.

## 14. Relevant Official References
- Fundamentals of Data Engineering (Reis & Housley).
- Apache Iceberg Specification (Apache Software Foundation).
- Data Mesh: Delivering Data-Driven Value at Scale (Zhamak Dehghani).

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with Apache Iceberg 1.6+, DuckDB 1.1+, and dbt-core 1.8+.
