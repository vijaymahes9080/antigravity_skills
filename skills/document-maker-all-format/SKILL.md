---
name: document-maker-all-format
description: Design, generate, edit, render, validate, and export professional PDFs, DOCX documents, PPTX presentations, XLSX spreadsheets, RTF files, and other supported document formats with flexible layouts and consistent visual quality.
---

# Professional Document Studio — All-Format Document Maker

## 1. Intended Role & Domain

- **Primary Domain**: Research, Docs & Communication
- **Target Roles**: Document Generation Engineer, Technical Report Designer, Presentation Architect, Spreadsheet Engineer
- **Architectural Layer**: Layer 2 (Specialized Technical Skills) — Master-level multi-format engine
- **Skill Status**: Active Specialist
- **Slash Commands**: `/document-maker-all-format`, `/doc-maker`, `/document-studio`

---

## 2. Activation Conditions

- **Direct Triggers**:
  `"generate PDF"`, `"create DOCX"`, `"make presentation"`, `"build PPTX"`, `"export XLSX"`,
  `"build report"`, `"document template"`, `"convert to PDF"`, `"create spreadsheet"`,
  `"write RTF"`, `"make report"`, `"professional document"`, `"document maker"`,
  `"export report"`, `"generate slides"`, `"all format document"`, `"document studio"`

- **Contextual Inferences**:
  - User requests academic, technical, or business reports in any structured format.
  - User asks to convert content briefs into formatted output files.
  - User needs reusable document templates, cover pages, or multi-section layouts.
  - User needs validated, openable, visually consistent output files.

- **Chained Predecessors**: `academic-report-writer`, `technical-researcher`, `workflow-automation-scripting`, `data-architecture-system-design`
- **Chained Successors**: `software-api-documentation-openapi`, `software-code-review-quality`

---

## 3. Explicit Exclusions

- Do **NOT** use when:
  - Building interactive web application UI components or SPA pages → use `react-nextjs-pro`
  - Designing database schemas or migrations → use `data-architecture-system-design`
  - Generating raw API documentation stubs → use `software-api-documentation-openapi`
  - Writing embedded firmware or hardware documentation
  - Fabricating citations, statistics, or source material not supplied by the user

---

## 4. Required Inputs & Context

Collect the following before generating any document:

| Input | Required | Notes |
|:---|:---:|:---|
| Content brief or raw content | ✅ | Text, bullet points, or structured data |
| Target format(s) | ✅ | PDF, DOCX, PPTX, XLSX, RTF, HTML, MD, TXT |
| Document title & author | ✅ | For headers, covers, and metadata |
| Audience & purpose | ✅ | Academic, executive, technical, internal |
| Page size & orientation | ⬜ | Default: A4 portrait |
| Brand colors & fonts | ⬜ | Default: neutral professional theme |
| Asset paths (images, logos) | ⬜ | Embedded if provided |
| Section structure / outline | ⬜ | Auto-generated from content if omitted |

If required inputs are missing, **ask before generating** — never assume or fabricate.

---

## 5. Expected Outputs & Artifacts

For every document generation task, deliver:

1. **Generated file(s)** in the requested format(s) — written to `./output/` or a user-specified path.
2. **Validation report** — `validate_doc.py` output confirming file integrity, page/slide count, text extractability, and any detected issues.
3. **Bootstrap confirmation** — confirmation that all required libraries are installed (`scripts/bootstrap.py`).
4. **Reuse instructions** — how to re-run generation with a different theme, content, or layout.
5. **Known limitations** — any format-specific constraints honestly documented.

---

## 6. Step-by-Step Operating Procedure

### Step 1 — Inspect

```python
# Run bootstrap to confirm environment
python scripts/bootstrap.py

# Probe existing files and assets
import pathlib
assets = list(pathlib.Path(".").rglob("*.png")) + list(pathlib.Path(".").rglob("*.jpg"))
existing_docs = list(pathlib.Path(".").rglob("*.pdf")) + list(pathlib.Path(".").rglob("*.docx"))
print(f"Assets found: {len(assets)} | Existing docs: {len(existing_docs)}")
```

