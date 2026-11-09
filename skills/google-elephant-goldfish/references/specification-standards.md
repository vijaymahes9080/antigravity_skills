# Elephant-Goldfish Model: Specification Standards Reference

This document defines the canonical specification structure, documentation hygiene standards, and style invariants required for all design artifacts.

---

## 1. Canonical Specification Schema

All production design specifications produced under this skill must adhere to the following 8-part structure:

```markdown
# [Feature Name] Technical Specification

## 1. Context, Motivation & Problem Statement
- High-level business and technical context.
- What problem does this solve? Why solve it now?
- Who is impacted?

## 2. Goals & Non-Goals
- Explicit, measurable goals (e.g., "p99 latency < 50ms at 1k QPS").
- Explicit non-goals (e.g., "Multi-region replication is out of scope for v1").

## 3. High-Level Architecture & Component Boundaries
- Mermaid diagram showing components, data flow, and external boundaries.
- Responsibilities of each new or modified service/module.

## 4. API, Protocols & Data Contracts
- Explicit request/response schemas (JSON schema, Protobuf, or TypeScript interfaces).
- Database migrations, table schemas, and indexing strategies.
- Idempotence keys and error code taxonomy.

## 5. Security, Privacy & Compliance
- Authentication & Authorization mechanisms (RBAC, scopes).
- Data sanitization, PII masking, secret storage.
- Threat modeling and attack vector analysis.

## 6. Failure Modes, Resiliency & Observability
- Behavior during network degradation, downstream timeouts, or crashes.
- Distributed tracing spans, metrics (SLIs/SLOs), and alert definitions.
- Rollback plan and emergency kill-switches.

## 7. Phased Implementation Plan
- Step-by-step ordered execution milestones.
- Exact file paths, classes, and tests to be created or modified.

## 8. Measurable Acceptance Criteria
- Exact test assertions, end-to-end user journeys, and performance benchmarks required for sign-off.
```

---

## 2. Documentation Hygiene & Language Invariants

### Banned Jargon & Promotional Language
To prevent AI-generated slop and maintain technical rigor, the following terms are banned in specifications:

| Banned Term / Style | Required Alternative |
| :--- | :--- |
| *Seamless / Seamlessly* | State exact integration mechanism (e.g., "via synchronous REST call") |
| *Robust / Robustly* | State exact fault-tolerance parameters (e.g., "retries 3 times with exponential backoff") |
| *Blazingly fast* | State measured latency SLO (e.g., "p95 response time under 15ms") |
| *Effortless / Intuitive* | State developer ergonomics (e.g., "requires a single CLI command with 2 arguments") |
| *State-of-the-art* | Specify benchmark comparison or proven algorithm |

### Mathematical & Algorithmic Rigor
- When describing complexity, use formal notation ($O(n \log n)$, $O(1)$).
- When specifying rates or budgets, provide concrete numerical limits ($100 \text{ req/sec}$, $256 \text{ MB}$).
