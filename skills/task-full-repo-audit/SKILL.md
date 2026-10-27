---
name: task-full-repo-audit
description: Execute a complete 360-degree repository audit covering architecture, code hygiene, security vulnerabilities, test coverage, outdated dependencies, and technical debt with an actionable remediation ledger. [Consolidated Master Skill: repo-audit]
---

# Task Workflow: Full Repository 360-Degree Audit

> [!NOTE]
> **Consolidated Master Workflow**: This skill has been consolidated into [repo-audit](../repo-audit/SKILL.md). All 360-degree codebase audit workflows, architecture reconstruction, and prioritized remediation ledger generation are executed through the master `repo-audit` engine.

## Supported Invocations
- `/task-full-repo-audit` (Maintained for full backward compatibility)
- `/repo-audit` (Direct Master Skill invocation)

## Core Capabilities Executed
When invoked via `/task-full-repo-audit`, Antigravity activates the unified master audit workflow defined in [repo-audit](../repo-audit/SKILL.md):
1. **Architectural & Topology Mapping**: Entry points, module boundaries, and Mermaid component diagrams.
2. **Dependency & Supply Chain Analysis**: Outdated packages, transitive CVEs, and license risks.
3. **Security & Vulnerability Scanning**: Hardcoded secrets, unauthenticated endpoints, and injection sinks.
4. **Code Quality & Test Coverage Assessment**: Test ratio, dead code, and complexity hotspots.
5. **Prioritized P0–P3 Remediation Ledger**: Immediate blockers through low-priority hygiene items.
6. **Phased 90-Day Engineering Remediation Roadmap**.

Please refer to [repo-audit/SKILL.md](../repo-audit/SKILL.md) for full execution steps and verification gates.
