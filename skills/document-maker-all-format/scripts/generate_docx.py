#!/usr/bin/env python3
"""
generate_docx.py — Professional DOCX generator using python-docx.

Usage:
    python scripts/generate_docx.py --title "My Report" --author "Author" \
        --output output/report.docx [--brief brief.json]
"""
import argparse
import json
import pathlib
import sys
from datetime import datetime
from typing import Any

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    from docx.shared import Cm, Pt, RGBColor
except ImportError:
    sys.exit("❌ python-docx not installed. Run: python scripts/bootstrap.py")

# ─── Design System ───────────────────────────────────────────────────────────
NAVY  = RGBColor(0x1A, 0x33, 0x80)
AMBER = RGBColor(0xF2, 0x99, 0x10)
NEAR_BLACK = RGBColor(0x26, 0x26, 0x26)
MUTED = RGBColor(0x8C, 0x8C, 0x8C)


def _set_doc_margins(doc: Document) -> None:
    for section in doc.sections:
        section.top_margin    = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin   = Cm(2.0)
        section.right_margin  = Cm(2.0)


def _set_run_color(run, rgb: RGBColor) -> None:
    run.font.color.rgb = rgb


def _add_cover(doc: Document, title: str, author: str, subject: str) -> None:
    """Add a styled cover page."""
    doc.add_paragraph()  # top spacer
    doc.add_paragraph()

    # Title
    title_para = doc.add_paragraph()
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title_para.add_run(title)
    run.font.size = Pt(32)
    run.font.bold = True
    _set_run_color(run, NAVY)

    # Divider line (via border)
    doc.add_paragraph()

    if subject:
        sub_para = doc.add_paragraph()
        sub_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sub_run = sub_para.add_run(subject)
        sub_run.font.size = Pt(14)
        sub_run.font.italic = True
        _set_run_color(sub_run, MUTED)
        doc.add_paragraph()

    # Author + date
    meta_para = doc.add_paragraph()
    meta_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if author:
        a_run = meta_para.add_run(f"Author: {author}")
        a_run.font.size = Pt(12)
        _set_run_color(a_run, NEAR_BLACK)
        meta_para.add_run("\n")

    d_run = meta_para.add_run(datetime.now().strftime("%B %d, %Y"))
    d_run.font.size = Pt(12)
    _set_run_color(d_run, MUTED)

    doc.add_page_break()


def _add_section(doc: Document, section: dict[str, Any]) -> None:
    level   = section.get("level", 2)
    heading = section.get("heading", "")
    content = section.get("content", "")

    # Map level to Word heading style
    style_map = {1: "Heading 1", 2: "Heading 2", 3: "Heading 3"}
    style = style_map.get(level, "Heading 2")

    h = doc.add_heading(heading, level=level)
    # Override default heading color
    if h.runs:
        _set_run_color(h.runs[0], NAVY)

    # Body paragraphs
    for para_text in content.split("\n\n"):
        para_text = para_text.strip()
        if not para_text:
            continue
        para = doc.add_paragraph(para_text.replace("\n", " "))
        para.style = doc.styles["Normal"]
        para.paragraph_format.space_after = Pt(6)
        para.paragraph_format.line_spacing = Pt(16)
        if para.runs:
            para.runs[0].font.size = Pt(11)
            _set_run_color(para.runs[0], NEAR_BLACK)

    doc.add_paragraph()  # section gap


def _add_table(doc: Document, table_data: dict[str, Any]) -> None:
    headers = table_data.get("headers", [])
    rows    = table_data.get("rows", [])
    caption = table_data.get("caption", "")

    if not (headers or rows):
        return

    col_count = len(headers) if headers else (len(rows[0]) if rows else 1)
    all_rows  = ([headers] if headers else []) + rows

    tbl = doc.add_table(rows=len(all_rows), cols=col_count)
    tbl.style = "Table Grid"

    for row_idx, row_data in enumerate(all_rows):
        row = tbl.rows[row_idx]
        for col_idx, cell_val in enumerate(row_data):
            if col_idx >= col_count:
                break
            cell = row.cells[col_idx]
            cell.text = str(cell_val)
            run = cell.paragraphs[0].runs
            if run:
                run[0].font.size = Pt(10)
            if row_idx == 0 and headers:
                # Header row styling
                tc = cell._tc
                tcPr = tc.get_or_add_tcPr()
                shd = OxmlElement("w:shd")
                shd.set(qn("w:fill"), "1A3380")
                shd.set(qn("w:color"), "auto")
                shd.set(qn("w:val"), "clear")
                tcPr.append(shd)
                if run:
                    run[0].font.bold = True
                    run[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    if caption:
        cap = doc.add_paragraph(caption)
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.paragraph_format.space_before = Pt(4)
        if cap.runs:
            cap.runs[0].font.size = Pt(9)
            cap.runs[0].font.italic = True
            _set_run_color(cap.runs[0], MUTED)

    doc.add_paragraph()


def generate(brief: dict[str, Any], output_path: str) -> str:
    """Generate DOCX from brief dict. Returns output path."""
    title   = brief.get("title", "Document")
    author  = brief.get("author", "")
    subject = brief.get("subject", "")
    sections = brief.get("sections", [])
    tables   = brief.get("tables", [])

    out = pathlib.Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp.docx")

    doc = Document()
    _set_doc_margins(doc)

    # Core properties
    props = doc.core_properties
    props.title   = title
    props.author  = author
    props.subject = subject
    props.created = datetime.now()

    _add_cover(doc, title, author, subject)

    for section in sections:
        _add_section(doc, section)

    for table_data in tables:
        _add_table(doc, table_data)

    doc.save(str(tmp))
    tmp.replace(out)

    size_kb = out.stat().st_size // 1024
    print(f"✅ DOCX generated: {out}  ({size_kb} KB)")
    return str(out)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a professional DOCX document.")
    parser.add_argument("--title",  default="Document")
    parser.add_argument("--author", default="")
    parser.add_argument("--output", default="output/document.docx")
    parser.add_argument("--brief",  default=None)
    args = parser.parse_args()

    if args.brief:
        brief = json.loads(pathlib.Path(args.brief).read_text(encoding="utf-8"))
    else:
        brief = {
            "title": args.title, "author": args.author,
            "subject": "Generated by document-maker-all-format",
            "sections": [
                {"heading": "Introduction", "level": 2,
                 "content": "This DOCX was generated by document-maker-all-format.\n\nIt uses python-docx 1.x with a professional design system."},
                {"heading": "Features", "level": 2,
                 "content": "Cover page, styled headings, body text, and tables are all supported."},
            ],
            "tables": [
                {"caption": "Table 1 — Supported Formats",
                 "headers": ["Format", "Engine"],
                 "rows": [["PDF","reportlab"],["DOCX","python-docx"],["PPTX","python-pptx"]]}
            ],
        }

    generate(brief, args.output)


if __name__ == "__main__":
    main()

