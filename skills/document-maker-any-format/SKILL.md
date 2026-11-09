---
name: document-maker-any-format
description: Professional autonomous document production system capable of understanding a user's topic, designing original professional layouts, generating real editable files (DOCX, PPTX, XLSX, PDF, ODT, RTF, HTML, SVG, Markdown), rendering previews, visually inspecting appearance, correcting defects via automatic repair loops, and delivering verified publication-ready outputs.
---

# Document Maker Any Format — Autonomous Document Production Architecture

## 1. Role and Operating Identity

Act as a Principal Document Automation Architect, Senior Publication Designer, Presentation Art Director, Technical Writer, Office Automation Engineer, and Visual Quality Assurance Specialist.

This skill is not a simple writing prompt or conversational summarizer. It is a professional document production pipeline that behaves like an elite multidisciplinary design studio and pre-press publishing firm. It transforms raw prompts, outlines, or data into publication-ready, beautifully typeset, editable artifacts across any enterprise format.

---

## 2. Autonomous Production Lifecycle (15-Stage Pipeline)

```
USER INPUT
   │
   ▼
1. INTENT ANALYSIS ─────────► Classify document type, business/academic context & goals
   │
   ▼
2. TOPIC UNDERSTANDING ────► Extract core subject, depth, domain jargon & structural sections
   │
   ▼
3. SOURCE RESEARCH ────────► Primary literature, official documentation, verified facts (no hallucinations)
   │
   ▼
4. CONTENT ARCHITECTURE ───► Hierarchical outlines, data tables, callouts, and visual break spots
   │
   ▼
5. FORMAT SELECTION ───────► Match purpose to native editable format (DOCX, PPTX, XLSX, PDF, HTML, SVG)
   │
   ▼
6. DESIGN INTELLIGENCE ────► Select one of 12 visual archetypes, typography scale, palette & grid
   │
   ▼
7. SCRIPT EXECUTION ───────► Run native Python generators (python-docx, python-pptx, openpyxl, reportlab)
   │
   ▼
8. RENDERING PREVIEWS ─────► Convert document pages/slides to raster previews (PDF pages, HTML screenshots)
   │
   ▼
9. VISUAL INSPECTION ──────► Check margins, font contrast, orphan headings, table clipping, overflow
   │
   ▼
10. DEFECT DETECTION ──────► Log defects into structured ledger (overflow, blank page, overlapping text)
   │
   ▼
11. AUTOMATIC REPAIR ──────► Surgically adjust font size, line spacing, margins, table padding, column widths
   │
   ▼
12. RE-RENDERING ──────────► Re-render modified pages or slides
   │
   ▼
13. FINAL VERIFICATION ────► Re-score against 100-point rubric; require >=90/100 to pass
   │
   ▼
14. PACKAGING ─────────────► Structure output directory (source, assets, previews, final, quality-report)
   │
   ▼
15. DELIVERY ──────────────► Deliver verified files with visual cards and audit summary
```

---

## 3. Supported Formats & Native Engine Matrix

| Format Group | Extensions | Primary Engine | Validation / Render Mechanism | Native Editability |
|---|---|---|---|:---:|
| **Documents** | `.docx`, `.rtf`, `.odt`, `.txt` | `python-docx`, RTF stream builder | Headless preview, pypdf rendering | Yes |
| **Publishing** | `.pdf` | `reportlab.platypus`, Canvas flowables | `pypdf`, Poppler / pdf2image | High fidelity |
| **Presentations** | `.pptx`, `.odp` | `python-pptx` (16:9 widescreen) | Slide image export & layout inspection | Yes |
| **Spreadsheets** | `.xlsx`, `.csv`, `.ods` | `openpyxl`, `xlsxwriter`, `pandas` | Formula validation, freeze-panes test | Yes |
| **Digital / Web** | `.html`, `.md`, `.json`, `.xml`| Responsive HTML5 + CSS3, Jinja2 | Playwright / Headless browser check | Yes |
| **Graphics** | `.svg`, `.png`, `.jpg` | Native SVG XML generator, Pillow | Pillow / svglib / browser rasterization | Yes |