Inspect:
- User-supplied content brief and structured data
- Available image/logo assets and their paths
- Installed libraries via `bootstrap.py`
- Existing document templates to reuse or avoid conflicts

### Step 2 — Plan

Select the generation engine using the **Engine Selection Matrix** (see `references/engine_matrix.md`):

| Format | Primary Engine | Library Version |
|:---|:---|:---|
| PDF | `reportlab` | 5.0+ |
| DOCX | `python-docx` | 1.2+ |
| PPTX | `python-pptx` | 1.0+ |
| XLSX | `openpyxl` | 3.1+ |
| RTF | Custom RTF writer | stdlib only |
| HTML | `Jinja2` + `lxml` | 3.1+ / 6.0+ |
| Markdown | `markdown-it-py` | 4.0+ |
| Plain Text | stdlib `textwrap` | stdlib |

Define the **Shared Design System**:

```python
DESIGN_SYSTEM = {
    "page_width_pt":  595.27,   # A4 width in points
    "page_height_pt": 841.89,   # A4 height in points
    "margin_pt":      56.69,    # 2 cm margins
    "font_heading":   "Helvetica-Bold",
    "font_body":      "Helvetica",
    "font_mono":      "Courier",
    "size_h1":        24,
    "size_h2":        18,
    "size_h3":        14,
    "size_body":      11,
    "size_caption":   9,
    "color_primary":  (0.10, 0.20, 0.50),   # deep navy (RGB 0–1)
    "color_accent":   (0.95, 0.60, 0.10),   # amber
    "color_body":     (0.15, 0.15, 0.15),   # near-black
    "color_muted":    (0.55, 0.55, 0.55),   # grey
    "line_spacing":   1.4,
    "paragraph_gap":  6,        # points after each paragraph
}
```

### Step 3 — Design

Apply these rules before generating any output:

1. **Hierarchy**: H1 → H2 → H3 → body — never skip levels.
2. **Grid alignment**: all elements align to consistent margins; no free-floating objects.
3. **Whitespace**: paragraph gap ≥ 6pt; section gap ≥ 18pt.
4. **Typography**: body 10–12pt; headings 14–24pt; captions 8–10pt.
5. **Overflow prevention**: wrap long text, tables, and URLs; never let text clip page edges.
6. **Pagination**: keep headings with their first paragraph; avoid orphan lines.
7. **Numbering**: auto page numbers in footer; figure/table captions numbered sequentially.
8. **Tables**: minimum column widths; header row styled differently; cell padding ≥ 4pt.
9. **Images**: aspect ratio preserved; never stretched; surrounded by at least 6pt padding.
10. **Theme consistency**: use `DESIGN_SYSTEM` tokens throughout — no hard-coded ad hoc values.

### Step 4 — Generate

Use the format-specific helper scripts:

```bash
# PDF
python scripts/generate_pdf.py --title "Report" --author "Author" --output output/report.pdf

# DOCX
python scripts/generate_docx.py --title "Report" --output output/report.docx

# PPTX
python scripts/generate_pptx.py --title "Presentation" --output output/slides.pptx

# XLSX
python scripts/generate_xlsx.py --title "Data Sheet" --output output/data.xlsx

# RTF
python scripts/generate_rtf.py --title "Document" --output output/document.rtf
```

Rules during generation:
- Build from **structured content and reusable templates** — never hard-code text positions.
- Embed fonts or use safe standard fallbacks (Helvetica, Times, Courier).
- Validate asset paths before embedding — skip missing images and log a warning.
- Write to a **temp file first**, then atomically rename to final destination.
- Keep generation **deterministic** — same input → same output every run.

### Step 5 — Validate

```bash
python scripts/validate_doc.py --file output/report.pdf
python scripts/validate_doc.py --file output/report.docx
python scripts/validate_doc.py --smoke-test   # validates all generated files
```

Checks performed per format:

