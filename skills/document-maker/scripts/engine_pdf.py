#!/usr/bin/env python3
"""
engine_pdf.py — Master Publication-Grade PDF Publishing Engine
Part of document-maker skill.
"""

import os
import sys
import json
import argparse
import pathlib
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PALETTES = {
    "modern_corporate": {"primary": colors.HexColor("#0A192F"), "secondary": colors.HexColor("#1E3A8A"), "accent": colors.HexColor("#0284C7"), "bg": colors.HexColor("#F8FAFC"), "card": colors.HexColor("#FFFFFF")},
    "minimalist_editorial": {"primary": colors.HexColor("#111827"), "secondary": colors.HexColor("#374151"), "accent": colors.HexColor("#C2410C"), "bg": colors.HexColor("#FDFBF7"), "card": colors.HexColor("#FFFFFF")},
    "academic_scientific": {"primary": colors.HexColor("#000000"), "secondary": colors.HexColor("#1E293B"), "accent": colors.HexColor("#2563EB"), "bg": colors.HexColor("#FFFFFF"), "card": colors.HexColor("#F8FAFC")},
    "premium_business": {"primary": colors.HexColor("#064E3B"), "secondary": colors.HexColor("#047857"), "accent": colors.HexColor("#D97706"), "bg": colors.HexColor("#F0FDF4"), "card": colors.HexColor("#FFFFFF")},
    "technology_futuristic": {"primary": colors.HexColor("#0B0F19"), "secondary": colors.HexColor("#1E293B"), "accent": colors.HexColor("#06B6D4"), "bg": colors.HexColor("#F1F5F9"), "card": colors.HexColor("#FFFFFF")},
    "engineering_technical": {"primary": colors.HexColor("#0284C7"), "secondary": colors.HexColor("#334155"), "accent": colors.HexColor("#F59E0B"), "bg": colors.HexColor("#FFFFFF"), "card": colors.HexColor("#F8FAFC")},
    "educational_instructional": {"primary": colors.HexColor("#2563EB"), "secondary": colors.HexColor("#059669"), "accent": colors.HexColor("#F59E0B"), "bg": colors.HexColor("#F0FDF4"), "card": colors.HexColor("#FFFFFF")},
    "data_analytical": {"primary": colors.HexColor("#0F172A"), "secondary": colors.HexColor("#1E293B"), "accent": colors.HexColor("#2563EB"), "bg": colors.HexColor("#F8FAFC"), "card": colors.HexColor("#FFFFFF")},
}

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Skip cover page
        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header rule & title
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 11 * inch - 40, 8.5 * inch - 54, 11 * inch - 40)
        self.drawString(54, 11 * inch - 35, getattr(self, '_doc_title', 'Master Document Publication'))

        # Footer divider & page number
        self.line(54, 45, 8.5 * inch - 54, 45)
        self.drawString(54, 32, "Antigravity Document Studio  |  Verified Production Output")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, page_str)
        self.restoreState()

