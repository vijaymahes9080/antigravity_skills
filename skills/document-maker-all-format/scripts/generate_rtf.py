#!/usr/bin/env python3
"""
generate_rtf.py — Lightweight RTF 1.9 document writer (stdlib only).

RTF (Rich Text Format) is a plain-text markup language. This writer
produces valid RTF 1.9 compatible with Microsoft Word, LibreOffice
Writer, Apple TextEdit, and WordPad.

Usage:
    python scripts/generate_rtf.py --title "Document" --author "Author" \
        --output output/document.rtf [--brief brief.json]

Limitations (documented, not hidden):
    • No embedded OLE objects
    • No complex merged-cell tables
    • No embedded raster images (text-only)
    • No animated content
"""
import argparse
import json
import pathlib
import re
from datetime import datetime
from typing import Any


# ─── RTF escape helpers ───────────────────────────────────────────────────────

def _rtf_escape(text: str) -> str:
    """Escape RTF special characters and encode non-ASCII as Unicode escapes."""
    text = text.replace("\\", "\\\\")
    text = text.replace("{",  "\\{")
    text = text.replace("}",  "\\}")
    # Encode non-ASCII characters as RTF Unicode escapes \uNNNN?
    result = []
    for ch in text:
        code = ord(ch)
        if code > 127:
            result.append(f"\\u{code}?")
        else:
            result.append(ch)
    return "".join(result)


def _rtf_para(text: str, style: str = "normal", level: int = 0) -> str:
    """Wrap text in RTF paragraph markup."""
    escaped = _rtf_escape(text)

    if style == "h1":
        return (
            f"\\pard\\sb240\\sa120\\keepn\\b\\fs48 {escaped}\\b0\\fs22\\par\n"
        )
    elif style == "h2":
        return (
            f"\\pard\\sb200\\sa100\\keepn\\b\\fs36\\cf2 {escaped}\\b0\\fs22\\cf0\\par\n"
        )
    elif style == "h3":
        return (
            f"\\pard\\sb160\\sa80\\keepn\\b\\fs28 {escaped}\\b0\\fs22\\par\n"
        )
    elif style == "caption":
        return (
            f"\\pard\\qc\\sb60\\sa60\\i\\fs18\\cf3 {escaped}\\i0\\fs22\\cf0\\par\n"
        )
    elif style == "bullet":
        return (
            f"\\pard\\li360\\fi-360\\sb40\\sa40\\fs22 \\bullet\\tab {escaped}\\par\n"
        )
    else:
        # Normal body paragraph
        return (
            f"\\pard\\sb40\\sa80\\sl276\\slmult1\\fs22 {escaped}\\par\n"
        )


def _rtf_table_row(cells: list[str], is_header: bool = False,
                   col_widths: list[int] | None = None) -> str:
    """Build a single RTF table row."""
    n = len(cells)
    if col_widths is None:
        col_widths = [2160] * n  # 2160 twips = ~3.8 cm

    row = "\\trowd\\trgaph108\\trleft-108\n"
    pos = 0
    for w in col_widths:
        pos += w
        row += f"\\clbrdrt\\brdrw15\\brdrs\\clbrdrl\\brdrw15\\brdrs"
        row += f"\\clbrdrb\\brdrw15\\brdrs\\clbrdrr\\brdrw15\\brdrs"
        if is_header:
            row += "\\clcbpat2"   # navy background (color index 2)
        row += f"\\cellx{pos}\n"

    for cell_text in cells:
        escaped = _rtf_escape(str(cell_text))
        if is_header:
            row += f"\\pard\\intbl\\b\\cf1\\fs20 {escaped}\\b0\\cf0\\cell\n"
        else:
            row += f"\\pard\\intbl\\fs20 {escaped}\\cell\n"

    row += "\\row\n"
    return row


def _rtf_table(table_data: dict[str, Any]) -> str:
    """Convert a table dict to RTF markup."""
    headers = table_data.get("headers", [])
    rows    = table_data.get("rows", [])
    caption = table_data.get("caption", "")
    col_count = len(headers) if headers else (len(rows[0]) if rows else 1)

    # Calculate column widths to fit page (total ~8640 twips for letter/A4 body)
    col_w = 8640 // col_count
    col_widths = [col_w] * col_count

    rtf = ""
    if headers:
        rtf += _rtf_table_row(headers, is_header=True, col_widths=col_widths)
    for row in rows:
        rtf += _rtf_table_row(row, is_header=False, col_widths=col_widths)

    rtf += "\\pard\n"  # End table context

    if caption:
        rtf += _rtf_para(caption, style="caption")

    return rtf


