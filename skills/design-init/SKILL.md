---
name: design-init
description: Initialize and define an intentional visual direction for the active project - design tokens, typography, color system, spacing grid, and design-system.md foundation. Use when starting a new UI feature, establishing a design language, or onboarding a project to a cohesive design system.
---

# Design System Initialization & Architecture

Establish the visual foundation for a project. Produces a comprehensive, durable `design-system.md` and semantic token architecture that serves as the single source of truth for all `/design-*` workflows.

## 1. Intended Role & Activation Criteria

Use this skill when:
- Starting a new frontend web or mobile project with no established design language.
- Modernizing an existing codebase by introducing a centralized token system.
- Formalizing design decisions before building complex UI features.

Do **not** use for:
- Refining an existing palette -> use `/design-colorize`
- Modifying typography hierarchy -> use `/design-typeset`
- Daily persistence of incremental decisions -> use `/design-memory`

## 2. Inputs Required

- Project technology stack (React, Next.js, Vue, Svelte, Tailwind, Flutter, Vanilla CSS).
- Product archetype (B2B SaaS, developer tooling, consumer mobile, fintech, e-commerce, editorial).
- Brand attributes (core brand color, logo, desired emotional tone).

## 3. Initialization Workflow

### Step 1 - Stack & Environment Discovery
Inspect project structure to detect framework and CSS tooling:
```powershell
Get-ChildItem -Path . -Recurse -Depth 2 -Filter "package.json", "pubspec.yaml", "tailwind.config.*", "tokens.css"
```
Determine if a pre-existing `design-system.md` exists. If present, extend rather than overwrite.

### Step 2 - Style & Palette Querying
Query the `frontend-ui-ux-intelligence` engine for domain-tailored color palettes and font combinations:
```bash
python "$HOME/.gemini/config/skills/frontend-ui-ux-intelligence/scripts/search.py" "<product-keywords>" --domain style --stack <stack>
python "$HOME/.gemini/config/skills/frontend-ui-ux-intelligence/scripts/search.py" "<product-keywords>" --domain color
python "$HOME/.gemini/config/skills/frontend-ui-ux-intelligence/scripts/search.py" "<product-keywords>" --domain typography
```

### Step 3 - Establish Core Design Tokens
Define the complete semantic token hierarchy:

```css
:root {
  /* Surface & Canvas Tokens */
  --color-bg-canvas: #090d16;
  --color-surface-subtle: #111827;
  --color-surface-raised: #1f2937;
  --color-surface-overlay: #374151;

  /* Text & Foreground Tokens */
  --color-text-primary: #f9fafb;
  --color-text-secondary: #9ca3af;
  --color-text-muted: #6b7280;

  /* Brand & Interactive Tokens */
  --color-brand-primary: #3b82f6;
  --color-brand-hover: #2563eb;
  --color-brand-active: #1d4ed8;

  /* Semantic Feedback Tokens */
  --color-status-success: #10b981;
  --color-status-warning: #f59e0b;
  --color-status-error: #ef4444;
  --color-status-info: #06b6d4;

  /* Typography Scale */
  --font-family-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-family-mono: 'JetBrains Mono', monospace;
  --font-size-xs: 0.75rem;     /* 12px */
  --font-size-sm: 0.875rem;    /* 14px */
  --font-size-base: 1.0rem;    /* 16px */
  --font-size-lg: 1.125rem;    /* 18px */
  --font-size-xl: 1.25rem;     /* 20px */
  --font-size-2xl: 1.5rem;     /* 24px */
  --font-size-3xl: 1.875rem;   /* 30px */
  --font-size-4xl: 2.25rem;    /* 36px */

  /* Spacing Scale (4px / 8px Grid) */
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1.0rem;   /* 16px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2.0rem;   /* 32px */
  --space-12: 3.0rem;  /* 48px */

  /* Geometry & Elevation */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
```

### Step 4 - Generate Project `design-system.md`
Write the canonical `design-system.md` at workspace root detailing:
1. Product Archetype & Design Intent.
2. Semantic Color Token Ledger (Light & Dark mode specifications).
3. Typography System & Font Pairing Rules.
4. Spacing, Geometry & Radii.
5. Interactive State Conventions (Focus rings, hover transitions).
6. Accessibility Targets (WCAG 2.2 AA).

## 4. Verification & Output
- Generated `design-system.md` committed at workspace root.
- Tokens exported to CSS custom properties or framework theme config.
- Next Recommended Step: Use `/design-colorize` to calibrate dark mode parity or `/design-typeset` for typography tuning.

## 5. Cross-References
- `/design-memory`: Durable storage and maintenance of decisions.
- `/design-colorize`: Deep color palette optimization.
- `/design-typeset`: Typographic hierarchy and font pairing.
- `/design-systems-engineer`: Comprehensive component library implementation.
