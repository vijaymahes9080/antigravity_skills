#!/usr/bin/env python3
"""docgen.py spec.json outdir -> builds .pptx .docx .pdf .xlsx from ONE spec. No watermarks.
pip install python-pptx python-docx reportlab openpyxl"""
import json, sys
from pathlib import Path

PRESETS = {
 "navy":     {"primary": "0F2747", "accent": "F2A900", "light": "F5F7FA", "text": "1F2933"},
 "teal":     {"primary": "0B3C49", "accent": "2EC4B6", "light": "F0F7F7", "text": "1B2B2F"},
 "plum":     {"primary": "3B1F4B", "accent": "FF6B6B", "light": "F8F4FA", "text": "2A1F33"},
 "forest":   {"primary": "1B4332", "accent": "D4A373", "light": "F4F8F5", "text": "1D2B24"},
 "charcoal": {"primary": "22252B", "accent": "00B894", "light": "F4F5F7", "text": "22252B"},
 "royal":    {"primary": "1E3A8A", "accent": "F97316", "light": "EFF4FF", "text": "172554"},
 "crimson":  {"primary": "7F1D1D", "accent": "FACC15", "light": "FEF6F6", "text": "2B1515"}}
def theme(spec):
    t = {"font": "Calibri", **PRESETS["navy"]}
    t.update(PRESETS.get(spec.get("preset", "navy"), {})); t.update(spec.get("theme", {})); return t
