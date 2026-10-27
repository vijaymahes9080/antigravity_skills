---
name: design-audit
description: Exhaustive UI code audit covering WCAG accessibility, responsive resilience, state completeness, Web Interface Guidelines (Vercel), performance (CLS/LCP/INP), and component consistency. Use when auditing existing screens, preparing a release, or reviewing UI code against best practices.
---

# Design Audit & Compliance Verification

Perform an exhaustive, objective audit of UI components and pages against modern craft and accessibility standards. Return findings as a prioritized severity table.

## 1. Intended Role & Activation Criteria

Use this skill when:
- Auditing existing UI code before a release, pull request merge, or production deployment.
- Reviewing an application screen against accessibility (WCAG 2.2 AA/AAA), performance, and design-system standards.
- A user asks to "review my UI", "check accessibility", "audit design", or "check against best practices".

Do **not** use for:
- Aesthetic / stylistic critique -> use `/design-critique`
- Live browser inspection of a running dev server -> use `/design-live`
- Pre-merge holistic sign-off across features -> use `/design-review`
- Surgical pixel-level polish and micro-interactions -> use `/design-polish`

## 2. Inputs Required

- Target files, components, or URL pattern to audit.
- Framework context (React, Next.js, Vue, Svelte, Flutter, Vanilla HTML/CSS).
- Project design memory (`design-system.md` or token files) for token compliance checking.

## 3. Comprehensive Audit Workflow

### Step 1 - Accessibility (WCAG 2.2 AA/AAA Compliance)
- **Color Contrast Ratios**:
  - Normal text (<18pt or <14pt bold): minimum 4.5:1 against its background.
  - Large text (>=18pt or >=14pt bold): minimum 3.0:1.
  - UI components, active borders, and icons: minimum 3.0:1.
- **Semantic HTML & Landmarks**:
  - Enforce correct semantic elements: `<main>`, `<nav>`, `<header>`, `<footer>`, `<aside>`, `<button>`, `<article>`.
  - Avoid `div` clickable elements; if required, ensure `role="button"`, `tabindex="0"`, and keydown handlers.
- **ARIA & Accessibility Tree**:
  - Verify `aria-label`, `aria-labelledby`, and `aria-describedby` on icon-only buttons and complex controls.
  - Dynamic content regions must use `aria-live="polite"` or `aria-live="assertive"`.
- **Focus Rings & Keyboard Navigation**:
  - Confirm high-contrast visible focus rings using `:focus-visible` (never `outline: none` without replacement).
  - Verify complete keyboard journey: Tab, Shift+Tab, Enter, Space, Escape without keyboard traps.
- **Touch Targets & Media**:
  - Minimum touch target: 44x44px for web, 48x48dp for mobile.
  - All visual `<img>` elements must have descriptive `alt` attributes; decorative images must specify `alt="" aria-hidden="true"`.

### Step 2 - Responsive Resilience & Layout Defense
- **Breakpoint Verification**:
  - Mobile portrait: 320px - 480px
  - Mobile landscape / small tablet: 481px - 767px
  - Tablet / small laptop: 768px - 1024px
  - Standard desktop: 1025px - 1440px
  - Ultra-wide: 1441px+
- **Layout Robustness**:
  - Enforce no horizontal scrolling at 320px minimum width.
  - Check text container overflow: utilize CSS `overflow-wrap: break-word` or `text-overflow: ellipsis` where truncation is intended.
  - Verify sticky headers, modal dialogs, and slide-out drawers across all viewports.

### Step 3 - Interactive State Completeness Matrix
Every interactive component must implement distinct visual styling for all required states:

