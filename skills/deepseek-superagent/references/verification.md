# DeepSeek SuperAgent: Verification Reference

This document outlines the testing, verification, and audit standards required before any deliverable is classified as `ready`.

---

## 1. Verification Hierarchy

Every code change must pass through a 4-tier verification ladder:

```
[ Tier 4: Diff & Cleanliness Audit ]   <-- Final gate
                 ^
[ Tier 3: New Feature / Fix Tests  ]   <-- Specific regression coverage
                 ^
[ Tier 2: Existing Regression Suite ]  <-- No broken existing behavior
                 ^
[ Tier 1: Static Analysis & Types  ]   <-- Clean compile, typecheck, lint
```

### Tier 1: Static Analysis & Type Safety
- **TypeScript / JavaScript**: `tsc --noEmit` or `npm run typecheck`
- **Python**: `mypy --strict <module>` or `pyright`
- **Rust**: `cargo check --all-targets`
- **Go**: `go vet ./...`
- **Linting**: Ensure code adheres to project linter without introducing new suppressions or warnings.

### Tier 2: Existing Regression Suite
- Run the repository's standard automated test suite for the affected package or module.
- All pre-existing tests must pass without regressions.

### Tier 3: Targeted Feature & Bugfix Tests
- For bugfixes: Author a minimal, reproducing unit test that fails without the fix and passes with it.
- For new features: Author comprehensive unit/integration tests exercising:
  - Happy path with realistic data inputs.
  - Boundary conditions (empty inputs, zero values, extreme bounds).
  - Error handling (network timeout, invalid payload, unauthorized access).

### Tier 4: Diff Cleanliness & Zero-Collateral Audit
- Inspect `git diff` against the base branch:
  - **No stray debugging code**: Remove console logs, print statements, debug flags.
  - **No unintended churn**: Verify no unrelated file formatting, imports reordering, or whitespace changes.
  - **Documentation integrity**: Ensure comments and docstrings match the new code behavior.

---

## 2. Verification Reporting Template

When declaring completion, the agent reports verification results using this schema:

```markdown
### Verification Summary

- **Typecheck**: PASSED (`tsc --noEmit`, 0 errors)
- **Unit Tests**: PASSED (42 passing, 0 failing)
- **New Test Added**: `tests/feature_test.ts::test_handles_edge_case` (PASSED)
- **Diff Audit**: Clean (1 file changed, 14 insertions, 2 deletions)
- **Safety Gate**: No destructive actions performed; no credentials touched.
```