| Check | PDF | DOCX | PPTX | XLSX | RTF/HTML/MD |
|:---|:---:|:---:|:---:|:---:|:---:|
| File exists & non-zero size | ✅ | ✅ | ✅ | ✅ | ✅ |
| Magic bytes / extension match | ✅ | ✅ | ✅ | ✅ | ✅ |
| Opens without error | ✅ | ✅ | ✅ | ✅ | ✅ |
| Page/slide/sheet count > 0 | ✅ | — | ✅ | ✅ | — |
| Text extractable | ✅ | ✅ | ✅ | ✅ | ✅ |
| No overflow / clipping detected | ✅ | ✅ | ✅ | — | — |
| Images present if expected | ✅ | ✅ | ✅ | — | — |
| Numbering & headings intact | ✅ | ✅ | ✅ | — | ✅ |

### Step 6 — Refine

Fix defects in priority order:

1. **Critical**: File corruption, zero-size output, unopenable file.
2. **High**: Text overflow, clipped content, wrong page count.
3. **Medium**: Alignment drift, inconsistent spacing, font substitution.
4. **Low**: Minor decorative tweaks, caption re-numbering.

After each fix, re-run `validate_doc.py` for the affected format.

### Step 7 — Deliver

Provide:
- Generated file paths with sizes
- Validation report summary
- Reuse instructions (how to change theme / content)
- Any unresolved limitations and their impact

---

## 7. Repository Inspection & Planning Requirements

```powershell
# Check for existing documents
Get-ChildItem -Recurse -Include "*.pdf","*.docx","*.pptx","*.xlsx","*.rtf" | Select-Object FullName, Length

# Verify Python libraries
python scripts/bootstrap.py

# Find image assets
Get-ChildItem -Recurse -Include "*.png","*.jpg","*.svg" | Select-Object FullName
```

**Preservation rules**:
- Never overwrite user-supplied source files.
- Always write output to `./output/` or a named subdirectory.
- Never delete existing documents unless explicitly authorized.

---

## 8. Tool & Dependency Requirements

### Python Libraries (installed)

| Library | Version | Purpose |
|:---|:---|:---|
| `reportlab` | 5.0.1 ✅ | PDF generation with full layout control |
| `python-docx` | 1.2.0 ✅ | DOCX read/write/template |
| `python-pptx` | 1.0+ (bootstrap installs) | PPTX slide generation |
| `openpyxl` | 3.1.5 ✅ | XLSX with formulas, charts, styles |
| `pypdf` | 6.21.1 ✅ | PDF inspection, merge, stamp |
| `Jinja2` | 3.1.6 ✅ | HTML/template rendering |
| `lxml` | 6.1.3 ✅ | XML/HTML tree manipulation |
| `Pillow` | 12.3.0 ✅ | Image resize, format conversion |
| `markdown-it-py` | 4.2.0 ✅ | Markdown parsing & rendering |

### Optional (enhances capability)

| Tool | Purpose | Install |
|:---|:---|:---|
| `pandoc` | Universal document conversion | System package |
| `weasyprint` | HTML → PDF with CSS | `pip install weasyprint` |
| `xlsxwriter` | Advanced XLSX charts | `pip install xlsxwriter` |

### Bootstrap

```bash
python scripts/bootstrap.py
```

---

## 9. Implementation Guidelines & Best Practices

### PDF (ReportLab)

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable
)
from reportlab.lib import colors
from reportlab.lib.units import cm

def build_pdf(output_path: str, title: str, sections: list[dict]) -> None:
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
        title=title,
    )
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("H1", parent=styles["h1"], fontSize=24, spaceAfter=12)
    h2 = ParagraphStyle("H2", parent=styles["h2"], fontSize=18, spaceAfter=8)
    body = ParagraphStyle("Body", parent=styles["Normal"], fontSize=11,
                          leading=15, spaceAfter=6)
    story = []
    for section in sections:
        story.append(Paragraph(section["heading"], h2))
        story.append(Paragraph(section["content"], body))
        story.append(Spacer(1, 0.3*cm))
    doc.build(story)
