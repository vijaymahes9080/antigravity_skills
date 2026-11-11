#!/usr/bin/env python3
"""
engine_xlsx.py — Master Enterprise Spreadsheet Production Engine
Part of document-maker skill.
"""

import os
import sys
import json
import argparse
import pathlib
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

PALETTES = {
    "modern_corporate": {"header_fill": "0A192F", "header_font": "FFFFFF", "zebra": "F8FAFC", "accent": "1E3A8A", "border": "CBD5E1"},
    "data_analytical": {"header_fill": "0F172A", "header_font": "FFFFFF", "zebra": "F1F5F9", "accent": "2563EB", "border": "94A3B8"},
    "premium_business": {"header_fill": "064E3B", "header_font": "FFFFFF", "zebra": "F0FDF4", "accent": "047857", "border": "A7F3D0"},
    "technology_futuristic": {"header_fill": "0B0F19", "header_font": "38BDF8", "zebra": "F8FAFC", "accent": "06B6D4", "border": "CBD5E1"},
    "engineering_technical": {"header_fill": "0284C7", "header_font": "FFFFFF", "zebra": "F0F9FF", "accent": "0369A1", "border": "BAE6FD"},
    "minimalist_editorial": {"header_fill": "111827", "header_font": "FFFFFF", "zebra": "F9FAFB", "accent": "374151", "border": "E5E7EB"},
}

def create_thin_border(color="CBD5E1"):
    side = Side(style='thin', color=color)
    return Border(left=side, right=side, top=side, bottom=side)

def create_summary_border(color="0A192F"):
    top_side = Side(style='thin', color=color)
    bot_side = Side(style='double', color=color)
    return Border(top=top_side, bottom=bot_side)

def sanitize_value(val):
    """Prevent CSV/formula injection on strings unless intended as formula."""
    if isinstance(val, str):
        v = val.strip()
        if v.startswith("="):
            # Keep genuine formula
            return v
        if v.startswith(("+", "-", "@", "\t", "\r")):
            return "'" + val
    return val

