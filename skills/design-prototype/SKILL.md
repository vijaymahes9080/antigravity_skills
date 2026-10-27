---
name: design-prototype
description: Generate and compare alternative visual directions and component prototypes. Use when exploring design options (e.g. Minimalist vs Bento vs Data-Dense) before committing to implementation.
---

# Design Prototyping & Visual Direction Exploration

Generate and compare alternative visual directions and component prototypes. Evaluate contrasting aesthetic archetypes side-by-side to reach confident design consensus before deep architectural implementation.

## 1. Intended Role & Activation Criteria

Use this skill when:
- Exploring new aesthetic directions for a feature, dashboard, or landing page.
- Comparing distinct layout archetypes (e.g., Editorial Minimalist vs Bento Grid vs Data-Dense Console).
- Creating rapid visual prototypes to resolve design uncertainty with the user.

Do **not** use for:
- Surgical CSS tuning on an approved design -> use `/design-polish`
- Pre-merge production review -> use `/design-review`
- Pure accessibility compliance verification -> use `/design-audit`

## 2. Inputs Required

- Target screen or component objective (e.g., Analytics Dashboard, Billing Portal, User Settings).
- Core information elements that must be rendered.
- Desired aesthetic exploration space.

## 3. Five Archetype Direction Matrix

Explore at least two contrasting archetypes from the matrix:

| Archetype | Characteristics | Best Suited For |
|---|---|---|
| **1. Minimalist Editorial** | Generous whitespace, refined serif/sans contrast, subtle 1px dividers, restrained monochromatic palette | Luxury brands, knowledge bases, long-form reading, executive summaries |
| **2. Bento Grid Modular** | Rounded compartmentalized cards, asymmetric spans, distinct visual hierarchy, micro-telemetry | Product landing pages, feature overviews, personal portfolios |
| **3. Data-Dense Console** | Monospace typography, compact row heights, high information density, integrated keyboard shortcuts | Developer tooling, observability dashboards, financial trading desks |
| **4. Glass & Depth Material** | Translucent floating layers, backdrop blurs, soft layered ambient shadows, vibrant accents | Modern macOS/iOS-style productivity tools, multimedia apps |
| **5. High-Contrast Bold** | Vivid color blocks, strong borders, assertive sans typography, sharp geometric corners | Modern fintech, creative agencies, youth-oriented applications |

## 4. Prototype Generation Protocol

1. **Scaffold Side-by-Side Variations**:
   - Create lightweight, self-contained prototype mockups using semantic tokens.
   - For rapid visual preview, use native rendering or programmatic mockups.
2. **Standardized Evaluation Criteria**:
   - Compare each variation across:
     - **Information Density**: How effectively does the user absorb data?
     - **Visual Ergonomics**: Eye travel and cognitive load.
     - **Brand Alignment**: Emotional resonance with product goals.
     - **Implementation Cost**: Engineering complexity to implement and maintain.
3. **User Consensus Gate**:
   - Present the alternatives clearly with trade-offs.
   - Confirm selected direction before proceeding to production engineering.

## 5. Cross-References
- `/design-init`: Establish full design tokens once archetype is selected.
- `/frontend-craft-design-engineering`: End-to-end craft design execution.
- `/image-generate`: Generate visual moodboards or hero mockups.
