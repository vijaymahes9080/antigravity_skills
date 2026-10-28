#!/usr/bin/env python3
"""
generate_pptx.py — Professional PPTX presentation generator using python-pptx.

Usage:
    python scripts/generate_pptx.py --title "Presentation" --author "Author" \
        --output output/slides.pptx [--brief brief.json]

Brief JSON format:
{
  "title": "Presentation Title",
  "author": "Author Name",
  "theme": "navy",
  "slides": [
    {"type": "title",    "title": "Main Title", "subtitle": "Subtitle"},
    {"type": "content",  "title": "Slide Title", "bullets": ["Point 1","Point 2"]},
    {"type": "two_col",  "title": "Two Columns",
     "left": "Left content", "right": "Right content"},
    {"type": "closing",  "title": "Thank You", "subtitle": "Contact info"}
  ]
}
"""
import argparse
import json
import pathlib
import sys
from datetime import datetime
from typing import Any

try:
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Emu, Inches, Pt
except ImportError:
    sys.exit("❌ python-pptx not installed. Run: python scripts/bootstrap.py")

# ─── Design System ───────────────────────────────────────────────────────────
NAVY       = RGBColor(0x1A, 0x33, 0x80)
AMBER      = RGBColor(0xF2, 0x99, 0x10)
NEAR_BLACK = RGBColor(0x26, 0x26, 0x26)
MUTED      = RGBColor(0x8C, 0x8C, 0x8C)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_BG   = RGBColor(0xF5, 0xF7, 0xFA)

SLIDE_W = Inches(13.33)  # 16:9 widescreen
SLIDE_H = Inches(7.5)

MARGIN_L = Inches(0.6)
MARGIN_T = Inches(0.4)
CONTENT_W = Inches(12.1)


def _new_presentation() -> Presentation:
    prs = Presentation()
    prs.slide_width  = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def _blank_slide(prs: Presentation):
    blank_layout = prs.slide_layouts[6]  # blank
    return prs.slides.add_slide(blank_layout)


def _add_bg(slide, color: RGBColor) -> None:
    """Fill slide background with a solid color."""
    from pptx.util import Emu
    from pptx.oxml.ns import qn
    from lxml import etree

    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def _text_box(slide, left, top, width, height,
              text: str, font_size: int, bold: bool = False,
              color: RGBColor = NEAR_BLACK,
              align=PP_ALIGN.LEFT, word_wrap: bool = True):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = word_wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    return txBox


def _add_accent_bar(slide, y_pos=None) -> None:
    """Add a horizontal amber accent bar."""
    if y_pos is None:
        y_pos = Inches(1.35)
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        MARGIN_L, y_pos, CONTENT_W, Inches(0.04)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = AMBER
    shape.line.fill.background()  # no border


