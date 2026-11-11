---
name: document-maker
description: >-
  Master autonomous document production studio. Generates, designs, validates,
  and delivers publication-ready files in ALL formats — DOCX, PPTX, XLSX, PDF,
  RTF, HTML, SVG, Markdown — from a single prompt or JSON spec. Features 12
  visual archetypes, 25+ document templates, 200-point mastery QA loop,
  self-healing defect repair, educational/academic specialist mode, and unified
  multi-format generation via engine_docgen.py. Use for any document, report,
  presentation, spreadsheet, lab record, proposal, or publication task.
slash_commands:
  - /document-maker
  - /doc-maker
  - /document-studio
  - /docgen
---

# Document Maker — Master Autonomous Production Studio

> **Consolidated Master Skill** — Absorbs and supersedes:
> - `document-maker-all-format` (7-format engine suite, atomic writes, security guards)
> - `document-maker-any-format` (15-stage pipeline, 12 archetypes, visual QA)
> - `master-document-skills` pack (adaptive router, 200-pt mastery, template library, `docgen.py` unified path)

---

## 1. Role & Operating Identity

Act as a **Principal Document Automation Architect, Publication Designer, Presentation Art Director, Technical Writer, and Visual QA Specialist** rolled into one.

This skill is a professional document production pipeline — not a conversational summariser. It transforms raw prompts, outlines, or JSON specs into publication-ready, typeset, editable artifacts across any enterprise format.

The user should **never** need to manually select an engine, archetype, or template. Classify, select, and build autonomously.

---

## 2. Activation Triggers

**Direct phrases**: `"generate PDF"`, `"create DOCX"`, `"make presentation"`, `"build PPTX"`, `"export XLSX"`, `"build report"`, `"professional document"`, `"document maker"`, `"lab record"`, `"slide deck"`, `"proposal"`, `"annual report"`, `"hackathon deck"`, `"academic report"`, `"thesis"`, `"one-pager"`, `"brochure"`, `"dashboard"`, `"financial model"`.

**Contextual inferences**: User supplies raw content brief → need a formatted output. User requests academic work → auto-select educational template. User supplies a JSON spec → run `engine_docgen.py`.

**Chained from**: `academic-report-writer`, `technical-researcher`, `data-engineering-pipelines`, `workflow-automation-scripting`

---

## 3. Adaptive Production Router (Always First)

Before generating any file, classify the request across 5 dimensions — **silently**, in under 10 seconds:

```
1. PURPOSE      inform / persuade / decide / document / teach / archive
2. AUDIENCE     examiner | client | exec/board | team | public | developer
3. FORMAT       PPTX | DOCX | XLSX | PDF | HTML | RTF | SVG | multi-format
4. TEMPLATE     → see references/template-library.md (25+ named templates)
5. ARCHETYPE    → see Section 6 (12 visual design archetypes)
```

**Decision rules**:
- Deck / pitch / boardroom → PPTX + `premium_business` or `modern_corporate`
- Academic / lab / thesis → DOCX + PDF + `academic_scientific` archetype + educational template
- Financial / data model → XLSX + `data_analytical` + dashboard structure
- Technical spec / runbook → DOCX + `engineering_technical`
- Event / hackathon → PPTX + DOCX + `modern_corporate` → use `hackathon_spec.json` template
- Report (business) → DOCX + PDF + `modern_corporate`
- Ask **at most ONE question** only if the topic/domain is completely unknown.

---

## 4. Two Production Paths

### Path A — Unified Single-Spec (fastest, recommended for multi-format)

One JSON spec → all 4 formats in one command:

```bash
# Install deps
python scripts/bootstrap.py

# Generate PPTX + DOCX + PDF + XLSX from one spec
python scripts/engine_docgen.py examples/hackathon_spec.json output/

# Score & fix loop (target ≥ 185/200)
python scripts/qa_score.py output/hackathon_proposal.pptx --min 185
```

