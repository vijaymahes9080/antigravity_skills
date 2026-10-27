---
name: task-decomposition
description: Breaking down complex user epics and software objectives into atomic, testable, and dependency-ordered implementation stages. Use when starting large engineering tasks or structuring complex multi-file changes.
---

# Systematic Task Decomposition & Architecture Planning

## 1. Intended Role & Domain
- **Primary Domain**: Software Architecture & Engineering Leadership
- **Target Roles**: Software Architect, Technical Lead, Product Engineer
- **Architectural Layer**: Layer 1 (Core Engineering Foundations)

## 2. Activation Conditions
- **Direct Triggers**: "decompose task", "plan implementation", "break down project", "architecture planning", "create execution stages".
- **Contextual Inferences**: High-complexity user requests spanning multiple subsystems or files.
- **Chained Predecessors**: `repo-audit`.

## 3. Explicit Exclusions
- Do NOT use when:
  - User requested a trivial single-line change.
  - The task has already been decomposed into approved actionable steps.

## 4. Required Inputs & Context
- High-level project requirements or feature brief.
- Current repository architecture and tech stack constraints.
- Non-functional requirements (latency, throughput, security, accessibility).

## 5. Expected Outputs & Artifacts
- Detailed Stage-by-Stage Implementation Plan.
- Dependency flow diagram (Mermaid).
- Concrete verification criteria for every milestone.

## 6. Step-by-Step Operating Procedure
1. **Scope & Constraint Clarification**:
   - Parse requirements, identify unstated assumptions, and delineate system boundaries.
2. **Subsystem Identification & Layering**:
   - Separate concerns: data models -> business logic -> service APIs -> user interface -> testing.
3. **Atomic Task Chunking**:
   - Ensure each task is independent, small enough to review, and has explicit inputs/outputs.
4. **Dependency Ordering & Critical Path Analysis**:
   - Arrange stages so prerequisites are built and tested before downstream consumers.
5. **Quality Gates & Checkpoint Definition**:
   - Establish passing criteria (tests, builds, benchmarks) for each milestone.

## 7. Repository Inspection & Planning Requirements
- Map existing components before proposing new ones:
  ```bash
  # Check directory structure and package organization
  find src/ -maxdepth 2 -type d
  ```
- Preservation rule: Minimize architectural drift; adhere to established project conventions.

## 8. Tool & Dependency Requirements
- Markdown formatting tools, Mermaid diagram syntax.

## 9. Implementation Guidelines & Best Practices
- Keep tasks atomic: each step should leave the codebase in a compilable, passing state.
- Avoid "big bang" deployments where all changes land at once without progressive validation.

## 10. Error Handling & Recovery Procedures
- Unforeseen dependency circularity: Extract shared interface or data contract to a lower foundation layer.

## 11. Security & Privacy Constraints
- Ensure architectural plans factor in authentication boundaries, secret management, and data encryption early in design.

## 12. Verification & Testing Requirements
- Verify that every proposed stage includes an automated verification command (e.g. `npm test`, `pytest`).
- Validate that the proposed architecture aligns with existing framework patterns.

## 13. Completion Criteria
- Implementation plan finalized with:
  1. Architectural overview & diagram
  2. Sequential stage breakdown
  3. Concrete automated verification plan
  4. Risk mitigation strategy.

## 14. Relevant Official References
- "Fundamentals of Software Architecture" (Mark Richards & Neal Ford).
- Google Engineering Practices: Small CL Guidelines.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Aligns with Antigravity planning mode guidelines.
