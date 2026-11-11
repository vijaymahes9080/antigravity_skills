#!/usr/bin/env python3
"""
engine_docx.py — Master High-Craft DOCX Document Production Engine
Part of document-maker skill.
"""

import os
import sys
import json
import argparse
import pathlib
import tempfile
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

PALETTES = {
    "modern_corporate": {"primary": "0A192F", "secondary": "1E3A8A", "accent": "38BDF8", "bg": "F8FAFC", "card": "FFFFFF"},
    "minimalist_editorial": {"primary": "111827", "secondary": "374151", "accent": "C2410C", "bg": "FDFBF7", "card": "FFFFFF"},
    "academic_scientific": {"primary": "000000", "secondary": "1E293B", "accent": "2563EB", "bg": "FFFFFF", "card": "F8FAFC"},
    "premium_business": {"primary": "064E3B", "secondary": "047857", "accent": "D97706", "bg": "F0FDF4", "card": "FFFFFF"},
    "technology_futuristic": {"primary": "0B0F19", "secondary": "1E293B", "accent": "06B6D4", "bg": "F1F5F9", "card": "FFFFFF"},
    "creative_experimental": {"primary": "581C87", "secondary": "EA580C", "accent": "F59E0B", "bg": "FAFAF9", "card": "FFFFFF"},
    "government_institutional": {"primary": "1E3A5F", "secondary": "991B1B", "accent": "0284C7", "bg": "F1F5F9", "card": "FFFFFF"},
    "engineering_technical": {"primary": "0284C7", "secondary": "334155", "accent": "F59E0B", "bg": "FFFFFF", "card": "F8FAFC"},
    "educational_instructional": {"primary": "2563EB", "secondary": "059669", "accent": "F59E0B", "bg": "F0FDF4", "card": "FFFFFF"},
    "magazine_publication": {"primary": "18181B", "secondary": "DC2626", "accent": "4B5563", "bg": "FFFFFF", "card": "F9FAFB"},
    "luxury_hospitality": {"primary": "271810", "secondary": "92400E", "accent": "EAB308", "bg": "FFFFF0", "card": "FFFFFF"},
    "data_analytical": {"primary": "0F172A", "secondary": "1E293B", "accent": "2563EB", "bg": "F8FAFC", "card": "FFFFFF"},
}

def hex_to_rgb(hex_str: str) -> RGBColor:
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join(c * 2 for c in hex_str)
    return RGBColor(int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))

def set_cell_background(cell, hex_color: str):
    hex_color = hex_color.lstrip("#")
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def add_header_footer(doc, title: str, organization: str, classification: str = "Confidential"):
    for s in doc.sections:
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run(f"{organization}  |  {title}")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = hex_to_rgb("64748B")

        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run(f"{classification}  •  Document Maker Autonomous Studio")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = hex_to_rgb("94A3B8")

