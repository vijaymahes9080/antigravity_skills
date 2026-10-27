---
name: design-test
description: Execute automated visual, interaction, and behavioral tests across user journeys. Use when verifying critical UI flows, responsive layouts, or regression prevention.
---

# Design Testing & UI Interaction Verification

Execute automated visual, component-state, and interaction verification across UI user journeys. Focus specifically on visual regression, design-system token compliance, and interactive component state coverage.

## 1. Intended Role & Scope Boundary

- **Primary Focus**: UI component interaction verification, visual layout assertions, design-system token adherence, and state transition coverage.
- **Explicit Scope Boundary**:
  - Use `/design-test` for UI-specific visual states, component rendering, keyboard focus journeys, and token validation.
  - Do **NOT** use for full-system E2E backend integration, API mocking, or multi-system end-to-end journey automation -> use `/testing-playwright-browser-automation`.

## 2. Inputs Required

- Target component or UI flow to test.
- Component test runner (Vitest, Jest, Playwright Component Testing, Flutter Widget Tests).
- Expected state behaviors (loading, empty, success, error, focus).

## 3. UI Verification Protocol

### Step 1 - Component State Coverage
Verify all required interactive states are represented in test suites:
- **Default & Hover**: Elements mount with correct styling and respond to pointer events.
- **Active & Focus-Visible**: Keyboard Tab events trigger visible focus ring classes or styles.
- **Disabled**: Assert `disabled` attribute, `aria-disabled="true"`, and pointer event suppression.
- **Loading & Skeleton**: Assert loading spinners or shimmer skeletons maintain correct dimensions.
- **Error & Validation**: Trigger input errors and assert visible error copy and ARIA attributes (`aria-invalid="true"`).

### Step 2 - Visual Layout & Breakpoint Testing
Assert layout resilience across viewport dimensions:
```typescript
// Example: Component viewport resilience test
test('navigation collapses to hamburger menu below 768px', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto('/dashboard');
  await expect(page.getByRole('button', { name: /open navigation menu/i })).toBeVisible();
  await expect(page.getByRole('navigation')).toBeHidden();
});
```

### Step 3 - Keyboard Navigation & Trap Prevention
- Verify focus traversal: Tab advances sequentially, Shift+Tab reverses.
- Dialog / Modal flows: Focus trapped inside active modal until Escape or Close is pressed.
- Return focus: Focus restored to the triggering button upon modal close.

### Step 4 - Execution Tool Fallbacks
- If headless Playwright or component testing dependencies are available: Run tests and assert DOM state.
- If dependencies are missing: Execute local unit/widget test runners (`npm test`, `flutter test`) and clearly document test coverage.

## 4. Cross-References
- `/testing-playwright-browser-automation`: End-to-end full stack browser automation and scraping.
- `/design-audit`: Static accessibility and responsive audit.
- `/frontend-ui-edge-case-testing`: Stress testing UI with pathological data.
