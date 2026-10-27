---
name: design-polish
description: Apply surgical, high-craft refinements to spacing, borders, alignment, hover states, and micro-interactions without unrelated rewrites. Use when a UI is mostly complete but lacks premium finish.
---

# Design Polish & Micro-Craft Refinement

Elevate digital interfaces from "functional" to "crafted" through high-precision micro-adjustments in spacing, optical alignment, surface depth, interactive states, and transitions.

## 1. Intended Role & Activation Criteria

Use this skill when:
- A user interface is functionally complete but feels unpolished, clumsy, or unfinished.
- Applying surgical refinements to padding, borders, shadows, and hover animations.
- Fine-tuning micro-interactions without touching backend business logic or state flow.

Do **not** use for:
- Greenfield scaffolding -> use `/design-init`
- Broad architectural redesign -> use `/frontend-craft-design-engineering`
- Codebase compliance auditing -> use `/design-audit`

## 2. Inputs Required

- Target component files or screen markup (TSX, JSX, CSS, HTML).
- Existing styling context and semantic design tokens.
- Specific areas needing polish (e.g., card headers, button states, table rows).

## 3. Surgical Polish Taxonomy & Directives

### 1. Spacing Rhythm & Optical Alignment
- **Align to 4px/8px Multipliers**: Eliminate arbitrary padding values (e.g., replace `padding: 13px 19px` with `padding: 12px 20px`).
- **Optical Vertical Centering**: Adjust icon baselines with `translate-y-[-1px]` or flex alignments so text and icons feel centered to the eye.
- **Content Padding Hierarchy**: Ensure internal card padding (`p-6`) exceeds nested element spacing (`gap-3`) to maintain clear spatial containers.

### 2. Surface Depth & Border Definition
- **Semi-Transparent Borders**: Replace harsh solid borders with subtle alpha channels (`border: 1px solid rgba(255, 255, 255, 0.08)` in dark mode; `rgba(0, 0, 0, 0.08)` in light mode).
- **Layered Natural Shadows**:
  ```css
  box-shadow:
    0 1px 2px rgba(0, 0, 0, 0.05),
    0 4px 12px rgba(0, 0, 0, 0.08);
  ```
- **Crisp Inner Highlights**: Add subtle top border highlights (`box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1)`) on buttons and cards for depth.

### 3. Micro-Interactions & Motion Timing
- **Duration Rules**:
  - Color, opacity, background shifts: `150ms ease-out`
  - Scale and transform interactions: `180ms cubic-bezier(0.16, 1, 0.3, 1)`
  - Layout expansions and drawer reveals: `250ms - 300ms ease`
- **Tactile Active Feedback**: Give buttons and cards immediate press feedback:
  ```css
  button:active {
    transform: scale(0.98);
  }
  ```
- **Smooth Hover Lift**:
  ```css
  .card {
    transition: transform 200ms ease, box-shadow 200ms ease;
  }
  .card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
  ```

### 4. Zero Collateral Disruption Rule
- Never rename component props, callbacks, or `data-testid` test attributes.
- Preserve all existing state hooks (`useState`, `useReducer`, `useEffect`).
- Changes must be strictly stylistic and isolated.

## 4. Verification & Diff Delivery
- Provide clear before/after code diffs highlighting the surgical changes.
- Verify that interactive click targets continue firing without occlusion.
- Test keyboard navigation `:focus-visible` states remain prominent.

## 5. Cross-References
- `/design-critique`: Diagnostic review before polish.
- `/frontend-interaction-design-polish`: Deep dive into Emil Kowalski micro-interaction patterns.
- `/design-live`: Verifying polished styles in an active development browser.
