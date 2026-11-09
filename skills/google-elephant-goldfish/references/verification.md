# Elephant-Goldfish Model: Verification & Drift Detection Reference

This document outlines the protocols for validating implementation fidelity against approved specifications and detecting architectural drift.

---

## 1. Drift Detection Methodology

Over time, codebases evolve, leading to divergence between written designs and actual code. The drift detection protocol systematically uncovers:
1. **Missing Features**: Capabilities specified in the design doc but absent in the codebase.
2. **Incomplete Models**: Structs, classes, or database tables missing fields mandated by the specification.
3. **Logic Shortcuts**: Hardcoded mock values or stubbed implementations where dynamic logic was planned.
4. **Architectural Divergence**: Components using patterns, libraries, or protocols different from the approved specification.

---

## 2. Drift Audit Procedure

When requested to run drift detection on design specifications (e.g., in `docs/designs/`):

1. **Intake & Scope**:
   - Locate the target specification (`approved_specification.md` or `docs/designs/<feature>.md`).
2. **Entity & Contract Extraction**:
   - Extract all mentioned files, symbols, types, endpoints, and schema definitions from the specification.
3. **Codebase AST Inspection**:
   - Inspect the corresponding source files using `read_file` or symbol searches.
   - Compare field-by-field, method-by-method, and route-by-route.
4. **Drift Classification**:
   - **BLOCKER DRIFT**: Core architectural invariant violated (e.g., authentication check missing, synchronous call used instead of queue).
   - **STRUCTURAL DRIFT**: Data model mismatch (e.g., column named `user_id` instead of `account_id`, missing index).
   - **DOCUMENTATION DRIFT**: Code is correct and intentionally updated, but specification was not updated to reflect approved changes.
5. **Drift Report Output**:
   - Write the audit report to `{YYYY-MM-DD}_DRIFT_REPORT.md` adhering to the standard schema:

```markdown
# Architectural Drift Audit Report: [Target Specification]
Date: [YYYY-MM-DD]
Status: [Divergent | Synchronized]

## Summary of Findings
- Total Specifications Checked: X
- Drift Instances Found: Y
- Critical Discrepancies: Z

## Detailed Divergences

### 1. [Component / Symbol Name]
- **Documented Specification**: [Description or schema in spec]
- **Actual Implementation**: `[path/to/source.ts:L45-L60]`
- **Divergence Category**: [Missing Feature | Incomplete Model | Logic Shortcut | Architectural Divergence]
- **Recommended Remediation**: [Update code to match spec OR update spec via approved change]
```

---

## 3. Acceptance Verification Checklist

Before an implemented feature is signed off against its Elephant-Goldfish specification:
- [ ] Every acceptance criterion defined in Section 8 of the specification has a passing automated test.
- [ ] No blocker or major drift remains between code AST and the document.
- [ ] All Goldfish review findings have recorded resolutions (Accepted, Contested, or Alternated) signed off by the author.
