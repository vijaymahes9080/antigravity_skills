#!/usr/bin/env python3
"""
engine_pptx.py — Master 16:9 Enterprise Presentation Production Engine
Part of document-maker skill.
"""

import os
import sys
import json
import argparse
import pathlib
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

PALETTES = {
    "modern_corporate": {"primary": "0A192F", "secondary": "1E3A8A", "accent": "38BDF8", "bg": "F8FAFC", "card": "FFFFFF", "text": "1E293B"},
    "minimalist_editorial": {"primary": "111827", "secondary": "374151", "accent": "C2410C", "bg": "FDFBF7", "card": "FFFFFF", "text": "1F2937"},
    "academic_scientific": {"primary": "000000", "secondary": "1E293B", "accent": "2563EB", "bg": "FFFFFF", "card": "F8FAFC", "text": "0F172A"},
    "premium_business": {"primary": "064E3B", "secondary": "047857", "accent": "D97706", "bg": "F0FDF4", "card": "FFFFFF", "text": "064E3B"},
    "technology_futuristic": {"primary": "0B0F19", "secondary": "1E293B", "accent": "06B6D4", "bg": "0F172A", "card": "1E293B", "text": "F8FAFC"},
    "creative_experimental": {"primary": "581C87", "secondary": "EA580C", "accent": "F59E0B", "bg": "FAFAF9", "card": "FFFFFF", "text": "18181B"},
    "government_institutional": {"primary": "1E3A5F", "secondary": "991B1B", "accent": "0284C7", "bg": "F1F5F9", "card": "FFFFFF", "text": "1E293B"},
    "engineering_technical": {"primary": "0284C7", "secondary": "334155", "accent": "F59E0B", "bg": "FFFFFF", "card": "F8FAFC", "text": "1E293B"},
    "educational_instructional": {"primary": "2563EB", "secondary": "059669", "accent": "F59E0B", "bg": "F0FDF4", "card": "FFFFFF", "text": "1E293B"},
    "magazine_publication": {"primary": "18181B", "secondary": "DC2626", "accent": "4B5563", "bg": "FFFFFF", "card": "F9FAFB", "text": "18181B"},
    "luxury_hospitality": {"primary": "271810", "secondary": "92400E", "accent": "EAB308", "bg": "FFFFF0", "card": "FFFFFF", "text": "271810"},
    "data_analytical": {"primary": "0F172A", "secondary": "1E293B", "accent": "2563EB", "bg": "F8FAFC", "card": "FFFFFF", "text": "0F172A"},
}

def hex_to_rgb(hex_str: str) -> RGBColor:
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join(c * 2 for c in hex_str)
    return RGBColor(int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))

def set_slide_background(slide, prs, hex_color: str):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = hex_to_rgb(hex_color)
    bg_shape.line.fill.background()
    # Move behind other elements
    slide.shapes._spTree.remove(bg_shape._element)
    slide.shapes._spTree.insert(2, bg_shape._element)

def add_header(slide, title_text: str, category_text: str, palette: dict, dark_mode: bool = False):
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    if category_text:
        cat_p = tf.paragraphs[0]
        cat_run = cat_p.add_run()
        cat_run.text = category_text.upper()
        cat_run.font.name = "Calibri"
        cat_run.font.size = Pt(9.5)
        cat_run.font.bold = True
        cat_run.font.color.rgb = hex_to_rgb(palette["accent"])
        title_p = tf.add_paragraph()
    else:
        title_p = tf.paragraphs[0]

    title_run = title_p.add_run()
    title_run.text = title_text
    title_run.font.name = "Calibri"
    title_run.font.size = Pt(24)
    title_run.font.bold = True
    title_run.font.color.rgb = hex_to_rgb("F8FAFC" if dark_mode else palette["primary"])

def add_footer(slide, title: str, org: str, palette: dict, dark_mode: bool = False):
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.7), Inches(0.3))
    tf = footer_box.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"{org}  •  {title}  •  Confidential & Certified Architecture"
    p.font.name = "Calibri"
    p.font.size = Pt(8.5)
    p.font.color.rgb = hex_to_rgb("64748B" if dark_mode else "94A3B8")

