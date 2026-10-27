---
name: frontend-web-interface-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices". [Consolidated Master Skill: design-audit]
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# Web Interface Guidelines & Craft Compliance

> [!NOTE]
> **Consolidated Master Workflow**: This skill has been consolidated into [design-audit](../design-audit/SKILL.md). All automated Vercel Web Interface Guidelines fetching, WCAG 2.2 AA/AAA accessibility checks, Core Web Vitals audits, and component consistency verifications are executed through the master `design-audit` engine.

## Supported Invocations
- `/frontend-web-interface-guidelines` (Maintained for full backward compatibility)
- `/design-audit` (Direct Master Skill invocation)
- `/wcag`, `/accessibility` (Related compliance aliases)

## Core Capabilities Executed
When invoked via `/frontend-web-interface-guidelines`, Antigravity activates the unified audit protocol defined in [design-audit](../design-audit/SKILL.md):
1. **Dynamic Guidelines Retrieval**: Fetches the latest rules from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`.
2. **File & Pattern Inspection**: Audits target files against typography scaling, interactive feedback, and responsive layout rules.
3. **Structured `file:line` Diagnostics**: Reports findings as a prioritized severity table (Critical, Warning, Polish) with precise code line locations.
4. **Comprehensive Craft Defense**: Verifies touch target dimensions, focus-visible outlines, and layout shift prevention.

Please refer to [design-audit/SKILL.md](../design-audit/SKILL.md) for full execution steps and verification gates.
