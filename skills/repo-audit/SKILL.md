---
name: repo-audit
description: Master 360-degree repository audit, architecture reconstruction, dependency vulnerability scanning, license compliance, code hygiene, and prioritized technical debt remediation ledger (P0-P3).
---

# Master Repository Audit & 360-Degree Architecture Reconstruction

## 1. Intended Role & Domain
- **Primary Domain**: Software Engineering Leadership, Architecture & Quality
- **Target Roles**: Software Architect, Principal Engineer, Technical Lead, Security Auditor
- **Architectural Layer**: Layer 1 (Core Engineering Standards & System Discovery)
- **Supported Invocations**: `/repo-audit`, `/task-full-repo-audit`

## 2. Activation Conditions
- **Direct Triggers**: "audit repository", "inspect codebase", "repo health check", "evaluate project architecture", "codebase overview", "full repo audit", "complete codebase audit", "360 code audit".
- **Contextual Inferences**: First turn in a new codebase, onboarding to unfamiliar repositories, quarterly technical debt audits, pre-refactoring risk assessments.
- **Chained Predecessors**: None (entry-point skill for codebase exploration).

## 3. Explicit Exclusions
- Do NOT use when:
  - User requested a simple 1-line localized syntax fix or quick typo fix.
  - Active destructive refactoring is requested without an audit requirement.

## 4. Required Inputs & Context
- Target repository root path.
- Project descriptor files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, etc.).
- Execution terminal for non-destructive inspection commands (`git`, `find`, `rg`).

## 5. Expected Outputs & Artifacts
1. **Architecture Topology Map**: Mermaid component & dependency diagram.
2. **Technology Stack & Runtime Manifest**: Core frameworks, runtimes, drivers, and toolchains.
3. **Prioritized Remediation Ledger**:
   - **P0 / Blocker**: Immediate security hazard, exposed credentials, active data loss vulnerability.
   - **P1 / High**: Severe performance bottleneck, missing authentication on sensitive routes, zero test coverage on core business logic.
   - **P2 / Medium**: Deprecated library versions, unindexed database queries, inconsistent error handling.
   - **P3 / Low**: Cosmetic lint warnings, minor documentation gaps, dead helper functions.
4. **Dependency Status & License Compliance Matrix**: Outdated packages, CVEs, unmaintained libraries, and license risks.
5. **Actionable 90-Day Engineering Remediation Roadmap**.

## 6. Step-by-Step Operating Procedure

### Step 1: Pre-flight & Topology Mapping
- Run depth-limited directory discovery avoiding `node_modules`, `.git`, `venv`, `target`, `dist`:
  ```bash
  git status -s
  git log -n 5 --oneline
  find . -maxdepth 3 -not -path '*/.*' -type d
  ```

### Step 2: Manifest & Dependency Extraction
- Inspect manifests to identify frameworks, runtime targets, and backing services:
  ```bash
  ls -la package.json pyproject.toml Cargo.toml go.mod pom.xml 2>/dev/null
  ```

### Step 3: Architecture & Boundary Tracing
- Map separation of concerns across API routes, controllers, business services, data models, and database access layers.

### Step 4: Security, Vulnerability & Supply Chain Scan
- Audit known CVEs, outdated packages, and license risks:
  ```bash
  npm audit --json 2>/dev/null || pip-audit 2>/dev/null || cargo audit 2>/dev/null || true
  ```
- Scan for hardcoded credentials and high-entropy secrets using ripgrep.

### Step 5: Code Quality & Test Coverage Assessment
- Check test harness presence, coverage metrics, and flaky test risks.
- Search for dead code, unhandled exceptions, and unmaintained legacy shims.

### Step 6: Synthesis & Remediation Ledger Delivery
- Compile findings into a structured markdown report with visual architecture diagrams and the phased P0–P3 remediation ledger.

## 7. Repository Inspection & Preservation Rules
- **Non-destructive execution ONLY**: Never modify, delete, or commit code files during an audit pass.
- **Redaction Rule**: Never print plaintext API keys, passwords, or secrets into logs or generated audit documents.

## 8. Verification & Testing Requirements
- Confirm that every identified architecture layer maps to an actual directory in the repository.
- Verify that reported dependency versions match the checked-in lockfiles.
- Ensure all findings cite exact file paths and line numbers:
  ```bash
  rg -n "issue_pattern" path/to/file
  ```

## 9. Relevant Official References
- ISO/IEC 25010: Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE).
- SEI CERT Coding Standards & Software Architecture in Practice (Clements, Bass, Kazman).
- OpenSSF Best Practices for Open Source Security.

## 10. Maintenance & Compatibility Notes
- Last audited: October 2026. Aligned with Antigravity 2.x and multi-language environments.
