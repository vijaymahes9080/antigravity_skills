---
name: design-systems-engineer
description: Architect, implement, and maintain scalable design systems, semantic design tokens (CSS custom properties), atomic components, theme engines (dark mode parity), and Storybook documentation.
---

# Design Systems Engineering & UI Architecture

## 1. Intended Role & Domain
- **Primary Domain**: UI/UX & Design Engineering
- **Target Roles**: Design Systems Engineer, UI/UX Designer, Senior Frontend Architect
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "design system", "design tokens", "component library", "theme engine", "dark mode parity", "storybook", "ui tokens".
- **Contextual Inferences**: Establishing design consistency across multiple frontend applications, refactoring ad-hoc CSS into systematic tokens.
- **Chained Predecessors**: `task-decomposition`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Backend CLI or database engine tasks with no user interface.
  - Quick throwaway prototypes with strict instructions to ignore design consistency.

## 4. Required Inputs & Context
- Brand palette, typography specifications, and spacing rhythm (e.g. 4px/8px grid).
- Target frontend stack (React, Vue, Svelte, or Vanilla Web Components).
- Visual assets, icon set, and responsive breakpoints.

## 5. Expected Outputs & Artifacts
- Semantic Design Token system (`tokens.css` with CSS custom properties).
- Primitive and composite atomic UI components (Button, Modal, Input, Card, Badge).
- Full dark/light mode theme engine with WCAG contrast parity.
- Component catalog and Storybook stories.

## 6. Step-by-Step Operating Procedure
1. **Token Hierarchy Architecture**:
   - Level 1: Global/Base tokens (`--color-blue-500: #3b82f6`).
   - Level 2: Semantic tokens (`--color-primary: var(--color-blue-500)`).
   - Level 3: Component tokens (`--btn-bg: var(--color-primary)`).
2. **Typography & Spatial Scale Definition**:
   - Establish fluid modular type scale using `clamp()` and mathematical spacing multipliers (`--space-1: 0.25rem`, `--space-2: 0.5rem`, `--space-4: 1rem`).
3. **Atomic Component Implementation**:
   - Build accessible components with strict variants (primary, secondary, destructive, ghost).
   - Enforce distinct interactive states: `hover`, `active`, `focus-visible`, `disabled`, and `loading`.
4. **Theme Engine & Contrast Parity**:
   - Define dark theme tokens matching or exceeding WCAG AA (4.5:1 for body, 3:1 for large text).
5. **Documentation & Visual Catalog**:
   - Document component API props, slots, and interactive states.

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection of styling architecture:
  ```bash
  find . -name "*token*.css" -o -name "tailwind.config.*" 2>/dev/null
  ```
- Preservation rule: Never hardcode hex color codes directly into component markup; always reference semantic token variables.

## 8. Tool & Dependency Requirements
- CSS3 Custom Properties, Modern CSS (Grid/Flexbox), Storybook (optional), PostCSS / CSS Modules.

## 9. Implementation Guidelines & Best Practices
- Always style `:focus-visible` to provide clear keyboard focus rings (`outline: 2px solid var(--focus-ring); outline-offset: 2px`).
- Use CSS variables at the root level for dynamic theme switching without page reloads:

```css
:root {
  --color-bg-canvas: #ffffff;
  --color-text-primary: #0f172a;
  --color-accent: #2563eb;
  --color-border: #e2e8f0;
  --radius-md: 0.5rem;
  --space-4: 1rem;
}

[data-theme='dark'] {
  --color-bg-canvas: #090d16;
  --color-text-primary: #f8fafc;
  --color-accent: #3b82f6;
  --color-border: #1e293b;
}

.btn-primary {
  background: var(--color-accent);
  color: #ffffff;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  border: 1px solid transparent;
  transition: background 150ms ease, transform 100ms ease;
}

.btn-primary:hover:not(:disabled) {
  filter: brightness(1.1);
}

.btn-primary:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}
```

## 10. Error Handling & Recovery Procedures
- Missing token fallback: Always provide fallback values in CSS variable references: `var(--color-accent, #0066cc)`.
- Flash of unstyled theme (FOUT): Inject minimal theme resolution script synchronously in HTML `<head>` before body render.

## 11. Security & Privacy Constraints
- Prevent CSS injection: Sanitize user-customized theme values before injecting into style tags.

## 12. Verification & Testing Requirements
- Verify WCAG contrast compliance:
  - Run automated color contrast check across all token combinations.
- Visual regression verification: Confirm component rendering across all defined breakpoints (mobile, tablet, desktop).

## 13. Completion Criteria
- Complete token dictionary established (Colors, Spacing, Typography, Radii, Shadows).
- Full dark mode parity verified without illegible text.
- Core component library functions with accessible keyboard navigation.

## 14. Relevant Official References
- W3C Design Tokens Community Group Specification.
- Brad Frost's Atomic Design Methodology.
- Radix UI & Shadcn Design System Architecture.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with modern CSS standards and evergreen browsers.

## 16. Cross-References & Related Workflows
- design-init: Establish initial design tokens, typography, and foundational system before building component libraries.
- design-memory: Read and persist durable project-specific design tokens and decisions in design-system.md.
- design-audit: Validate token compliance and accessibility of built components.
