# Content Brief Template — document-maker-all-format

<!--
Fill in this template to drive document generation.
Remove sections you don't need. The agent will use this
as the authoritative source — nothing will be fabricated.
-->

# Document Brief

## Metadata

```yaml
title:    "Your Document Title Here"
author:   "Author Name or Organization"
subject:  "Brief one-line description of the document"
keywords: ["keyword1", "keyword2", "keyword3"]
language: "en-US"
version:  "1.0"
date:     "2026-10-28"
```

---

## Target Output Formats

Check all that apply:

- [ ] PDF  (`.pdf`) — `scripts/generate_pdf.py`
- [ ] DOCX (`.docx`) — `scripts/generate_docx.py`
- [ ] PPTX (`.pptx`) — `scripts/generate_pptx.py`
- [ ] XLSX (`.xlsx`) — `scripts/generate_xlsx.py`
- [ ] RTF  (`.rtf`) — `scripts/generate_rtf.py`
- [ ] HTML (`.html`) — Jinja2 template
- [ ] Markdown (`.md`)
- [ ] Plain Text (`.txt`)

---

## Layout & Design Preferences

```yaml
page_size:    "A4"          # A4 | Letter | Legal
orientation:  "portrait"    # portrait | landscape
margins:      "standard"    # standard (2cm) | narrow (1.5cm) | wide (3cm)

theme:
  primary_color:  "#1A3380"  # Heading / bar color
  accent_color:   "#F29910"  # Dividers / highlights
  body_color:     "#262626"  # Body text
  font_heading:   "Helvetica-Bold"
  font_body:      "Helvetica"
  font_size_body: 11

include_cover:        true
include_toc:          false
include_page_numbers: true
include_header:       true
include_footer:       true
```

---

## Content Outline

### Section 1 — [Section Name]

**Heading level**: 1 / 2 / 3

Write the body content here. Separate paragraphs with a blank line.

This is the second paragraph of this section.

- Bullet point one
- Bullet point two
- Bullet point three

### Section 2 — [Section Name]

Content for section 2 goes here.

### Section 3 — [Section Name]

Content for section 3 goes here.

---

## Tables

### Table 1 — [Table Name]

| Column A | Column B | Column C |
|:---------|:---------|:---------|
| Value 1  | Value 2  | Value 3  |
| Value 4  | Value 5  | Value 6  |

*Caption: Brief description of what this table shows.*

---

## Images / Assets

List image paths (relative to project root) and captions:

```yaml
images:
  - path:    "assets/logo.png"
    caption: "Figure 1 — Company Logo"
    width:   "4cm"
  - path:    "assets/chart.png"
    caption: "Figure 2 — Q3 Performance Chart"
    width:   "12cm"
```

---

## For PPTX Presentations — Slide Plan

```yaml
slides:
  - type:     "title"
    title:    "Presentation Title"
    subtitle: "Subtitle or author name"

  - type:     "content"
    title:    "Slide 2 Title"
    bullets:
      - "First key point"
      - "Second key point"
      - "Third key point"

  - type:     "two_col"
    title:    "Comparison Slide"
    left:     "Left side content"
    right:    "Right side content"

  - type:     "closing"
    title:    "Thank You"
    subtitle: "Contact: name@example.com"
```

---

## For XLSX Spreadsheets — Sheet Plan

```yaml
sheets:
  - name: "Summary"
    headers: ["Metric", "Q1", "Q2", "Q3", "Q4"]
    rows:
      - ["Revenue", 120000, 145000, 138000, 162000]
      - ["Costs",    80000,  92000,  88000, 105000]
      - ["Profit",   40000,  53000,  50000,  57000]
    freeze_panes: true
    auto_filter:  true

  - name: "Details"
    headers: ["Item", "Description", "Value"]
    rows:
      - ["Item A", "Description A", "100"]
      - ["Item B", "Description B", "200"]
```

---

## Acceptance Criteria

List what must be true for this document to be considered complete:

- [ ] All sections present and correctly ordered
- [ ] Title, author, and date on cover page
- [ ] Tables render without overflow
- [ ] Page numbers visible in footer
- [ ] File opens without error in native application
- [ ] Spelling and formatting reviewed
- [ ] Validation passes (`python scripts/validate_doc.py --file output/<file>`)

---

## Additional Notes

_Any special instructions, constraints, or context the agent should know._

