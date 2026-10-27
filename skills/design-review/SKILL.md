---
name: design-review
description: Holistic pre-merge UI review covering design-system token compliance, cross-viewport consistency, edge-case stress testing, and sign-off gate. Use before merging UI changes or preparing for production deployment.
---

# Design Review & Pre-Merge Gate

Conduct a holistic pre-merge quality and consistency review for user interfaces. Ensure code changes preserve design-system tokens, behave gracefully across all viewports, and pass strict release criteria.

## 1. Intended Role & Activation Criteria

Use this skill when:
- A UI feature or redesign is complete and pending pull request approval or production merge.
- Verifying that code changes adhere to project design memory (`design-system.md`).
- Stress testing UI components under extreme viewport, localization, and data edge cases.

Do **not** use for:
- Initial aesthetic critique -> use `/design-critique`
- Code accessibility checklist -> use `/design-audit`
- Initial project setup -> use `/design-init`

## 2. Inputs Required

- Git diff or list of modified frontend components.
- Project design system documentation (`design-system.md`, `tokens.css`, or Tailwind config).
- Target device profiles and supported screen resolutions.

## 3. Four-Stage Review Protocol

### Stage 1 - Design Token & System Compliance
- **Color Token Enforcement**: Check that no raw hex/rgb values exist in markup or CSS files. All values must reference semantic tokens (`var(--color-primary)`, `var(--color-surface)`).
- **Spacing Scale Alignment**: Ensure paddings and margins utilize defined increments (4px/8px multiples).
- **Typography Scale Verification**: Headings and body copy must map directly to project scale tokens (`--font-size-lg`, `--font-size-base`).
- **Surface Elevation**: Verify that shadows, borders, and modal overlays adhere to the project's elevation hierarchy.

### Stage 2 - Cross-Viewport Matrix
Review each modified view across key breakpoints:

| Viewport Profile | Resolution | Verification Gate |
|---|---|---|
| **Mobile Narrow** | 320px - 375px | Zero horizontal scroll; touch targets >= 44px; collapsed navigation |
| **Mobile Standard** | 390px - 430px | Comfortable line length; thumb-zone reachability |
| **Tablet Portrait** | 768px - 834px | Multi-column layouts collapse or reflow gracefully |
| **Desktop Standard**| 1280px - 1440px | Balanced content container width (max-w-7xl); readable line lengths |
| **Ultra-Wide** | 1920px+ | Proper container centering; content does not stretch indefinitely |

### Stage 3 - Edge-Case & Stress Testing
Stress-test UI against boundary conditions:
- **String Length Extremes**: Extra-long usernames ("Alexandrina Montgomery-Westerfield"), zero-character empty fields, unbreakable strings.
- **Data Densities**: Empty state (0 records), single item, pagination boundary (10,000+ items).
- **Localization & Script Support**: Non-Latin glyphs, right-to-left layout direction, extended line heights for Indic scripts.
- **Network / Async Delays**: Slow network simulated skeleton states, error banners, idempotent retry actions.

### Stage 4 - Sign-Off Gate & Release Decision
Evaluate overall release readiness against criteria:
- [ ] No regression in accessibility or keyboard navigation.
- [ ] 100% token adherence with zero undeclared hex codes.
- [ ] Responsive layouts verified across all breakpoints.
- [ ] Visual hierarchy clear with unambiguous primary CTA.

## 4. Structured Review Report

```markdown
# UI Pre-Merge Review - [Feature Name]

## 1. Token Compliance: PASS / CONDITIONAL / FAIL
- Semantic Tokens: 100% compliant
- Hardcoded Values: 0 found

## 2. Cross-Viewport Matrix
- Mobile (320px): PASS (no overflow)
- Tablet (768px): PASS (graceful reflow)
- Desktop (1440px): PASS (centered container)

## 3. Edge-Case Findings
- Long text truncation: Verified with ellipsis and tooltip
- Empty states: Implemented with CTA button

## 4. Final Sign-Off Recommendation
- [APPROVED FOR MERGE] / [CHANGES REQUESTED]
```

## 5. Cross-References & Related Skills
- `/design-audit`: Specific WCAG 2.2 and Core Web Vitals checks.
- `/design-memory`: Update durable project design decisions post-merge.
- `/frontend-ui-edge-case-testing`: Deep data stress-testing.
