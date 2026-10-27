---
name: database-postgresql-performance-optimization
description: Advanced PostgreSQL 16+ engineering, complex schema design, indexing strategies (B-Tree, GIN, BRIN), query optimization with EXPLAIN ANALYZE, and ACID transactional integrity.
---

# PostgreSQL Advanced Engineering & Optimization

## 1. Intended Role & Domain
- **Primary Domain**: Data Engineering & Database Architecture
- **Target Roles**: Database Developer, Database Administrator, Backend Developer
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "postgresql", "postgres optimization", "explain analyze", "sql indexing", "gin index", "brin index", "database migration".
- **Contextual Inferences**: Repositories using PostgreSQL, Alembic, Prisma, Drizzle, or raw SQL migrations.
- **Chained Predecessors**: `task-decomposition`, `repo-audit`.

## 3. Explicit Exclusions
- Do NOT use when:
  - NoSQL-only tasks (e.g. MongoDB, Redis key-value cache, DynamoDB).
  - Client-side browser storage (IndexedDB, LocalStorage).

## 4. Required Inputs & Context
- Entity Relationship requirements or existing DDL schema.
- Slow query text or performance bottleneck scenario.
- PostgreSQL 14+ target environment.

## 5. Expected Outputs & Artifacts
- Normalized 3NF or dimensional schema migration script (`UP` and `DOWN`).
- Targeted indexes with justified memory/write cost trade-offs.
- `EXPLAIN (ANALYZE, BUFFERS)` execution plan interpretation and optimized query rewrite.

## 6. Step-by-Step Operating Procedure
1. **Schema & Constraint Design**:
   - Define tables with explicit primary keys (`UUIDv7` or `BIGINT GENERATED ALWAYS AS IDENTITY`).
   - Enforce foreign keys with appropriate `ON DELETE` semantics (`CASCADE` or `RESTRICT`).
   - Add `CHECK` constraints to ensure data invariants at the database level.
2. **Indexing Selection**:
   - B-Tree for equality and range queries on high-cardinality keys.
   - GIN for JSONB and full-text search (`to_tsvector`).
   - BRIN for massive append-only time-series tables naturally ordered by timestamp.
3. **Query Analysis & Profiling**:
   - Run `EXPLAIN (ANALYZE, BUFFERS, TIMING)` to identify Sequential Scans, high buffer hits, and expensive hash joins.
4. **Migration & Zero-Downtime Rollout**:
   - Create indexes concurrently (`CREATE INDEX CONCURRENTLY`) to prevent blocking table writes.
5. **Connection Pooling & Health Verification**:
   - Verify connection pool parameters (PgBouncer or client pool size).

## 7. Repository Inspection & Planning Requirements
- Non-destructive query and migration check:
  ```bash
  grep -i "CREATE TABLE" migrations/*.sql 2>/dev/null || find . -name "*schema.prisma"
  ```
- Preservation rule: Never drop columns or tables in production migrations without a phased deprecation period.

## 8. Tool & Dependency Requirements
- `psql` CLI, pg_stat_statements, Alembic / Flyway / Prisma / Drizzle.

## 9. Implementation Guidelines & Best Practices
- Never use `SELECT *` in production code; select explicit columns to allow index-only scans.
- Use composite indexes with the most selective equality column first, followed by range columns.
- Use `JSONB` for semi-structured data, but extract high-query fields into relational columns.

```sql
-- Zero-downtime concurrent index creation
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_customer_status
ON orders (customer_id, status)
INCLUDE (total_amount)
WHERE status != 'cancelled';
```

## 10. Error Handling & Recovery Procedures
- Deadlocks detected: Ensure all application transactions acquire table locks or row updates in a consistent, uniform order.
- Connection starvation: Limit pool size per application worker (formula: `pool_size = (core_count * 2) + effective_spindle_count`).

## 11. Security & Privacy Constraints
- Prevent SQL Injection: ALWAYS use parameterized queries with placeholders (`$1`, `%s`, `?`); never concatenate raw strings.
- Enforce Row Level Security (RLS) for multi-tenant isolation where appropriate.

## 12. Verification & Testing Requirements
- Verify query plan:
  ```sql
  EXPLAIN (ANALYZE, BUFFERS) 
  SELECT order_id, total_amount FROM orders WHERE customer_id = 42 AND status = 'shipped';
  ```
- Confirm `Index Scan` or `Index Only Scan` is used instead of `Seq Scan`.

## 13. Completion Criteria
- DDL scripts syntactically valid with reversible migrations.
- Indexes created concurrently with zero write lockouts.
- Query execution plan verified with significant reduction in buffer reads.

## 14. Relevant Official References
- PostgreSQL Official Documentation (postgresql.org/docs/current/).
- Use The Index, Luke (Markus Winand).

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with PostgreSQL 15, 16, and 17.