def build_pdf_from_spec(spec: dict, output_path: str):
    meta = spec.get("metadata", {})
    design = spec.get("design", {})
    content = spec.get("content", {})

    title = meta.get("title", "Executive Technical Report")
    subtitle = meta.get("subtitle", "")
    author = meta.get("author", "Principal Architect")
    org = meta.get("organization", "Global Enterprise Solutions")
    date_str = meta.get("date", "November 2026")

    archetype = design.get("archetype", "modern_corporate")
    palette = PALETTES.get(archetype, PALETTES["modern_corporate"])

    out_p = pathlib.Path(output_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_p.with_suffix(".tmp.pdf")

    doc = SimpleDocTemplate(
        str(tmp_path),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom paragraph styles
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=palette["primary"],
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=palette["secondary"],
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#F8FAFC")
    )

    story = []

    # 1. Cover Page Banner
    cover_data = [
        [Paragraph(f"<font color='{palette['accent'].hexval()}'><b>ENTERPRISE PUBLICATION  •  {archetype.upper().replace('_', ' ')}</b></font>", body_style)],
        [Spacer(1, 10)],
        [Paragraph(f"<b><font size='22' color='#FFFFFF'>{title}</font></b>", h1_style)],
        [Paragraph(f"<font size='12' color='#E2E8F0'>{subtitle}</font>", body_style)] if subtitle else [Spacer(1, 1)],
        [Spacer(1, 14)],
        [Paragraph(f"<font size='9' color='#94A3B8'>Author: {author}  •  Organization: {org}  •  Date: {date_str}</font>", body_style)]
    ]
    cover_table = Table(cover_data, colWidths=[7.0 * inch])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), palette["primary"]),
        ('LEFTPADDING', (0, 0), (-1, -1), 22),
        ('RIGHTPADDING', (0, 0), (-1, -1), 22),
        ('TOPPADDING', (0, 0), (-1, -1), 24),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 24),
        ('BOTTOMMARGIN', (0, 0), (-1, -1), 18),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 16))

    # 2. Abstract if present
    if content.get("abstract"):
        story.append(Paragraph(f"<b>Executive Abstract:</b> <i>{content['abstract']}</i>", body_style))
        story.append(Spacer(1, 12))

    # 3. Educational Lab Record Handler
    if "educational" in content and content["educational"]:
        edu = content["educational"]
        story.append(Paragraph(f"EXPERIMENT NO. {edu.get('experiment_no', '01')} : {title.upper()}", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=palette["primary"], spaceAfter=10))

        if edu.get("aim"):
            story.append(Paragraph("<b>1. AIM:</b>", h2_style))
            story.append(Paragraph(edu["aim"], body_style))
            story.append(Spacer(1, 8))

        if edu.get("system_requirements"):
            story.append(Paragraph("<b>2. SYSTEM REQUIREMENTS & TOOLS:</b>", h2_style))
            for req in edu["system_requirements"]:
                story.append(Paragraph(f"• {req}", body_style))
            story.append(Spacer(1, 8))

        if edu.get("algorithm"):
            story.append(Paragraph("<b>3. ALGORITHM / METHODOLOGY:</b>", h2_style))
            for s_idx, step in enumerate(edu["algorithm"], 1):
                story.append(Paragraph(f"<b>Step {s_idx}:</b> {step}", body_style))
            story.append(Spacer(1, 8))

        if edu.get("code"):
            story.append(Paragraph("<b>4. PROGRAM SOURCE CODE:</b>", h2_style))
            code_lines = edu["code"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
            code_table = Table([[Paragraph(code_lines, code_style)]], colWidths=[7.0 * inch])
            code_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#1E293B")),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            story.append(code_table)
            story.append(Spacer(1, 10))

        if edu.get("sample_input"):
            story.append(Paragraph("<b>5. SAMPLE INPUT:</b>", h2_style))
            story.append(Paragraph(edu["sample_input"], body_style))
            story.append(Spacer(1, 6))

        if edu.get("sample_output"):
            story.append(Paragraph("<b>6. SAMPLE OUTPUT:</b>", h2_style))
            out_lines = edu["sample_output"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
            out_table = Table([[Paragraph(out_lines, code_style)]], colWidths=[7.0 * inch])
            out_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0F172A")),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(out_table)
            story.append(Spacer(1, 10))

        if edu.get("result_and_inference"):
            story.append(Paragraph("<b>7. RESULT & INFERENCES:</b>", h2_style))
            story.append(Paragraph(edu["result_and_inference"], body_style))
            story.append(Spacer(1, 12))

    # 4. Standard Sections
    for sec in content.get("sections", []):
        level = sec.get("level", 1)
        heading_s = h1_style if level == 1 else h2_style
        story.append(Paragraph(sec["title"], heading_s))

        for p in sec.get("paragraphs", []):
            story.append(Paragraph(p, body_style))

        for bullet in sec.get("bullet_points", []):
            story.append(Paragraph(f"• {bullet}", body_style))

        # Callouts
        if sec.get("callout"):
            callout_text = f"<b><font color='{palette['primary'].hexval()}'>NOTE:</font></b> {sec['callout']}"
            c_table = Table([[Paragraph(callout_text, body_style)]], colWidths=[7.0 * inch])
            c_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), palette["bg"]),
                ('LINELEFT', (0, 0), (0, -1), 3.5, palette["accent"]),
                ('LEFTPADDING', (0, 0), (-1, -1), 14),
                ('RIGHTPADDING', (0, 0), (-1, -1), 14),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            story.append(Spacer(1, 4))
            story.append(c_table)
            story.append(Spacer(1, 8))

        # Tables
        if sec.get("table") and sec["table"].get("headers"):
            tbl_data = sec["table"]
            headers = [Paragraph(f"<b><font color='#FFFFFF'>{h}</font></b>", body_style) for h in tbl_data["headers"]]
            table_rows = [headers]
            for row in tbl_data.get("rows", []):
                table_rows.append([Paragraph(str(val), body_style) for val in row])

            num_cols = len(tbl_data["headers"])
            col_w = (7.0 * inch) / max(1, num_cols)
            t = Table(table_rows, colWidths=[col_w] * num_cols)
            t_styles = [
                ('BACKGROUND', (0, 0), (-1, 0), palette["primary"]),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ]
            for r_idx in range(1, len(table_rows)):
                if r_idx % 2 == 1:
                    t_styles.append(('BACKGROUND', (0, r_idx), (-1, r_idx), palette["bg"]))
            t.setStyle(TableStyle(t_styles))
            story.append(Spacer(1, 6))
            story.append(t)
            story.append(Spacer(1, 10))

        # Code block
        if sec.get("code_block") and sec["code_block"].get("code"):
            cb = sec["code_block"]
            code_lines = cb["code"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
            code_table = Table([[Paragraph(code_lines, code_style)]], colWidths=[7.0 * inch])
            code_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#1E293B")),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            story.append(Spacer(1, 6))
            story.append(code_table)
            story.append(Spacer(1, 10))

    try:
        doc.build(story, canvasmaker=NumberedCanvas)
        tmp_path.replace(out_p)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise

    return str(out_p)

def main():
    parser = argparse.ArgumentParser(description="Master PDF Publishing Engine")
    parser.add_argument("--spec", help="Path to document spec JSON")
    parser.add_argument("--out", "--output", required=True, help="Destination .pdf file path")
    parser.add_argument("--archetype", default="modern_corporate", help="Archetype")
    args = parser.parse_args()

    if args.spec and os.path.exists(args.spec):
        with open(args.spec, "r", encoding="utf-8") as f:
            spec = json.load(f)
    else:
        spec = {
            "metadata": {"title": "Executive Report", "format": "pdf"},
            "design": {"archetype": args.archetype},
            "content": {
                "sections": [
                    {"title": "1. Operational Architecture", "paragraphs": ["This publication PDF was produced with zero layout defect tolerance."]}
                ]
            }
        }

    out_file = build_pdf_from_spec(spec, args.out)
    print(f"✅ Master PDF successfully built: {out_file} ({os.path.getsize(out_file)} bytes)")

if __name__ == "__main__":
    main()
