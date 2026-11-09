# Quality Rubric & Automated QA Defect Matrix

This document defines the 100-point scoring algorithm and the automated defect repair procedures executed by `document-maker-any-format`.

---

## 1. The 100-Point Scoring Matrix

| Dimension | Max Points | Passing Bar | Metric & Verification Method |
|---|:---:|:---:|---|
| **Content Accuracy** | 25 | $\ge 23$ | Verified technical assertions, real outputs (no dummy filler like 'Lorem Ipsum' or placeholder brackets `[TODO]`), substantiated claims. |
| **Completeness** | 15 | $\ge 14$ | Presence of all requested sections, tables, headers, footers, code listings, and metadata. |
| **Visual Design** | 20 | $\ge 18$ | Intentional color palette matching chosen archetype, balanced typographic scale, visual hierarchy, no generic AI styling. |
| **Formatting & Layout** | 15 | $\ge 14$ | Margin consistency, table alignment, page break hygiene, no accidental blank pages, no orphaned headings. |
| **Technical Integrity** | 15 | $\ge 14$ | Valid file syntax, passes format parsers (`python-docx`, `python-pptx`, `openpyxl`, `reportlab`), working Excel formulas. |
| **Accessibility & Readability** | 10 | $\ge 9$ | WCAG AA contrast ratio ($\ge 4.5:1$ for body text), readable font sizes, tabular data alignment. |
| **Total Score** | **100** | **$\ge 90$** | **Mandatory overall pass threshold.** |

---

## 2. Fatal Defect Rules (Immediate 0 Points & Block Delivery)

Any of the following causes immediate task failure until auto-repaired:
1. **Corrupted File**: Generated file cannot be parsed or opened by its standard runtime.
2. **Missing Essential Section**: Missing Aim, Code, or Output in an academic lab record; missing Financials in a business plan.
3. **Fabricated Experimental Output**: Fake simulated numbers presented as real machine verification.
4. **Accidental Blank Pages**: Completely empty pages generated due to incorrect page breaks or oversized trailing Spacers.
5. **Clipped or Overlapping Text**: Slide or page text extending beyond margins or overlapping sibling elements.

---

## 3. Defect Taxonomy & Automated Repair Table

| Defect Code | Description | Automated Repair Action |
|---|---|---|
| `DEF-001` | Text overflowing page or slide boundary | Reduce font size by 0.5–1.0pt, decrease paragraph spacing from 6pt to 4pt, adjust line spacing from 1.25 to 1.15. |
| `DEF-002` | Accidental trailing blank page | Remove superfluous `PageBreak()` or reduce trailing `Spacer` height by 50%. |
| `DEF-003` | Table column clipping | Compute explicit column widths proportionally from page printable width; wrap cell content in Paragraph flowables. |
| `DEF-004` | Orphaned heading at page bottom | Set `keep_with_next = True` on heading paragraph style; insert explicit page break before heading if remaining page height $< 1.5$ inches. |
| `DEF-005` | Low contrast text on dark background | Automatically elevate text brightness or swap fill color to guarantee $\ge 4.5:1$ contrast ratio. |
| `DEF-006` | Formula syntax error in spreadsheet | Correct cell coordinate reference; wrap in `=IFERROR(..., 0)` to prevent `#REF!` or `#DIV/0!`. |
| `DEF-007` | Broken image aspect ratio | Constrain image dimensions maintaining natural width/height ratio; never stretch or skew. |
