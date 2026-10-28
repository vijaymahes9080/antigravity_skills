#!/usr/bin/env python3
"""
generate_pdf.py — Professional PDF generator using ReportLab.

Usage:
    python scripts/generate_pdf.py --title "My Report" --author "Author Name" \
        --output output/report.pdf [--brief brief.json]

The brief JSON format:
{
  "title": "Report Title",
  "author": "Author",
  "subject": "Optional subject",
  "sections": [
    {"heading": "Introduction", "content": "Body text here...", "level": 2},
    {"heading": "Methods",      "content": "...",               "level": 2}
  ],
  "tables": [
    {"caption": "Table 1", "headers": ["A","B","C"], "rows": [["1","2","3"]]}
  ]
}
"""
import argparse
import json
import os
import pathlib
import sys
from datetime import datetime
from typing import Any

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.lib.pagesizes import A4, LETTER
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm, mm
    from reportlab.platypus import (
        HRFlowable, Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
        Table, TableStyle,
    )
    from reportlab.platypus.tableofcontents import TableOfContents
except ImportError:
    sys.exit("❌ reportlab not installed. Run: python scripts/bootstrap.py")


# ─── Design System ───────────────────────────────────────────────────────────
NAVY    = colors.HexColor("#1A3380")
AMBER   = colors.HexColor("#F29910")
NEAR_BLACK = colors.HexColor("#262626")
MUTED   = colors.HexColor("#8C8C8C")
LIGHT_BG = colors.HexColor("#F5F7FA")
WHITE   = colors.white


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "h1": ParagraphStyle("H1", parent=base["Normal"],
                             fontSize=26, leading=32, textColor=NAVY,
                             fontName="Helvetica-Bold", spaceAfter=14, spaceBefore=0),
        "h2": ParagraphStyle("H2", parent=base["Normal"],
                             fontSize=18, leading=24, textColor=NAVY,
                             fontName="Helvetica-Bold", spaceAfter=8, spaceBefore=16),
        "h3": ParagraphStyle("H3", parent=base["Normal"],
                             fontSize=14, leading=18, textColor=NEAR_BLACK,
                             fontName="Helvetica-Bold", spaceAfter=6, spaceBefore=10),
        "body": ParagraphStyle("Body", parent=base["Normal"],
                               fontSize=11, leading=16, textColor=NEAR_BLACK,
                               fontName="Helvetica", spaceAfter=6),
        "caption": ParagraphStyle("Caption", parent=base["Normal"],
                                  fontSize=9, leading=12, textColor=MUTED,
                                  fontName="Helvetica-Oblique", spaceAfter=4,
                                  alignment=TA_CENTER),
        "cover_title": ParagraphStyle("CoverTitle", parent=base["Normal"],
                                      fontSize=32, leading=40, textColor=NAVY,
                                      fontName="Helvetica-Bold", alignment=TA_CENTER),
        "cover_sub": ParagraphStyle("CoverSub", parent=base["Normal"],
                                    fontSize=14, leading=18, textColor=MUTED,
                                    fontName="Helvetica", alignment=TA_CENTER),
        "footer": ParagraphStyle("Footer", parent=base["Normal"],
                                 fontSize=8, textColor=MUTED,
                                 fontName="Helvetica", alignment=TA_CENTER),
    }


def _add_page_number(canvas, doc) -> None:
    """Draw header/footer on every page except the cover."""
    canvas.saveState()
    page = canvas.getPageNumber()
    if page == 1:
        canvas.restoreState()
        return
    w, h = A4
    # Top rule
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, h - 1.8*cm, w - 2*cm, h - 1.8*cm)
    # Footer page number
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(w / 2, 1.2*cm, f"Page {page}")
    canvas.restoreState()


def build_cover(title: str, author: str, subject: str, styles: dict) -> list:
    story = []
    story.append(Spacer(1, 5*cm))
    story.append(HRFlowable(width="100%", thickness=3, color=AMBER, spaceAfter=24))
    story.append(Paragraph(title, styles["cover_title"]))
    story.append(HRFlowable(width="100%", thickness=1, color=MUTED, spaceBefore=12, spaceAfter=12))
    if subject:
        story.append(Paragraph(subject, styles["cover_sub"]))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(f"<b>Author:</b> {author}", styles["cover_sub"]))
    story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}", styles["cover_sub"]))
    story.append(PageBreak())
    return story