def build_docx_from_spec(spec: dict, output_path: str):
    doc = Document()
    meta = spec.get("metadata", {})
    design = spec.get("design", {})
    content = spec.get("content", {})
    
    archetype = design.get("archetype", "modern_corporate")
    palette = PALETTES.get(archetype, PALETTES["modern_corporate"])
    if design.get("primary_color"):
        palette["primary"] = design["primary_color"].lstrip("#")
    if design.get("accent_color"):
        palette["accent"] = design["accent_color"].lstrip("#")

    # Margin Setup (0.85 in = 61.2 pt)
    for s in doc.sections:
        s.top_margin = Inches(0.85)
        s.bottom_margin = Inches(0.85)
        s.left_margin = Inches(0.85)
        s.right_margin = Inches(0.85)

    title = meta.get("title", "Enterprise Document")
    subtitle = meta.get("subtitle", "")
    author = meta.get("author", "Principal Architect")
    org = meta.get("organization", "Enterprise Studio")
    date_str = meta.get("date", "2026-11-10")
    classification = meta.get("classification", "Confidential")

    add_header_footer(doc, title, org, classification)

    # 1. Cover Page
    cover_table = doc.add_table(rows=1, cols=1)
    cover_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cell = cover_table.cell(0, 0)
    set_cell_background(c_cell, palette["primary"])
    set_cell_margins(c_cell, top=500, bottom=500, left=350, right=350)
    
    cp = c_cell.paragraphs[0]
    cp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    c_tag = cp.add_run(f"ENTERPRISE VERIFIED SPECIFICATION  |  {archetype.upper().replace('_', ' ')}\n\n")
    c_tag.font.name = "Calibri"
    c_tag.font.size = Pt(9.5)
    c_tag.font.bold = True
    c_tag.font.color.rgb = hex_to_rgb(palette["accent"])

    c_title = cp.add_run(f"{title}\n")
    c_title.font.name = "Calibri"
    c_title.font.size = Pt(26)
    c_title.font.bold = True
    c_title.font.color.rgb = hex_to_rgb("FFFFFF")

    if subtitle:
        c_sub = cp.add_run(f"{subtitle}\n\n")
        c_sub.font.name = "Calibri"
        c_sub.font.size = Pt(13)
        c_sub.font.color.rgb = hex_to_rgb("E2E8F0")

    c_meta = cp.add_run(f"Author: {author}  •  Organization: {org}  •  Date: {date_str}\nStatus: Certified Production Release")
    c_meta.font.name = "Calibri"
    c_meta.font.size = Pt(9.5)
    c_meta.font.color.rgb = hex_to_rgb("94A3B8")

    doc.add_paragraph().paragraph_format.space_after = Pt(16)

    # 2. Abstract / Executive Summary if present
    if content.get("abstract"):
        ap = doc.add_paragraph()
        ap.paragraph_format.space_before = Pt(8)
        ap.paragraph_format.space_after = Pt(12)
        ar_title = ap.add_run("Executive Abstract: ")
        ar_title.font.bold = True
        ar_title.font.color.rgb = hex_to_rgb(palette["primary"])
        ar_body = ap.add_run(content["abstract"])
        ar_body.font.italic = True

    # 3. Educational Lab Record Handler
    if "educational" in content and content["educational"]:
        edu = content["educational"]
        h1 = doc.add_paragraph()
        h1.paragraph_format.space_before = Pt(16)
        h1.paragraph_format.space_after = Pt(8)
        h1.paragraph_format.keep_with_next = True
        r = h1.add_run(f"EXPERIMENT NO. {edu.get('experiment_no', '01')} : {title.upper()}")
        r.font.name = "Calibri"
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = hex_to_rgb(palette["primary"])

        # Aim Block
        if edu.get("aim"):
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(6)
            p.add_run("1. AIM:\n").font.bold = True
            p.add_run(edu["aim"])

        # System Requirements
        if edu.get("system_requirements"):
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(6)
            p.add_run("2. SYSTEM REQUIREMENTS & TOOLS:\n").font.bold = True
            for req in edu["system_requirements"]:
                doc.add_paragraph(f"• {req}", style='List Bullet')

        # Algorithm
        if edu.get("algorithm"):
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(6)
            p.add_run("3. ALGORITHM / METHODOLOGY:\n").font.bold = True
            for step_idx, step in enumerate(edu["algorithm"], 1):
                p_step = doc.add_paragraph(f"Step {step_idx}: {step}")
                p_step.paragraph_format.left_indent = Inches(0.25)
                p_step.paragraph_format.space_after = Pt(3)

        # Code Block
        if edu.get("code"):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(4)
            p.add_run("4. PROGRAM CODE:\n").font.bold = True

            c_table = doc.add_table(rows=1, cols=1)
            c_cell = c_table.cell(0, 0)
            set_cell_background(c_cell, "1E293B")
            set_cell_margins(c_cell, top=120, bottom=120, left=150, right=150)
            code_p = c_cell.paragraphs[0]
            code_p.paragraph_format.space_after = Pt(0)
            c_run = code_p.add_run(edu["code"])
            c_run.font.name = "Consolas"
            c_run.font.size = Pt(9)
            c_run.font.color.rgb = hex_to_rgb("F8FAFC")

        # Sample Input & Output
        if edu.get("sample_input"):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(4)
            p.add_run("5. SAMPLE INPUT:\n").font.bold = True
            p.add_run(edu["sample_input"])

        if edu.get("sample_output"):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(4)
            p.add_run("6. SAMPLE OUTPUT:\n").font.bold = True
            
            o_table = doc.add_table(rows=1, cols=1)
            o_cell = o_table.cell(0, 0)
            set_cell_background(o_cell, "0F172A")
            set_cell_margins(o_cell, top=100, bottom=100, left=150, right=150)
            out_p = o_cell.paragraphs[0]
            out_p.paragraph_format.space_after = Pt(0)
            o_run = out_p.add_run(edu["sample_output"])
            o_run.font.name = "Consolas"
            o_run.font.size = Pt(9)
            o_run.font.color.rgb = hex_to_rgb("38BDF8")

        # Result & Inference
        if edu.get("result_and_inference"):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(6)
            p.add_run("7. RESULT & INFERENCE:\n").font.bold = True
            p.add_run(edu["result_and_inference"])

    # 4. Standard Sections Handler
    for sec in content.get("sections", []):
        level = sec.get("level", 1)
        hp = doc.add_paragraph()
        hp.paragraph_format.space_before = Pt(14)
        hp.paragraph_format.space_after = Pt(6)
        hp.paragraph_format.keep_with_next = True
        
        hrun = hp.add_run(sec["title"])
        hrun.font.name = "Calibri"
        hrun.font.bold = True
        if level == 1:
            hrun.font.size = Pt(16)
            hrun.font.color.rgb = hex_to_rgb(palette["primary"])
        elif level == 2:
            hrun.font.size = Pt(13)
            hrun.font.color.rgb = hex_to_rgb(palette["secondary"])
        else:
            hrun.font.size = Pt(11.5)
            hrun.font.color.rgb = hex_to_rgb("334155")

        for p_text in sec.get("paragraphs", []):
            p = doc.add_paragraph(p_text)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.2

        for bullet in sec.get("bullet_points", []):
            bp = doc.add_paragraph(bullet, style='List Bullet')
            bp.paragraph_format.space_after = Pt(3)

        # Callouts
        if sec.get("callout"):
            c_box = doc.add_table(rows=1, cols=1)
            c_box.alignment = WD_TABLE_ALIGNMENT.CENTER
            c_b_cell = c_box.cell(0, 0)
            set_cell_background(c_b_cell, palette["bg"])
            set_cell_margins(c_b_cell, top=140, bottom=140, left=200, right=200)
            cb_p = c_b_cell.paragraphs[0]
            cb_p.paragraph_format.space_after = Pt(0)
            cb_tag = cb_p.add_run("KEY TAKEAWAY: ")
            cb_tag.font.bold = True
            cb_tag.font.size = Pt(10)
            cb_tag.font.color.rgb = hex_to_rgb(palette["primary"])
            cb_run = cb_p.add_run(sec["callout"])
            cb_run.font.size = Pt(10)
            cb_run.font.italic = True
            doc.add_paragraph().paragraph_format.space_after = Pt(6)

        # Tables
        if sec.get("table") and sec["table"].get("headers"):
            tbl_data = sec["table"]
            headers = tbl_data["headers"]
            rows = tbl_data.get("rows", [])
            t = doc.add_table(rows=len(rows) + 1, cols=len(headers))
            t.alignment = WD_TABLE_ALIGNMENT.CENTER

            # Header row
            for idx, h_text in enumerate(headers):
                cell = t.cell(0, idx)
                set_cell_background(cell, palette["primary"])
                set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
                hp = cell.paragraphs[0]
                hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                hrun = hp.add_run(str(h_text))
                hrun.font.name = "Calibri"
                hrun.font.bold = True
                hrun.font.size = Pt(10)
                hrun.font.color.rgb = hex_to_rgb("FFFFFF")

            # Data rows with zebra striping
            for r_idx, row in enumerate(rows, start=1):
                bg_color = palette["bg"] if r_idx % 2 == 1 else "FFFFFF"
                for c_idx, val in enumerate(row):
                    cell = t.cell(r_idx, c_idx)
                    set_cell_background(cell, bg_color)
                    set_cell_margins(cell, top=80, bottom=80, left=140, right=140)
                    dp = cell.paragraphs[0]
                    # Right align numeric values
                    val_str = str(val)
                    if any(val_str.strip().startswith(c) for c in "$€£0123456789+-"):
                        dp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    else:
                        dp.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    drun = dp.add_run(val_str)
                    drun.font.name = "Calibri"
                    drun.font.size = Pt(9.5)
                    drun.font.color.rgb = hex_to_rgb("1E293B")

            doc.add_paragraph().paragraph_format.space_after = Pt(8)

        # Code Block
        if sec.get("code_block") and sec["code_block"].get("code"):
            cb = sec["code_block"]
            c_table = doc.add_table(rows=1, cols=1)
            c_cell = c_table.cell(0, 0)
            set_cell_background(c_cell, "1E293B")
            set_cell_margins(c_cell, top=120, bottom=120, left=150, right=150)
            code_p = c_cell.paragraphs[0]
            code_p.paragraph_format.space_after = Pt(0)
            c_run = code_p.add_run(cb["code"])
            c_run.font.name = "Consolas"
            c_run.font.size = Pt(9)
            c_run.font.color.rgb = hex_to_rgb("F8FAFC")
            doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Atomic write
    out_p = pathlib.Path(output_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_p.with_suffix(".tmp.docx")
    try:
        doc.save(str(tmp_path))
        tmp_path.replace(out_p)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise

    return str(out_p)

def main():
    parser = argparse.ArgumentParser(description="Master DOCX Production Engine")
    parser.add_argument("--spec", help="Path to document spec JSON")
    parser.add_argument("--out", "--output", required=True, help="Destination .docx file path")
    parser.add_argument("--title", default="Executive Document", help="Document title if no spec")
    parser.add_argument("--author", default="Principal Architect", help="Author name")
    parser.add_argument("--archetype", default="modern_corporate", help="Design archetype")
    args = parser.parse_args()

    if args.spec and os.path.exists(args.spec):
        with open(args.spec, "r", encoding="utf-8") as f:
            spec = json.load(f)
    else:
        spec = {
            "metadata": {"title": args.title, "author": args.author, "format": "docx"},
            "design": {"archetype": args.archetype},
            "content": {
                "sections": [
                    {"title": "1. Executive Summary", "paragraphs": ["This document was generated using Document Maker Studio."]},
                    {"title": "2. Production Verification", "paragraphs": ["All layout properties and typography standards are verified."]}
                ]
            }
        }

    out_file = build_docx_from_spec(spec, args.out)
    print(f"✅ Master DOCX successfully built: {out_file} ({os.path.getsize(out_file)} bytes)")

if __name__ == "__main__":
    main()

