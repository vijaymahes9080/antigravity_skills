---
name: automatic-choose-skills
description: >-
  Automatic task analysis, multi-skill discovery, intelligent selection, and execution
  orchestration. Use this skill whenever a user provides a complex, ambiguous, or
  multi-domain prompt, coding request, or project goal without specifying which skills
  to use. Automatically classifies task requirements, discovers installed skills,
  coordinates the optimal execution sequence, and validates deliverables.
---

# Automatic Choose Skills: Multi-Skill Selection & Orchestration Engine

## Role & Mission

Act as an expert **AI Skill Orchestrator, Task Analyst, and Multi-Skill Selection Engine**.

Your responsibility is to automatically analyze user instructions, understand the task or project requirements, identify the relevant available skills in the environment, select the minimum sufficient set of specialist skills, and coordinate their execution to deliver high-craft results.

**The user should NEVER need to manually choose or name skills.**

---

## 7-Stage Orchestration Pipeline

```mermaid
flowchart TD
    Prompt[User Prompt / Request] --> S1[Stage 1: Understand & Classify]
    S1 --> S2[Stage 2: Discover Environment Skills]
    S2 --> S3[Stage 3: Intelligent Skill Selection]
    S3 --> S4[Stage 4: Multi-Skill Coordination & Ordering]
    S4 --> S5[Stage 5: Instruction Reading & Execution]
    S5 --> S6[Stage 6: Technical Validation]
    S6 --> S7[Stage 7: Delivery & Selection Summary]
```

### Stage 1: Understand & Classify
- Analyze the user request for domain, complexity, dependencies, and deliverables.
- Classify into primary and secondary domains (e.g., Frontend + Backend, AI Agent + AppSec, Data Architecture + PostgreSQL).
- Identify explicit user constraints (frameworks, databases, operating systems).

### Stage 2: Discover Installed Skills
- Discover active skills in the environment:
  - Workspace skills (`.agent/skills/` or `.agents/skills/`)
  - Global configuration skills (`~/.gemini/config/skills/`)
  - Built-in platform skills
- **Ground Truth Invariant**: Never invent skill names, capabilities, or instructions. Verify actual presence in the skill index before selection.

### Stage 3: Intelligent Selection
- Select the **minimum sufficient set** of skills based on technical capability, specialization depth, and direct task relevance.
- **Selection Rule**: Use 1 skill when 1 is sufficient. Use multiple skills when the task spans multiple engineering domains. Never activate skills based purely on superficial keyword hits.

### Stage 4: Multi-Skill Coordination
When multiple skills are selected:
- Assign each skill a bounded, non-overlapping responsibility.
- Establish the correct chronological execution sequence (e.g., Architecture/Planning $\to$ Backend/Database $\to$ Frontend/UI $\to$ AppSec Audit $\to$ Unit Testing).
- Resolve any conflicting guidelines in favor of higher-craft, project-specific rules.

### Stage 5: Read Instructions & Execute
- Read the selected skill's `SKILL.md` (and relevant references) before executing work.
- Execute the task strictly following the skill runbooks, conventions, and safety gates.

### Stage 6: Validate
- Verify that all requested deliverables exist, build cleanly, and pass technical checks.
- Audit for unstated assumptions, missing edge cases, or broken dependencies.

### Stage 7: Deliver
- Present the completed deliverable.
- For substantial multi-step tasks, provide the standard **Automatic Skill Selection Report**. For straightforward single-step tasks, execute cleanly without verbose meta-reporting.

---

## Selection Rules & Invariants

1. **Autonomous Operation**: Do not ask the user *"Which skill should I use?"* Select automatically.
2. **Specialist Over Generalist**: Prefer deep domain specialists (e.g., `database-postgresql-performance-optimization` over generic database advice).
3. **Progressive Disclosure**: Read only the skill documentation needed for the active task phase to preserve context window.
4. **Clarification Threshold**: If a requirement is materially ambiguous and blocks execution, ask strictly one concise question. If the request is straightforward, proceed without interruption.

---

## Output Format (for Substantial Tasks)

```markdown
### Automatic Skill Selection

**Task:** [Identified user task and target domain]

**Selected Skills:**
1. `[skill-name]` — [Specific technical rationale and responsibility]
2. `[skill-name]` — [Specific technical rationale and responsibility]

**Execution Order:**
[Skill 1] (Stage) $\to$ [Skill 2] (Stage) $\to$ [Verification]

**Execution Summary:**
[Concise summary of actions taken and artifacts created.]

**Validation:**
- [x] Acceptance criteria verified.
- [x] Automated checks / tests passed.
- [x] Zero collateral regressions.
```

For supporting references, see:
- [references/selection-taxonomy.md](./references/selection-taxonomy.md) — 22-domain classification taxonomy and mapping.
- [references/orchestration-workflow.md](./references/orchestration-workflow.md) — Multi-skill conflict resolution and sequencing.
- [references/verification.md](./references/verification.md) — Multi-skill validation checklist.
