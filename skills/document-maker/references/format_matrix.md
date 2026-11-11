# Unified Format Matrix & Engine Selection Guide

This matrix specifies the supported formats, runtime engines, library dependencies, and feature coverage for `document-maker`.

---

## 1. Format-to-Engine Mapping

| Format | Extension | Primary Engine | Library Dependency | Install Status | Editability | Best Use Case |
|---|---|---|---|---|:---:|---|
| **Microsoft Word** | `.docx` | `engine_docx.py` | `python-docx` $\ge 1.1$ | ✅ Installed | Full Native | Enterprise reports, proposals, formal documentation |
| **Microsoft PowerPoint** | `.pptx` | `engine_pptx.py` | `python-pptx` $\ge 1.0$ | ✅ Installed | Full Native | Executive decks, board briefings, tech roadmaps |
| **Microsoft Excel** | `.xlsx` | `engine_xlsx.py` | `openpyxl` $\ge 3.1$ | ✅ Installed | Full Native | Financial models, KPI matrices, audit schedules |
| **Adobe PDF** | `.pdf` | `engine_pdf.py` | `reportlab` $\ge 4.0$ + `pypdf` | ✅ Installed | Publication Export | Formal publications, print-ready records, legal filings |
| **Rich Text Format** | `.rtf` | `engine_rtf.py` | Builtin `stdlib` (No pip) | ✅ Builtin | High Native | Cross-platform compatibility, legacy systems, WordPad |
| **Responsive Web** | `.html` | `engine_html.py` | Builtin `stdlib` / `Jinja2` | ✅ Builtin | Digital Interactive | Browser-viewable reports, interactive dark-mode docs |
| **Vector Graphic** | `.svg` | `engine_svg.py` | Builtin XML generator | ✅ Builtin | Infinite Scale | System architecture diagrams, workflow schematics |
| **Markdown** | `.md` | Plaintext Markdown generator | Builtin `stdlib` | ✅ Builtin | Raw Source | Developer READMEs, technical knowledge base |
| **Plain Text** | `.txt` | `stdlib textwrap` generator | Builtin `stdlib` | ✅ Builtin | Text Only | Raw logs, plain transcripts, batch dumps |

---

## 2. Deep Engine Feature Comparison

| Capability | DOCX | PPTX | XLSX | PDF | RTF | HTML | SVG |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Hero / Cover Page** | ✅ | ✅ | ⬜ | ✅ | ✅ | ✅ | ✅ |
| **Multi-Level Headings** | ✅ | ✅ | ⬜ | ✅ | ✅ | ✅ | ⬜ |
| **Dynamic Header & Footer** | ✅ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ⬜ |
| **Two-Pass "Page X of Y"** | ✅ | ✅ | ⬜ | ✅ | ✅ | ⬜ | ⬜ |
| **Card / Bento Containers** | ✅ | ✅ | ⬜ | ✅ | ⬜ | ✅ | ✅ |
| **Zebra Striped Tables** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ |
| **Live Spreadsheets Formulas** | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| **Freeze Panes** | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| **Syntax-Highlighted Code** | ✅ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ⬜ |
| **Callout Boxes (Warning/Tip)** | ✅ | ✅ | ⬜ | ✅ | ⬜ | ✅ | ✅ |
| **Formula Injection Defense** | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| **RTF Control-Word Escaping** | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| **HTML Autoescape Guard** | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ |
| **Visual QA Previews** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Automated Repair Loop** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

*Legend: ✅ Fully Supported | ⬜ Not Applicable to this format*

---

## 3. Atomic Write Architecture

All generation engines in `document-maker` strictly implement the **Atomic File Write Pattern**:
1. Documents are generated into an isolated temporary file (`.tmp.<ext>`).
2. The file is validated for non-zero byte size and magic header integrity.
3. Upon validation success, the temp file atomically replaces the final destination.
4. On any failure, the temporary file is unlinked immediately, ensuring zero zero-byte or corrupt files are ever delivered to the user.

---

## 4. Optional Tool Extensions

| Tool | Enhancement Provided | Installation Command |
|---|---|---|
| `pandoc` | Universal cross-format conversion (Markdown $\leftrightarrow$ DOCX/PDF) | `winget install JohnMacFarlane.Pandoc` |
| `weasyprint` | CSS3 Paged Media rendering (HTML $\rightarrow$ Pixel-perfect PDF) | `pip install weasyprint` |
| `xlsxwriter` | Advanced native chart embedding in Excel | `pip install xlsxwriter` |
| `pdf2image` + `poppler` | Direct high-resolution multi-page PDF rasterization | System poppler binaries |