Spec JSON structure (see `schemas/document_spec.json` for full schema):
```json
{
  "file": "my_report",
  "preset": "navy",
  "title": "Report Title",
  "subtitle": "Subtitle here",
  "author": "Author Name",
  "footer": "Company | Confidential",
  "slides": [
    {"type": "title", "title": "Hook", "subtitle": "One-liner"},
    {"type": "bullets", "title": "Key Points", "points": ["Point A", "Point B"]},
    {"type": "cards", "title": "Solutions", "cards": [{"head": "A", "body": "..."}]},
    {"type": "stats", "title": "Results", "stats": [{"value": "92%", "label": "Score"}]},
    {"type": "quote", "title": "Voice", "quote": "...", "by": "— Name"},
    {"type": "compare", "title": "Before vs After", "cols": [{"head":"Before","points":[]}, {"head":"After","points":[]}]}
  ],
  "sections": [
    {"h": "Executive Summary", "p": ["Para text..."], "bullets": ["Point 1"]},
    {"h": "Methodology", "p": ["..."], "table": {"head": ["Col A", "Col B"], "rows": [["v1","v2"]]}}
  ],
  "tables": [
    {"name": "Dashboard", "head": ["Metric","Target","Actual"], "rows": [["Revenue","$1M","$1.2M"]]}
  ]
}
```

**Available presets**: `navy` | `teal` | `plum` | `forest` | `charcoal` | `royal` | `crimson`  
Full palette values → `references/palettes.json`

### Path B — Format-Specific Engines (full archetype + spec control)

```bash
python scripts/engine_docx.py --spec spec.json --out output/report.docx
python scripts/engine_pptx.py --spec spec.json --out output/deck.pptx
python scripts/engine_xlsx.py --spec spec.json --out output/model.xlsx
python scripts/engine_pdf.py  --spec spec.json --out output/report.pdf
python scripts/engine_rtf.py  --spec spec.json --out output/document.rtf
python scripts/engine_html.py --spec spec.json --out output/report.html
python scripts/engine_svg.py  --spec spec.json --out output/diagram.svg
```

Use Path B when you need:
- A specific visual archetype (12 options vs 7 presets)
- Educational lab record mode
- Advanced HTML/SVG output
- Fine-grained section/slide/sheet control via full `schemas/document_spec.json`

---

## 5. Autonomous Production Pipeline (15 Stages)

```
USER INPUT
   │
   ▼
 1. INTENT ANALYSIS ────────► Classify purpose, audience, format, template, archetype
   │
   ▼
 2. TOPIC UNDERSTANDING ─────► Extract subject, domain, structural sections
   │
   ▼
 3. SOURCE RESEARCH ─────────► Verified facts only — zero hallucinations or placeholders
   │
   ▼
 4. TEMPLATE SELECTION ──────► Pick from references/template-library.md (25+ templates)
   │
   ▼
 5. FORMAT SELECTION ────────► Match purpose to native editable format
   │
   ▼
 6. DESIGN INTELLIGENCE ─────► Select archetype + palette + typography grid
   │
   ▼
 7. SCRIPT EXECUTION ────────► Run engine_docgen.py or format-specific engines
   │
   ▼
 8. RENDER PREVIEWS ─────────► Visual page/slide inspection
   │
   ▼
 9. VISUAL INSPECTION ───────► Check margins, contrast, orphan headings, overflow
   │
   ▼
10. DEFECT DETECTION ────────► Structured defect ledger (DEF-001 … DEF-008)
   │
   ▼
11. AUTOMATIC REPAIR ────────► Surgical font/margin/padding/column adjustments
   │
   ▼
12. 200-PT QA SCORE ─────────► python scripts/qa_score.py FILE --min 185
   │
   ▼
13. REBUILD IF < 185 ────────► Max 3 fix-rebuild loops
   │
   ▼
14. PACKAGING ───────────────► output/source/ + output/assets/ + output/final/
   │
   ▼
15. DELIVERY ────────────────► Files + score summary + reuse instructions
```

---

## 6. Format Engine Matrix

