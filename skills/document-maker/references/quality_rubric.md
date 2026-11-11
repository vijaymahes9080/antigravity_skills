# 100-Point Quality Rubric & Self-Healing Defect Repair Ledger

This document details the objective quality evaluation algorithm and automated defect repair catalog executed by `document-maker`.

---

## 1. The 100-Point Scoring Algorithm

Every generated document undergoes comprehensive inspection across six core dimensions:

| Dimension | Max Points | Pass Threshold | Verification Mechanism |
|---|:---:|:---:|---|
| **1. Content Precision & Depth** | 25 | $\ge 23$ | Verified facts, authentic data/terminal results (zero fabricated hallucinations or placeholder `[TODO]` tokens). |
| **2. Structural Completeness** | 15 | $\ge 14$ | Presence of all requisite sections, callouts, tables, metadata headers, and footers. |
| **3. Visual Craft & Archetype** | 20 | $\ge 18$ | Strict adherence to chosen archetype color palette, typography hierarchy, margin rhythm, and visual balance. |
| **4. Layout & Pagination Hygiene** | 15 | $\ge 14$ | Margin consistency, table column auto-fitting, prevention of orphan headings, elimination of accidental blank pages. |
| **5. Technical Integrity** | 15 | $\ge 14$ | Magic byte validation, zip container integrity, working spreadsheet formulas, error-free document parsing. |
| **6. Accessibility & Readability** | 10 | $\ge 9$ | WCAG 2.2 AA contrast ratios ($\ge 4.5:1$ text contrast), optical font sizing, clear visual delimiters. |
| **Total Score** | **100** | **$\ge 90$** | **Mandatory Pass Threshold for Delivery.** |

---

## 2. Fatal Defect Rules (Immediate 0 Points)

If any fatal defect is detected, the document receives an immediate **Score of 0** and delivery is blocked until repaired:
1. **Unparseable / Corrupted Output**: The target runtime cannot open or parse the file.
2. **Zero-Byte File**: Empty file generated due to uncaught pipeline exception.
3. **Accidental Blank Pages**: Blank white pages caused by excessive trailing spacers or improper page breaks.
4. **Clipped or Overlapping Content**: Text or tables spilling outside physical margins or colliding with adjacent containers.
5. **Fabricated Output / Dummy Text**: Dummy text such as `Lorem Ipsum`, `Insert Title Here`, or simulated fake test outputs.

---

## 3. Defect Taxonomy & Automated Self-Healing Repair Table

When defects are detected during inspection, `repair_loop.py` automatically applies surgical corrective actions:

| Defect Code | Defect Classification | Diagnostic Indicator | Self-Healing Repair Action |
|---|---|---|---|
| `DEF-001` | **Content Overflow** | Text or table exceeds page/slide bounding box | Dynamically reduce font size by 0.5–1.0pt, reduce paragraph spacing from 6pt to 4pt, and adjust line spacing from 1.25x to 1.15x. |
| `DEF-002` | **Trailing Blank Page** | Trailing empty page in PDF/DOCX | Remove redundant `PageBreak()` calls and reduce trailing `Spacer` elements by $\ge 50\%$. |
| `DEF-003` | **Table Column Clipping** | Table width exceeds printable margin width | Recompute column widths proportionally based on `printable_width / total_weight` and enable auto-wrap. |
| `DEF-004` | **Orphaned Heading** | Heading positioned within 1.5 inches of bottom margin | Enforce `keep_with_next = True` on paragraph styles; insert explicit page break before the heading. |
| `DEF-005` | **Low Contrast Ratio** | Foreground/background contrast $< 4.5:1$ | Automatically elevate text luminance or swap background fill to compliant token from the archetype palette. |
| `DEF-006` | **Spreadsheet Formula Error** | `#REF!`, `#VALUE!`, or unclosed parenthesis | Re-index formula coordinates and wrap expression in `=IFERROR(<expression>, 0)`. |
| `DEF-007` | **Formula Injection Threat** | Cell starts with `=`, `+`, `-`, `@`, `\t` without safe escaping | Prepend a single quote (`'`) to string values to deactivate spreadsheet execution. |
| `DEF-008` | **Image Distortion** | Non-proportional image scaling | Recalculate dimensions enforcing natural aspect ratio `width = height * (orig_w / orig_h)`. |

