# Elephant-Goldfish Model: Design Methodology Reference

This guide details the upstream ideation, requirements discovery, and drafting phases governed by the Elephant role.

---

## 1. Upstream Ideation & Brainstorming Protocol

When exploring a new feature or architectural pivot, the Elephant must resist rushing to code:

### Step 1.1: Multi-Turn Problem Grounding
- Ask open-ended, probing questions in chat:
  - *What is the specific bottleneck or capability gap being addressed?*
  - *What are the non-negotiable performance, latency, or compliance constraints?*
  - *Who are the primary consumers (internal services, third-party developers, end-users)?*
- Never use pre-canned multiple-choice question tools for open-ended concept discovery. Let the user articulate raw intent.

### Step 1.2: The Contrarian Check (YAGNI & Complexity Minimization)
Before writing specifications, evaluate:
- Can an existing open-source package or internal library solve this without custom engineering?
- Does the repository already contain a utility or abstraction that can be reused?
- What happens if we do not build this feature?

### Step 1.3: Generating the Concepts Brief
Synthesize the brainstorming output into `concepts_brief.md`:
```markdown
# Concept Brief: [Feature Name]

## 1. Problem Statement
Concise, jargon-free summary of the problem and business/engineering motivation.

## 2. Core Working Hypothesis
The proposed architectural solution and why it is superior to alternatives.

## 3. Explicit Non-Goals
Boundaries defining what this feature will intentionally NOT do.

## 4. Key Constraints & Unknowns
Latency budgets, backward compatibility limits, and unresolved technical dependencies.
```

---

## 2. Section-by-Section Drafting Protocol

Once the concept brief is established, the Elephant drafts `design_draft.md` incrementally:

```
[ Section 1: Context & Goals ]       --> [ User Approval Gate ]
              |
[ Section 2: Architecture & Flow ]    --> [ User Approval Gate ]
              |
[ Section 3: Data Model & Contracts ] --> [ User Approval Gate ]
              |
[ Section 4: Operational & Security ] --> [ User Approval Gate ]
              |
[ Section 5: Implementation Plan ]   --> [ User Approval Gate ]
```

### The Section Approval Gate Invariant
After drafting each section:
1. Write the updated content to `design_draft.md`.
2. Provide a 2–3 sentence chat summary highlighting the key design choices made in that section.
3. Include a clickable link to `design_draft.md`.
4. Prompt the user for approval or revision before starting the next section.

---

## 3. The "Author Decides Architecture" Rule

When faced with architectural trade-offs (e.g., synchronous REST vs. async Kafka, Postgres JSONB vs. normalized tables, polling vs. WebSockets):
1. **Never guess or quietly pick a preference.**
2. **Present up to 3 distinct architectural options**, each structured as:
   - **Mechanism**: How it works concretely.
   - **Trade-offs**: Latency, complexity, operational cost, maintenance burden.
   - **Failure Conditions**: Under what workload or environment condition this choice degrades or fails.
3. Ask the human author to select the desired direction.
4. If the user replies *"you choose"* or *"pick the best"*, re-emphasize the primary trade-off and ask for alignment on the trade-off priority.
