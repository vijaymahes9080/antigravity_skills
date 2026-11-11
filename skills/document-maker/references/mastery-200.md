# Mastery Scale: 200 points (100 Core + 100 Distinction)
A score above 100 is only meaningful if the scale really goes to 200, so this skill measures to 200.
| Tier | Score | Meaning |
|---|---|---|
| Needs work | <150 | Fix before sharing |
| Pro | 150-184 | Client-ready |
| Master+ | 185-200 | Distinction: could be shown as a portfolio piece |
**Core (100)**: layout integrity (no overflow/out-of-bounds), readability (font size, density, contrast), hierarchy, consistency (fonts, palette, footer), structure (headings, TOC, numbers).
**Distinction (100)**: speaker notes everywhere, native editable charts with insight titles and sources, layout variety without 3 repeats, accessibility (alt text, metadata, reading order), closing call to action, cover/opening polish, substance (enough real content), print/screen readiness.
**Loop (mandatory)**: build -> `python scripts/qa_score.py FILE --min 185` -> apply listed fixes -> rebuild; max 3 loops. Then do a human-eye render check (soffice -> pdf -> png) for what the script cannot see: image quality, visual balance, tone fit, factual accuracy.
**Limits**: the script measures structure, not taste or truth. Always review the story and facts yourself.
