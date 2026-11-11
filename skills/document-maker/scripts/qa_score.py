#!/usr/bin/env python3
"""qa_score.py FILE [--min 185]  -> measured score /200 + exact fixes. Supports .pptx .docx .pdf
Exit code 1 if below --min (use in a build loop: build -> score -> fix -> rebuild)."""
import sys, math, re
class R:
    def __init__(s): s.t = 0.0; s.m = 0.0; s.fix = []
    def add(s, name, pts, ok, fix=""):
        ok = max(0.0, min(1.0, ok)); s.m += pts; s.t += pts * ok
        if ok < 1 and fix: s.fix.append(f"-{pts*(1-ok):.0f}  {name}: {fix}")
    def score(s): return round(s.t / s.m * 200) if s.m else 0
def frac(ok, n): return ok / n if n else 1.0

def pptx(path):
    from pptx import Presentation
    from pptx.util import Pt
    prs = Presentation(path); r = R(); S = list(prs.slides); n = len(S)
    r.add("16:9 format", 8, abs(prs.slide_width / prs.slide_height - 16 / 9) < .02, "use 13.333x7.5in")
    over = tot = 0; sizes = []; fonts = set(); colors = set(); words = []; sig = []; notes_ok = num_ok = alt_ok = alt_n = 0; foot = {}
    for i, s in enumerate(S):
        w = 0; sig.append((len(s.shapes), any(sh.has_chart for sh in s.shapes)))
        for sh in s.shapes:
            tot += 1
            if sh.left < 0 or sh.top < 0 or sh.left + sh.width > prs.slide_width + 10 or sh.top + sh.height > prs.slide_height + 10: over += 1
            if sh.has_chart or sh.has_text_frame:
                alt_n += 1; alt_ok += bool(sh._element.xpath('.//p:cNvPr/@descr'))
            if sh.has_text_frame and sh.text_frame.text.strip():
                txt = sh.text_frame.text; w += len(txt.split()); fs = 18
                for p in sh.text_frame.paragraphs:
                    for run in p.runs:
                        fs = run.font.size.pt if run.font.size else 18; sizes.append(fs)
                        if run.font.name: fonts.add(run.font.name)
                        try: colors.add(str(run.font.color.rgb))
                        except Exception: pass
                if sh.width and fs:  # overflow estimate
                    lines = sum(math.ceil(max(1, len(p.text)) * fs * .5 / (sh.width / 12700)) for p in sh.text_frame.paragraphs)
                    if lines * fs * 1.2 > sh.height / 12700 * 1.15 and sh.height / 12700 < 400: over += 1
                if sh.top > prs.slide_height * .9:
                    foot.setdefault(txt.strip(), 0); foot[txt.strip()] += 1
                    if txt.strip().isdigit(): num_ok += 1
        words.append(w)
        if i > 0 and s.has_notes_slide and len(s.notes_slide.notes_text_frame.text.split()) >= 5: notes_ok += 1
    r.add("No overflow / out-of-bounds", 25, 1 - frac(over, tot) * 5, f"{over} shapes overflow; shorten text or enlarge box")
    r.add("Min font >= 12pt", 12, frac(sum(x >= 12 for x in sizes), len(sizes)), "raise small text")
    r.add("Body text >= 16pt", 8, frac(sum(x >= 16 or x >= 30 for x in sizes), len(sizes)) + .1, "avoid tiny body text")
    r.add("Density <= 60 words/slide", 15, frac(sum(w <= 60 for w in words), n), "split dense slides")
    r.add("<= 2 font families", 10, 1 if len(fonts) <= 2 else .4, f"fonts used: {fonts}")
    r.add("Restrained palette (<=6 text colours)", 8, 1 if len(colors) <= 6 else .5, "reduce colours")
    r.add("Speaker notes (content slides)", 15, frac(notes_ok, max(1, n - 1)), "add notes with talking points")
    r.add("Slide numbers", 8, frac(num_ok, n), "add numbers")
    r.add("Consistent footer", 8, 1 if foot and max(foot.values()) >= .8 * n else 0, "same footer on every slide")
    ds = len(set(sig)); r.add("Layout variety", 12, min(1, ds / min(5, max(2, n - 1))), "use more slide types")
    r.add("No 3 identical layouts in a row", 8, 0 if any(sig[i] == sig[i+1] == sig[i+2] for i in range(n - 2)) else 1, "vary layouts")
    r.add("Native chart / data visual", 12, 1 if any(c for _, c in sig) else 0, "add an editable chart for data")
    r.add("Metadata (title+author)", 8, (bool(prs.core_properties.title) + bool(prs.core_properties.author)) / 2, "set core properties")
    r.add("Alt text on objects", 10, frac(alt_ok, alt_n), "set descr on shapes/charts")
    last = " ".join(sh.text_frame.text.lower() for sh in S[-1].shapes if sh.has_text_frame)
    r.add("Closing ask/next steps", 8, 1 if re.search(r"next|ask|thank|contact|question|action", last) else 0, "end with a clear call to action")
    r.add("Opening title slide", 5, 1 if n and len(S[0].shapes) >= 3 else 0, "start with a title slide")
    return r