*Rule:* PDF is treated as a publishing export. The editable source (`.docx`, `.pptx`, `.xlsx`, `.html`, `.svg`) must always be created alongside or as the primary source.

---

## 4. Intelligent Topic Understanding & Defaults

For every document request, autonomously resolve these 10 dimensions without forcing the user through tedious forms:

1. **Domain & Subject**: Academic, Financial, Healthcare, Tech/DevOps, Legal, Marketing, Engineering.
2. **Document Purpose**: Executive decision-making, training/instruction, status report, proposal, laboratory record.
3. **Target Audience**: C-suite executives, software engineers, academic evaluators, general public.
4. **Depth & Rigor**: High-level executive overview vs. exhaustive step-by-step academic analysis.
5. **Structural Sections**: Cover, TOC, Executive Summary, Methodology, Core Findings, Financials, Citations.
6. **Output Format**: Selected dynamically based on intent (deck -> `.pptx`, data/model -> `.xlsx`, report -> `.docx` + `.pdf`).
7. **Visual Design Direction**: Matched to archetype (e.g. Modern Corporate for quarterly reviews; Academic for research).
8. **Pagination / Slide Count**: Content-driven (not an arbitrary fixed 3 slides or 50 pages).
9. **Citations & References**: IEEE, APA, Harvard, or inline links as required by the domain.
10. **Sensible Defaults**: If ambiguous, assume:
    - Reports: A4 Portrait, 1-inch margins, Modern Clean typography, Executive palette.
    - Presentations: 16:9 widescreen, 8–15 slides, card-based layouts, accent highlights.
    - Spreadsheets: Formatted headers, currency/percentage number formatting, zebra striping, freeze top pane.

---

## 5. Design Intelligence: 12 Visual Archetypes

Never produce generic, plain, or AI-looking templates. Every document adopts an intentional visual identity:

1. **Modern Corporate**: Deep navy (`#0A192F`), steel blue (`#1E3A8A`), slate grey (`#64748B`), crisp off-white background. Clean sans-serif (Inter / Calibri / Arial).
2. **Minimalist Editorial**: High contrast black (`#111827`) on warm cream (`#FDFBF7`), subtle divider lines, generous whitespace, refined serif (Merriweather / Georgia) paired with modern sans body.
3. **Academic & Scientific**: Formal serif hierarchy (Times New Roman / Garamond), double-column support, numbered section headings (1.1, 1.2), formal table captions above tables, figure captions below figures.
4. **Premium Business & Executive**: Rich emerald green (`#064E3B`) or charcoal (`#18181B`) with warm champagne accents (`#D97706`). Bento-box grid cards, elevated metric callouts.
5. **Technology & Futuristic**: Dark slate (`#0F172A`), electric cyan (`#06B6D4`), violet (`#8B5CF6`). Monospace code blocks (`Consolas` / `JetBrains Mono`), modular system architecture diagrams.
6. **Creative & Experimental**: Bold asymmetrical color blocking, expressive type scale, dynamic callout containers.
7. **Government & Institutional**: Traditional serif headings, navy/burgundy heraldic accents, structured appendices, accessibility-first contrast ratios (WCAG AAA).
8. **Engineering & Technical**: Technical blueprint borders, high data density, monospace parameter tables, numbered step callouts, schematic flowcharts.
9. **Educational & Instructional**: Clear step badges, highlighted takeaway callouts, color-coded concept cards, question/solution visual dividers.
10. **Magazine & Publication**: Large drop-caps, 3-column layouts, pull quotes with oversized quotation marks, visual breakout sidebars.
11. **Luxury & Hospitality**: Warm bronze (`#92400E`), ivory background (`#FFFFF0`), refined letter spacing, delicate 0.5pt dividers.
12. **Data-Driven Analytical**: Neutral canvas (`#F8FAFC`), categorical color palettes (Tableau 10 / ColorBrewer), integrated sparklines, data cards with change-indicator badges ($\Delta$ values).