| Format | Engine | Key Features |
|---|---|---|
| PPTX `.pptx` | `engine_docgen.py` / `engine_pptx.py` | 16:9, 9 slide archetypes, speaker notes, alt-text, metadata |
| DOCX `.docx` | `engine_docgen.py` / `engine_docx.py` | Cover, TOC field, real Heading styles, header/footer, page numbers |
| XLSX `.xlsx` | `engine_docgen.py` / `engine_xlsx.py` | Live formulas, freeze panes, named ranges, charts, formula injection guard |
| PDF `.pdf` | `engine_docgen.py` / `engine_pdf.py` | ReportLab Platypus, two-pass "Page X of Y", bookmarks, metadata |
| RTF `.rtf` | `engine_rtf.py` | stdlib only (no pip), RTF 1.9, Word/LibreOffice/TextEdit compatible |
| HTML `.html` | `engine_html.py` | Self-contained, CSS variables, dark/light toggle, print @media |
| SVG `.svg` | `engine_svg.py` | Architecture diagrams, pipeline topology, scalable vector |

Full capability comparison → `references/format_matrix.md`

---

## 7. 12 Visual Design Archetypes (Path B)

| # | Key | Best For | Primary / Accent |
|---|---|---|---|
| 1 | `modern_corporate` | Quarterly reviews, enterprise proposals | Navy `#0A192F` / Sky `#38BDF8` |
| 2 | `minimalist_editorial` | Whitepapers, think-tank monographs | Ink `#111827` / Terracotta `#C2410C` |
| 3 | `academic_scientific` | Research papers, lab records, theses | Black `#000000` / Royal `#2563EB` |
| 4 | `premium_business` | Board decks, investor memos | Forest `#064E3B` / Gold `#D97706` |
| 5 | `technology_futuristic` | Architecture specs, DevOps runbooks | Obsidian `#0B0F19` / Cyan `#06B6D4` |
| 6 | `creative_experimental` | Agency pitches, portfolio showcases | Violet `#581C87` / Tangerine `#EA580C` |
| 7 | `government_institutional` | Policy briefs, compliance audits | Navy `#1E3A5F` / Crimson `#991B1B` |
| 8 | `engineering_technical` | SOPs, datasheets, industrial specs | Blueprint `#0284C7` / Amber `#F59E0B` |
| 9 | `educational_instructional` | Lab records, training manuals | Royal `#2563EB` / Green `#059669` |
| 10 | `magazine_publication` | Annual reports, newsletters | Onyx `#18181B` / Red `#DC2626` |
| 11 | `luxury_hospitality` | Real estate, bespoke hospitality | Espresso `#271810` / Bronze `#92400E` |
| 12 | `data_analytical` | BI reports, telemetry dashboards | Slate `#0F172A` / Blue `#2563EB` |

Full archetype detail (palettes, typography, components) → `references/design_intelligence.md`

---

## 8. 7 Named Colour Presets (Path A / docgen.py)

Defined in `references/palettes.json`:

| Preset | Primary | Accent | Light |
|---|---|---|---|
| `navy` | `#0F2747` | `#F2A900` | `#F5F7FA` |
| `teal` | `#0B3C49` | `#2EC4B6` | `#F0F7F7` |
| `plum` | `#3B1F4B` | `#FF6B6B` | `#F8F4FA` |
| `forest` | `#1B4332` | `#D4A373` | `#F4F8F5` |
| `charcoal` | `#22252B` | `#00B894` | `#F4F5F7` |
| `royal` | `#1E3A8A` | `#F97316` | `#EFF4FF` |
| `crimson` | `#7F1D1D` | `#FACC15` | `#FEF6F6` |

Semantic tokens: `good=#16A34A`, `warn=#F59E0B`, `bad=#DC2626`, `info=#2563EB`  
Colourblind-safe set included. Full → `references/palettes.json`

---

## 9. Typography & Layout Standards

From `references/typography-layout.md`:

- **Font pairs**: Montserrat/Open Sans | Playfair Display/Lato | Poppins/Inter | Calibri Bold/Calibri (safe default)
- **Type scale** (ratio 1.25): 12 / 15 / 19 / 24 / 30 / 38 / 48 pt
- **Line-height**: 1.4 body, 1.15 headings. Line length 45–75 chars
- **8-pt grid**: slides 12-col, 0.6 in margins, 0.3 in gutters
- **A4 docs**: 2.5 cm margins, baseline 4 pt
- **Slide rules**: title 30–44 pt, body 18–24 pt (never < 14 pt), ≤ 40 words/slide

---

