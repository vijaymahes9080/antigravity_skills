#!/usr/bin/env python3
"""
engine_svg.py — Master Scalable Vector Graphics Architecture Production Engine
Part of document-maker skill.
"""

import os
import sys
import json
import argparse
import html
import pathlib

def build_svg_from_spec(spec: dict, output_path: str):
    meta = spec.get("metadata", {})
    title = html.escape(meta.get("title", "Autonomous Document Production Architecture"))
    subtitle = html.escape(meta.get("subtitle", "Multi-Tier Unified Pipeline & Self-Healing Verification"))

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 640" width="100%" height="100%">
  <defs>
    <linearGradient id="gradBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0A192F" />
      <stop offset="100%" stop-color="#0F172A" />
    </linearGradient>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1E293B" />
      <stop offset="100%" stop-color="#0F172A" />
    </linearGradient>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.35" />
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1000" height="640" rx="16" fill="url(#gradBg)" />

  <!-- Title & Header -->
  <text x="50" y="60" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="24" font-weight="bold" fill="#F8FAFC">{title}</text>
  <text x="50" y="90" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#38BDF8">{subtitle}</text>

  <!-- Node 1: Intent & Archetype -->
  <g transform="translate(50, 140)">
    <rect width="260" height="200" rx="12" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="1.5" filter="url(#shadow)" />
    <circle cx="35" cy="35" r="14" fill="#38BDF8" />
    <text x="31" y="40" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0A192F">1</text>
    <text x="60" y="40" font-family="sans-serif" font-size="16" font-weight="bold" fill="#F8FAFC">Intent &amp; Spec</text>
    <text x="25" y="80" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; Topic Understanding</text>
    <text x="25" y="105" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; Format Matching (DOCX/PPTX)</text>
    <text x="25" y="130" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; 12 Visual Archetypes</text>
    <text x="25" y="155" font-family="sans-serif" font-size="12" fill="#38BDF8">&bull; Zero Hallucination Research</text>
  </g>

  <!-- Arrow 1 -> 2 -->
  <path d="M 310 240 L 370 240" stroke="#38BDF8" stroke-width="2" stroke-dasharray="4" />

  <!-- Node 2: Native Production -->
  <g transform="translate(370, 140)">
    <rect width="260" height="200" rx="12" fill="url(#cardGrad)" stroke="#818CF8" stroke-width="1.5" filter="url(#shadow)" />
    <circle cx="35" cy="35" r="14" fill="#818CF8" />
    <text x="31" y="40" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0A192F">2</text>
    <text x="60" y="40" font-family="sans-serif" font-size="16" font-weight="bold" fill="#F8FAFC">Native Production</text>
    <text x="25" y="80" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; python-docx &amp; python-pptx</text>
    <text x="25" y="105" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; openpyxl Formula Engine</text>
    <text x="25" y="130" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; ReportLab NumberedCanvas</text>
    <text x="25" y="155" font-family="sans-serif" font-size="12" fill="#818CF8">&bull; Atomic File Safety</text>
  </g>

  <!-- Arrow 2 -> 3 -->
  <path d="M 630 240 L 690 240" stroke="#818CF8" stroke-width="2" stroke-dasharray="4" />

  <!-- Node 3: QA & Repair Loop -->
  <g transform="translate(690, 140)">
    <rect width="260" height="200" rx="12" fill="url(#cardGrad)" stroke="#34D399" stroke-width="1.5" filter="url(#shadow)" />
    <circle cx="35" cy="35" r="14" fill="#34D399" />
    <text x="31" y="40" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0A192F">3</text>
    <text x="60" y="40" font-family="sans-serif" font-size="16" font-weight="bold" fill="#F8FAFC">QA &amp; Repair</text>
    <text x="25" y="80" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; 100-Point Scoring Rubric</text>
    <text x="25" y="105" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; Visual Preview Rendering</text>
    <text x="25" y="130" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; Defect Ledger (DEF-001..8)</text>
    <text x="25" y="155" font-family="sans-serif" font-size="12" fill="#34D399">&bull; Self-Healing Loop (&gt;=90)</text>
  </g>

  <!-- Bottom Tier: Format Coverage Strip -->
  <g transform="translate(50, 390)">
    <rect width="900" height="190" rx="12" fill="url(#cardGrad)" stroke="#334155" stroke-width="1" />
    <text x="30" y="40" font-family="sans-serif" font-size="16" font-weight="bold" fill="#F8FAFC">Enterprise Format Coverage &amp; Output Destinations</text>
    <text x="30" y="70" font-family="sans-serif" font-size="13" fill="#94A3B8">DOCX (Reports) &bull; PPTX (16:9 Widescreen) &bull; XLSX (Financial Models) &bull; PDF (Publication) &bull; RTF &bull; HTML &bull; SVG</text>

    <!-- Verified Badge -->
    <rect x="30" y="100" width="160" height="36" rx="6" fill="#064E3B" stroke="#059669" />
    <text x="45" y="123" font-family="sans-serif" font-size="12" font-weight="bold" fill="#34D399">✓ 100% Verified Pass</text>

    <rect x="210" y="100" width="200" height="36" rx="6" fill="#1E293B" stroke="#38BDF8" />
    <text x="225" y="123" font-family="sans-serif" font-size="12" font-weight="bold" fill="#38BDF8">★ 12 Visual Archetypes</text>

    <rect x="430" y="100" width="220" height="36" rx="6" fill="#1E293B" stroke="#818CF8" />
    <text x="445" y="123" font-family="sans-serif" font-size="12" font-weight="bold" fill="#818CF8">🛡 Safe Formula Guard</text>
  </g>
</svg>"""

    out_p = pathlib.Path(output_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_p.with_suffix(".tmp.svg")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        tmp_path.replace(out_p)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise

    return str(out_p)

def main():
    parser = argparse.ArgumentParser(description="Master SVG Architecture Engine")
    parser.add_argument("--spec", help="Path to document spec JSON")
    parser.add_argument("--out", "--output", required=True, help="Destination .svg file path")
    args = parser.parse_args()

    if args.spec and os.path.exists(args.spec):
        with open(args.spec, "r", encoding="utf-8") as f:
            spec = json.load(f)
    else:
        spec = {"metadata": {"title": "Autonomous Architecture", "format": "svg"}}

    out_file = build_svg_from_spec(spec, args.out)
    print(f"✅ Master SVG successfully built: {out_file} ({os.path.getsize(out_file)} bytes)")

if __name__ == "__main__":
    main()

