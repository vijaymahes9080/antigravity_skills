#!/usr/bin/env python3
"""
engine_docx.py — High-Craft DOCX Document Production Engine
Part of document-maker-any-format skill
"""

import os
import sys
import json
import argparse
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

PALETTES = {
    "modern_corporate": {"primary": "0A192F", "secondary": "1E3A8A", "accent": "38BDF8", "bg": "F8FAFC"},
    "minimalist_editorial": {"primary": "111827", "secondary": "374151", "accent": "C2410C", "bg": "FDFBF7"},
    "academic_scientific": {"primary": "1E293B", "secondary": "334155", "accent": "2563EB", "bg": "FFFFFF"},
    "premium_business": {"primary": "064E3B", "secondary": "047857", "accent": "D97706", "bg": "F0FDF4"},
    "technology_futuristic": {"primary": "0B0F19", "secondary": "1E293B", "accent": "06B6D4", "bg": "F1F5F9"},
}

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    return RGBColor(int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))

def set_cell_background(cell, hex_color):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_header_footer(doc, title, organization):
    for s in doc.sections:
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run(f"{organization}  |  {title}")
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = hex_to_rgb("64748B")

        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Generated with Antigravity Document Automation — Confidential")
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = hex_to_rgb("94A3B8")

def build_docx(spec, output_path):
    doc = Document()
    meta = spec.get("metadata", {})
    design = spec.get("design", {})
    archetype = design.get("archetype", "modern_corporate")
    palette = PALETTES.get(archetype, PALETTES["modern_corporate"])

    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    primary_rgb = hex_to_rgb(palette["primary"])
    secondary_rgb = hex_to_rgb(palette["secondary"])

    # Cover Page
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(72)
    title_p.paragraph_format.space_after = Pt(12)
    t_run = title_p.add_run(meta.get("title", "Executive Document"))
    t_run.font.name = "Arial"
    t_run.font.size = Pt(28)
    t_run.font.bold = True
    t_run.font.color.rgb = primary_rgb

    if meta.get("subtitle"):
        sub_p = doc.add_paragraph()
        sub_p.paragraph_format.space_after = Pt(24)
        sub_run = sub_p.add_run(meta["subtitle"])
        sub_run.font.name = "Arial"
        sub_run.font.size = Pt(14)
        sub_run.font.color.rgb = secondary_rgb

    meta_p = doc.add_paragraph()
    meta_p.paragraph_format.space_after = Pt(48)
    org_run = meta_p.add_run(f"Prepared for: {meta.get('organization', 'Enterprise Partner')}\nAuthor: {meta.get('author', 'System Architect')}\nDate: {meta.get('date', 'November 2026')}")
    org_run.font.size = Pt(10)
    org_run.font.color.rgb = hex_to_rgb("475569")

    doc.add_page_break()
    add_header_footer(doc, meta.get("title", ""), meta.get("organization", ""))

    # Table of Contents
    toc_p = doc.add_paragraph()
    toc_p.paragraph_format.space_after = Pt(12)
    toc_run = toc_p.add_run("Table of Contents")
    toc_run.font.size = Pt(18)
    toc_run.font.bold = True
    toc_run.font.color.rgb = primary_rgb

    sections = spec.get("content", {}).get("sections", [])
    for idx, sec in enumerate(sections, 1):
        item_p = doc.add_paragraph()
        item_p.paragraph_format.space_after = Pt(4)
        num_run = item_p.add_run(f"{idx}.0  {sec.get('title', '')}")
        num_run.font.size = Pt(10.5)
        num_run.font.color.rgb = secondary_rgb
        dots_run = item_p.add_run(" " + "." * 60 + " ")
        dots_run.font.color.rgb = hex_to_rgb("CBD5E1")
        page_run = item_p.add_run(f"Page {idx + 1}")
        page_run.font.size = Pt(10.5)

    doc.add_page_break()

    # Sections
    for idx, sec in enumerate(sections, 1):
        h_p = doc.add_paragraph()
        h_p.paragraph_format.space_before = Pt(18)
        h_p.paragraph_format.space_after = Pt(6)
        h_p.paragraph_format.keep_with_next = True
        h_run = h_p.add_run(f"{idx}.0 {sec.get('title', 'Section')}")
        h_run.font.name = "Arial"
        h_run.font.size = Pt(16)
        h_run.font.bold = True
        h_run.font.color.rgb = primary_rgb

        for para_text in sec.get("paragraphs", []):
            p = doc.add_paragraph()
            p.paragraph_format.line_spacing = 1.2
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(para_text)
            run.font.name = "Calibri"
            run.font.size = Pt(11)
            run.font.color.rgb = hex_to_rgb("1E293B")

        if sec.get("callout"):
            callout_tbl = doc.add_table(rows=1, cols=1)
            callout_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            cell = callout_tbl.cell(0, 0)
            cell.width = Inches(6.5)
            set_cell_background(cell, palette["bg"])
            set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
            cp = cell.paragraphs[0]
            c_run = cp.add_run(f"★ Key Takeaway: {sec['callout']}")
            c_run.font.size = Pt(10.5)
            c_run.font.bold = True
            c_run.font.color.rgb = secondary_rgb
            doc.add_paragraph().paragraph_format.space_after = Pt(6)

        if sec.get("code_block"):
            cb = sec["code_block"]
            code_tbl = doc.add_table(rows=1, cols=1)
            cell = code_tbl.cell(0, 0)
            cell.width = Inches(6.5)
            set_cell_background(cell, "0F172A")
            set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
            code_p = cell.paragraphs[0]
            code_run = code_p.add_run(cb.get("code", ""))
            code_run.font.name = "Consolas"
            code_run.font.size = Pt(9.5)
            code_run.font.color.rgb = hex_to_rgb("38BDF8")
            doc.add_paragraph().paragraph_format.space_after = Pt(6)

        if sec.get("table"):
            t_data = sec["table"]
            headers = t_data.get("headers", [])
            rows = t_data.get("rows", [])
            if headers:
                tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
                tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
                hdr_cells = tbl.rows[0].cells
                for i, h_text in enumerate(headers):
                    hdr_cells[i].text = h_text
                    set_cell_background(hdr_cells[i], palette["primary"])
                    set_cell_margins(hdr_cells[i], top=120, bottom=120, left=120, right=120)
                    for r in hdr_cells[i].paragraphs[0].runs:
                        r.font.bold = True
                        r.font.size = Pt(10)
                        r.font.color.rgb = hex_to_rgb("FFFFFF")
                for r_idx, row_values in enumerate(rows):
                    row_cells = tbl.rows[r_idx + 1].cells
                    bg = palette["bg"] if r_idx % 2 == 1 else "FFFFFF"
                    for c_idx, val in enumerate(row_values):
                        if c_idx < len(row_cells):
                            row_cells[c_idx].text = str(val)
                            set_cell_background(row_cells[c_idx], bg)
                            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=120, right=120)
                            for r in row_cells[c_idx].paragraphs[0].runs:
                                r.font.size = Pt(9.5)
                                r.font.color.rgb = hex_to_rgb("334155")
                doc.add_paragraph().paragraph_format.space_after = Pt(12)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.save(output_path)
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DOCX Production Engine")
    parser.add_argument("--spec", required=True, help="Path to JSON spec")
    parser.add_argument("--out", required=True, help="Output .docx file path")
    args = parser.parse_args()

    with open(args.spec, "r", encoding="utf-8") as f:
        spec_data = json.load(f)
    out_file = build_docx(spec_data, args.out)
    print(f"SUCCESS: Generated DOCX at {out_file}")
