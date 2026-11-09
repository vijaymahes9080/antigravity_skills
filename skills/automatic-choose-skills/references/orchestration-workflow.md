# Automatic Choose Skills: Orchestration Workflow Reference

This guide details the multi-skill sequencing patterns, responsibility division, and conflict resolution rules used when coordinating multiple specialist skills.

---

## 1. Typical Multi-Skill Sequencing Archetypes

### Archetype A: Greenfield Feature (Design to Deployment)
```
[ google-elephant-goldfish ] --> Draft spec & run independent Goldfish review
              |
[ architecture-system-design-review ] --> Validate system boundaries & contracts
              |
[ database-postgresql-performance-optimization ] --> Model schemas & indexes
              |
[ fastapi-pro / react-nextjs-pro ] --> Implement API & UI layers
              |
[ appsec-owasp-audit ] --> Security scan & input validation hardening
              |
[ testing-unit-test-generation ] --> Generate automated unit test coverage
              |
[ docker-containerization ] --> Build production distroless/alpine container
```

### Archetype B: Autonomous Bugfix & Surgical Remediation
```
[ deepseek-superagent ] --> Bind mandate, prepare isolated workspace
              |
[ root-cause-debugging ] --> Formulate hypothesis, isolate root cause
              |
[ python-pro / node-typescript-pro ] --> Apply surgical patch with zero collateral edits
              |
[ testing-unit-test-generation ] --> Add regression unit test
              |
[ deepseek-superagent ] --> Verify tests, run diff audit, report ready
```

### Archetype C: AI-Powered Application Engineering
```
[ ai-agent-architect ] --> Design ReAct loops, tool schemas, state graphs
              |
[ ai-rag-retrieval-engineering ] --> Configure hybrid search & reranking
              |
[ ai-inference-infrastructure / local-llm-integration ] --> Configure model serving / vLLM
              |
[ ai-evaluation-safety ] --> Red-team prompt injection & toxic output defenses
```

---

## 2. Responsibility Division Protocol

When multiple skills are active concurrently:
1. **Single Source of Truth**: Only ONE skill governs code writing in a specific file at any given moment.
2. **Phase Hand-Off**: A skill's output serves as the explicit input for the next skill in the pipeline (e.g., the schema output from `data-architecture-system-design` becomes the model definition in `fastapi-pro`).
3. **Audit Before Merge**: Security and quality skills (`appsec-owasp-audit`, `repo-audit`) run as verification gates before declaring completion.

---

## 3. Conflict Resolution Invariants

When two selected skills provide overlapping or contradictory guidance:
1. **Safety Over Speed**: Security and authorization invariants (e.g., OWASP defenses, non-destructive gates) always override optimization or developer convenience.
2. **Project-Local Over Global**: Project-specific rules (`AGENTS.md`, workspace skills) override generic global instructions.
3. **Specialist Over Generalist**: In domain-specific mechanics (e.g., PostgreSQL query indexing), the specialist skill overrides general database guidance.
4. **Zero Collateral Edits**: Code refactoring instructions must never override the principle of minimal, targeted changes for bug fixes.
