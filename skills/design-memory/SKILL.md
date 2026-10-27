---
name: design-memory
description: Read and persist durable project-specific design decisions into design-system.md. Use at the start of any UI task to retrieve decisions, and at the end of design tasks to record permanent choices.
---

# Design Memory & Decision Persistence

Maintain persistent, project-local design intelligence and architectural decisions. Ensure long-term design coherence across agent sessions by treating `design-system.md` at workspace root as the authoritative record.

## 1. Intended Role & Activation Criteria

Use this skill when:
- **At the start of any UI task**: Inspect and retrieve established project design decisions.
- **At the conclusion of design tasks**: Record durable decisions, token additions, and pattern conventions.
- Resolving ambiguity regarding project fonts, color tokens, spacing conventions, or responsive breakpoints.

Do **not** use for:
- Writing one-off temporary notes or debug logs.
- Storing API keys, credentials, or personal secrets (strict prohibition).

## 2. Structured `design-system.md` Schema

The design memory file must adhere to this structured format:

```markdown
# Design System - [Project Name]
_Last Updated: [ISO Date] | Architecture Version: 2.x_

## 1. Visual Direction & Archetype
- **Aesthetic Persona**: [e.g., Clean Data-Dense Developer Console with subtle dark elevation]
- **Target Audience**: [e.g., Cloud Infrastructure Engineers]

## 2. Semantic Color Token System
- Canvas Background: `--color-bg-canvas: #090d16`
- Surface Raised: `--color-surface: #111827`
- Primary Brand Accent: `--color-primary: #3b82f6`
- Text Primary: `--color-text-primary: #f9fafb`
- Status Colors: Error `#ef4444`, Warning `#f59e0b`, Success `#10b981`

## 3. Typography System
- Display Font: [Family, e.g., 'Inter', weights 600, 700]
- Body Font: [Family, e.g., 'Inter', weights 400, 500]
- Code / Monospace: [Family, e.g., 'JetBrains Mono']
- Scale Ratio: [e.g., Minor Third 1.200]

## 4. Spacing & Spatial Geometry
- Grid Multiplier: 4px / 8px base
- Border Radii: Sm 4px, Md 8px, Lg 12px, Full 9999px
- Elevation: Layered natural shadows with 1px semi-transparent borders

## 5. Component Patterns & Conventions
- Buttons: Primary, Secondary Ghost, Destructive with active tactile scaling
- Forms: Explicit labels, floating helper text, high-contrast focus rings
- Empty States: Actionable icon + description + primary action

## 6. Responsive Breakpoints
- Mobile: 320px - 480px
- Tablet: 768px - 1024px
- Desktop: 1280px+
```

## 3. Two-Way Memory Protocol

### Step 1 - Pre-Task Memory Retrieval
Before modifying any UI:
1. Search for `design-system.md` at workspace root or `.interface-design/system.md`.
2. Parse established tokens and layout rules.
3. Adhere strictly to retrieved parameters; do not invent conflicting colors or arbitrary fonts.

### Step 2 - Post-Task Memory Persistence
When durable design choices are introduced:
1. Update `design-system.md` with new token definitions.
2. Note the date and justification for any token additions.
3. Commit `design-system.md` alongside code changes.

## 4. Security & Isolation Boundaries
- NEVER store environment secrets, authentication credentials, or user PII in `design-system.md`.
- Keep memory strictly focused on design architecture, tokens, and UX patterns.

## 5. Cross-References
- `/design-init`: Create the initial `design-system.md` file.
- `/design-review`: Validate changes against design memory.
- `/design-systems-engineer`: Maintain code token implementations.