def build_xlsx_from_spec(spec: dict, output_path: str):
    wb = openpyxl.Workbook()
    default_sheet = wb.active
    wb.remove(default_sheet)

    meta = spec.get("metadata", {})
    design = spec.get("design", {})
    archetype = design.get("archetype", "data_analytical")
    palette = PALETTES.get(archetype, PALETTES["data_analytical"])

    sheets_data = spec.get("content", {}).get("sheets", [])
    if not sheets_data:
        sheets_data = [
            {
                "name": "Summary Dashboard",
                "freeze_panes": "A3",
                "tables": [
                    {
                        "title": "System Performance & Resource Telemetry",
                        "headers": ["Service Cluster", "Allocated CPU", "RAM (GB)", "Active Threads", "Utilization (%)", "Health Status"],
                        "rows": [
                            ["Inference Cluster Alpha", 64, 256.0, 1850, 0.784, "HEALTHY"],
                            ["Inference Cluster Beta", 128, 512.0, 3920, 0.842, "OPTIMAL"],
                            ["Embeddings Service", 32, 128.0, 940, 0.621, "HEALTHY"],
                            ["Vector Database Core", 64, 256.0, 2100, 0.895, "ALERT"]
                        ],
                        "summary_row": ["Total / Average", "=SUM(B4:B7)", "=SUM(C4:C7)", "=SUM(D4:D7)", "=AVERAGE(E4:E7)", "VERIFIED"],
                        "column_formats": ["text", "integer", "decimal", "integer", "percentage", "text"]
                    }
                ]
            }
        ]

    for sheet_spec in sheets_data:
        title = sheet_spec.get("name", "Sheet")[:31]
        ws = wb.create_sheet(title=title)
        ws.views.sheetView[0].showGridLines = True
        
        freeze = sheet_spec.get("freeze_panes", "A2")
        ws.freeze_panes = freeze

        current_row = 1
        for table in sheet_spec.get("tables", []):
            tbl_title = table.get("title", "")
            if tbl_title:
                t_cell = ws.cell(row=current_row, column=1, value=tbl_title)
                t_cell.font = Font(name="Calibri", size=13, bold=True, color="0A192F")
                current_row += 1

            headers = table.get("headers", [])
            col_formats = table.get("column_formats", [])
            
            # Header Row
            for col_idx, h in enumerate(headers, start=1):
                cell = ws.cell(row=current_row, column=col_idx, value=h)
                cell.font = Font(name="Calibri", size=11, bold=True, color=palette["header_font"])
                cell.fill = PatternFill(start_color=palette["header_fill"], end_color=palette["header_fill"], fill_type="solid")
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                cell.border = create_thin_border(palette["border"])
            ws.row_dimensions[current_row].height = 26
            header_row_idx = current_row
            current_row += 1

            # Data Rows
            rows = table.get("rows", [])
            for r_i, row in enumerate(rows):
                fill_color = palette["zebra"] if r_i % 2 == 1 else "FFFFFF"
                for col_idx, val in enumerate(row, start=1):
                    cell = ws.cell(row=current_row, column=col_idx)
                    safe_val = sanitize_value(val)
                    cell.value = safe_val
                    cell.font = Font(name="Calibri", size=10.5)
                    cell.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
                    cell.border = create_thin_border(palette["border"])

                    fmt = col_formats[col_idx - 1] if col_idx - 1 < len(col_formats) else None
                    if fmt == "currency":
                        cell.number_format = '$#,##0.00'
                        cell.alignment = Alignment(horizontal="right")
                    elif fmt == "percentage":
                        cell.number_format = '0.0%'
                        cell.alignment = Alignment(horizontal="right")
                    elif fmt == "integer":
                        cell.number_format = '#,##0'
                        cell.alignment = Alignment(horizontal="right")
                    elif fmt == "decimal":
                        cell.number_format = '#,##0.00'
                        cell.alignment = Alignment(horizontal="right")
                    elif isinstance(val, (int, float)):
                        cell.alignment = Alignment(horizontal="right")
                    else:
                        cell.alignment = Alignment(horizontal="left")

                ws.row_dimensions[current_row].height = 20
                current_row += 1

            # Summary Row
            summary = table.get("summary_row")
            if summary:
                for col_idx, val in enumerate(summary, start=1):
                    cell = ws.cell(row=current_row, column=col_idx)
                    cell.value = sanitize_value(val)
                    cell.font = Font(name="Calibri", size=11, bold=True, color="0A192F")
                    cell.fill = PatternFill(start_color=palette["zebra"], end_color=palette["zebra"], fill_type="solid")
                    cell.border = create_summary_border(palette["header_fill"])

                    fmt = col_formats[col_idx - 1] if col_idx - 1 < len(col_formats) else None
                    if fmt == "currency":
                        cell.number_format = '$#,##0.00'
                        cell.alignment = Alignment(horizontal="right")
                    elif fmt == "percentage":
                        cell.number_format = '0.0%'
                        cell.alignment = Alignment(horizontal="right")
                    elif fmt == "integer":
                        cell.number_format = '#,##0'
                        cell.alignment = Alignment(horizontal="right")
                    elif fmt == "decimal":
                        cell.number_format = '#,##0.00'
                        cell.alignment = Alignment(horizontal="right")
                    elif isinstance(val, (int, float)):
                        cell.alignment = Alignment(horizontal="right")

                ws.row_dimensions[current_row].height = 22
                current_row += 1

            current_row += 2  # Spacing between tables

        # Auto-adjust column widths
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or "")
                if cell.number_format and ('$' in cell.number_format or '%' in cell.number_format):
                    max_len = max(max_len, len(val_str) + 6)
                else:
                    max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = min(max(max_len + 4, 12), 48)

    out_p = pathlib.Path(output_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_p.with_suffix(".tmp.xlsx")
    try:
        wb.save(str(tmp_path))
        tmp_path.replace(out_p)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise

    return str(out_p)

def main():
    parser = argparse.ArgumentParser(description="Master XLSX Production Engine")
    parser.add_argument("--spec", help="Path to document spec JSON")
    parser.add_argument("--out", "--output", required=True, help="Destination .xlsx file path")
    parser.add_argument("--archetype", default="data_analytical", help="Archetype")
    args = parser.parse_args()

    if args.spec and os.path.exists(args.spec):
        with open(args.spec, "r", encoding="utf-8") as f:
            spec = json.load(f)
    else:
        spec = {"metadata": {"title": "Financial Model", "format": "xlsx"}, "design": {"archetype": args.archetype}}

    out_file = build_xlsx_from_spec(spec, args.out)
    print(f"✅ Master XLSX successfully built: {out_file} ({os.path.getsize(out_file)} bytes)")

if __name__ == "__main__":
    main()

