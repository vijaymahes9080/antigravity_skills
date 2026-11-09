#!/usr/bin/env python3
"""
engine_html.py — Responsive HTML & Digital Report Production Engine
Part of document-maker-any-format skill
"""

import os
import sys
import json
import argparse

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
:root {{
  --primary: #0A192F;
  --secondary: #1E3A8A;
  --accent: #0284C7;
  --bg-main: #F8FAFC;
  --card-bg: #FFFFFF;
  --text-main: #1E293B;
  --text-muted: #64748B;
  --border: #E2E8F0;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: var(--bg-main);
  color: var(--text-main);
  line-height: 1.6;
  padding: 40px 20px;
}}
.container {{
  max-width: 900px;
  margin: 0 auto;
  background: var(--card-bg);
  padding: 50px 60px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--border);
}}
.cover {{
  border-bottom: 2px solid var(--border);
  padding-bottom: 30px;
  margin-bottom: 40px;
}}
.cover h1 {{
  font-size: 2.2rem;
  color: var(--primary);
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 10px;
}}
.cover .subtitle {{
  font-size: 1.15rem;
  color: var(--secondary);
  font-weight: 500;
  margin-bottom: 20px;
}}
.cover .meta {{
  font-size: 0.9rem;
  color: var(--text-muted);
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}}
h2 {{
  font-size: 1.4rem;
  color: var(--primary);
  margin-top: 35px;
  margin-bottom: 12px;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--border);
}}
p {{
  margin-bottom: 14px;
  color: var(--text-main);
  font-size: 1.0rem;
}}
.callout {{
  background-color: #EFF6FF;
  border-left: 4px solid var(--secondary);
  padding: 16px 20px;
  margin: 20px 0;
  border-radius: 0 8px 8px 0;
  font-size: 0.98rem;
  font-weight: 500;
  color: #1E3A8A;
}}
pre.code-block {{
  background: #0F172A;
  color: #38BDF8;
  padding: 18px;
  border-radius: 8px;
  font-family: "Consolas", "Courier New", monospace;
  font-size: 0.9rem;
  overflow-x: auto;
  margin: 18px 0;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 0.95rem;
}}
th {{
  background: var(--primary);
  color: white;
  text-align: left;
  padding: 10px 14px;
  font-weight: 600;
}}
td {{
  padding: 10px 14px;
  border-bottom: 1px solid var(--border);
}}
tr:nth-child(even) td {{
  background: #F8FAFC;
}}
.footer {{
  margin-top: 50px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
  font-size: 0.85rem;
  color: var(--text-muted);
  text-align: center;
}}
@media print {{
  body {{ background: #fff; padding: 0; }}
  .container {{ box-shadow: none; border: none; padding: 0; }}
  h2 {{ page-break-after: avoid; }}
  table, pre {{ page-break-inside: avoid; }}
}}
</style>
</head>
<body>
<div class="container">
  <div class="cover">
    <h1>{title}</h1>
    {subtitle_html}
    <div class="meta">
      <span><strong>Author:</strong> {author}</span>
      <span><strong>Organization:</strong> {organization}</span>
      <span><strong>Date:</strong> {date}</span>
    </div>
  </div>

  <div class="content">
    {sections_html}
  </div>

  <div class="footer">
    Antigravity Publication Studio &bull; Autonomous Document Production Pipeline &bull; Verified Final
  </div>
</div>
</body>
</html>
"""

def build_html(spec, output_path):
    meta = spec.get("metadata", {})
    title = meta.get("title", "Technical Document")
    subtitle = meta.get("subtitle", "")
    author = meta.get("author", "Principal Architect")
    org = meta.get("organization", "Enterprise Studio")
    date_str = meta.get("date", "November 2026")

    subtitle_html = f'<div class="subtitle">{subtitle}</div>' if subtitle else ""

    sections_html_parts = []
    for idx, sec in enumerate(spec.get("content", {}).get("sections", []), 1):
        sec_h2 = f"<h2>{idx}.0 {sec.get('title', 'Section')}</h2>"
        sections_html_parts.append(sec_h2)

        for p_text in sec.get("paragraphs", []):
            sections_html_parts.append(f"<p>{p_text}</p>")

        if sec.get("callout"):
            sections_html_parts.append(f'<div class="callout">&#9733; <strong>Key Takeaway:</strong> {sec["callout"]}</div>')

        if sec.get("code_block"):
            c = sec["code_block"].get("code", "")
            sections_html_parts.append(f'<pre class="code-block"><code>{c}</code></pre>')

        if sec.get("table"):
            t_spec = sec["table"]
            tbl_lines = ["<table><thead><tr>"]
            for h in t_spec.get("headers", []):
                tbl_lines.append(f"<th>{h}</th>")
            tbl_lines.append("</tr></thead><tbody>")
            for row in t_spec.get("rows", []):
                tbl_lines.append("<tr>")
                for cell in row:
                    tbl_lines.append(f"<td>{cell}</td>")
                tbl_lines.append("</tr>")
            tbl_lines.append("</tbody></table>")
            sections_html_parts.append("".join(tbl_lines))

    full_html = HTML_TEMPLATE.format(
        title=title,
        subtitle_html=subtitle_html,
        author=author,
        organization=org,
        date=date_str,
        sections_html="\n".join(sections_html_parts)
    )

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTML Production Engine")
    parser.add_argument("--spec", required=True, help="Path to JSON spec")
    parser.add_argument("--out", required=True, help="Output .html path")
    args = parser.parse_args()

    with open(args.spec, "r", encoding="utf-8") as f:
        data = json.load(f)
    res = build_html(data, args.out)
    print(f"SUCCESS: Generated HTML at {res}")