def generate(brief: dict[str, Any], output_path: str) -> str:
    title    = brief.get("title", "Document")
    author   = brief.get("author", "")
    sections = brief.get("sections", [])
    tables   = brief.get("tables", [])
    date_str = datetime.now().strftime("%B %d, %Y")

    # ── RTF Header ──────────────────────────────────────────────────────────
    header = (
        "{\\rtf1\\ansi\\ansicpg1252\\deff0\\deflang1033\n"
        "{\\fonttbl\n"
        "{\\f0\\froman\\fprq2\\fcharset0 Times New Roman;}\n"
        "{\\f1\\fswiss\\fprq2\\fcharset0 Arial;}\n"
        "{\\f2\\fmodern\\fprq1\\fcharset0 Courier New;}\n"
        "}\n"
        # Color table: 0=auto, 1=white, 2=navy, 3=grey/muted, 4=near-black
        "{\\colortbl;"
        "\\red255\\green255\\blue255;"           # 1 = white
        "\\red26\\green51\\blue128;"             # 2 = navy #1A3380
        "\\red140\\green140\\blue140;"           # 3 = muted #8C8C8C
        "\\red38\\green38\\blue38;"              # 4 = near-black #262626
        "\\red242\\green153\\blue16;"            # 5 = amber #F29910
        "}\n"
        "{\\info\n"
        f"{{\\title {_rtf_escape(title)}}}\n"
        f"{{\\author {_rtf_escape(author)}}}\n"
        f"{{\\creatim\\yr{datetime.now().year}\\mo{datetime.now().month}"
        f"\\dy{datetime.now().day}}}\n"
        f"{{\\comment Generated by document-maker-all-format}}\n"
        "}\n"
        # Page setup: A4, 2cm margins (1134 twips ≈ 2cm)
        "\\paperw11906\\paperh16838\n"
        "\\margl1134\\margr1134\\margt1417\\margb1417\n"
        "\\widowctrl\\hyphauto\n"
        "\\f1\\fs22\\cf4\n"  # default: Arial 11pt, near-black
    )

    # ── Cover Page ──────────────────────────────────────────────────────────
    body = ""
    body += "\\pard\\sb1440\\sa240\\qc"   # vertical push + centered
    body += f"{{\\b\\fs64\\cf2 {_rtf_escape(title)}}}"
    body += "\\par\n"
    body += "\\pard\\qc\\sb120\\sa120"
    body += f"{{\\fs28\\cf3 {_rtf_escape(author)}}}"
    body += "\\par\n"
    body += f"{{\\pard\\qc\\sb60\\fs22\\cf3 {_rtf_escape(date_str)}\\par}}\n"
    body += "\\page\n"  # page break after cover

    # ── Sections ────────────────────────────────────────────────────────────
    for section in sections:
        level   = section.get("level", 2)
        heading = section.get("heading", "")
        content = section.get("content", "")

        style_map = {1: "h1", 2: "h2", 3: "h3"}
        body += _rtf_para(heading, style=style_map.get(level, "h2"))

        for para_text in content.split("\n\n"):
            para_text = para_text.strip()
            if not para_text:
                continue
            # Detect bullet lists (lines starting with • or -)
            if re.match(r"^[•\-\*]\s", para_text):
                for line in para_text.split("\n"):
                    line = re.sub(r"^[•\-\*]\s*", "", line.strip())
                    if line:
                        body += _rtf_para(line, style="bullet")
            else:
                body += _rtf_para(para_text.replace("\n", " "))

    # ── Tables ──────────────────────────────────────────────────────────────
    for table_data in tables:
        caption = table_data.get("caption", "")
        if caption:
            body += _rtf_para(caption, style="caption")
        body += _rtf_table(table_data)

    # ── Footer & close ──────────────────────────────────────────────────────
    footer = "}\n"  # close \rtf1

    rtf_content = header + body + footer

    # Atomic write
    out = pathlib.Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp.rtf")
    tmp.write_text(rtf_content, encoding="utf-8", errors="replace")
    tmp.replace(out)

    size_kb = out.stat().st_size // 1024
    print(f"✅ RTF generated: {out}  ({size_kb} KB)")
    return str(out)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a professional RTF document.")
    parser.add_argument("--title",  default="Document")
    parser.add_argument("--author", default="")
    parser.add_argument("--output", default="output/document.rtf")
    parser.add_argument("--brief",  default=None)
    args = parser.parse_args()

    if args.brief:
        brief = json.loads(pathlib.Path(args.brief).read_text(encoding="utf-8"))
    else:
        brief = {
            "title": args.title, "author": args.author,
            "sections": [
                {"heading": "Introduction", "level": 2,
                 "content": "This RTF document was generated by document-maker-all-format.\n\nIt uses a custom RTF 1.9 writer built on Python stdlib — no external dependencies."},
                {"heading": "Features", "level": 2,
                 "content": "• Cover page with title and author\n• Styled headings H1, H2, H3\n• Body paragraphs with proper spacing\n• Bullet lists\n• Tables with header rows"},
            ],
            "tables": [
                {"caption": "Table 1 — RTF Compatibility",
                 "headers": ["Application", "Platform", "Status"],
                 "rows": [
                     ["Microsoft Word",   "Windows/macOS", "✅ Full"],
                     ["LibreOffice Writer","Cross-platform","✅ Full"],
                     ["Apple TextEdit",   "macOS",         "✅ Basic"],
                     ["WordPad",          "Windows",       "✅ Basic"],
                 ]}
            ],
        }

    generate(brief, args.output)


if __name__ == "__main__":
    main()