| State | Elements Required | Verification Criteria |
|---|---|---|
| **Default** | All components | Clear visual hierarchy and contrast against surface |
| **Hover** | Desktop interactive elements | Subtle elevation, background tint, or border shift (150ms ease) |
| **Active / Pressed** | Buttons, list rows | Tactile feedback (e.g., `transform: scale(0.98)` or darker surface) |
| **Focus-Visible** | All keyboard interactives | 2px solid ring with 2px offset; never suppressed |
| **Disabled** | Unavailable controls | `opacity: 0.5-0.6`, `cursor: not-allowed`, `aria-disabled="true"` |
| **Loading / Skeleton** | Async content surfaces | Pulse or shimmer animation maintaining exact layout dimensions |
| **Empty** | Tables, feeds, search results | Helpful guidance, descriptive graphic/icon, primary call-to-action |
| **Error** | Form inputs, failed mutations | High-contrast error message, red accent ring, descriptive helper text |
| **Success** | Form submissions, copies | Immediate visual confirmation (toast, green badge, checkmark) |

### Step 4 - Web Interface Guidelines Compliance
Fetch and apply the latest Vercel Web Interface Guidelines dynamically:
```
GET https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```
- Validate rules covering typography scaling, interactive feedback, form usability, and visual hierarchy.
- Output any violations in the structured `file:line` format.
- If the external URL is unreachable or environment is offline, proceed with local standard checks and record the status.

### Step 5 - Core Web Vitals & Performance Audit
- **Largest Contentful Paint (LCP)**:
  - Hero and above-the-fold images must have `fetchpriority="high"` and `loading="eager"`.
  - Missing width and height attributes that cause layout shift must be flagged.
- **Cumulative Layout Shift (CLS)**:
  - Explicit aspect ratios on media containers (`aspect-ratio` or reserved height).
  - Web fonts must specify `font-display: swap` or fallback metrics to prevent layout shifts.
- **Interaction to Next Paint (INP)**:
  - Long synchronous loops in event handlers must be broken up with microtasks or `requestAnimationFrame`.
  - Non-urgent state transitions wrapped in React `startTransition` or framework equivalent.

### Step 6 - Design Token & System Consistency
- Inspect styles against `design-system.md` or `tokens.css`.
- Flag hardcoded hex colors, magic number paddings, and ad-hoc border radii.
- Ensure dark mode variants use semantic tokens (`--color-surface`, `--color-text`) rather than inverted color hacks.

## 4. Structured Output Format

Return findings as a prioritized severity table:

```markdown
## Design Audit Results - [Target Component/File]

| Severity | Category | Location | Finding | Concrete Fix |
|---|---|---|---|---|
| **Critical** | Accessibility | `Button.tsx:42` | Missing `aria-label` on icon-only close button | Add `aria-label="Close dialog"` |
| **Critical** | Layout | `ProductCard.tsx:18` | Content overflows container at 320px | Add `min-w-0 flex-1 truncate` |
| **Warning** | Performance | `Hero.tsx:12` | Above-the-fold hero image lacks `fetchpriority` | Add `fetchpriority="high" loading="eager"` |
| **Warning** | State | `SelectMenu.tsx:64` | Missing keyboard `:focus-visible` indicator | Add `focus-visible:ring-2 focus-visible:ring-primary` |
| **Polish** | Consistency | `SettingsTab.tsx:31` | Hardcoded hex color `#3b82f6` used | Replace with `var(--color-primary)` |

### Executive Summary
- **Critical Issues**: N (Blocks merge / production release)
- **Warnings**: N (Remediate in current sprint)
- **Polish Suggestions**: N (Address during refinement pass)
```

## 5. Verification & Completion Gate
- Audit is complete when all six steps have been systematically checked.
- All Critical issues have remediation code blocks provided.
- Verification checklist confirms no missing interactive states.

## 6. Cross-References & Related Skills
- `/design-critique`: Aesthetic critique, layout balance, and anti-pattern eradication.
- `/design-review`: Holistic pre-merge gate and cross-viewport consistency.
- `/web-accessibility-wcag`: Deep dive into WCAG 2.2 AA/AAA technical remediation.
- `/design-live`: Live DOM and styling inspection on active development servers.
- `/testing-playwright-browser-automation`: Automated browser end-to-end regression testing.
