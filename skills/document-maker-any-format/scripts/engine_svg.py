#!/usr/bin/env python3
"""
engine_svg.py — Scalable Vector Graphics Production Engine
Part of document-maker-any-format skill
"""

import os
import sys
import json
import argparse

def build_architecture_svg(spec, output_path):
    meta = spec.get("metadata", {})
    title = meta.get("title", "System Architecture & Processing Pipeline")
    subtitle = meta.get("subtitle", "Autonomous Multi-Tier Document Generation Topology")

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600" width="100%" height="100%">
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
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000" flood-opacity="0.3" />
    </filter>
  </defs>

  <rect width="1000" height="600" rx="16" fill="url(#gradBg)" />

  <text x="50" y="60" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="24" font-weight="bold" fill="#F8FAFC">{title}</text>
  <text x="50" y="90" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#38BDF8">{subtitle}</text>

  <g transform="translate(50, 140)">
    <rect width="260" height="180" rx="12" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="1.5" filter="url(#shadow)" />
    <circle cx="35" cy="35" r="14" fill="#38BDF8" />
    <text x="31" y="40" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0A192F">1</text>
    <text x="60" y="40" font-family="sans-serif" font-size="16" font-weight="bold" fill="#F8FAFC">Intent &amp; Archetype</text>
    <text x="25" y="80" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; Topic Understanding</text>
    <text x="25" y="105" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; Format Matching (DOCX/PPTX)</text>
    <text x="25" y="130" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; 12 Visual Archetypes Selection</text>
    <text x="25" y="155" font-family="sans-serif" font-size="12" fill="#38BDF8">&bull; Zero Hallucination Research</text>
  </g>

  <path d="M 310 230 L 370 230" stroke="#38BDF8" stroke-width="2" stroke-dasharray="4" />

  <g transform="translate(370, 140)">
    <rect width="260" height="180" rx="12" fill="url(#cardGrad)" stroke="#818CF8" stroke-width="1.5" filter="url(#shadow)" />
    <circle cx="35" cy="35" r="14" fill="#818CF8" />
    <text x="31" y="40" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0A192F">2</text>
    <text x="60" y="40" font-family="sans-serif" font-size="16" font-weight="bold" fill="#F8FAFC">Native Production</text>
    <text x="25" y="80" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; python-docx &amp; python-pptx</text>
    <text x="25" y="105" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; openpyxl Model Formulas</text>
    <text x="25" y="130" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; ReportLab Platypus Engine</text>
    <text x="25" y="155" font-family="sans-serif" font-size="12" fill="#818CF8">&bull; Full Editable Source Artifacts</text>
  </g>

  <path d="M 630 230 L 690 230" stroke="#818CF8" stroke-width="2" stroke-dasharray="4" />

  <g transform="translate(690, 140)">
    <rect width="260" height="180" rx="12" fill="url(#cardGrad)" stroke="#34D399" stroke-width="1.5" filter="url(#shadow)" />
    <circle cx="35" cy="35" r="14" fill="#34D399" />
    <text x="31" y="40" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0A192F">3</text>
    <text x="60" y="40" font-family="sans-serif" font-size="16" font-weight="bold" fill="#F8FAFC">Automated QA &amp; Repair</text>
    <text x="25" y="80" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; Headless Page Rendering</text>
    <text x="25" y="105" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; Overflow &amp; Blank Page Audits</text>
    <text x="25" y="130" font-family="sans-serif" font-size="12" fill="#94A3B8">&bull; Surgical Defect Repair Loop</text>
    <text x="25" y="155" font-family="sans-serif" font-size="12" fill="#34D399">&bull; 100-Point Quality Ledger</text>
  </g>

  <g transform="translate(50, 370)">
    <rect width="900" height="160" rx="12" fill="#0F172A" stroke="#334155" stroke-width="1" />
    <text x="30" y="40" font-family="sans-serif" font-size="15" font-weight="bold" fill="#E2E8F0">ENTERPRISE DELIVERY BENCHMARKS</text>
    <line x1="30" y1="55" x2="870" y2="55" stroke="#334155" stroke-width="1" />

    <text x="50" y="95" font-family="sans-serif" font-size="28" font-weight="bold" fill="#34D399">&ge; 90 / 100</text>
    <text x="50" y="125" font-family="sans-serif" font-size="12" fill="#94A3B8">Mandatory QA Score</text>

    <text x="320" y="95" font-family="sans-serif" font-size="28" font-weight="bold" fill="#38BDF8">100%</text>
    <text x="320" y="125" font-family="sans-serif" font-size="12" fill="#94A3B8">Native Editability Guarantee</text>

    <text x="600" y="95" font-family="sans-serif" font-size="28" font-weight="bold" fill="#A855F7">0%</text>
    <text x="600" y="125" font-family="sans-serif" font-size="12" fill="#94A3B8">Fabricated Evidence / Hallucination</text>
  </g>
</svg>
"""

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SVG Production Engine")
    parser.add_argument("--spec", required=True, help="Path to JSON spec")
    parser.add_argument("--out", required=True, help="Output .svg path")
    args = parser.parse_args()

    with open(args.spec, "r", encoding="utf-8") as f:
        data = json.load(f)
    res = build_architecture_svg(data, args.out)
    print(f"SUCCESS: Generated SVG at {res}")

