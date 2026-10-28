# Engine Selection Matrix — document-maker-all-format

## Format → Engine → Library Mapping

| Format | Extension | Primary Engine | Library | Version | Install Status |
|:---|:---|:---|:---|:---|:---|
| **PDF** | `.pdf` | ReportLab | `reportlab` | 5.0.1 | ✅ Installed |
| **DOCX** | `.docx` | python-docx | `python-docx` | 1.2.0 | ✅ Installed |
| **PPTX** | `.pptx` | python-pptx | `python-pptx` | 1.0+ | ✅ Installed (bootstrap) |
| **XLSX** | `.xlsx` | openpyxl | `openpyxl` | 3.1.5 | ✅ Installed |
| **RTF** | `.rtf` | Custom RTF Writer | `stdlib` | builtin | ✅ No install needed |
| **HTML** | `.html` | Jinja2 + lxml | `Jinja2`, `lxml` | 3.1.6 / 6.1.3 | ✅ Installed |
| **Markdown** | `.md` | markdown-it-py | `markdown-it-py` | 4.2.0 | ✅ Installed |
| **Plain Text** | `.txt` | stdlib textwrap | `textwrap` | builtin | ✅ No install needed |

---

## Engine Capability Matrix

| Capability | PDF | DOCX | PPTX | XLSX | RTF | HTML | MD | TXT |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Cover page | ✅ | ✅ | ✅ | — | ✅ | ✅ | — | — |
| Styled headings (H1–H3) | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| Body paragraphs | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| Bullet lists | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| Tables | ✅ | ✅ | ⬜ | ✅ | ✅ | ✅ | ✅ | — |
| Formulas / calculations | — | — | — | ✅ | — | — | — | — |
| Charts | — | — | — | ✅ | — | — | — | — |
| Image embedding | ✅ | ✅ | ✅ | — | — | ✅ | ✅ | — |
| Page numbering | ✅ | ✅ | ✅ | — | ✅ | — | — | — |
| Headers & footers | ✅ | ✅ | ✅ | — | ✅ | ✅ | — | — |
| Font embedding | ✅ | ✅ | ✅ | ✅ | — | — | — | — |
| Unicode / multilingual | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| PDF/A compatibility | ⬜ | — | — | — | — | — | — | — |
| Editable in native app | — | ✅ | ✅ | ✅ | ✅ | — | — | — |
| Printable | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | — |

✅ = Supported | ⬜ = Partial / Planned | — = Not applicable

---

## Optional Enhancement Tools

| Tool | Purpose | How to Install | Impact |
|:---|:---|:---|:---|
| `pandoc` | Universal format conversion (MD↔DOCX, HTML↔PDF, etc.) | System package manager | Enables cross-format conversion pipelines |
| `weasyprint` | HTML → PDF with full CSS3 support | `pip install weasyprint` | Better HTML→PDF than ReportLab for CSS-styled docs |
| `xlsxwriter` | Advanced XLSX chart generation | `pip install xlsxwriter` | Richer chart types than openpyxl |
| `pypandoc` | Python wrapper for pandoc | `pip install pypandoc` | Programmatic pandoc access |

---

## Engine Selection Decision Tree

```
User requests a document output format
           │
     ┌─────▼──────┐
     │ Is it PDF? │──YES──► reportlab 5.x (generate_pdf.py)
     └─────┬──────┘
           │NO
     ┌─────▼──────┐
     │ Is it DOCX?│──YES──► python-docx 1.2 (generate_docx.py)
     └─────┬──────┘
           │NO
     ┌─────▼──────┐
     │ Is it PPTX?│──YES──► python-pptx (generate_pptx.py)
     └─────┬──────┘
           │NO
     ┌─────▼──────┐
     │ Is it XLSX?│──YES──► openpyxl 3.x (generate_xlsx.py)
     └─────┬──────┘
           │NO
     ┌─────▼──────┐
     │ Is it RTF? │──YES──► Custom RTF writer (generate_rtf.py)
     └─────┬──────┘
           │NO
     ┌─────▼──────┐
     │ Is it HTML?│──YES──► Jinja2 + lxml
     └─────┬──────┘
           │NO
     ┌─────▼────────┐
     │ Is it MD/TXT?│──YES──► markdown-it-py / textwrap
     └─────┬────────┘
           │NO
     ┌─────▼────────────────┐
     │ Unknown format?      │──► Ask user for clarification
     └──────────────────────┘
```

---

## Shared Design System Tokens

```python
DESIGN_SYSTEM = {
    # Page geometry (A4 in points: 1pt = 1/72 inch)
    "page_width_pt":   595.27,
    "page_height_pt":  841.89,
    "margin_top_pt":   170.08,   # 2.5cm
    "margin_bottom_pt":170.08,
    "margin_left_pt":  141.73,   # 2.0cm
    "margin_right_pt": 141.73,

    # Typography (all sizes in pt)
    "font_heading":    "Helvetica-Bold / Calibri Bold / Arial Bold",
    "font_body":       "Helvetica / Calibri / Arial",
    "font_mono":       "Courier New",
    "size_cover":      32,
    "size_h1":         26,
    "size_h2":         18,
    "size_h3":         14,
    "size_body":       11,
    "size_caption":    9,
    "size_footer":     8,
    "leading_body":    16,       # line height for body text

    # Colors (hex)
    "color_primary":   "#1A3380",  # deep navy
    "color_accent":    "#F29910",  # amber
    "color_body":      "#262626",  # near-black
    "color_muted":     "#8C8C8C",  # grey
    "color_bg_light":  "#F5F7FA",  # table alt row background
    "color_white":     "#FFFFFF",

    # Spacing
    "para_gap_pt":     6,          # space after paragraph
    "section_gap_pt":  18,         # space between sections
    "table_padding_pt":6,          # cell padding
    "image_padding_pt":6,          # image margins
}
```

