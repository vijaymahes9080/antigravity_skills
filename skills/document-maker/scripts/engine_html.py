#!/usr/bin/env python3
"""
engine_html.py — Master Responsive HTML Report Production Engine
Part of document-maker skill.
"""

import os
import sys
import json
import argparse
import html
import pathlib

PALETTES = {
    "modern_corporate": {"primary": "#0A192F", "secondary": "#1E3A8A", "accent": "#0284C7", "bg": "#F8FAFC", "card": "#FFFFFF", "text": "#1E293B", "border": "#E2E8F0"},
    "minimalist_editorial": {"primary": "#111827", "secondary": "#374151", "accent": "#C2410C", "bg": "#FDFBF7", "card": "#FFFFFF", "text": "#1F2937", "border": "#E5E7EB"},
    "academic_scientific": {"primary": "#000000", "secondary": "#1E293B", "accent": "#2563EB", "bg": "#FFFFFF", "card": "#F8FAFC", "text": "#0F172A", "border": "#CBD5E1"},
    "premium_business": {"primary": "#064E3B", "secondary": "#047857", "accent": "#D97706", "bg": "#F0FDF4", "card": "#FFFFFF", "text": "#064E3B", "border": "#A7F3D0"},
    "technology_futuristic": {"primary": "#0B0F19", "secondary": "#1E293B", "accent": "#06B6D4", "bg": "#0F172A", "card": "#1E293B", "text": "#F8FAFC", "border": "#334155"},
    "engineering_technical": {"primary": "#0284C7", "secondary": "#334155", "accent": "#F59E0B", "bg": "#FFFFFF", "card": "#F8FAFC", "text": "#1E293B", "border": "#BAE6FD"},
    "educational_instructional": {"primary": "#2563EB", "secondary": "#059669", "accent": "#F59E0B", "bg": "#F0FDF4", "card": "#FFFFFF", "text": "#1E293B", "border": "#BBF7D0"},
    "data_analytical": {"primary": "#0F172A", "secondary": "#1E293B", "accent": "#2563EB", "bg": "#F8FAFC", "card": "#FFFFFF", "text": "#0F172A", "border": "#CBD5E1"},
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
:root {{
  --primary: {primary};
  --secondary: {secondary};
  --accent: {accent};
  --bg-main: {bg};
  --card-bg: {card};
  --text-main: {text};
  --border: {border};
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: var(--bg-main);
  color: var(--text-main);
  line-height: 1.6;
  padding: 40px 20px;
  transition: background-color 0.3s ease, color 0.3s ease;
}}
.container {{
  max-width: 900px;
  margin: 0 auto;
  background: var(--card-bg);
  padding: 45px 55px;
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
  border: 1px solid var(--border);
}}
.header-bar {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid var(--border);
  padding-bottom: 20px;
  margin-bottom: 30px;
}}
.brand-tag {{
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--accent);
  letter-spacing: 0.05em;
}}
.theme-btn {{
  background: transparent;
  border: 1px solid var(--border);
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.85rem;
  cursor: pointer;
  color: var(--text-main);
}}
.cover h1 {{
  font-size: 2.2rem;
  color: var(--primary);
  font-weight: 800;
  line-height: 1.25;
  margin-bottom: 8px;
}}
.cover .subtitle {{
  font-size: 1.15rem;
  color: var(--secondary);
  font-weight: 500;
  margin-bottom: 14px;
}}
.meta-strip {{
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 0.9rem;
  color: #64748B;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 30px;
}}
h2 {{
  font-size: 1.4rem;
  color: var(--primary);
  margin: 28px 0 14px 0;
  font-weight: 700;
  border-left: 4px solid var(--accent);
  padding-left: 12px;
}}
h3 {{
  font-size: 1.15rem;
  color: var(--secondary);
  margin: 20px 0 10px 0;
}}
p {{ margin-bottom: 14px; }}
ul, ol {{ margin-bottom: 16px; padding-left: 24px; }}
li {{ margin-bottom: 6px; }}
.callout {{
  background: var(--bg-main);
  border-left: 4px solid var(--accent);
  padding: 16px 20px;
  border-radius: 0 8px 8px 0;
  margin: 20px 0;
  font-size: 0.95rem;
}}
.callout strong {{ color: var(--primary); }}
table {{
  width: 100%;
  border-collapse: collapse;
  margin: 24px 0;
  font-size: 0.92rem;
}}
th {{
  background-color: var(--primary);
  color: #FFFFFF;
  text-align: left;
  padding: 10px 14px;
  font-weight: 600;
}}
td {{
  padding: 9px 14px;
  border-bottom: 1px solid var(--border);
}}
tr:nth-child(even) {{
  background-color: var(--bg-main);
}}
pre {{
  background: #0F172A;
  color: #F8FAFC;
  padding: 16px 20px;
  border-radius: 8px;
  overflow-x: auto;
  font-family: Consolas, Monaco, "Courier New", monospace;
  font-size: 0.88rem;
  margin: 20px 0;
}}
.footer-bar {{
  margin-top: 50px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
  font-size: 0.85rem;
  color: #94A3B8;
  display: flex;
  justify-content: space-between;
}}
@media print {{
  body {{ padding: 0; background: #FFF; }}
  .container {{ box-shadow: none; border: none; padding: 0; max-width: 100%; }}
  .theme-btn {{ display: none; }}
}}
</style>
</head>
<body>
<div class="container">
  <div class="header-bar">
    <div class="brand-tag">Document Maker • {archetype_title}</div>
    <button class="theme-btn" onclick="toggleTheme()">Toggle Contrast</button>
  </div>
  <div class="cover">
    <h1>{title}</h1>
    {subtitle_html}
    <div class="meta-strip">
      <span>Author: <strong>{author}</strong></span>
      <span>Organization: <strong>{org}</strong></span>
      <span>Date: <strong>{date_str}</strong></span>
    </div>
  </div>
  {content_body}
  <div class="footer-bar">
    <span>Verified Autonomous Output</span>
    <span>Document Maker Studio</span>
  </div>
</div>
<script>
function toggleTheme() {{
  const b = document.body;
  if (b.style.filter === 'invert(0.9) hue-rotate(180deg)') {{
    b.style.filter = '';
  }} else {{
    b.style.filter = 'invert(0.9) hue-rotate(180deg)';
  }}
}}
</script>
</body>
</html>
"""

def build_html_from_spec(spec: dict, output_path: str):
    meta = spec.get("metadata", {})
    design = spec.get("design", {})
    content = spec.get("content", {})

    title = html.escape(meta.get("title", "Executive Technical Report"))
    subtitle = meta.get("subtitle", "")
    author = html.escape(meta.get("author", "Principal Architect"))
    org = html.escape(meta.get("organization", "Enterprise Studio"))
    date_str = html.escape(meta.get("date", "2026-11-10"))

    archetype = design.get("archetype", "modern_corporate")
    palette = PALETTES.get(archetype, PALETTES["modern_corporate"])

    subtitle_html = f'<div class="subtitle">{html.escape(subtitle)}</div>' if subtitle else ''

    body_parts = []

    if content.get("abstract"):
        body_parts.append(f'<div class="callout"><strong>Executive Abstract:</strong> <em>{html.escape(content["abstract"])}</em></div>')

    # Educational Lab Record
    if "educational" in content and content["educational"]:
        edu = content["educational"]
        exp_no = html.escape(str(edu.get("experiment_no", "01")))
        body_parts.append(f'<h2>Experiment No. {exp_no}: {title}</h2>')

        if edu.get("aim"):
            body_parts.append(f'<h3>1. Aim</h3><p>{html.escape(edu["aim"])}</p>')

        if edu.get("system_requirements"):
            body_parts.append('<h3>2. System Requirements & Tools</h3><ul>')
            for req in edu["system_requirements"]:
                body_parts.append(f'<li>{html.escape(req)}</li>')
            body_parts.append('</ul>')

        if edu.get("algorithm"):
            body_parts.append('<h3>3. Algorithm / Methodology</h3><ol>')
            for step in edu["algorithm"]:
                body_parts.append(f'<li>{html.escape(step)}</li>')
            body_parts.append('</ol>')

        if edu.get("code"):
            body_parts.append(f'<h3>4. Program Source Code</h3><pre><code>{html.escape(edu["code"])}</code></pre>')

        if edu.get("sample_output"):
            body_parts.append(f'<h3>5. Sample Output</h3><pre><code>{html.escape(edu["sample_output"])}</code></pre>')

        if edu.get("result_and_inference"):
            body_parts.append(f'<h3>6. Result & Inference</h3><p>{html.escape(edu["result_and_inference"])}</p>')

    # Standard Sections
    for sec in content.get("sections", []):
        stitle = html.escape(sec.get("title", ""))
        level = sec.get("level", 1)
        tag = "h2" if level == 1 else "h3"
        body_parts.append(f'<{tag}>{stitle}</{tag}>')

        for p in sec.get("paragraphs", []):
            body_parts.append(f'<p>{html.escape(p)}</p>')

        if sec.get("bullet_points"):
            body_parts.append('<ul>')
            for b in sec["bullet_points"]:
                body_parts.append(f'<li>{html.escape(b)}</li>')
            body_parts.append('</ul>')

        if sec.get("callout"):
            body_parts.append(f'<div class="callout"><strong>Takeaway:</strong> {html.escape(sec["callout"])}</div>')

        if sec.get("table") and sec["table"].get("headers"):
            headers = sec["table"]["headers"]
            rows = sec["table"].get("rows", [])
            body_parts.append('<table><thead><tr>')
            for h in headers:
                body_parts.append(f'<th>{html.escape(str(h))}</th>')
            body_parts.append('</tr></thead><tbody>')
            for row in rows:
                body_parts.append('<tr>')
                for val in row:
                    body_parts.append(f'<td>{html.escape(str(val))}</td>')
                body_parts.append('</tr>')
            body_parts.append('</tbody></table>')

        if sec.get("code_block") and sec["code_block"].get("code"):
            body_parts.append(f'<pre><code>{html.escape(sec["code_block"]["code"])}</code></pre>')

    content_body = "\n".join(body_parts)

    rendered_html = HTML_TEMPLATE.format(
        title=title,
        subtitle_html=subtitle_html,
        author=author,
        org=org,
        date_str=date_str,
        archetype_title=archetype.upper().replace("_", " "),
        primary=palette["primary"],
        secondary=palette["secondary"],
        accent=palette["accent"],
        bg=palette["bg"],
        card=palette["card"],
        text=palette["text"],
        border=palette["border"],
        content_body=content_body
    )

    out_p = pathlib.Path(output_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_p.with_suffix(".tmp.html")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)
        tmp_path.replace(out_p)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise

    return str(out_p)

def main():
    parser = argparse.ArgumentParser(description="Master HTML Production Engine")
    parser.add_argument("--spec", help="Path to document spec JSON")
    parser.add_argument("--out", "--output", required=True, help="Destination .html file path")
    args = parser.parse_args()

    if args.spec and os.path.exists(args.spec):
        with open(args.spec, "r", encoding="utf-8") as f:
            spec = json.load(f)
    else:
        spec = {"metadata": {"title": "Executive Report", "format": "html"}}

    out_file = build_html_from_spec(spec, args.out)
    print(f"✅ Master HTML successfully built: {out_file} ({os.path.getsize(out_file)} bytes)")

if __name__ == "__main__":
    main()