```

### DOCX (python-docx)

```python
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_docx(output_path: str, title: str, sections: list[dict]) -> None:
    doc = Document()
    # Set margins
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)

    # Title
    heading = doc.add_heading(title, level=0)
    heading.runs[0].font.color.rgb = RGBColor(0x1A, 0x33, 0x80)

    for section_data in sections:
        doc.add_heading(section_data["heading"], level=2)
        para = doc.add_paragraph(section_data["content"])
        para.paragraph_format.space_after = Pt(6)

    doc.save(output_path)
```

### PPTX (python-pptx)

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def build_pptx(output_path: str, title: str, slides: list[dict]) -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.33)   # 16:9 widescreen
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]   # blank

    for slide_data in slides:
        slide = prs.slides.add_slide(blank_layout)
        # Title box
        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(1.2))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = slide_data.get("title", "")
        p.runs[0].font.size = Pt(28)
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(0x1A, 0x33, 0x80)

    prs.save(output_path)
```

### XLSX (openpyxl)

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def build_xlsx(output_path: str, title: str, sheets: list[dict]) -> None:
    wb = Workbook()
    wb.remove(wb.active)   # Remove default sheet

    for sheet_data in sheets:
        ws = wb.create_sheet(title=sheet_data["name"][:31])
        ws.sheet_view.showGridLines = True

        # Header row
        header_fill = PatternFill("solid", fgColor="1A3380")
        header_font = Font(color="FFFFFF", bold=True, size=11)
        for col_idx, header in enumerate(sheet_data.get("headers", []), start=1):
            cell = ws.cell(row=1, column=col_idx, value=header)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center")

        # Data rows
        for row_idx, row in enumerate(sheet_data.get("rows", []), start=2):
            for col_idx, value in enumerate(row, start=1):
                ws.cell(row=row_idx, column=col_idx, value=value)

        # Auto-width columns
        for col in ws.columns:
            max_len = max((len(str(c.value or "")) for c in col), default=10)
            ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 60)

    wb.save(output_path)
