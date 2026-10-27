---
name: task-surgical-bugfix
description: Fix a specific software bug with minimal, targeted changes without any collateral refactoring, unintended behavioral modifications, or stylistic disruption. [Consolidated Master Skill: root-cause-debugging]
---

# Task Workflow: Surgical Bugfix Without Collateral Changes

> [!NOTE]
> **Consolidated Master Workflow**: This skill has been consolidated into [root-cause-debugging](../root-cause-debugging/SKILL.md). All surgical bugfix discipline, causal hypothesis isolation, minimal diff guarantees, and regression testing rules are executed through the master `root-cause-debugging` engine.

## Supported Invocations
- `/task-surgical-bugfix` (Maintained for full backward compatibility)
- `/root-cause-debugging` (Direct Master Skill invocation)
- `/debug` (Common alias)

## Core Capabilities Executed
When invoked via `/task-surgical-bugfix`, Antigravity activates the unified master debugging workflow defined in [root-cause-debugging](../root-cause-debugging/SKILL.md):
1. **Scope Lockdown & Baseline Verification**: Reproduce the defect before editing any files.
2. **Collateral Boundary Demarcation**: Strict prohibition of formatting changes, renames, or unrelated edits.
3. **Surgical Patch Application**: Targeted root-cause resolution with minimum lines altered.
4. **Reproducing Regression Test Creation**: Dedicated test guarding the defect.
5. **Diff Audit & Suite Verification**: `git diff --stat` inspection and full test suite verification.

Please refer to [root-cause-debugging/SKILL.md](../root-cause-debugging/SKILL.md) for full execution steps and verification gates.
