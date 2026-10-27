---
name: design-critique
description: Aesthetic and ergonomic critique of an interface - visual hierarchy, spacing rhythm, color mood, typography, motion, and cognitive load. Use to identify why a UI feels clumsy, generic, or visually cluttered, and to eliminate AI-generated anti-patterns.
---

# Design Critique & Aesthetic Evaluation

Provide a structured aesthetic and ergonomic critique. Articulate *why* a design feels unbalanced or template-generated and prescribe concrete, actionable visual improvements.

## 1. Intended Role & Activation Criteria

Use this skill when:
- An interface is functionally working but looks amateurish, generic, or AI-generated.
- Evaluating visual hierarchy, spacing rhythms, font balance, or color harmony.
- Eliminating common UI anti-patterns (purple-indigo gradients, equal-weight icon grids, unstyled cards).

Do **not** use for:
- Code compliance audits (WCAG, HTML semantics) -> use `/design-audit`
- Pre-merge holistic release gate -> use `/design-review`
- Applying surgical CSS code micro-fixes -> use `/design-polish`

## 2. Inputs Required

- Screenshot, visual mockups, or source code for the component/screen.
- Target audience and product persona (e.g., enterprise B2B SaaS, developer tool, luxury consumer, fintech).
- Project branding constraints (brand palette, typography guidelines).

## 3. Six-Dimensional Critique Matrix

### 1. Visual Hierarchy & Focal Clarity
- **Primary Anchor**: Is there exactly one primary visual anchor per viewport?
- **Weight Distribution**: Do secondary and tertiary elements defer visually to the primary call-to-action?
- **Scanning Rhythm**: Does the layout support natural F-pattern or Z-pattern eye tracking without disorientation?

### 2. Spacing Rhythm & Spatial Geometry
- **Consistent Grid Multiplier**: Are spacing increments strictly based on an intentional scale (4px/8px base)?
- **Optical vs Mathematical Alignment**: Are asymmetrical icons and centered headings optically balanced rather than mechanically centered?
- **Proximity Grouping**: Are related elements grouped tightly with generous whitespace separating distinct sections (Gestalt law of proximity)?

### 3. Color Harmony & Emotional Register
- **Intentional Mood**: Does the palette establish the right emotional tone rather than defaulting to generic blue/purple palettes?
- **Accent Restraint**: Is the accent color restricted to interactive focal points (max 1 dominant accent, 1 semantic accent active)?
- **Surface Depth**: Are surfaces elevated using lightness steps and subtle borders rather than heavy drop shadows?

### 4. Typography & Information Hierarchy
- **Type Scale**: Is there an expressive, intentional contrast between Display/Heading and Body text?
- **Font Ergonomics**: Are line-heights calibrated comfortably (1.4-1.6 for body, 1.1-1.2 for headings)?
- **Weight Meaning**: Are font weights used semantically (e.g., regular for body, medium for labels, bold for critical numbers)?

### 5. Motion, Physics & Feedback
- **Purposeful Transitions**: Do transitions communicate spatial continuity and state changes rather than purely decorative motion?
- **Natural Durations**: Micro-interactions timed at 150-250ms with easing curves (`cubic-bezier(0.16, 1, 0.3, 1)`); avoid sluggish 500ms animations.

### 6. Cognitive Load & Progressive Disclosure
- **Information Density**: Is the screen overwhelming the user with simultaneous inputs?
- **Progressive Disclosure**: Are advanced options tucked into contextual disclosures, drawers, or secondary tabs?

## 4. AI-Generated Anti-Pattern Catalog

| AI Anti-Pattern | Craft Replacement |
|---|---|
| **Purple/Indigo Gradient Hero** | Solid high-contrast surface with crisp typographic hierarchy or architectural grid |
| **8-Card Equal Weight Feature Grid** | Asymmetrical bento grid highlighting 1-2 flagship features with supporting telemetry |
| **Heavy Drop Shadows on White Cards** | 1px border (`border: 1px solid rgba(0,0,0,0.08)`) with minimal 2px soft blur |
| **Indiscriminate Glassmorphism** | Crisp solid surfaces; reserve backdrop blur exclusively for floating navigation and modal backdrops |
| **Generic Stock Vector Graphics** | Real product screenshots, interactive telemetry widgets, or clean typographic focal points |

## 5. Before / After Structured Prescription

Deliver every critique recommendation with clear contrast:

```markdown
### Critique Item: [Dimension Name] - [Issue Summary]
- **Current State (Before)**: Generic centered card with `#6366f1` gradient and equal-weight action buttons.
- **Root Diagnosis**: Lacks visual hierarchy, looks template-produced, confuses primary vs secondary intent.
- **Elevated Prescription (After)**: Flat neutral background `#0f172a`, bold left-aligned heading with `font-feature-settings: "cv02"`, solid primary button `#3b82f6`, ghost secondary button with subtle border.
```

## 6. Output Summary Format
- **Critical Visual Deficiencies**: Violations of hierarchy or branding that harm credibility.
- **Moderate Enhancements**: Layout, typography, and contrast refinements.
- **High-Craft Polish Suggestions**: Micro-spacings, optical nudges, and subtle depth layers.

## 7. Cross-References & Related Skills
- `/design-audit`: Objective WCAG and responsive compliance.
- `/design-polish`: Direct execution of surgical micro-adjustments.
- `/frontend-ui-ux-intelligence`: Query curated product palettes and typography combinations.
- `/design-prototype`: Explore alternative visual directions.