def build_table(table_data: dict, styles: dict) -> list:
    """Convert a table dict into a ReportLab Table flowable."""
    headers = table_data.get("headers", [])
    rows = table_data.get("rows", [])
    caption = table_data.get("caption", "")

    all_rows = [headers] + rows if headers else rows
    col_count = max(len(r) for r in all_rows) if all_rows else 1
    page_w = A4[0] - 4*cm  # usable width

    tbl = Table(all_rows, colWidths=[page_w / col_count] * col_count,
                repeatRows=1 if headers else 0)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0), 10),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 1), (-1, -1), 10),
        ("GRID",          (0, 0), (-1, -1), 0.5, MUTED),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))

    result = [tbl]
    if caption:
        result.append(Paragraph(caption, styles["caption"]))
    result.append(Spacer(1, 0.4*cm))
    return result


def generate(brief: dict[str, Any], output_path: str) -> str:
    """Generate a PDF from a content brief dict. Returns the output path."""
    title   = brief.get("title", "Document")
    author  = brief.get("author", "")
    subject = brief.get("subject", "")
    sections = brief.get("sections", [])
    tables   = {t.get("caption", ""): t for t in brief.get("tables", [])}

    # Atomic write
    out = pathlib.Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp.pdf")

    doc = SimpleDocTemplate(
        str(tmp),
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
        title=title, author=author, subject=subject,
        creator="document-maker-all-format",
    )

    styles = build_styles()
    story: list = []

    # Cover page
    story += build_cover(title, author, subject, styles)

    # Sections
    for section in sections:
        level = section.get("level", 2)
        heading = section.get("heading", "")
        content = section.get("content", "")

        style_key = {1: "h1", 2: "h2", 3: "h3"}.get(level, "h2")
        story.append(Paragraph(heading, styles[style_key]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=MUTED, spaceAfter=4))

        # Split content into paragraphs at double newline
        for para_text in content.split("\n\n"):
            para_text = para_text.strip()
            if para_text:
                story.append(Paragraph(para_text.replace("\n", " "), styles["body"]))

        story.append(Spacer(1, 0.3*cm))

    doc.build(story, onFirstPage=_add_page_number, onLaterPages=_add_page_number)

    # Atomic rename
    tmp.replace(out)
    size_kb = out.stat().st_size // 1024
    print(f"✅ PDF generated: {out}  ({size_kb} KB)")
    return str(out)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a professional PDF document.")
    parser.add_argument("--title",  default="Document", help="Document title")
    parser.add_argument("--author", default="",         help="Author name")
    parser.add_argument("--output", default="output/document.pdf", help="Output PDF path")
    parser.add_argument("--brief",  default=None,       help="Path to JSON content brief")
    args = parser.parse_args()

    if args.brief:
        brief = json.loads(pathlib.Path(args.brief).read_text(encoding="utf-8"))
    else:
        # Demo brief
        brief = {
            "title":   args.title,
            "author":  args.author,
            "subject": "Generated by document-maker-all-format",
            "sections": [
                {"heading": "Introduction",   "level": 2,
                 "content": "This document was generated by the document-maker-all-format skill.\n\nIt demonstrates professional PDF output using ReportLab 5.x with a consistent design system."},
                {"heading": "Key Features",   "level": 2,
                 "content": "• Cover page with title, author, and date\n\n• Styled headings (H1, H2, H3)\n\n• Body text with proper leading and spacing\n\n• Tables with alternating row colors\n\n• Page numbers in the footer"},
                {"heading": "Design System",  "level": 2,
                 "content": "The design system uses Navy (#1A3380) as the primary color and Amber (#F29910) as the accent, with Helvetica as the body font family."},
            ],
            "tables": [
                {"caption": "Table 1 — Format Support Matrix",
                 "headers": ["Format", "Engine", "Status"],
                 "rows": [
                     ["PDF",  "reportlab 5.x",   "✅ Active"],
                     ["DOCX", "python-docx 1.2",  "✅ Active"],
                     ["PPTX", "python-pptx 1.x",  "✅ Active"],
                     ["XLSX", "openpyxl 3.1",     "✅ Active"],
                     ["RTF",  "Custom writer",    "✅ Active"],
                 ]}
            ],
        }

    generate(brief, args.output)


if __name__ == "__main__":
    main()