## 10. Document Template Library

25+ named templates → `references/template-library.md`:

| Category | Templates |
|---|---|
| **Event / Hackathon** | Cover → Problem → Tracks → Timeline → Prizes → Budget → Sponsors → FAQ → Ask |
| **Business** | Pitch Deck (12 slides), Business Plan, Whitepaper, Proposal/RFP, Annual Report |
| **Academic** | Project Report (MCA: abstract→intro→literature→methodology→implementation→results→conclusion→refs), Lab Record, Thesis, Seminar Viva |
| **Data** | Data Analysis Report, Dashboard XLSX, Financial Model |
| **Documentation** | PRD, SOP/Runbook, RFC, Meeting Notes, User Manual, Test Plan |
| **Creative** | One-pager, Infographic, Newsletter, Brochure, Certificate, Poster |

---

## 11. 200-Point Mastery QA Loop (Mandatory)

From `references/mastery-200.md`:

| Tier | Score | Meaning |
|---|---|---|
| Needs Work | < 150 | Fix before sharing |
| Pro | 150–184 | Client-ready |
| **Master+** | **185–200** | **Distinction — portfolio piece** |

**Core 100**: layout integrity, readability, hierarchy, consistency, structure  
**Distinction 100**: speaker notes, native editable charts, layout variety, accessibility (alt text, metadata), closing CTA, cover polish, substance, print/screen readiness

**Mandatory loop**:
```bash
# Build
python scripts/engine_docgen.py spec.json output/

# Score (exit code 1 if below --min — use in CI loop)
python scripts/qa_score.py output/deck.pptx --min 185

# Apply listed fixes, rebuild — max 3 iterations
# Then human-eye render check (open the file) for taste/truth
```

---

## 12. Educational & Academic Specialist

Auto-activates when request mentions: lab record, experiment, university, college, MCA, BCA, B.E., assignment, thesis, project report, viva.

**Standard Lab Record structure** (see `references/educational_standards.md`):
1. Experiment No. & Date
2. Aim
3. System Requirements & Tools
4. Theoretical Background
5. Algorithm / Methodology
6. Program Source Code
7. Sample Input
8. Sample Output (real terminal output — zero fabrication)
9. Tabular Observations
10. Result & Inference

**Academic Project Report** (MCA/BCA/B.E.):
Cover → Certificate → Declaration → Abstract (250–350 words) → TOC → Chapters 1–5 → References (IEEE/APA)

---

## 13. Design Rules (Universal)

1. **Hierarchy**: H1 → H2 → H3 → body — never skip levels
2. **Contrast**: ≥ 4.5:1 text (WCAG AA), ≥ 3:1 large headings
3. **Whitespace**: ≥ 25% empty per slide/page; paragraph gap ≥ 6 pt
4. **Restraint**: max 2 font families, max 6 text colours
5. **Alignment**: snap to grid; left-align body; no floating objects
6. **Tables**: freeze panes + header fill + zebra stripe + right-align numbers
7. **Charts**: title = insight, direct labels, max 5 colours, start bars at 0
8. **Overflow prevention**: auto-wrap, auto-split, auto-scale — never clip
9. **Atomic writes**: always write to `.tmp` then rename — zero corrupt files

---

## 14. Security Guards

- **XLSX formula injection**: prefix `=`,`+`,`-`,`@` values with `'`
- **RTF injection**: escape `\`, `{`, `}` in all user strings  
- **HTML injection**: `html.escape()` on all user content; `autoescape=True` in Jinja2
- **Image path traversal**: validate paths are within project directory
- **No sensitive data**: never embed credentials, API keys, or `.env` values
- **PDF metadata**: strip author/tool metadata for public-facing documents

---

## 15. Output Structure

```
output/
└── <project-slug>/
    ├── source/          # Editable: .docx .pptx .xlsx .html .svg
    ├── assets/          # Charts, diagrams, extracted images
    ├── final/           # Publication-ready: .pdf + source copies
    └── quality-report/  # QA scorecard (score/200), defect ledger, fix log