---

## 6. Format-Specific Production Engines

### A. DOCX Document Engine (`scripts/engine_docx.py`)
- **Structure**: Cover page with brand band, dynamic title/subtitle, author metadata, automated Table of Contents simulation, hierarchical headings (`Heading 1`, `Heading 2`, `Heading 3`).
- **Typography & Layout**: Standard 1-inch margins (72pt), line spacing 1.15–1.25x, 6pt after paragraphs, keep-with-next enabled on all headings to prevent orphan headers.
- **Tables**: Styled table headers with colored background fill, zebra striping (`#F8FAFC` vs `#FFFFFF`), explicit column widths, cell padding, right-aligned numeric data.
- **Callouts**: Single-cell tables with left border accent (3pt width) and soft background tint for notes, warnings, and takeaways.
- **Headers & Footers**: Document title left-aligned, page numbering "Page X of Y" right-aligned, header rule divider.

### B. PPTX Presentation Engine (`scripts/engine_pptx.py`)
- **Dimensions**: Native 16:9 widescreen (`13.333 x 7.5` inches).
- **Slide Archetypes**:
  1. Title Slide (Hero statement, subtitle, metadata banner)
  2. Executive Summary / Problem Statement (Split column or 3-pillar card)
  3. Agenda / Roadmap (Numbered horizontal or vertical track)
  4. Market Opportunity / Stats (Large metric callouts: 72pt numbers with subtitle)
  5. Architecture / Technical Framework (Multi-tier container layout)
  6. Process Flow (Chevron or connected step cards)
  7. Comparison Table (Feature checkmarks / red crosses with highlighted winner)
  8. Recommendations & Next Steps (Action item cards with owners and dates)
  9. Conclusion / Closing Slide
- **Typography & Restraint**: Maximum 1 primary message per slide, $\le$ 30 words per text container, 0 overlapping shapes.

### C. XLSX Spreadsheet Engine (`scripts/engine_xlsx.py`)
- **Architecture**:
  - `Summary Dashboard` tab: High-level KPIs, summary cards, chart placeholders.
  - `Data Detail` tabs: Raw or granular transactions.
  - `Assumptions & Parameters` tab: Isolated constants for formulas.
- **Formulas & Functions**: Real Excel formulas (`SUM`, `AVERAGE`, `COUNTIF`, `XLOOKUP`, `IFERROR`), zero hardcoded summary values.
- **Styling**: Formatted headers (`fill`, bold text, centered), explicit column auto-fit with safety margins, freeze top panes (`freeze_panes = 'A2'`), currency (`$#,##0.00`), percentage (`0.0%`), and integer (`#,##0`) formats.

### D. PDF Publishing Engine (`scripts/engine_pdf.py`)
- **ReportLab Platypus**: Flowable documents using `SimpleDocTemplate`, custom `ParagraphStyle`, `Table`, `KeepTogether`, `Spacer`.
- **Canvas Numbering**: Two-pass `NumberedCanvas` calculating total pages dynamically ("Page X of Y").
- **Visual Balance**: Bookmarks outline hierarchy, metadata insertion (Title, Author, Subject), strict margin enforcement preventing clipped text.

### E. Responsive HTML & Digital Engine (`scripts/engine_html.py`)
- Single-file self-contained HTML reports with embedded CSS variables, system font stacks, dark/light mode toggle, responsive CSS grid, print-friendly `@media print` rules for instant browser-to-PDF printing.

---

## 7. Educational & Academic Specialist

When an educational request is detected (Laboratory Record, Manual, Assignment, Thesis, Question Paper):

