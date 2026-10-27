---
name: design-live
description: Inspect and refine running applications using real-time browser tooling, live DOM inspection, and visual feedback. Use when fine-tuning an active development server or debugging visual quirks.
---

# Design Live & Real-Time Browser Refinement

Inspect, debug, and refine active running web applications in real time using Antigravity browser subagent tooling, DOM tree inspection, visual screenshot capture, and live hot-reload verification.

## 1. Intended Role & Activation Criteria

Use this skill when:
- An active local development server (e.g., `localhost:3000`, `localhost:5173`, `localhost:8080`) is running.
- Debugging visual glitches, unexpected layout shifts, z-index stacking bugs, or clipping issues.
- Fine-tuning responsive UI behavior and live hover/modal transitions directly in the browser environment.

Do **not** use for:
- Static code compliance without running a dev server -> use `/design-audit`
- Automated headless end-to-end test suites -> use `/testing-playwright-browser-automation`
- Aesthetic evaluation of static mockups -> use `/design-critique`

## 2. Inputs Required

- Active local development server URL and port.
- Specific component, route, or visual defect to investigate.
- Responsive viewport width to inspect (e.g., 375px mobile, 768px tablet, 1440px desktop).

## 3. Real-Time Inspection Protocol

### Step 1 - Dev Server Health & Route Verification
1. Verify development server is alive and responding on target port.
2. Confirm the target route loads cleanly without critical JavaScript runtime errors.

### Step 2 - Antigravity Browser Subagent Orchestration
1. Launch `browser_subagent` to navigate to the target URL.
2. Capture visual screenshots and inspect the DOM structure.
3. Check browser console logs for resource 404s, unhandled promise rejections, or CSS warnings.

### Step 3 - Visual Defect Isolation & Code Hot-Reload
1. **Z-Index & Stacking Context Bugs**: Inspect parent containers for unexpected `overflow: hidden`, `transform`, or `z-index` collisions.
2. **Flexbox & Grid Truncation**: Identify missing `min-w-0` on flex children causing container blowouts.
3. **Live Code Fix**: Apply targeted style adjustments in source files.
4. **Verification**: Confirm instant hot-reload in the browser and re-capture screenshot to validate fix.

### Step 4 - Honest Tooling Reporting
- If browser subagent tooling is disabled or dev server is offline, clearly report what was verified statically and what requires live runtime validation.

## 4. Cross-References
- `/design-polish`: Apply surgical CSS refinements identified during live sessions.
- `/design-audit`: Run full compliance audit post-fix.
- `/testing-playwright-browser-automation`: Script automated browser regression tests.
