# DeepSeek SuperAgent: Execution Workflow

This guide details the operational phases an agent follows when executing software engineering tasks under the `deepseek-superagent` skill.

---

## Phase 1: Intake, Triage & Mandate Formulation

1. **Trigger Intake**:
   - Ingest user task or issue description.
   - Determine whether the request is **Explicit** (user initiated directly) or **Inferred** (system/CI health trigger).
2. **Repository Discovery**:
   - Inspect workspace root for project guidelines: `AGENTS.md`, `CONTRIBUTING.md`, `README.md`.
   - Read build definitions (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.).
   - Confirm active branch and git status.
3. **Mandate Formulation**:
   - Define task scope boundaries: files eligible for modification, target functionality, and explicit non-goals.
   - Formulate single-sentence confirmation: *"Acknowledged: Implementing `<feature_or_fix>` in `<component>` with automated verification."*

---

## Phase 2: Isolated Execution Preparation

1. **Isolation Strategy**:
   - In Antigravity, invoke a worker subagent with isolated context (`invoke_subagent` with `Workspace: 'branch'` or `'share'`), or establish a clean git working branch.
   - Ensure the worker operates with a dedicated working directory or bounded scope to avoid collateral drift.
2. **Context Delivery**:
   - Pass the exact mandate, relevant file paths, test commands, and constraints to the worker subagent.
   - Include any known error logs or issue descriptions.

---

## Phase 3: Investigation & Surgical Implementation

1. **Context Tracing**:
   - Read relevant source code, type definitions, and test fixtures.
   - Search references using grep or codebase symbols rather than broad scans.
2. **Hypothesis Formulation**:
   - Formulate the minimal set of code modifications needed to fulfill the mandate.
   - Ensure zero collateral refactoring or formatting modifications in unrelated files.
3. **Implementation**:
   - Apply surgical edits using targeted replacement tools.
   - Maintain existing coding conventions, comments, and docstrings.

---

## Phase 4: Local Verification Loop

1. **Build & Typecheck**:
   - Run local type checks (e.g., `tsc --noEmit`, `mypy`, `cargo check`).
   - If typecheck fails, diagnose and fix within the worker session without notifying the user unless blocked.
2. **Unit & Regression Testing**:
   - Execute existing test suites covering the modified module.
   - Author a new test case specifically exercising the new functionality or bug fix.
   - Run tests and capture deterministic pass/fail results.
3. **Diff Self-Review**:
   - Review git diff (`git diff`) before declaring readiness.
   - Verify:
     - No stray debug statements or print statements left behind.
     - No credentials or sensitive data introduced.
     - No unintended whitespace or formatting disruptions.

---

## Phase 5: Checkpoints & Structured Reporting

1. **Safety Checkpoint Evaluation**:
   - Evaluate whether any proposed action triggers the Mandatory Human Approval list (see [references/safety-and-authorization.md](./safety-and-authorization.md)).
   - If triggered, pause and prompt the user with a single, clear question.
2. **Status Reporting**:
   - **`ready`**: Code fully implemented, tests passing, diff clean, deliverable prepared.
   - **`blocked`**: Hard blocker encountered (e.g., missing API key, unresolvable architecture ambiguity). Provide the exact blocker and single actionable question.
   - **`failed`**: Repeated verification failures after bounded retries. Provide failure summary and attempted remedies.
   - **`dropped`**: Task deemed unnecessary (e.g., already solved, cannot reproduce, or violates mandate). Provide 1-sentence rationale.
3. **Delivery**:
   - Commit changes with conventional commit format.
   - Prepare pull request or deliver final code artifacts with test verification evidence.