def build_pptx_from_spec(spec: dict, output_path: str):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    meta = spec.get("metadata", {})
    design = spec.get("design", {})
    content = spec.get("content", {})

    archetype = design.get("archetype", "modern_corporate")
    palette = PALETTES.get(archetype, PALETTES["modern_corporate"])
    if design.get("primary_color"):
        palette["primary"] = design["primary_color"].lstrip("#")
    if design.get("accent_color"):
        palette["accent"] = design["accent_color"].lstrip("#")

    dark_mode = archetype == "technology_futuristic"
    title = meta.get("title", "Enterprise Presentation")
    org = meta.get("organization", "Enterprise AI Systems")

    slides_data = content.get("slides", [])
    if not slides_data:
        slides_data = [
            {"type": "title", "title": title, "subtitle": meta.get("subtitle", "Strategic Architecture Briefing")},
            {"type": "cards", "title": "Strategic Foundation", "category": "OVERVIEW", "cards": [
                {"header": "Scalable Execution", "body": "Continuous batching and deterministic execution pipelines."},
                {"header": "Visual Excellence", "body": "Bespoke design archetypes ensuring high visual craft."},
                {"header": "Verified Safety", "body": "Automated scoring rubric enforcing production thresholds."}
            ]}
        ]

    for slide_data in slides_data:
        stype = slide_data.get("type", "cards")
        slide = prs.slides.add_slide(blank_layout)
        set_slide_background(slide, prs, palette["bg"])
        add_footer(slide, title, org, palette, dark_mode)

        if stype == "title":
            # Hero Title Slide
            hero_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.5))
            hero_box.fill.solid()
            hero_box.fill.fore_color.rgb = hex_to_rgb(palette["primary"])
            hero_box.line.fill.background()

            tf = hero_box.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.8)
            tf.margin_top = Inches(0.8)
            tf.margin_right = Inches(0.8)

            tag_p = tf.paragraphs[0]
            tag_r = tag_p.add_run()
            tag_r.text = f"ENTERPRISE STRATEGIC BRIEFING  •  {archetype.upper().replace('_', ' ')}\n\n"
            tag_r.font.size = Pt(11)
            tag_r.font.bold = True
            tag_r.font.color.rgb = hex_to_rgb(palette["accent"])

            title_p = tf.add_paragraph()
            title_r = title_p.add_run()
            title_r.text = f"{slide_data.get('title', title)}\n"
            title_r.font.size = Pt(32)
            title_r.font.bold = True
            title_r.font.color.rgb = hex_to_rgb("FFFFFF")

            sub_p = tf.add_paragraph()
            sub_text = slide_data.get("subtitle") or meta.get("subtitle", "")
            sub_r = sub_p.add_run()
            sub_r.text = f"{sub_text}\n\n"
            sub_r.font.size = Pt(16)
            sub_r.font.color.rgb = hex_to_rgb("E2E8F0")

            meta_p = tf.add_paragraph()
            meta_r = meta_p.add_run()
            meta_r.text = f"Author: {meta.get('author', 'Principal Architect')}  •  {meta.get('date', '2026-11-10')}"
            meta_r.font.size = Pt(10)
            meta_r.font.color.rgb = hex_to_rgb("94A3B8")

        elif stype == "cards":
            add_header(slide, slide_data.get("title", ""), slide_data.get("category", ""), palette, dark_mode)
            cards = slide_data.get("cards", [])
            num_cards = max(1, min(len(cards), 4))
            total_w = 11.733
            card_w = (total_w - (num_cards - 1) * 0.35) / num_cards
            card_h = 4.8
            top_y = 1.7

            for idx, c in enumerate(cards[:4]):
                left_x = 0.8 + idx * (card_w + 0.35)
                box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_x), Inches(top_y), Inches(card_w), Inches(card_h))
                box.fill.solid()
                box.fill.fore_color.rgb = hex_to_rgb(palette["card"])
                box.line.color.rgb = hex_to_rgb(palette["secondary"] if dark_mode else "CBD5E1")
                box.line.width = Pt(1)

                tf = box.text_frame
                tf.word_wrap = True
                tf.margin_left = Inches(0.35)
                tf.margin_top = Inches(0.4)
                tf.margin_right = Inches(0.35)

                num_p = tf.paragraphs[0]
                num_r = num_p.add_run()
                num_r.text = f"0{idx+1}\n\n"
                num_r.font.size = Pt(12)
                num_r.font.bold = True
                num_r.font.color.rgb = hex_to_rgb(palette["accent"])

                head_p = tf.add_paragraph()
                head_r = head_p.add_run()
                head_r.text = f"{c.get('header', '')}\n\n"
                head_r.font.size = Pt(18)
                head_r.font.bold = True
                head_r.font.color.rgb = hex_to_rgb("F8FAFC" if dark_mode else palette["primary"])

                body_p = tf.add_paragraph()
                body_r = body_p.add_run()
                body_r.text = c.get("body", "")
                body_r.font.size = Pt(12)
                body_r.font.color.rgb = hex_to_rgb("94A3B8" if dark_mode else palette["text"])

        elif stype == "stats":
            add_header(slide, slide_data.get("title", ""), slide_data.get("category", ""), palette, dark_mode)
            cards = slide_data.get("cards", [])
            num_cards = max(1, min(len(cards), 4))
            total_w = 11.733
            card_w = (total_w - (num_cards - 1) * 0.35) / num_cards
            top_y = 2.0
            card_h = 4.2

            for idx, c in enumerate(cards[:4]):
                left_x = 0.8 + idx * (card_w + 0.35)
                box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_x), Inches(top_y), Inches(card_w), Inches(card_h))
                box.fill.solid()
                box.fill.fore_color.rgb = hex_to_rgb(palette["card"])
                box.line.color.rgb = hex_to_rgb(palette["secondary"] if dark_mode else "E2E8F0")
                box.line.width = Pt(1.5)

                tf = box.text_frame
                tf.word_wrap = True
                tf.margin_left = Inches(0.35)
                tf.margin_top = Inches(0.5)
                tf.margin_right = Inches(0.35)

                stat_p = tf.paragraphs[0]
                stat_r = stat_p.add_run()
                stat_r.text = f"{c.get('stat', '0%')}\n\n"
                stat_r.font.size = Pt(40)
                stat_r.font.bold = True
                stat_r.font.color.rgb = hex_to_rgb(palette["accent"])

                head_p = tf.add_paragraph()
                head_r = head_p.add_run()
                head_r.text = f"{c.get('header', '')}\n\n"
                head_r.font.size = Pt(16)
                head_r.font.bold = True
                head_r.font.color.rgb = hex_to_rgb("F8FAFC" if dark_mode else palette["primary"])

                body_p = tf.add_paragraph()
                body_r = body_p.add_run()
                body_r.text = c.get("body", "")
                body_r.font.size = Pt(11.5)
                body_r.font.color.rgb = hex_to_rgb("94A3B8" if dark_mode else palette["text"])

        elif stype in ("conclusion", "custom"):
            add_header(slide, slide_data.get("title", ""), slide_data.get("category", "KEY TAKEAWAYS"), palette, dark_mode)
            box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
            box.fill.solid()
            box.fill.fore_color.rgb = hex_to_rgb(palette["card"])
            box.line.color.rgb = hex_to_rgb("CBD5E1")
            box.line.width = Pt(1)

            tf = box.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.6)
            tf.margin_top = Inches(0.6)
            tf.margin_right = Inches(0.6)

            bullets = slide_data.get("bullets", [])
            for b_idx, bullet in enumerate(bullets):
                p = tf.paragraphs[0] if b_idx == 0 else tf.add_paragraph()
                p.space_after = Pt(14)
                r_num = p.add_run()
                r_num.text = "✓  "
                r_num.font.bold = True
                r_num.font.size = Pt(14)
                r_num.font.color.rgb = hex_to_rgb(palette["accent"])
                r_text = p.add_run()
                r_text.text = bullet
                r_text.font.size = Pt(14)
                r_text.font.color.rgb = hex_to_rgb("F8FAFC" if dark_mode else palette["text"])

    out_p = pathlib.Path(output_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_p.with_suffix(".tmp.pptx")
    try:
        prs.save(str(tmp_path))
        tmp_path.replace(out_p)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise

    return str(out_p)

def main():
    parser = argparse.ArgumentParser(description="Master PPTX Production Engine")
    parser.add_argument("--spec", help="Path to document spec JSON")
    parser.add_argument("--out", "--output", required=True, help="Destination .pptx file path")
    parser.add_argument("--title", default="Executive Presentation", help="Title")
    parser.add_argument("--author", default="Principal Architect", help="Author")
    parser.add_argument("--archetype", default="premium_business", help="Archetype")
    args = parser.parse_args()

    if args.spec and os.path.exists(args.spec):
        with open(args.spec, "r", encoding="utf-8") as f:
            spec = json.load(f)
    else:
        spec = {
            "metadata": {"title": args.title, "author": args.author, "format": "pptx"},
            "design": {"archetype": args.archetype},
            "content": {
                "slides": [
                    {"type": "title", "title": args.title, "subtitle": "Autonomous Presentation Studio"},
                    {"type": "cards", "title": "Execution Highlights", "category": "MILESTONES", "cards": [
                        {"header": "Architectural Design", "body": "16:9 widescreen layout adhering to visual archetypes."},
                        {"header": "Automatic Verification", "body": "Every slide inspected for text bounds and contrast."}
                    ]}
                ]
            }
        }

    out_file = build_pptx_from_spec(spec, args.out)
    print(f"✅ Master PPTX successfully built: {out_file} ({os.path.getsize(out_file)} bytes)")

if __name__ == "__main__":
    main()
