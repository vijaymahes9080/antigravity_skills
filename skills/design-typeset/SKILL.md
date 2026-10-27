---
name: design-typeset
description: Review and enhance typography - font pairings, text hierarchy, scale ratios, line length, leading, and multilingual support. Use when improving reading ergonomics, fixing typographic inconsistencies, or establishing a new type system.
---

# Design Typeset & Typographic Engineering

Review, calibrate, and elevate typography across user interfaces. Establish legible font pairings, modular scale ratios, comfortable reading line lengths, and multilingual script support.

## 1. Intended Role & Activation Criteria

Use this skill when:
- Establishing or refactoring the typography system for a digital product.
- Resolving font rendering issues, awkward line-heights, or cramped text blocks.
- Optimizing reading ergonomics (measure, leading, kerning, contrast).
- Implementing multilingual or non-Latin script typography (Indic, Arabic, CJK).

Do **not** use for:
- Full design system initialization -> use `/design-init`
- Color contrast remediation alone -> use `/design-colorize`
- Component-level spacing polish -> use `/design-polish`

## 2. Inputs Required

- Current typography definitions (CSS, Tailwind font family configuration, Google Fonts imports).
- Primary language and internationalization requirements.
- Target reading medium (dense desktop dashboard, mobile reader, marketing hero).

## 3. Typographic Engineering Protocol

### Step 1 - Modular Scale Architecture
Adopt a mathematical ratio suited for the product archetype:
- **Major Second (1.125)**: Ideal for dense data tables, developer consoles, and enterprise dashboards.
- **Minor Third (1.200)**: Clean balance for SaaS applications and general product interfaces.
- **Major Third (1.250)**: Expressive hierarchy for editorial content and marketing landing pages.
- **Perfect Fourth (1.333)**: Dramatic contrast for media-heavy, high-impact hero layouts.

### Step 2 - Font Pairing Discovery
Query the curated typography database:
```bash
python "$HOME/.gemini/config/skills/frontend-ui-ux-intelligence/scripts/search.py" "<product-keywords>" --domain typography
```
Recommended Archetypes:
- **Technical & Modern**: Inter (Body) + JetBrains Mono (Code/Metrics)
- **Editorial & Authoritative**: Newsreader / Playfair Display (Headings) + Inter (Body)
- **Neutral & Contemporary**: Plus Jakarta Sans / Outfit (Headings) + DM Sans (Body)

### Step 3 - Reading Ergonomics Calibration
- **Measure (Line Length)**: Maintain 45 to 75 characters per line (optimal ~65 characters) for paragraph text (`max-w-prose` or `max-width: 65ch`).
- **Leading (Line Height)**:
  - Display / Hero (36px+): `line-height: 1.1 - 1.2`
  - Subheadings (20px - 32px): `line-height: 1.25 - 1.35`
  - Body Text (14px - 18px): `line-height: 1.5 - 1.6`
  - Data Tables & Code: `line-height: 1.35 - 1.45`
- **Tracking (Letter Spacing)**:
  - Tighten large headings: `letter-spacing: -0.02em to -0.03em`.
  - Loosen small uppercase caps: `letter-spacing: 0.05em to 0.1em`.

### Step 4 - Multilingual & Non-Latin Font Fallbacks
- Ensure font stack defines comprehensive fallbacks:
  ```css
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans Tamil', 'Noto Sans', sans-serif;
  ```
- For Indic scripts (e.g. Tamil), increase line-height by at least 15% (`line-height: 1.7`) to prevent clipping of upper and lower vowel markers.

## 4. Verification & Testing
- Inspect text rendering across Chrome, Safari, and Firefox.
- Confirm `font-display: swap` is applied to avoid invisible text during font loading (FOIT).
- Verify headings wrap without orphan words using CSS `text-wrap: balance` or `text-wrap: pretty`.

## 5. Cross-References
- `/design-init`: Complete design token setup.
- `/design-audit`: WCAG contrast ratio validation.
- `/frontend-ui-ux-intelligence`: Font pairing library.
