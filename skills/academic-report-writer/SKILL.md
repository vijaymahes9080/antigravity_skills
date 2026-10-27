---
name: academic-report-writer
description: Formal technical report writing, academic research papers, mathematical typography (LaTeX), methodology documentation, experimental findings, and publication-ready drafting.
---

# Academic Technical Report & Scientific Writing

## 1. Intended Role & Domain
- **Primary Domain**: Research, Documentation & Academic Work
- **Target Roles**: Academic Report Writer, Documentation Engineer, Technical Presentation Designer
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "academic paper", "technical report", "write research paper", "latex report", "methodology documentation", "scientific paper draft", "experiment findings report".
- **Contextual Inferences**: Academic paper authoring, technical whitepapers, engineering specifications, experimental documentation.
- **Chained Predecessors**: `technical-researcher`, `reproducible-data-science`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Drafting informal chat messages, social media posts, or marketing newsletters.
  - Executing code or software build commands.

## 4. Required Inputs & Context
- Research findings, experimental data, algorithms, or technical design specifications.
- Target publication or report format (ACM, IEEE, Springer, Overleaf LaTeX, GitHub Markdown).
- Mathematical equations or data visualization charts.

## 5. Expected Outputs & Artifacts
- Publication-ready document (LaTeX source or GFM Markdown) structured with standard IMRaD format (Introduction, Methods, Results, and Discussion).
- Mathematical notations rendered in proper LaTeX syntax (`$...$` and `$$...$$`).
- Properly formatted tables and figures with descriptive captions.
- Integrated bibliography with citation keys.

## 6. Step-by-Step Operating Procedure
1. **Abstract & Executive Problem Framing**:
   - Write a concise 200-word abstract: Problem, Proposed Solution, Methodology, Quantitative Results, and Core Implication.
2. **Introduction & Related Work Positioning**:
   - Establish historical context, state-of-the-art limitations, and the specific novel contributions of the work.
3. **Formal Methodology & Mathematical Specification**:
   - Detail system architecture, data models, and algorithms with formal notation and pseudocode.
4. **Experimental Setup & Empirical Results**:
   - Present quantitative metrics in clear tables and comparative charts.
   - Accompany numbers with statistical significance (p-values, confidence intervals).
5. **Discussion, Limitations & Future Work**:
   - Critically evaluate edge cases, trade-offs, and threats to external validity.

## 7. Repository Inspection & Planning Requirements
- Non-destructive check of documentation or LaTeX files:
  ```bash
  find . -name "*.tex" -o -name "*.bib" -o -name "paper.md" 2>/dev/null
  ```
- Preservation rule: Avoid AI buzzwords, vague hyperbole ("groundbreaking", "revolutionary"), and maintain neutral, objective scientific tone.

## 8. Tool & Dependency Requirements
- LaTeX / Pandoc / Markdown renderer, BibTeX bibliography manager.

## 9. Implementation Guidelines & Best Practices
- Every figure and table must be explicitly referenced and explained in the running text (e.g., "As demonstrated in Table 2...").
- Use consistent mathematical symbols: define all variables upon first appearance.

```latex
\begin{table}[h]
\centering
\caption{Comparative Inference Latency and Model Memory Footprint across Quantization Schemes.}
\label{tab:inference_benchmarks}
\begin{tabular}{lccc}
\hline
\textbf{Quantization} & \textbf{Memory (GB)} & \textbf{Latency (ms)} & \textbf{Perplexity} \\
\hline
FP16 (Baseline) & 16.2 & 42.1 & 5.82 \\
INT8 (SmoothQuant) & 8.4 & 24.3 & 5.89 \\
INT4 (AWQ) & 4.6 & 16.8 & 6.04 \\
\hline
\end{tabular}
\end{table}
```

## 10. Error Handling & Recovery Procedures
- Missing citation details: Search Crossref or Google Scholar for official DOI and complete author list before inserting placeholder.

## 11. Security & Privacy Constraints
- Never include proprietary enterprise secrets, unreleased patient data, or unanonymized user surveys in academic manuscripts.

## 12. Verification & Testing Requirements
- Check for broken cross-references (`??` in LaTeX output or broken markdown anchors).
- Verify that all equations parse without syntax errors.

## 13. Completion Criteria
- Document follows rigorous academic structure with complete sections.
- Tables and figures are referenced and numbered accurately.
- Quantitative claims are supported by experimental data.

## 14. Relevant Official References
- IEEE Editorial Style Manual for Authors.
- The Chicago Manual of Style (17th Edition).
- ACM Primary Article Templates & Publication Workflow.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with LaTeX2e, Overleaf, and GitHub Flavored Markdown.