def _solid_shape(slide, shape_type, left, top, width, height, color: RGBColor):
    """Add a shape with a solid fill color (safe pattern for python-pptx)."""
    shape = slide.shapes.add_shape(shape_type, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()  # remove border line
    return shape


def _slide_title(slide, prs: Presentation, title: str, subtitle: str = "") -> None:
    """Build a title / cover slide."""
    _add_bg(slide, NAVY)

    # Central title box
    _text_box(slide,
              MARGIN_L, Inches(2.5), CONTENT_W, Inches(1.8),
              title, 40, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    # Amber underline
    _solid_shape(slide, 1, MARGIN_L, Inches(4.4), CONTENT_W, Inches(0.05), AMBER)

    if subtitle:
        _text_box(slide,
                  MARGIN_L, Inches(4.6), CONTENT_W, Inches(0.8),
                  subtitle, 20, color=LIGHT_BG, align=PP_ALIGN.CENTER)

    # Date
    _text_box(slide,
              MARGIN_L, Inches(6.5), CONTENT_W, Inches(0.4),
              datetime.now().strftime("%B %d, %Y"), 12,
              color=MUTED, align=PP_ALIGN.CENTER)


def _slide_content(slide, prs: Presentation, title: str, bullets: list[str]) -> None:
    """Build a title + bullet points slide."""
    _add_bg(slide, WHITE)

    # Heading bar
    _solid_shape(slide, 1, Emu(0), Emu(0), SLIDE_W, Inches(1.2), NAVY)

    _text_box(slide, MARGIN_L, Inches(0.15), CONTENT_W, Inches(0.9),
              title, 28, bold=True, color=WHITE)

    _add_accent_bar(slide, y_pos=Inches(1.22))

    # Bullets
    content_top = Inches(1.5)
    bullet_h = Inches(0.55)
    for idx, bullet in enumerate(bullets[:10]):  # cap at 10 bullets
        y = content_top + idx * bullet_h
        if y + bullet_h > Inches(7.2):
            break  # prevent overflow
        _text_box(slide, MARGIN_L + Inches(0.3), y, CONTENT_W - Inches(0.3), bullet_h,
                  f"• {bullet}", 18, color=NEAR_BLACK)


def _slide_two_col(slide, prs: Presentation, title: str,
                   left: str, right: str) -> None:
    """Build a two-column content slide."""
    _add_bg(slide, WHITE)
    _solid_shape(slide, 1, Emu(0), Emu(0), SLIDE_W, Inches(1.2), NAVY)
    _text_box(slide, MARGIN_L, Inches(0.15), CONTENT_W, Inches(0.9),
              title, 28, bold=True, color=WHITE)
    _add_accent_bar(slide, y_pos=Inches(1.22))

    half_w = Inches(5.8)
    # Left column
    _text_box(slide, MARGIN_L, Inches(1.4), half_w, Inches(5.8),
              left, 16, color=NEAR_BLACK)
    # Vertical divider
    _solid_shape(slide, 1, Inches(6.85), Inches(1.4), Inches(0.03), Inches(5.6), MUTED)
    # Right column
    _text_box(slide, Inches(7.0), Inches(1.4), half_w, Inches(5.8),
              right, 16, color=NEAR_BLACK)


def _slide_closing(slide, prs: Presentation, title: str, subtitle: str) -> None:
    """Build a closing / thank-you slide."""
    _add_bg(slide, NEAR_BLACK)
    _text_box(slide, MARGIN_L, Inches(2.8), CONTENT_W, Inches(1.4),
              title, 40, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    if subtitle:
        _text_box(slide, MARGIN_L, Inches(4.4), CONTENT_W, Inches(0.8),
                  subtitle, 18, color=AMBER, align=PP_ALIGN.CENTER)


SLIDE_BUILDERS = {
    "title":   _slide_title,
    "content": _slide_content,
    "two_col": _slide_two_col,
    "closing": _slide_closing,
}


def generate(brief: dict[str, Any], output_path: str) -> str:
    slides_data = brief.get("slides", [])
    out = pathlib.Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp.pptx")

    prs = _new_presentation()

    for slide_data in slides_data:
        slide_type = slide_data.get("type", "content")
        slide = _blank_slide(prs)
        builder = SLIDE_BUILDERS.get(slide_type, _slide_content)

        if slide_type == "title":
            builder(slide, prs, slide_data.get("title", ""), slide_data.get("subtitle", ""))
        elif slide_type == "content":
            builder(slide, prs, slide_data.get("title", ""), slide_data.get("bullets", []))
        elif slide_type == "two_col":
            builder(slide, prs, slide_data.get("title", ""),
                    slide_data.get("left", ""), slide_data.get("right", ""))
        elif slide_type == "closing":
            builder(slide, prs, slide_data.get("title", ""), slide_data.get("subtitle", ""))
        else:
            builder(slide, prs, slide_data.get("title", ""), slide_data.get("bullets", []))

    prs.save(str(tmp))
    tmp.replace(out)

    size_kb = out.stat().st_size // 1024
    slide_count = len(prs.slides)
    print(f"✅ PPTX generated: {out}  ({slide_count} slides, {size_kb} KB)")
    return str(out)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a professional PPTX presentation.")
    parser.add_argument("--title",  default="Presentation")
    parser.add_argument("--author", default="")
    parser.add_argument("--output", default="output/presentation.pptx")
    parser.add_argument("--brief",  default=None)
    args = parser.parse_args()

    if args.brief:
        brief = json.loads(pathlib.Path(args.brief).read_text(encoding="utf-8"))
    else:
        brief = {
            "title": args.title, "author": args.author,
            "slides": [
                {"type": "title", "title": args.title,
                 "subtitle": f"Presented by {args.author}" if args.author else "Professional Presentation"},
                {"type": "content", "title": "Document Generation Capabilities",
                 "bullets": ["PDF via ReportLab 5.x", "DOCX via python-docx 1.2",
                             "PPTX via python-pptx", "XLSX via openpyxl 3.x",
                             "RTF, HTML, Markdown, Plain Text"]},
                {"type": "two_col", "title": "Design System",
                 "left": "Colors\n• Navy #1A3380\n• Amber #F29910\n• Near-Black #262626",
                 "right": "Typography\n• Helvetica / Arial\n• Body: 11–18pt\n• Headings: 24–40pt"},
                {"type": "closing", "title": "Thank You",
                 "subtitle": "document-maker-all-format | Antigravity Skill"},
            ],
        }

    generate(brief, args.output)


if __name__ == "__main__":
    main()
