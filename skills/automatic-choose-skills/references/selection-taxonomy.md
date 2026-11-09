# Automatic Choose Skills: Selection Taxonomy Reference

This taxonomy maps user task categories to core engineering capabilities and skill specializations.

---

## 1. Primary Domain Taxonomy

| Domain Category | Core Capabilities & Deliverables | Archetypal Skill Specialization |
| :--- | :--- | :--- |
| **Full-Stack / Modern Web** | App Router, Server Actions, TanStack Query, hydration | `react-nextjs-pro`, `node-typescript-pro` |
| **Backend & Microservices** | Async APIs, high-throughput I/O, OpenAPI 3.1 | `fastapi-pro`, `java-modern`, `modern-cpp` |
| **Database Engineering** | Schema modeling, indexing, ACID transactions, tuning | `database-postgresql-performance-optimization`, `data-architecture-system-design` |
| **UI/UX & Frontend Craft** | Design systems, WCAG 2.2 AA, motion, typography | `frontend-craft-design-engineering`, `frontend-interface-design-system`, `design-audit` |
| **Agentic AI & LLMs** | Tool-calling reliability, ReAct loops, LangGraph | `ai-agent-architect`, `multi-agent-orchestration`, `local-llm-integration` |
| **RAG & Information Retrieval** | Hybrid search, BM25 + dense vector, reranking | `ai-rag-retrieval-engineering` |
| **AI Inference Serving** | vLLM, PagedAttention, continuous batching, FP8/AWQ | `ai-inference-infrastructure` |
| **Cybersecurity & AppSec** | SAST, OWASP Top 10, secret scanning, hardening | `appsec-owasp-audit`, `cybersecurity-sast-vulnerability-scan` |
| **Cloud & DevOps** | GitHub Actions, containerization, multi-stage Docker | `docker-containerization`, `devops-ci-cd-github`, `cloud-security-hardening` |
| **Data Engineering** | Pipelines, dbt, Spark, Iceberg/Delta lake formats | `data-engineering-pipelines`, `reproducible-data-science` |
| **Architecture & System Design**| Clean architecture, microservices, DDD, trade-offs | `architecture-system-design-review`, `google-elephant-goldfish` |
| **Autonomous Engineering** | Mandates, isolated worker sessions, attention economy | `deepseek-superagent` |
| **Mobile Development** | Flutter 3.x, Dart 3, reactive state, ADB testing | `mobile-flutter-application-engineering` |
| **Embedded & IoT** | C/C++, ARM Cortex-M, FreeRTOS, TinyML, INT8 | `embedded-firmware-c`, `edge-ai-tinyml` |
| **Testing & Quality Assurance** | Playwright browser automation, unit test generation | `testing-playwright-browser-automation`, `testing-unit-test-generation` |
| **Debugging & Root Cause** | Hypothesis-driven debugging, zero-collateral bugfixes | `root-cause-debugging`, `task-surgical-bugfix` |
| **Technical Writing & RFCs** | Design specs, LaTeX typography, academic papers | `academic-report-writer`, `software-api-documentation-openapi` |

---

## 2. Selection Criteria Matrix

When multiple candidate skills are available for a task:

1. **Direct Relevance (Priority: Critical)**: Does the skill directly address the core language, framework, or task objective?
2. **Capability Fit (Priority: Critical)**: Does the skill contain the exact runbook or tool workflow required (e.g., PostgreSQL query optimization vs. generic SQL)?
3. **User Deliverable (Priority: High)**: Does the skill's expected output match what the user requested (e.g., design specification vs. working code vs. test suite)?
4. **Specialization Depth (Priority: High)**: Choose a focused specialist over a broad generalist when deep domain expertise is required.
5. **Composability (Priority: High)**: Can the skills work together in a pipeline without contradictory instructions?
