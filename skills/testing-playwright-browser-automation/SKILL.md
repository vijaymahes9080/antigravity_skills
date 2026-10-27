---
name: testing-playwright-browser-automation
description: Resilient browser automation and E2E testing with Playwright, robust role-based locators, visual regression testing, network request intercept/mocking, and headless scraping.
---

# Browser Automation & Playwright Engineering

## 1. Intended Role & Domain
- **Primary Domain**: Automation & Quality Assurance
- **Target Roles**: Browser Automation Developer, QA and Automation Engineer, Web Scraping Specialist
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "playwright", "browser automation", "e2e testing", "web scraping automation", "headless browser", "ui test automation", "intercept network request".
- **Contextual Inferences**: Repositories containing `playwright.config.ts`, `tests/e2e/`, automated UI workflows.
- **Chained Predecessors**: `task-decomposition`, `react-nextjs-pro`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Performing unit testing of pure mathematical functions without a browser environment.
  - Testing low-level C/C++ or embedded firmware.

## 4. Required Inputs & Context
- Target website URL or local development server address (e.g. `http://localhost:3000`).
- User interaction flow (e.g., login -> navigate to settings -> update profile -> assert success banner).
- Target browser engines (Chromium, Firefox, WebKit).

## 5. Expected Outputs & Artifacts
- Playwright test script (`tests/e2e/workflow.spec.ts`).
- Robust Page Object Model (POM) classes encapsulating selectors and interactions.
- Network mock handlers for external third-party API dependencies.
- HTML test execution report and visual diff snapshots.

## 6. Step-by-Step Operating Procedure
1. **Locators & Accessibility First**:
   - Use user-facing role locators (`page.getByRole('button', { name: 'Submit' })`, `page.getByLabel('Email')`) rather than fragile CSS/XPath paths (`div > div:nth-child(3)`).
2. **Auto-Waiting & Race Condition Prevention**:
   - Rely on Playwright's built-in auto-waiting assertions (`await expect(locator).toBeVisible()`).
   - Forbid arbitrary sleep timers (`page.waitForTimeout(5000)` is an anti-pattern).
3. **Network Interception & API Mocking**:
   - Intercept flaky or expensive backend calls using `page.route()` to return deterministic JSON mocks.
4. **Visual Regression Verification**:
   - Capture element screenshots and compare against baseline images using `expect(page).toHaveScreenshot()`.
5. **Trace & Artifact Recording**:
   - Configure video recording and trace capture on test failure for deterministic debugging.

## 7. Repository Inspection & Planning Requirements
- Non-destructive Playwright setup check:
  ```bash
  npx playwright --version 2>/dev/null || echo "Playwright not installed"
  ls -la playwright.config.* 2>/dev/null
  ```
- Preservation rule: Never hardcode production credentials in test files; inject via test environment variables.

## 8. Tool & Dependency Requirements
- Node.js 18+, `@playwright/test`, Playwright browser binaries (`npx playwright install --with-deps chromium`).

## 9. Implementation Guidelines & Best Practices
- Structure tests using the Page Object Model (POM) pattern for maintainability:

```typescript
import { type Page, type Locator, expect } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorBanner: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email address');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign in' });
    this.errorBanner = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, pass: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(pass);
    await this.submitButton.click();
  }
}
```

## 10. Error Handling & Recovery Procedures
- Element click intercepted: Verify if a sticky header, modal backdrop, or loading overlay is obscuring the element; wait for overlay detachment.
- Flaky network timeouts: Increase navigation timeout gracefully or verify DNS resolution.

## 11. Security & Privacy Constraints
- Sanitize browser test recordings: Prevent passwords or sensitive customer billing info from appearing in failure video artifacts.

## 12. Verification & Testing Requirements
- Execute Playwright test suite:
  ```bash
  npx playwright test --project=chromium --reporter=list
  ```
- Verify trace artifacts on failure:
  ```bash
  npx playwright show-report 2>/dev/null || true
  ```

## 13. Completion Criteria
- End-to-end user journey executes reliably without flaky timeouts.
- All assertions pass using accessible role locators.
- HTML report generated with 100% passing tests.

## 14. Relevant Official References
- Playwright Official Documentation (playwright.dev).
- W3C WebDriver BiDi Specification.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with Playwright v1.45+ and modern headless browser automation.


## Consolidated Capabilities (from webapp-testing)
- Source Workflow: Functional duplicate: Playwright local web testing & screenshot logs merged into Playwright automation.
# Web Application Testing

To test local web applications, write native Python Playwright scripts.

**Helper Scripts Available**:
- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

**Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is abslutely necessary. These scripts can be very large and thus pollute your context window. They exist to be called directly as black-box scripts rather than ingested into your context window.

## Decision Tree: Choosing Your Approach

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Example: Using with_server.py

To start a server, run `--help` first, then use the helper:

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers (e.g., backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

To create an automation script, include only Playwright logic (servers are managed automatically):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173') # Server already running and ready
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

## Common Pitfall

❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

## Best Practices

- **Use bundled scripts as black boxes** - To accomplish a task, consider whether one of the scripts available in `scripts/` can help. These scripts handle common, complex workflows reliably without cluttering the context window. Use `--help` to see usage, then invoke directly. 
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`

## Reference Files

- **examples/** - Examples showing common patterns:
  - `element_discovery.py` - Discovering buttons, links, and inputs on a page
  - `static_html_automation.py` - Using file:// URLs for local HTML
  - `console_logging.py` - Capturing console logs during automation