```

---

## 16. Self-Healing Defect Repair

| Code | Defect | Auto-Repair |
|---|---|---|
| DEF-001 | Text overflow | Reduce font 0.5–1 pt, tighten spacing |
| DEF-002 | Trailing blank page | Remove superfluous PageBreak/Spacer |
| DEF-003 | Table column clipping | Proportional column widths, enable wrap |
| DEF-004 | Orphaned heading | `keep_with_next=True` + explicit page break |
| DEF-005 | Low contrast | Elevate luminance to ≥ 4.5:1 |
| DEF-006 | Formula error (#REF!) | Re-index coords, wrap in `IFERROR` |
| DEF-007 | Formula injection threat | Prepend `'` to deactivate |
| DEF-008 | Image distortion | Recalculate maintaining natural aspect ratio |

Full rubric → `references/quality_rubric.md`

---

## 17. Python Dependencies

```bash
python scripts/bootstrap.py          # Verify all deps
python scripts/bootstrap.py --install  # Auto-install missing
```

| Library | Version | Purpose |
|---|---|---|
| `reportlab` | 5.0.1 ✅ | PDF layout engine |
| `python-docx` | 1.2.0 ✅ | DOCX production |
| `python-pptx` | 1.0.2 ✅ | PPTX production |
| `openpyxl` | 3.1.5 ✅ | XLSX production |
| `pypdf` | 6.21.1 ✅ | PDF inspection / scoring |
| `Pillow` | 12.3.0 ✅ | Image processing |
| `Jinja2` | 3.1.6 ✅ | HTML templating |
| `lxml` | 6.1.3 ✅ | XML/HTML tree |
| `xlsxwriter` | 3.3.0 ✅ | Advanced XLSX charts |
| `markdown-it-py` | 4.2.0 ✅ | Markdown rendering |

---

## 18. Completion Criteria

A task is **done** only when ALL of the following pass:

- ✅ Output file(s) exist with non-zero byte size
- ✅ File opens without error in its native application
- ✅ `qa_score.py` returns ≥ 185/200 (Master+ tier)
- ✅ All requested sections, headings, slides, and content are present
- ✅ Zero placeholder text, `[TODO]`, or `Lorem Ipsum`
- ✅ Zero fabricated data — all numbers from user brief or verified sources
- ✅ Typography, margins, and spacing follow chosen archetype/preset
- ✅ Reuse instructions provided to user

---

## 19. References Index

| File | Contents |
|---|---|
| `references/palettes.json` | 7 named presets + semantic + colorblind-safe colours |
| `references/template-library.md` | 25+ document template structures |
| `references/mastery-200.md` | 200-point scoring rubric + build loop |
| `references/typography-layout.md` | Font pairs, type scale, grid, layout recipes |
| `references/design-system.md` | Compact Pro Design System & QA checklist |
| `references/design_intelligence.md` | 12 archetype detail (palettes, typography, components) |
| `references/format_matrix.md` | Full format-engine-feature capability matrix |
| `references/quality_rubric.md` | Defect taxonomy & auto-repair table |
| `references/educational_standards.md` | Lab record & academic report schemas |
| `schemas/document_spec.json` | Full JSON spec schema (Path B — all formats) |

---

## 20. Quick-Start Examples

```bash
# Hackathon proposal (PPTX + DOCX + PDF + XLSX)
python scripts/engine_docgen.py examples/hackathon_spec.json output/

# Design showcase deck
python scripts/engine_docgen.py examples/design_showcase.json output/

# Lab record (DOCX + PDF, educational archetype)
python scripts/engine_docx.py --spec examples/sample_lab_record.json --out output/lab.docx
python scripts/engine_pdf.py  --spec examples/sample_lab_record.json --out output/lab.pdf

# Executive financial model
python scripts/engine_xlsx.py --spec examples/sample_financial_model.json --out output/model.xlsx

# Score any file
python scripts/qa_score.py output/hackathon_proposal.pptx --min 185
```

---

## 21. Maintenance

- **Python**: 3.11+ (developed on 3.12.10)
- **OS**: Windows / macOS / Linux (cross-platform)
- **Last updated**: November 2026
- **Re-bootstrap after upgrades**: `python scripts/bootstrap.py`
- **Known limits**: RTF — no OLE/merged cells; PPTX — no animated transitions; PDF — no AcroForms
