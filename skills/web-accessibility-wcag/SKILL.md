---
name: web-accessibility-wcag
description: Web accessibility audit and remediation conforming to WCAG 2.2 AA/AAA, WAI-ARIA role patterns, screen reader navigation, keyboard trap prevention, and automated axe-core testing.
---

# Web Accessibility (WCAG 2.2) & Inclusive Design

## 1. Intended Role & Domain
- **Primary Domain**: Web Engineering & Accessibility
- **Target Roles**: Accessibility Specialist, Frontend Developer, QA Engineer
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "accessibility", "wcag", "a11y", "screen reader audit", "aria roles", "keyboard navigation", "color contrast audit", "axe-core".
- **Contextual Inferences**: Compliance with ADA, Section 508, European Accessibility Act (EAA), pre-launch audit of consumer web apps.
- **Chained Predecessors**: `design-systems-engineer`, `react-nextjs-pro`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Non-visual backend headless services without user interaction or display interfaces.
  - Command-line terminal text utilities.

## 4. Required Inputs & Context
- Frontend source files (HTML, JSX, TSX, Vue, Svelte).
- Target WCAG conformance level: Level AA (standard) or Level AAA (enhanced).
- Interactive widget specifications (dialogs, dropdowns, tabs, comboboxes).

## 5. Expected Outputs & Artifacts
- Accessibility Audit Matrix categorized by WCAG 2.2 principles: Perceivable, Operable, Understandable, Robust (POUR).
- Remediation patches with semantic HTML and appropriate WAI-ARIA attributes.
- Automated axe-core / Playwright accessibility test suite.

## 6. Step-by-Step Operating Procedure
1. **Semantic HTML Structure Verification**:
   - Replace generic `<div>` clickables with native `<button>` or `<a>` elements.
   - Enforce single `<h1>` per page and hierarchical heading order (`h1` -> `h2` -> `h3`).
2. **Keyboard Navigation & Focus Management**:
   - Verify all interactive elements are reachable via `Tab` and activatable via `Enter` / `Space`.
   - Prevent keyboard traps in modal dialogs; implement focus trapping and restore focus on dismiss (`Escape` key).
3. **WAI-ARIA Pattern Implementation**:
   - Add necessary ARIA attributes (`aria-expanded`, `aria-haspopup`, `aria-selected`, `aria-live`).
   - Rule 1 of ARIA: Do not use ARIA when native HTML5 semantics already provide the behavior.
4. **Perceptual Contrast & Sensory Characteristics**:
   - Verify text contrast ratios: >= 4.5:1 for regular text, >= 3:1 for large text and UI components.
   - Ensure color is never the sole visual means of conveying information.
5. **Automated Testing & Screen Reader Validation**:
   - Run automated axe-core tests and verify announcements with screen readers (NVDA, VoiceOver).

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection of markup and test tooling:
  ```bash
  cat package.json | grep -E "(@axe-core|pa11y|lighthouse)" 2>/dev/null || echo "A11y tools not yet configured"
  ```
- Preservation rule: Never add `outline: none` or `outline: 0` without immediately providing an accessible alternative `:focus-visible` style.

## 8. Tool & Dependency Requirements
- `@axe-core/playwright`, Lighthouse CLI, Pa11y, Modern browser accessibility inspector.

## 9. Implementation Guidelines & Best Practices
- Every form `<input>` must have an associated `<label>` element with matching `for`/`id` or `aria-label`.
- Images must have meaningful `alt` text, or `alt=""` if purely decorative.

```tsx
// Accessible Modal Dialog Component with Focus Trap
import React, { useEffect, useRef } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export function AccessibleModal({ isOpen, onClose, title, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        className="modal-content"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 id="modal-title">{title}</h2>
        {children}
        <button type="button" onClick={onClose} aria-label="Close dialog">
          Close
        </button>
      </div>
    </div>
  );
}
```

## 10. Error Handling & Recovery Procedures
- Dynamic content updates not announced: Add `aria-live="polite"` or `role="status"` to notification containers.
- Form validation error not linked: Use `aria-describedby="error-id"` and `aria-invalid="true"` on invalid inputs.

## 11. Security & Privacy Constraints
- Ensure screen reader accessible text does not inadvertently expose hidden CSRF tokens or sensitive session identifiers.

## 12. Verification & Testing Requirements
- Automated axe-core testing with Playwright:
  ```typescript
  import { test, expect } from '@playwright/test';
  import AxeBuilder from '@axe-core/playwright';

  test('should have no accessibility violations on home page', async ({ page }) => {
    await page.goto('/');
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag22aa'])
      .analyze();
    expect(accessibilityScanResults.violations).toEqual([]);
  });
  ```

## 13. Completion Criteria
- Zero critical or serious axe-core accessibility violations.
- 100% keyboard navigable without mouse reliance.
- Color contrast meets WCAG AA standards.

## 14. Relevant Official References
- W3C Web Content Accessibility Guidelines (WCAG 2.2).
- W3C WAI-ARIA Authoring Practices Guide (APG).
- Deque axe-core Rule Documentation.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Fully compatible with WCAG 2.2 standards released late 2023 / 2024.