def rgb(h): return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def build_pptx(spec, out):
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor as C
    from pptx.enum.shapes import MSO_SHAPE
    t = theme(spec); P, A, L, T = (C(*rgb(t[k])) for k in ("primary", "accent", "light", "text")); W = C(255, 255, 255)
    prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
    prs.core_properties.title = spec['title']; prs.core_properties.author = spec.get('author', 'Author')
    def box(s, x, y, w, h, fill, shape=MSO_SHAPE.RECTANGLE):
        sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        sh.fill.solid(); sh.fill.fore_color.rgb = fill; sh.line.fill.background(); sh._element.xpath('.//p:cNvPr')[0].set('descr', 'decorative shape'); return sh
    def text(s, x, y, w, h, txt, size=18, bold=False, color=T):
        tbx = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tbx._element.xpath('.//p:cNvPr')[0].set('descr', txt[:90]); tf = tbx.text_frame; tf.word_wrap = True
        r = tf.paragraphs[0].add_run(); r.text = txt; r.font.size = Pt(size); r.font.bold = bold
        r.font.color.rgb = color; r.font.name = t["font"]
    for i, sl in enumerate(spec["slides"]):
        s = prs.slides.add_slide(prs.slide_layouts[6]); k = sl.get("type", "bullets")
        if k == "title":
            box(s, 0, 0, 13.333, 7.5, P); box(s, 0.8, 3.55, 1.6, 0.08, A)
            text(s, 0.8, 1.9, 11.5, 1.6, sl["title"], 44, True, W); text(s, 0.8, 3.8, 11.5, 1, sl.get("subtitle", ""), 22, False, C(220, 226, 235))
        else:
            box(s, 0, 0, 13.333, 1.1, P); box(s, 0, 1.1, 13.333, 0.06, A); text(s, 0.6, 0.22, 12, 0.8, sl["title"], 30, True, W)
            if k == "bullets":
                tbx = s.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(11.7), Inches(5)); tbx._element.xpath('.//p:cNvPr')[0].set('descr', sl["title"]); tf = tbx.text_frame; tf.word_wrap = True
                for j, b in enumerate(sl["points"]):
                    p = tf.paragraphs[0] if j == 0 else tf.add_paragraph(); r = p.add_run(); r.text = "• " + b
                    r.font.size = Pt(22); r.font.color.rgb = T; r.font.name = t["font"]; p.space_after = Pt(12)
            elif k == "cards":
                n = len(sl["cards"]); w = (11.9 - (n - 1) * .3) / n
                for j, c in enumerate(sl["cards"]):
                    x = .7 + j * (w + .3); box(s, x, 1.7, w, 4.6, L); box(s, x, 1.7, w, .1, A)
                    text(s, x + .2, 2.0, w - .4, .8, c["head"], 22, True, P); text(s, x + .2, 2.9, w - .4, 3.2, c["body"], 16)
            elif k == "stats":
                n = len(sl["stats"]); w = 11.9 / n
                for j, c in enumerate(sl["stats"]):
                    text(s, .7 + j * w, 2.4, w - .2, 1.3, c["value"], 54, True, P); text(s, .7 + j * w, 3.8, w - .2, 1, c["label"], 18)
            elif k == "quote":
                box(s, 0.8, 1.9, 0.12, 3.2, A)
                text(s, 1.2, 1.8, 11, 3, "\u201c" + sl["quote"] + "\u201d", 34, True, P); text(s, 1.2, 5.2, 11, .8, "\u2014 " + sl.get("by", ""), 18)
            elif k == "compare":
                for j, c in enumerate(sl["cols"]):
                    x = .7 + j * 6.1; box(s, x, 1.7, 5.8, .7, P if j == 0 else A); text(s, x + .2, 1.8, 5.4, .6, c["head"], 22, True, W if j == 0 else P)
                    box(s, x, 2.4, 5.8, 4.0, L)
                    tbx = s.shapes.add_textbox(Inches(x + .2), Inches(2.6), Inches(5.4), Inches(3.6)); tbx._element.xpath('.//p:cNvPr')[0].set('descr', c["head"]); tf = tbx.text_frame; tf.word_wrap = True
                    for m, b in enumerate(c["points"]):
                        pp = tf.paragraphs[0] if m == 0 else tf.add_paragraph(); r = pp.add_run(); r.text = "\u2022 " + b; r.font.size = Pt(18); r.font.color.rgb = T; r.font.name = t["font"]; pp.space_after = Pt(10)
            elif k == "chart":
                from pptx.chart.data import CategoryChartData
                from pptx.enum.chart import XL_CHART_TYPE as X, XL_LEGEND_POSITION as LP
                cd = CategoryChartData(); cd.categories = sl["cats"]
                for n, v in sl["series"].items(): cd.add_series(n, v)
                ct = {"bar": X.COLUMN_CLUSTERED, "line": X.LINE_MARKERS, "pie": X.PIE, "hbar": X.BAR_CLUSTERED}[sl.get("kind", "bar")]
                gf = s.shapes.add_chart(ct, Inches(.8), Inches(1.5), Inches(8.2), Inches(5.2), cd); gf._element.xpath('.//p:cNvPr')[0].set('descr', sl['title'] + ': ' + sl.get('insight', '')); ch = gf.chart
                ch.has_legend = len(sl["series"]) > 1 or sl.get("kind") == "pie"
                if ch.has_legend: ch.legend.position = LP.BOTTOM; ch.legend.include_in_layout = False
                if sl.get("kind") != "pie":
                    for ser in ch.plots[0].series: ser.format.fill.solid(); ser.format.fill.fore_color.rgb = P
                    ch.plots[0].has_data_labels = True
                box(s, 9.4, 1.7, .08, 4.4, A); text(s, 9.7, 1.7, 3.2, 4.4, sl.get("insight", ""), 20, True, P)
            elif k == "timeline":
                n = len(sl["steps"]); w = 11.9 / n; box(s, .7, 3.3, 11.9, .06, P)
                for j, c in enumerate(sl["steps"]):
                    x = .7 + j * w; box(s, x + w / 2 - .15, 3.18, .3, .3, A, MSO_SHAPE.OVAL)
                    text(s, x, 2.3, w, .8, c["when"], 18, True, P); text(s, x, 3.7, w - .1, 2, c["what"], 15)
        text(s, .6, 6.95, 8, .4, spec.get("footer", ""), 12, False, C(120, 130, 140)); text(s, 12.0, 6.95, 1, .4, str(i + 1), 12, False, C(120, 130, 140))
        if sl.get("source"): text(s, .6, 6.6, 10, .3, "Source: " + sl["source"], 12, False, C(120, 130, 140))
        if i > 0:
            auto = sl.get("notes") or ("Talking points: " + sl["title"] + ". " + " ".join(sl.get("points", [c.get("head", "") + " " + c.get("body", "") for c in sl.get("cards", [])] + [str(c.get("value", "")) + " " + c.get("label", "") for c in sl.get("stats", [])])) + " Pause, check understanding, then move on.")
            s.notes_slide.notes_text_frame.text = auto
    prs.save(out)

def _field(run, code):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    for typ, txt in (("begin", None), (None, code), ("end", None)):
        if typ: e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), typ)
        else: e = OxmlElement("w:instrText"); e.text = txt
        run._r.append(e)

