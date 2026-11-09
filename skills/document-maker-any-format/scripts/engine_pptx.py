#!/usr/bin/env python3
"""
engine_pptx.py — 16:9 Enterprise Presentation Production Engine
Part of document-maker-any-format skill
"""

import os
import sys
import json
import argparse
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

PALETTES = {
    "modern_corporate": {"primary": "0A192F", "secondary": "1E3A8A", "accent": "38BDF8", "bg": "F8FAFC", "card": "FFFFFF"},
    "premium_business": {"primary": "064E3B", "secondary": "047857", "accent": "D97706", "bg": "F0FDF4", "card": "FFFFFF"},
    "technology_futuristic": {"primary": "0B0F19", "secondary": "1E293B", "accent": "06B6D4", "bg": "0F172A", "card": "1E293B"},
    "minimalist_editorial": {"primary": "111827", "secondary": "374151", "accent": "C2410C", "bg": "FDFBF7", "card": "FFFFFF"}
}

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    return RGBColor(int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))

def set_slide_background(slide, prs, hex_color):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = hex_to_rgb(hex_color)
    bg_shape.line.fill.background()
    slide.shapes._spTree.remove(bg_shape._element)
    slide.shapes._spTree.insert(2, bg_shape._element)

def add_header(slide, title_text, category_text, palette):
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.2))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    if category_text:
        cat_p = tf.paragraphs[0]
        cat_run = cat_p.add_run()
        cat_run.text = category_text.upper()
        cat_run.font.size = Pt(10)
        cat_run.font.bold = True
        cat_run.font.color.rgb = hex_to_rgb(palette["accent"])
        title_p = tf.add_paragraph()
    else:
        title_p = tf.paragraphs[0]

    title_run = title_p.add_run()
    title_run.text = title_text
    title_run.font.size = Pt(24)
    title_run.font.bold = True
    title_run.font.color.rgb = hex_to_rgb(palette["primary"])