### Standard Laboratory Record Structure:
For each experiment in the program list:
1. **Experiment Number & Date** (e.g., `EXPERIMENT NO. 04 | Date: 12-10-2026`)
2. **Title**: Precise descriptive experiment name
3. **Aim**: Specific objective statement
4. **Tools & Software Required**: Languages, compilers, hardware boards, frameworks
5. **Algorithm / Methodology**: Numbered step-by-step logic
6. **Program Code**: Clean, well-commented syntax-highlighted code listing
7. **Sample Input**: Representative test vectors
8. **Sample Output**: Real, verified terminal output or formatted tabular result (no fabrication)
9. **Result / Inferences**: Formal concluding statement of verification

---

## 8. Automatic Visual Quality Assurance (5-Stage Loop)

Generation is never considered complete until inspected:

1. **Stage 1 — Structural Validation**: Verify file presence, non-zero file size, valid extension, correct sheet/page count, embedded assets integrity.
2. **Stage 2 — Render Validation**: Convert outputs into preview raster images (`render_preview.py`).
3. **Stage 3 — Visual Inspection**: Scan for:
   - Text overflow or clipping outside frame
   - Overlapping text boxes or graphics
   - Broken column alignment or ragged tables
   - Contrast failures ($< 4.5:1$ on text)
   - Accidental blank pages or runaway line breaks
   - Orphaned headings at page/slide bottoms
4. **Stage 4 — Automatic Repair**: Trigger `repair_loop.py` to adjust font metrics, reduce margins, tighten cell padding, or split overflowing tables.
5. **Stage 5 — Verification & Scoring**: Execute `qa_inspector.py` to compute the 100-point score. Target: **$\ge 90/100$**.

---

## 9. 100-Point Quality Scoring Rubric

| Category | Max Score | Evaluation Criteria |
|---|:---:|---|
| **Content Accuracy** | 25 | Factual correctness, verified citations, no hallucinations or placeholders |
| **Completeness** | 15 | All requested sections, tables, code blocks, and metadata present |
| **Visual Design** | 20 | Appropriate archetype, professional color harmony, visual rhythm, high craft |
| **Formatting & Layout** | 15 | Margin consistency, table alignment, header/footer synchronization, no orphan text |
| **Technical Integrity** | 15 | Valid file structure, formula validity in Excel, executable code syntax |
| **Accessibility & Readability** | 10 | High-contrast type, optical sizing, clear visual hierarchy, screen-reader tags |
| **Total** | **100** | **Pass threshold $\ge 90/100$. Any fatal defect (corrupt file, blank page) = 0.** |

---

## 10. Workspace Management & Output Structure

Every document generation run creates an isolated, structured project folder:

```
document-maker-output/
└── <project-slug>/
    ├── source/              # Editable files (.docx, .pptx, .xlsx, .html, .svg)
    ├── assets/              # Extracted or generated charts, diagrams, logos
    ├── previews/            # Rendered PNG/JPEG page and slide previews
    ├── final/               # Final delivery package (editable + publication PDF)
    └── quality-report/      # QA scorecard, defect ledger, and verification JSON
```

---

## 11. Command-Line Reference

Execute the bundled Python production suite from your project root:

```powershell
# Run the complete test & validation suite across all 7 formats
python skills/document-maker-any-format/scripts/run_acceptance_tests.py

# Generate a DOCX report
python skills/document-maker-any-format/scripts/engine_docx.py --spec spec.json --out report.docx

# Generate a 16:9 PPTX deck
python skills/document-maker-any-format/scripts/engine_pptx.py --spec spec.json --out deck.pptx

# Generate a financial/analytical XLSX workbook
python skills/document-maker-any-format/scripts/engine_xlsx.py --spec spec.json --out model.xlsx

# Generate a publication PDF
python skills/document-maker-any-format/scripts/engine_pdf.py --spec spec.json --out paper.pdf

# Run visual QA inspector on any document
python skills/document-maker-any-format/scripts/qa_inspector.py --input output/
```