def build_docx(spec, out):
    from docx import Document
    from docx.shared import Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    t = theme(spec); d = Document(); d.core_properties.title = spec['title']; d.core_properties.author = spec.get('author', 'Author')
    d.styles["Normal"].font.name = t["font"]; d.styles["Normal"].font.size = Pt(11)
    for h in ("Heading 1", "Heading 2"):
        d.styles[h].font.name = t["font"]; d.styles[h].font.color.rgb = RGBColor(*rgb(t["primary"]))
    p = d.add_paragraph(); p.paragraph_format.space_before = Pt(120); r = p.add_run(spec["title"]); r.font.size = Pt(34); r.bold = True; r.font.color.rgb = RGBColor(*rgb(t["primary"]))
    r = d.add_paragraph().add_run(spec.get("subtitle", "")); r.font.size = Pt(16); r.font.color.rgb = RGBColor(*rgb(t["accent"]))
    d.add_paragraph(spec.get("author", "")); d.add_page_break()
    d.add_heading("Contents", 1); _field(d.add_paragraph().add_run(), 'TOC \\o "1-2" \\h \\z \\u'); d.add_page_break()
    for sec in spec.get("sections", []):
        d.add_heading(sec["h"], 1)
        for para in sec.get("p", []): d.add_paragraph(para)
        for b in sec.get("bullets", []): d.add_paragraph(b, style="List Bullet")
        if "table" in sec:
            tb = sec["table"]; tbl = d.add_table(rows=1, cols=len(tb["head"])); tbl.style = "Light Grid Accent 1"
            for i, h in enumerate(tb["head"]): tbl.rows[0].cells[i].text = h
            for row in tb["rows"]:
                cs = tbl.add_row().cells
                for i, v in enumerate(row): cs[i].text = str(v)
    fp = d.sections[0].footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER; fp.add_run(spec.get("footer", "") + "  |  Page "); _field(fp.add_run(), "PAGE")
    d.save(out)

def build_pdf(spec, out):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, ListFlowable
    t = theme(spec); P = colors.HexColor("#" + t["primary"]); A = colors.HexColor("#" + t["accent"]); ss = getSampleStyleSheet()
    H1 = ParagraphStyle("H1", parent=ss["Heading1"], textColor=P, fontSize=18, spaceBefore=14, spaceAfter=8)
    BD = ParagraphStyle("BD", parent=ss["BodyText"], fontSize=10.5, leading=15)
    TT = ParagraphStyle("TT", parent=ss["Title"], textColor=P, fontSize=32, leading=38, alignment=0)
    def foot(c, doc):
        c.saveState(); c.setFont("Helvetica", 8); c.setFillColor(colors.grey)
        c.drawString(2 * cm, 1.2 * cm, spec.get("footer", "")); c.drawRightString(A4[0] - 2 * cm, 1.2 * cm, str(doc.page)); c.restoreState()
    f = [Spacer(1, 6 * cm), Paragraph(spec["title"], TT), Paragraph(spec.get("subtitle", ""), ParagraphStyle("s", parent=BD, fontSize=15, textColor=A)), Spacer(1, 1 * cm), Paragraph(spec.get("author", ""), BD), PageBreak()]
    for sec in spec.get("sections", []):
        f.append(Paragraph(sec["h"], H1))
        for para in sec.get("p", []): f += [Paragraph(para, BD), Spacer(1, 6)]
        if sec.get("bullets"): f.append(ListFlowable([Paragraph(b, BD) for b in sec["bullets"]], bulletType="bullet", start="•"))
        if "table" in sec:
            tb = sec["table"]; tab = Table([tb["head"]] + [[Paragraph(str(v), BD) for v in r] for r in tb["rows"]], repeatRows=1)
            tab.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), P), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#" + t["light"])]), ("GRID", (0, 0), (-1, -1), .25, colors.lightgrey), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            f += [Spacer(1, 8), tab]
    SimpleDocTemplate(out, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm, title=spec["title"], author=spec.get("author", "")).build(f, onFirstPage=foot, onLaterPages=foot)

def build_xlsx(spec, out):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter
    t = theme(spec); wb = Workbook(); wb.remove(wb.active)
    for tb in spec.get("tables", []):
        ws = wb.create_sheet(tb["name"][:31]); ws.append(tb["head"])
        for r in tb["rows"]: ws.append(r)
        for c in ws[1]: c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor=t["primary"]); c.alignment = Alignment(horizontal="center")
        ws.freeze_panes = "A2"; ws.auto_filter.ref = ws.dimensions
        for i, col in enumerate(ws.columns, 1): ws.column_dimensions[get_column_letter(i)].width = min(60, max(len(str(c.value or "")) for c in col) + 3)
    wb.save(out)

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1])); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    stem = spec.get("file", "document")
    if spec.get("slides"): build_pptx(spec, out / f"{stem}.pptx")
    if spec.get("sections"): build_docx(spec, out / f"{stem}.docx"); build_pdf(spec, str(out / f"{stem}.pdf"))
    if spec.get("tables"): build_xlsx(spec, out / f"{stem}.xlsx")
    print("built ->", sorted(p.name for p in out.iterdir()))
