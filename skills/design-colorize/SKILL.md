---
name: design-colorize
description: Audit and optimize color palettes, semantic token relationships, dark mode parity, and WCAG contrast. Use when refining branding, adjusting color mood, or fixing low-contrast text.
---

# Design Colorize & Palette Architecture

Harmonize color palettes into an accessible, semantic, tokenized color architecture with first-class dark mode parity and strict WCAG contrast compliance.

## 1. Intended Role & Activation Criteria

Use this skill when:
- Establishing or refining brand color palettes and UI theme colors.
- Auditing and fixing low-contrast text, borders, and interactive elements.
- Building dark mode parity with tailored surface elevation rather than naive color inversion.
- Replacing scattered raw hex codes with a clean semantic token structure.

Do **not** use for:
- Initial project scaffold -> use `/design-init`
- Typographic scale adjustments -> use `/design-typeset`
- Code-level accessibility compliance report -> use `/design-audit`

## 2. Inputs Required

- Existing color declarations (CSS variables, Tailwind colors, theme files).
- Brand identity or primary seed colors.
- Target theme modes (light mode, dark mode, high contrast).

## 3. Systematic Color Architecture Workflow

### Step 1 - Curated Palette Discovery
Query the curated color intelligence database:
```bash
python "$HOME/.gemini/config/skills/frontend-ui-ux-intelligence/scripts/search.py" "<keywords>" --domain color
```

### Step 2 - Three-Tier Token Hierarchy
1. **Primitive Scales (Global Tints)**:
   - `blue-50`: `#eff6ff`, ..., `blue-500`: `#3b82f6`, ..., `blue-900`: `#1e3a8a`.
   - `slate-50`: `#f8fafc`, ..., `slate-900`: `#0f172a`.
2. **Semantic Tokens (Functional Purpose)**:
   - `--bg-canvas`: Default page background.
   - `--bg-surface`: Card and component background.
   - `--text-primary`: High-contrast body and heading copy.
   - `--text-secondary`: Supporting context copy.
   - `--border-subtle`: 1px surface dividers.
   - `--brand-primary`: Main call-to-action color.
3. **Component Tokens (Element Specific)**:
   - `--button-primary-bg: var(--brand-primary)`

### Step 3 - Dark Mode Parity Architecture
Dark mode must be crafted as a distinct aesthetic space:
- **Avoid Pure Pitch Black (`#000000`)**: Use deep tinted neutrals (e.g., `#090d16` or `#0f172a`) to reduce eye strain and allow room for darker shadows.
- **Surface Elevation Hierarchy**:
  - Base Canvas: `hsl(222, 47%, 6%)`
  - Raised Card (Level 1): `hsl(222, 47%, 10%)`
  - Hover Surface (Level 2): `hsl(222, 47%, 14%)`
  - Modal / Overlay (Level 3): `hsl(222, 47%, 18%)`
- **Desaturate Vibrant Accents**: Reduce color saturation by 10-15% in dark mode to prevent chromatic aberration and visual glare.

### Step 4 - WCAG 2.2 Contrast Verification
Verify contrast mathematically before finalizing tokens:
- Primary text against surface: >= 7:1 (AAA) or >= 4.5:1 (AA).
- Secondary / helper text: >= 4.5:1 (AA).
- Non-text interactive boundaries and icons: >= 3:1.

## 4. Verification Output
- Semantic token CSS snippet ready for insertion.
- Light and Dark mode side-by-side contrast ledger.
- Zero raw hex codes remaining in component markup.

## 5. Cross-References
- `/design-init`: Initial design system creation.
- `/design-audit`: Automated accessibility audits.
- `/frontend-ui-ux-intelligence`: Product palette search engine.