def build_pptx(spec, output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    meta = spec.get("metadata", {})
    design = spec.get("design", {})
    archetype = design.get("archetype", "modern_corporate")
    palette = PALETTES.get(archetype, PALETTES["modern_corporate"])
    blank_layout = prs.slide_layouts[6]

    # Title Slide
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, prs, palette["primary"])

    title_box = slide1.shapes.add_textbox(Inches(1.2), Inches(2.0), Inches(10.9), Inches(3.2))
    tf1 = title_box.text_frame
    tf1.word_wrap = True

    p_t = tf1.paragraphs[0]
    r_t = p_t.add_run()
    r_t.text = meta.get("title", "Executive Presentation")
    r_t.font.size = Pt(40)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(255, 255, 255)

    if meta.get("subtitle"):
        p_sub = tf1.add_paragraph()
        p_sub.space_before = Pt(16)
        r_sub = p_sub.add_run()
        r_sub.text = meta["subtitle"]
        r_sub.font.size = Pt(18)
        r_sub.font.color.rgb = hex_to_rgb(palette["accent"])

    p_meta = tf1.add_paragraph()
    p_meta.space_before = Pt(28)
    r_meta = p_meta.add_run()
    r_meta.text = f"{meta.get('author', 'Principal Architect')}  |  {meta.get('organization', 'Enterprise Architecture')}  |  {meta.get('date', '2026')}"
    r_meta.font.size = Pt(12)
    r_meta.font.color.rgb = RGBColor(148, 163, 184)

    # Content Slides
    slides_data = spec.get("content", {}).get("slides", [])
    for s_idx, s_info in enumerate(slides_data, 1):
        slide = prs.slides.add_slide(blank_layout)
        set_slide_background(slide, prs, palette["bg"])
        add_header(slide, s_info.get("title", "Slide Title"), s_info.get("category", "Analysis"), palette)

        s_type = s_info.get("type", "cards")

        if s_type in ["cards", "3_column"]:
            cards = s_info.get("cards", [])
            card_count = max(len(cards), 1)
            gap = 0.4
            total_gap = gap * (card_count - 1)
            avail_w = 11.7 - total_gap
            card_w = avail_w / card_count

            for c_i, card in enumerate(cards):
                left = Inches(0.8 + c_i * (card_w + gap))
                top = Inches(2.0)
                width = Inches(card_w)
                height = Inches(4.6)

                card_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
                card_shape.fill.solid()
                card_shape.fill.fore_color.rgb = hex_to_rgb(palette["card"])
                card_shape.line.color.rgb = hex_to_rgb("CBD5E1")
                card_shape.line.width = Pt(1)

                ctf = card_shape.text_frame
                ctf.word_wrap = True
                ctf.margin_left = ctf.margin_right = Inches(0.25)
                ctf.margin_top = Inches(0.3)

                if card.get("stat"):
                    p_stat = ctf.paragraphs[0]
                    r_stat = p_stat.add_run()
                    r_stat.text = card["stat"]
                    r_stat.font.size = Pt(36)
                    r_stat.font.bold = True
                    r_stat.font.color.rgb = hex_to_rgb(palette["accent"])
                    p_hdr = ctf.add_paragraph()
                    p_hdr.space_before = Pt(8)
                else:
                    p_hdr = ctf.paragraphs[0]

                r_hdr = p_hdr.add_run()
                r_hdr.text = card.get("header", f"Pillar {c_i+1}")
                r_hdr.font.size = Pt(16)
                r_hdr.font.bold = True
                r_hdr.font.color.rgb = hex_to_rgb(palette["primary"])

                p_bdy = ctf.add_paragraph()
                p_bdy.space_before = Pt(12)
                r_bdy = p_bdy.add_run()
                r_bdy.text = card.get("body", "")
                r_bdy.font.size = Pt(11)
                r_bdy.font.color.rgb = hex_to_rgb("475569")

        elif s_type in ["bullets", "summary"]:
            bullets = s_info.get("bullets", [])
            b_box = slide.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.0), Inches(4.6))
            btf = b_box.text_frame
            btf.word_wrap = True

            for b_i, bullet_text in enumerate(bullets):
                bp = btf.paragraphs[0] if b_i == 0 else btf.add_paragraph()
                if b_i > 0:
                    bp.space_before = Pt(14)
                brun = bp.add_run()
                brun.text = f"•  {bullet_text}"
                brun.font.size = Pt(14)
                brun.font.color.rgb = hex_to_rgb(palette["primary"])

            side_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.2), Inches(2.0), Inches(3.3), Inches(4.6))
            side_shape.fill.solid()
            side_shape.fill.fore_color.rgb = hex_to_rgb(palette["primary"])
            side_shape.line.fill.background()
            stf = side_shape.text_frame
            stf.word_wrap = True
            stf.margin_left = stf.margin_right = Inches(0.3)
            stf.margin_top = Inches(0.4)

            sp_t = stf.paragraphs[0]
            sr_t = sp_t.add_run()
            sr_t.text = "CORE OBJECTIVE"
            sr_t.font.size = Pt(11)
            sr_t.font.bold = True
            sr_t.font.color.rgb = hex_to_rgb(palette["accent"])

            sp_b = stf.add_paragraph()
            sp_b.space_before = Pt(12)
            sr_b = sp_b.add_run()
            sr_b.text = s_info.get("subtitle", "Deliver robust, production-grade output verified by automated QA.")
            sr_b.font.size = Pt(13)
            sr_b.font.color.rgb = RGBColor(241, 245, 249)

        if s_info.get("notes"):
            notes_slide = slide.notes_slide
            text_frame = notes_slide.notes_text_frame
            text_frame.text = s_info["notes"]

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    prs.save(output_path)
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PPTX Production Engine")
    parser.add_argument("--spec", required=True, help="Path to JSON spec")
    parser.add_argument("--out", required=True, help="Output .pptx path")
    args = parser.parse_args()

    with open(args.spec, "r", encoding="utf-8") as f:
        data = json.load(f)
    res = build_pptx(data, args.out)
    print(f"SUCCESS: Generated PPTX at {res}")

