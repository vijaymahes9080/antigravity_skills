#!/usr/bin/env python3
"""
engine_pdf.py — Publication-Grade PDF Publishing Engine
Part of document-maker-any-format skill
"""

import os
import sys
import json
import argparse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

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
            return
        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748B"))

        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 11 * inch - 40, 8.5 * inch - 54, 11 * inch - 40)
        self.drawString(54, 11 * inch - 35, getattr(self, '_doc_title', 'Enterprise Document'))

        self.line(54, 45, 8.5 * inch - 54, 45)
        self.drawString(54, 32, "Antigravity Publication Studio  |  Verified Output")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, page_str)
        self.restoreState()

def build_pdf(spec, output_path):
    meta = spec.get("metadata", {})
    title = meta.get("title", "Executive Technical Report")
    author = meta.get("author", "Principal Architect")
    org = meta.get("organization", "Global Enterprise Solutions")
    date_str = meta.get("date", "November 2026")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor('#0A192F'),
        spaceAfter=14
    )

    style_cover_sub = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=24
    )

    style_h1 = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#0A192F'),
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=8
    )

    style_callout = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1E3A8A')
    )

    style_code = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#0284C7')
    )

    story = []

    # Cover Page
    story.append(Spacer(1, 120))
    story.append(Paragraph(title, style_cover_title))
    if meta.get("subtitle"):
        story.append(Paragraph(meta["subtitle"], style_cover_sub))
    story.append(HRFlowable(width="100%", thickness=3, color=colors.HexColor('#38BDF8'), spaceBefore=8, spaceAfter=24))

    meta_text = f"<b>Organization:</b> {org}<br/><b>Author:</b> {author}<br/><b>Publication Date:</b> {date_str}"
    story.append(Paragraph(meta_text, style_body))
    story.append(PageBreak())

    # Sections
    sections = spec.get("content", {}).get("sections", [])
    for idx, sec in enumerate(sections, 1):
        sec_title = f"{idx}.0 {sec.get('title', 'Section')}"
        story.append(Paragraph(sec_title, style_h1))

        for p_text in sec.get("paragraphs", []):
            story.append(Paragraph(p_text, style_body))

        if sec.get("callout"):
            callout_data = [[Paragraph(f"<b>Key Takeaway:</b> {sec['callout']}", style_callout)]]
            t_call = Table(callout_data, colWidths=[7.0 * inch])
            t_call.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
                ('LINELEFT', (0, 0), (0, -1), 3.0, colors.HexColor('#1E3A8A')),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12)
            ]))
            story.append(Spacer(1, 4))
            story.append(t_call)
            story.append(Spacer(1, 8))

        if sec.get("code_block"):
            code_str = sec["code_block"].get("code", "").replace("\n", "<br/>")
            code_data = [[Paragraph(code_str, style_code)]]
            t_code = Table(code_data, colWidths=[7.0 * inch])
            t_code.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0F172A')),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10)
            ]))
            story.append(Spacer(1, 4))
            story.append(t_code)
            story.append(Spacer(1, 8))

        if sec.get("table"):
            t_spec = sec["table"]
            headers = [Paragraph(f"<b>{h}</b>", ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)) for h in t_spec.get("headers", [])]
            t_rows = [headers]
            for row in t_spec.get("rows", []):
                t_rows.append([Paragraph(str(val), ParagraphStyle('TD', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor('#1E293B'))) for val in row])

            num_cols = len(t_spec.get("headers", [1]))
            col_w = (7.0 * inch) / max(num_cols, 1)
            table_obj = Table(t_rows, colWidths=[col_w] * num_cols)
            table_obj.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0A192F')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(Spacer(1, 6))
            story.append(table_obj)
            story.append(Spacer(1, 10))

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.build(story, canvasmaker=NumberedCanvas)
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Publishing Engine")
    parser.add_argument("--spec", required=True, help="Path to JSON spec")
    parser.add_argument("--out", required=True, help="Output .pdf path")
    args = parser.parse_args()

    with open(args.spec, "r", encoding="utf-8") as f:
        data = json.load(f)
    res = build_pdf(data, args.out)
    print(f"SUCCESS: Generated PDF at {res}")

