---
name: root-cause-debugging
description: Systematic hypothesis-driven root-cause debugging, AST-level trace analysis, minimal surgical patching, zero-collateral-edits enforcement, and regression test verification.
---

# Master Root-Cause Debugging & Surgical Bugfix Engineering

## 1. Intended Role & Domain
- **Primary Domain**: Software Engineering, Reliability & Maintenance
- **Target Roles**: Senior Software Engineer, Site Reliability Engineer (SRE), Bugfix Specialist, QA Automation Engineer
- **Architectural Layer**: Layer 1 (Core Engineering Standards & Defensive Patching)
- **Supported Invocations**: `/root-cause-debugging`, `/task-surgical-bugfix`, `/debug`

## 2. Activation Conditions
- **Direct Triggers**: "debug error", "fix stack trace", "investigate exception", "find root cause", "troubleshoot crash", "surgical bugfix", "fix this bug without touching anything else", "minimal diff bugfix", "isolated patch".
- **Contextual Inferences**: Failed unit test outputs, unhandled runtime crashes, production error logs, regression investigations.
- **Chained Predecessors**: `repo-audit` or direct issue report.

## 3. Explicit Exclusions
- Do NOT use when:
  - User is designing greenfield features without existing code or bugs.
  - User explicitly requests broad refactoring or architectural redesign alongside the bugfix.

## 4. Required Inputs & Context
- Stack trace, crash log, or reproducing test case.
- Source code files involved in the execution stack.
- Expected behavior vs actual erroneous behavior.
- Language test runner (`pytest`, `npm test`, `cargo test`, `go test`).

## 5. Expected Outputs & Artifacts
1. **Root-Cause Explanation**: Causal chain analysis articulating why the defect occurred.
2. **Reproducing Test Case**: Minimal isolated test demonstrating the failure prior to patch application.
3. **Minimal Surgical Patch**: Focused Git diff containing strictly the lines necessary to resolve root cause.
4. **Verification Report**: Test execution proving zero regressions across the broader test suite.

## 6. Step-by-Step Operating Procedure

### Step 1: Baseline Lockdown & Reproduction
- Establish baseline by running the existing test runner.
- Create or execute an isolated minimal reproducer proving the defect exists:
  ```bash
  # Run focused test
  npm test -- -t "offending test case" || pytest tests/test_offending.py -v
  ```

### Step 2: Causal Mechanism & Git History Tracing
- Inspect variable states, async event ordering, null/undefined propagation, or boundary conditions.
- Trace author intent via Git blame and commit history:
  ```bash
  git log -S "offendingFunction" -p -n 3
  git blame -L 120,140 path/to/file
  ```

### Step 3: Falsifiable Hypothesis Formulation
- Explicitly state: *"The error occurs because condition X causes variable Y to be uninitialized or out of bounds during event Z."*

### Step 4: Surgical Boundary Demarcation & Patch Application
- Apply the targeted logical fix with **zero collateral edits**:
  - Do NOT reformat untouched lines.
  - Do NOT rename unrelated variables.
  - Do NOT modify unrelated comments or docstrings.
  - Fix the root problem (e.g. correct state transition), never swallow errors with defensive empty `catch` blocks.

```python
# Before (buggy: off-by-one on boundary condition)
def get_latest_item(items: list):
    return items[len(items)]  # IndexError

# After (surgical fix: bounds check and correct index, identical signature)
def get_latest_item(items: list):
    return items[-1] if items else None
```

### Step 5: Diff Audit & Regression Verification
- Audit diff surface area:
  ```bash
  git diff --stat
  git diff --shortstat
  ```
- Run the focused reproducer test (must turn GREEN).
- Run the complete project test suite to guarantee 100% zero side effects:
  ```bash
  pytest || npm test || cargo test
  ```

## 7. Preservation Rules & Collateral Protection
- **Smallest Viable Diff**: If a 2-line fix solves the root cause, do not edit 50 lines.
- **Contract Freezing**: Preserve all existing public API signatures, parameters, and return types.

## 8. Verification & Testing Requirements
- Confirm bug is reproduced before fixing.
- Confirm bug is resolved after fixing.
- 100% passing rate on previously working tests.

## 9. Relevant Official References
- Google Engineering Practices: "The Smallest CL".
- "Why Programs Fail: A Guide to Systematic Debugging" (Andreas Zeller).
- Working Effectively with Legacy Code (Michael Feathers).

## 10. Maintenance & Compatibility Notes
- Last audited: October 2026. Universal across Python, TypeScript/JavaScript, Go, Rust, Java, and C/C++.
