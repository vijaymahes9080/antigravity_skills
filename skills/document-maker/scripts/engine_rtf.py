#!/usr/bin/env python3
"""
engine_rtf.py — Master Lightweight RTF 1.9 Document Engine (stdlib only)
Part of document-maker skill.
"""

import os
import sys
import json
import argparse
import pathlib

def _rtf_escape(text: str) -> str:
    if text is None:
        return ""
    text = str(text)
    text = text.replace("\\", "\\\\")
    text = text.replace("{", "\\{")
    text = text.replace("}", "\\}")
    res = []
    for ch in text:
        code = ord(ch)
        if code > 127:
            res.append(f"\\u{code}?")
        else:
            res.append(ch)
    return "".join(res)

def build_rtf_from_spec(spec: dict, output_path: str):
    meta = spec.get("metadata", {})
    design = spec.get("design", {})
    content = spec.get("content", {})

    title = meta.get("title", "Executive Technical Report")
    subtitle = meta.get("subtitle", "")
    author = meta.get("author", "Principal Architect")
    org = meta.get("organization", "Enterprise Studio")
    date_str = meta.get("date", "2026-11-10")

    archetype = design.get("archetype", "modern_corporate")

    # Font and color tables
    # Color table: 0=auto, 1=navy (#0A192F: 10,25,47), 2=blue (#1E3A8A: 30,58,138), 3=accent (#0284C7: 2,132,199), 4=muted (#64748B: 100,116,139), 5=bg (#F8FAFC: 248,250,252)
    header = (
        "{\\rtf1\\ansi\\ansicpg1252\\deff0\\deflang1033\n"
        "{\\fonttbl{\\f0\\fnil\\fcharset0 Calibri;}{\\f1\\fnil\\fcharset0 Consolas;}{\\f2\\fnil\\fcharset0 Times New Roman;}}\n"
        "{\\colortbl ;\\red10\\green25\\blue47;\\red30\\green58\\blue138;\\red2\\green132\\blue199;\\red100\\green116\\blue139;\\red248\\green250\\blue252;}\n"
        "\\viewkind4\\uc1\\pard\\f0\\fs22\n"
    )

    # Margins: 1 inch = 1440 twips
    margins = "\\margl1440\\margr1440\\margt1440\\margb1440\n"

    # Header & Footer
    hf = (
        "{\\header\\pard\\qr\\f0\\fs17\\cf4 " + _rtf_escape(f"{org}  |  {title}") + "\\par}\n"
        "{\\footer\\pard\\qc\\f0\\fs17\\cf4 " + _rtf_escape("Confidential  •  Document Maker Autonomous Studio") + "  •  Page {\\chpgn}\\par}\n"
    )

    body = []

    # Title block
    body.append("{\\pard\\sa200\\b\\fs48\\cf1 " + _rtf_escape(title) + "\\par}\n")
    if subtitle:
        body.append("{\\pard\\sa140\\b\\fs26\\cf2 " + _rtf_escape(subtitle) + "\\par}\n")
    body.append("{\\pard\\sa240\\fs18\\cf4 " + _rtf_escape(f"Author: {author}  •  Organization: {org}  •  Date: {date_str}") + "\\par}\n")
    body.append("{\\pard\\brdrb\\brdrs\\brdrw10\\brdrcf3\\sa200\\par}\n")

    # Abstract
    if content.get("abstract"):
        body.append("{\\pard\\sa180\\i\\fs22 " + _rtf_escape(f"Abstract: {content['abstract']}") + "\\par}\n")

    # Educational lab record
    if "educational" in content and content["educational"]:
        edu = content["educational"]
        body.append("{\\pard\\sa160\\keepn\\b\\fs32\\cf1 " + _rtf_escape(f"EXPERIMENT NO. {edu.get('experiment_no', '01')} : {title.upper()}") + "\\par}\n")

        if edu.get("aim"):
            body.append("{\\pard\\sa80\\keepn\\b\\fs24\\cf2 1. AIM:\\par}\n")
            body.append("{\\pard\\sa140\\fs22 " + _rtf_escape(edu["aim"]) + "\\par}\n")

        if edu.get("system_requirements"):
            body.append("{\\pard\\sa80\\keepn\\b\\fs24\\cf2 2. SYSTEM REQUIREMENTS & TOOLS:\\par}\n")
            for req in edu["system_requirements"]:
                body.append("{\\pard\\li360\\sa60\\fs22 \\bullet  " + _rtf_escape(req) + "\\par}\n")

        if edu.get("algorithm"):
            body.append("{\\pard\\sa80\\keepn\\b\\fs24\\cf2 3. ALGORITHM / METHODOLOGY:\\par}\n")
            for s_idx, step in enumerate(edu["algorithm"], 1):
                body.append("{\\pard\\li360\\sa60\\fs22 " + _rtf_escape(f"Step {s_idx}: {step}") + "\\par}\n")

        if edu.get("code"):
            body.append("{\\pard\\sa80\\keepn\\b\\fs24\\cf2 4. PROGRAM SOURCE CODE:\\par}\n")
            for line in edu["code"].splitlines():
                body.append("{\\pard\\li360\\f1\\fs18\\cf1 " + _rtf_escape(line) + "\\par}\n")

        if edu.get("sample_output"):
            body.append("{\\pard\\sa80\\keepn\\b\\fs24\\cf2 5. SAMPLE OUTPUT:\\par}\n")
            for line in edu["sample_output"].splitlines():
                body.append("{\\pard\\li360\\f1\\fs18\\cf3 " + _rtf_escape(line) + "\\par}\n")

        if edu.get("result_and_inference"):
            body.append("{\\pard\\sa80\\keepn\\b\\fs24\\cf2 6. RESULT & INFERENCES:\\par}\n")
            body.append("{\\pard\\sa140\\fs22 " + _rtf_escape(edu["result_and_inference"]) + "\\par}\n")

    # Sections
    for sec in content.get("sections", []):
        level = sec.get("level", 1)
        font_size = "32" if level == 1 else "26"
        color_tag = "\\cf1" if level == 1 else "\\cf2"
        body.append(f"{{\\pard\\sb200\\sa100\\keepn\\b\\fs{font_size}{color_tag} " + _rtf_escape(sec["title"]) + "\\par}\n")

        for p in sec.get("paragraphs", []):
            body.append("{\\pard\\sa120\\fs22 " + _rtf_escape(p) + "\\par}\n")

        for bullet in sec.get("bullet_points", []):
            body.append("{\\pard\\li360\\sa60\\fs22 \\bullet  " + _rtf_escape(bullet) + "\\par}\n")

        if sec.get("callout"):
            body.append("{\\pard\\li360\\ri360\\sb80\\sa140\\brdrl\\brdrs\\brdrw25\\brdrcf3\\i\\fs20\\cf1 " + _rtf_escape(f"Note: {sec['callout']}") + "\\par}\n")

        if sec.get("table") and sec["table"].get("headers"):
            headers = sec["table"]["headers"]
            rows = sec["table"].get("rows", [])
            # Simple RTF Table representation
            col_width = int(8640 / max(1, len(headers)))
            # Header
            header_def = "\\trowd\\trgaph108"
            for i in range(1, len(headers) + 1):
                header_def += f"\\clbrdrt\\brdrs\\clbrdrl\\brdrs\\clbrdrb\\brdrs\\clbrdrr\\brdrs\\cellx{i * col_width}"
            body.append(header_def + "\n")
            for h in headers:
                body.append("{\\pard\\qc\\b\\fs20\\cf1 " + _rtf_escape(str(h)) + "\\cell}")
            body.append("\\row\n")

            # Rows
            for row in rows:
                row_def = "\\trowd\\trgaph108"
                for i in range(1, len(headers) + 1):
                    row_def += f"\\clbrdrt\\brdrs\\clbrdrl\\brdrs\\clbrdrb\\brdrs\\clbrdrr\\brdrs\\cellx{i * col_width}"
                body.append(row_def + "\n")
                for val in row:
                    body.append("{\\pard\\fs20 " + _rtf_escape(str(val)) + "\\cell}")
                body.append("\\row\n")

        if sec.get("code_block") and sec["code_block"].get("code"):
            body.append("{\\pard\\sb80\\sa40\\b\\fs20\\cf2 Code Listing:\\par}\n")
            for line in sec["code_block"]["code"].splitlines():
                body.append("{\\pard\\li360\\f1\\fs18\\cf1 " + _rtf_escape(line) + "\\par}\n")

    full_rtf = header + margins + hf + "".join(body) + "}\n"

    out_p = pathlib.Path(output_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_p.with_suffix(".tmp.rtf")
    try:
        with open(tmp_path, "w", encoding="ascii", errors="replace") as f:
            f.write(full_rtf)
        tmp_path.replace(out_p)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise

    return str(out_p)

def main():
    parser = argparse.ArgumentParser(description="Master RTF Production Engine")
    parser.add_argument("--spec", help="Path to document spec JSON")
    parser.add_argument("--out", "--output", required=True, help="Destination .rtf file path")
    args = parser.parse_args()

    if args.spec and os.path.exists(args.spec):
        with open(args.spec, "r", encoding="utf-8") as f:
            spec = json.load(f)
    else:
        spec = {"metadata": {"title": "Executive Report", "format": "rtf"}}

    out_file = build_rtf_from_spec(spec, args.out)
    print(f"✅ Master RTF successfully built: {out_file} ({os.path.getsize(out_file)} bytes)")

if __name__ == "__main__":
    main()