```

### RTF (Custom Writer)

RTF is a plain-text markup format. The custom writer in `scripts/generate_rtf.py`
outputs valid RTF 1.9 compatible with Microsoft Word, LibreOffice, and Apple TextEdit.

Key tags used:
```
{\rtf1\ansi\deff0  — RTF header
{\fonttbl ... }    — Font table
{\colortbl ... }   — Color table
\b \b0             — Bold on/off
\i \i0             — Italic on/off
\fs24              — Font size (half-points: 24 = 12pt)
\par               — Paragraph break
\page              — Page break
```

---

## 10. Error Handling & Recovery Procedures

| Error | Detection | Recovery |
|:---|:---|:---|
| `ModuleNotFoundError` for `pptx` | `ImportError` in generate_pptx.py | Run `bootstrap.py` automatically |
| Image file not found | `FileNotFoundError` during embed | Log warning, skip image, continue |
| Text overflow on PDF page | Content exceeds `DESIGN_SYSTEM["page_height_pt"]` | Auto-split into continuation page |
| DOCX table too wide | Column widths exceed page width | Auto-scale columns proportionally |
| XLSX formula error | `#REF!`, `#VALUE!` in cell | Log affected cell, replace with raw value |
| Zero-size output file | `os.path.getsize()` == 0 | Delete, raise `DocumentGenerationError`, retry |
| PPTX slide overflow | Text box content truncated by pptx | Reduce font size by 1pt until fits, min 8pt |
| Corrupt output (magic bytes mismatch) | `validate_doc.py` magic check | Delete corrupt file, regenerate from scratch |

```python
# Atomic write pattern — use for all formats
import os, tempfile, pathlib

def atomic_write(content_fn, output_path: str) -> None:
    """Write via temp file to prevent partial corruption."""
    p = pathlib.Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    try:
        content_fn(str(tmp))             # write to temp
        tmp.replace(p)                   # atomic rename
    except Exception:
        tmp.unlink(missing_ok=True)      # clean up temp on failure
        raise
```

---

## 11. Security & Privacy Constraints

- **Never embed** credentials, API keys, passwords, or `.env` values in generated documents.
- **Template injection**: Jinja2 templates must use `autoescape=True` for HTML output.
- **RTF injection**: Escape `\`, `{`, `}` characters in user-supplied strings to prevent RTF control-word injection.
- **XLSX formula injection**: Prefix strings starting with `=`, `+`, `-`, `@` with a single quote (`'`) to prevent spreadsheet formula execution.
- **Image path traversal**: Validate image paths are within the project directory before embedding.
- **PDF metadata**: Strip sensitive author/tool metadata from output PDFs when producing public-facing documents.

```python
# XLSX formula injection prevention
def safe_cell_value(value: str) -> str:
    FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")
    if isinstance(value, str) and value.startswith(FORMULA_PREFIXES):
        return "'" + value
    return value
```

---

## 12. Verification & Testing Requirements

### Automated checks (run after every generation)

```bash
# Validate single file
python scripts/validate_doc.py --file output/report.pdf

# Smoke test all outputs
python scripts/validate_doc.py --smoke-test --dir output/

# Bootstrap probe
python scripts/bootstrap.py
```

### Manual verification checklist

- [ ] File opens without error in the native application (Adobe Reader, Word, PowerPoint, Excel)
- [ ] Page/slide count matches the content brief
- [ ] All headings, sections, and numbering are intact
- [ ] Tables and images render correctly — no clipping or overflow
- [ ] Headers and footers appear on every page
- [ ] Fonts are readable and consistent
- [ ] No blank pages except intentional section breaks
- [ ] Unicode and special characters display correctly

---

## 13. Completion Criteria

A generation task is **complete** when ALL of the following are true:

1. ✅ Output file(s) exist with non-zero size.
2. ✅ `validate_doc.py` reports no critical issues.
3. ✅ File opens without error in its native application.
4. ✅ Page/slide/sheet count matches the content brief.
5. ✅ All required sections, headings, and content are present.
6. ✅ Typography, margins, and spacing follow the `DESIGN_SYSTEM`.
7. ✅ No fabricated content — all text comes from user-supplied brief.
8. ✅ Reuse instructions provided.

If any criterion fails, return to **Step 5 (Validate) → Step 6 (Refine)** before delivering.

---

## 14. Relevant Official References

- **ReportLab**: https://docs.reportlab.com/reportlab/userguide/
- **python-docx**: https://python-docx.readthedocs.io/
- **python-pptx**: https://python-pptx.readthedocs.io/
- **openpyxl**: https://openpyxl.readthedocs.io/
- **pypdf**: https://pypdf.readthedocs.io/
- **Jinja2**: https://jinja.palletsprojects.com/
- **RTF Specification 1.9**: Microsoft Open Specification (MS-RTF)
- **OOXML Standard**: ISO/IEC 29500 (DOCX/PPTX/XLSX container format)
- **PDF/A Standard**: ISO 32000-2 (PDF 2.0)
- **OpenDocument Format**: OASIS ODF 1.3

---

## 15. Maintenance & Compatibility Notes

- **Last audited**: October 2026
- **Python compatibility**: 3.11+ (developed on 3.12.10)
- **Node.js compatibility**: 20+ (developed on 24.14.0)
- **OS**: Cross-platform — Windows, macOS, Linux
- **Known limitations**:
  - RTF output: No embedded OLE objects, no complex tables with merged cells.
  - PPTX: Animated transitions not supported; static slides only.
  - PDF: No interactive form fields (AcroForms) in current version.
  - Pandoc: Not installed; install separately for advanced conversion pipelines.
- **Upgrade path**: When `pandoc` is installed, the skill auto-detects and uses it for
  advanced format conversions (MD → DOCX, HTML → PDF with full CSS support).
- **Re-bootstrap after upgrades**: Run `python scripts/bootstrap.py` whenever Python or
  pip is upgraded to confirm library compatibility.