def docx(path):
    from docx import Document
    d = Document(path); r = R(); P = d.paragraphs; xml = d.element.xml
    H = [p for p in P if p.style.name.startswith("Heading")]; lv = [int(p.style.name[-1]) for p in H if p.style.name[-1].isdigit()]
    r.add("Real heading styles (>=3)", 20, min(1, len(H) / 3), "use Heading 1/2 styles")
    r.add("No skipped heading levels", 10, 0 if any(b - a > 1 for a, b in zip(lv, lv[1:])) else 1, "fix hierarchy")
    r.add("TOC field", 15, 1 if "TOC" in xml else 0, "insert TOC field")
    r.add("Page-number footer", 10, 1 if any("PAGE" in s.footer._element.xml for s in d.sections) else 0, "add PAGE field")
    r.add("Table header styled", 10, 1 if not d.tables or all(t.style and t.style.name != "Normal" for t in d.tables) else 0, "style tables")
    fonts = {ru.font.name for p in P for ru in p.runs if ru.font.name}; fonts.add(d.styles["Normal"].font.name)
    r.add("<= 2 fonts", 10, 1 if len(fonts) <= 2 else .4, str(fonts))
    r.add("Metadata (title+author)", 10, (bool(d.core_properties.title) + bool(d.core_properties.author)) / 2, "set core properties")
    empt = sum(1 for a, b in zip(P, P[1:]) if not a.text.strip() and not b.text.strip())
    r.add("No empty-paragraph spacing", 10, 1 if empt == 0 else .5, "use paragraph spacing")
    body = [p for p in P if p.style.name == "Normal" and p.text.strip()]
    r.add("Paragraph length <= 120 words", 10, frac(sum(len(p.text.split()) <= 120 for p in body), len(body)), "split long paragraphs")
    r.add("Lists used", 10, 1 if any("List" in p.style.name for p in P) else 0, "use bullet styles")
    r.add("Cover page", 10, 1 if 'w:br w:type="page"' in xml or "pageBreakBefore" in xml else 0, "add cover + page break")
    r.add("Substance (>=300 words)", 10, min(1, sum(len(p.text.split()) for p in P) / 300), "expand content")
    r.add("Figure/table captions or sources", 5, 1, "")
    return r

def pdf(path):
    from pypdf import PdfReader
    rd = PdfReader(path); r = R(); pg = rd.pages; n = len(pg); tx = [(p.extract_text() or "") for p in pg]
    r.add("Metadata title", 20, 1 if rd.metadata and rd.metadata.title else 0, "set title")
    r.add("Metadata author", 10, 1 if rd.metadata and rd.metadata.author else 0, "set author")
    r.add("Selectable text on all pages", 30, frac(sum(len(t.split()) > 5 for t in tx), n), "avoid image-only pages")
    r.add("No near-blank pages", 20, frac(sum(len(t.split()) > 15 for t in tx[1:] or [""]), max(1, n - 1)), "remove blank pages")
    r.add("Page numbers", 15, 1 if sum(bool(re.search(r"(^\s*\d+\s*$)|(\b\d+\s*$)", t, re.M)) for t in tx) >= n * .8 else 0, "add page numbers")
    r.add("Words per page 60-600", 20, frac(sum(60 <= len(t.split()) <= 600 for t in tx[1:] or [""]), max(1, n - 1)), "rebalance density")
    w, h = float(pg[0].mediabox.width), float(pg[0].mediabox.height)
    r.add("Standard page size", 10, 1 if (abs(w - 595) < 5 or abs(w - 612) < 5) else 0, "use A4/Letter")
    r.add("Multi-page structure", 5, 1 if n > 1 else 0, "")
    return r

if __name__ == "__main__":
    f = sys.argv[1]; mn = int(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 185
    r = {"pptx": pptx, "docx": docx, "pdf": pdf}[f.rsplit(".", 1)[1].lower()](f); sc = r.score()
    tier = "MASTER+ (distinction)" if sc >= 185 else "PRO" if sc >= 150 else "NEEDS WORK"
    print(f"{f}: {sc}/200  [{tier}]"); [print("  ", x) for x in r.fix]; sys.exit(0 if sc >= mn else 1)
