# Elephant-Goldfish Model: Review Methodology Reference

This guide details the dispatch, execution, and synthesis of independent Goldfish reviews using Antigravity's subagent architecture.

---

## 1. True Goldfish Isolation Protocol

A Goldfish review is fundamentally distinct from an ordinary self-review:

> **Core Isolation Mandate**: A Goldfish reviewer must evaluate the draft document and referenced source code **without** having read the upstream brainstorming conversation or author discussions. This removes confirmation bias and mimics a senior staff engineer reading an RFC for the first time.

### Dispatching Subagents in Antigravity
When running in Antigravity, invoke each reviewer using the `invoke_subagent` tool:
- **Role**: e.g., `"Skeptical Architect (Zoom-Out Goldfish)"`, `"Design Critic Goldfish"`, `"Tech Lead Goldfish"`.
- **Model**: `'inherit'` or `'pro'`.
- **Prompt**: Pass the target document path, referenced source files, and the specialized lens instructions verbatim.
- **Independence**: Because each subagent runs in its own conversation context, it is a genuine Goldfish reviewer.

---

## 2. Specialized Reviewer Personas

### Persona A: Zoom-Out Goldfish (Skeptical Architect)
- **Directive**: High-altitude simplicity, anti-overengineering, YAGNI enforcement.
- **Audit Vectors**:
  - *Premature Optimizations*: Adding caching layers, background queues, or sharding before bottlenecks are measured.
  - *Altitude Drops (Weeds)*: Pseudocode or variable names cluttering architectural interface definitions.
  - *Architectural Dead-Ends*: Tight coupling that prevents future modular extraction.

### Persona B: Comprehension Goldfish
- **Directive**: Plain-language precision, jargon elimination, clarity audit.
- **Audit Vectors**:
  - *Hand-Waving*: Phrases like "system processes the event smoothly" without stating the algorithm or retry policy.
  - *Missing Definitions*: Undefined acronyms or proprietary concepts.
  - *Logical Gaps*: Steps where step 3 assumes outputs not produced by step 2.

### Persona C: Design Critic Goldfish
- **Directive**: Security, reliability, failure modes, scale boundaries.
- **Audit Vectors**:
  - *Partition Handling*: What happens when the database or external API times out?
  - *Idempotence*: Are retried webhooks or events safely deduplicated?
  - *Auth & Secrets*: Are tokens stored in code? Is least-privilege enforced?

### Persona D: Codebase Details Goldfish
- **Directive**: Ground truth verification against existing repository AST.
- **Audit Vectors**:
  - *Hallucinated Symbols*: Does class `UserProfileService` actually exist in the codebase?
  - *Schema Mismatch*: Does the database model match the claimed ORM entity?
  - *Duplicated Abstractions*: Does a helper function duplicate an existing utility in `src/utils`?

### Persona E: Implementation Readiness Goldfish (Tech Lead)
- **Directive**: Complete, unambiguous, executable task list.
- **Audit Vectors**:
  - *Vague Steps*: "Update frontend" vs. "Add loading state spinner to `CheckoutButton.tsx`".
  - *Missing Test Plan*: No unit test, mock strategy, or E2E scenario specified.
  - *Hidden Decisions*: Forcing the junior implementer to decide database indexes or HTTP status codes.

---

## 3. Standard Finding Schema

All Goldfish findings must adhere to this standardized schema:

```markdown
### Finding [ID]: [Short Descriptive Title]
- **Severity**: [Blocker | Major | Nit]
- **Lens**: [Zoom-Out | Comprehension | Design Critic | Codebase Details | Implementation Readiness]
- **Location**: `[file_path]:[line_range]` or section name
- **Deficiency**: Precise technical explanation of why the current text or design is defective.
- **Evidence**: Grounded citation (code symbol, RFC standard, or missing requirement).
- **Actionable Remedy**: Concrete, unambiguous change required to resolve the finding.
```

---

## 4. Elephant Resolution Protocol

Once findings are collected, the Elephant ingests the report and evaluates each item:

1. **ACCEPT**: The finding is valid. Elephant proposes the exact textual edit to the design draft.
2. **CONTEST**: The critique is based on a misunderstanding or out-of-scope constraint. The Elephant provides verifiable evidence (e.g., pointing to code or approved constraint) explaining why the current design stands.
3. **ALTERNATIVE**: The critique identifies a real issue, but the Goldfish's proposed remedy is sub-optimal. The Elephant presents an alternative fix with trade-offs.

All resolutions are recorded in a **Findings Ledger** before finalizing `approved_specification.md`.
