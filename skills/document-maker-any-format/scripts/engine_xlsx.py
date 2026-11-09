#!/usr/bin/env python3
"""
engine_xlsx.py — Advanced Enterprise Spreadsheet Production Engine
Part of document-maker-any-format skill
"""

import os
import sys
import json
import argparse
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

PALETTE = {
    "header_fill": "0A192F",
    "header_font": "FFFFFF",
    "accent_fill": "1E3A8A",
    "zebra_fill": "F8FAFC",
    "border_color": "CBD5E1"
}

def create_thin_border(color="CBD5E1"):
    side = Side(style='thin', color=color)
    return Border(left=side, right=side, top=side, bottom=side)

def build_xlsx(spec, output_path):
    wb = openpyxl.Workbook()
    default_sheet = wb.active
    wb.remove(default_sheet)

    meta = spec.get("metadata", {})
    sheets_data = spec.get("content", {}).get("sheets", [])

    if not sheets_data:
        sheets_data = [
            {
                "name": "KPI Dashboard",
                "tables": [
                    {
                        "title": "Enterprise Performance Metrics (FY2026)",
                        "headers": ["Metric", "Target", "Q1 Actual", "Q2 Actual", "YTD Variance", "Status"],
                        "rows": [
                            ["Enterprise Revenue ($M)", 45.0, 48.2, 51.6, "=C4+D4-(B4*2)", "EXCEEDED"],
                            ["Operating Margin (%)", 0.28, 0.31, 0.32, "=AVERAGE(C5:D5)-B5", "ON TRACK"],
                            ["Active Enterprise Clients", 350, 372, 410, "=D6-B6", "AHEAD"],
                            ["System Uptime SLO (%)", 0.999, 0.9995, 0.9998, "=AVERAGE(C7:D7)-B7", "EXCEEDED"],
                            ["Average Latency (ms)", 45, 38, 36, "=AVERAGE(C8:D8)-B8", "OPTIMAL"]
                        ],
                        "summary_row": ["Total / Average", "=AVERAGE(B4:B8)", "=AVERAGE(C4:C8)", "=AVERAGE(D4:D8)", "=AVERAGE(E4:E8)", "COMPLIANT"]
                    }
                ]
            },
            {
                "name": "Financial Detail",
                "tables": [
                    {
                        "title": "Quarterly Cost Breakdown ($ in Thousands)",
                        "headers": ["Department / Category", "Budget", "Actual", "Variance", "% Variance"],
                        "rows": [
                            ["Cloud Infrastructure (Compute)", 1200, 1140, "=B4-C4", "=D4/B4"],
                            ["Model Inference & Serving", 850, 890, "=B5-C5", "=D5/B5"],
                            ["Engineering Personnel", 3400, 3350, "=B6-C6", "=D6/B6"],
                            ["Security & Compliance Audits", 350, 310, "=B7-C7", "=D7/B7"],
                            ["Tooling & SaaS Licenses", 420, 435, "=B8-C8", "=D8/B8"]
                        ],
                        "summary_row": ["Total Operating Expenses", "=SUM(B4:B8)", "=SUM(C4:C8)", "=SUM(D4:D8)", "=D9/B9"]
                    }
                ]
            }
        ]

    for s_info in sheets_data:
        ws = wb.create_sheet(title=s_info.get("name", "Sheet"))
        ws.views.sheetView[0].showGridLines = True

        row_cursor = 1
        ws.cell(row=row_cursor, column=1, value=meta.get("title", "Executive Financial Model"))
        ws.cell(row=row_cursor, column=1).font = Font(name="Arial", size=14, bold=True, color="0A192F")
        row_cursor += 2

        for tbl in s_info.get("tables", []):
            if tbl.get("title"):
                ws.cell(row=row_cursor, column=1, value=tbl["title"])
                ws.cell(row=row_cursor, column=1).font = Font(name="Arial", size=11, bold=True, color="1E3A8A")
                row_cursor += 1

            headers = tbl.get("headers", [])
            header_row_idx = row_cursor
            ws.freeze_panes = f"A{header_row_idx + 1}"

            for col_idx, h in enumerate(headers, 1):
                c = ws.cell(row=header_row_idx, column=col_idx, value=h)
                c.font = Font(name="Arial", size=10, bold=True, color=PALETTE["header_font"])
                c.fill = PatternFill(start_color=PALETTE["header_fill"], end_color=PALETTE["header_fill"], fill_type="solid")
                c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                c.border = create_thin_border()
            row_cursor += 1

            rows = tbl.get("rows", [])
            for r_i, row_data in enumerate(rows):
                is_zebra = (r_i % 2 == 1)
                fill_color = PALETTE["zebra_fill"] if is_zebra else "FFFFFF"

                for col_idx, val in enumerate(row_data, 1):
                    c = ws.cell(row=row_cursor, column=col_idx, value=val)
                    c.font = Font(name="Arial", size=10)
                    c.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
                    c.border = create_thin_border()

                    if isinstance(val, (int, float)):
                        if 0 < val < 1.0:
                            c.number_format = "0.0%"
                        elif val >= 1000:
                            c.number_format = "#,##0"
                        else:
                            c.number_format = "#,##0.00"
                        c.alignment = Alignment(horizontal="right", vertical="center")
                    elif isinstance(val, str) and val.startswith("="):
                        c.alignment = Alignment(horizontal="right", vertical="center")
                        c.font = Font(name="Arial", size=10, bold=True)
                    else:
                        c.alignment = Alignment(horizontal="left", vertical="center")
                row_cursor += 1

            if tbl.get("summary_row"):
                for col_idx, val in enumerate(tbl["summary_row"], 1):
                    c = ws.cell(row=row_cursor, column=col_idx, value=val)
                    c.font = Font(name="Arial", size=10, bold=True, color="0A192F")
                    c.fill = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")
                    top_b = Side(style='thin', color="0A192F")
                    bot_b = Side(style='double', color="0A192F")
                    c.border = Border(top=top_b, bottom=bot_b, left=top_b, right=top_b)
                    if isinstance(val, str) and val.startswith("="):
                        c.alignment = Alignment(horizontal="right", vertical="center")
                    elif isinstance(val, (int, float)):
                        c.alignment = Alignment(horizontal="right", vertical="center")
                    else:
                        c.alignment = Alignment(horizontal="left", vertical="center")
                row_cursor += 2

        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or "")
                max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = max(max_len + 4, 14)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    wb.save(output_path)
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="XLSX Production Engine")
    parser.add_argument("--spec", required=True, help="Path to JSON spec")
    parser.add_argument("--out", required=True, help="Output .xlsx path")
    args = parser.parse_args()

    with open(args.spec, "r", encoding="utf-8") as f:
        data = json.load(f)
    res = build_xlsx(data, args.out)
    print(f"SUCCESS: Generated XLSX at {res}")
