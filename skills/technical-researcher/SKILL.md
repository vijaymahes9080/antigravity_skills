---
name: technical-researcher
description: Conduct rigorous technical research, literature reviews, primary source verification, academic citation (APA/BibTeX), benchmark evaluation, and technology radar assessments.
---

# Technical Research & Literature Synthesis

## 1. Intended Role & Domain
- **Primary Domain**: Data, Research & Academic Work
- **Target Roles**: Technical Researcher, Research Assistant, Technology Analyst, Literature Review Assistant
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "technical research", "literature review", "research synthesis", "compare state of the art", "technology evaluation", "verify primary sources", "academic citations".
- **Contextual Inferences**: Investigating new software architectures, evaluating competing libraries, scientific paper summaries.
- **Chained Predecessors**: None or `task-decomposition`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Performing routine code refactoring without research questions.
  - Generating generic promotional marketing copy.

## 4. Required Inputs & Context
- Core research question or technology evaluation scope.
- Target domains, candidate frameworks, or academic topic keywords.
- Citation format requirements (APA 7th, IEEE, BibTeX).

## 5. Expected Outputs & Artifacts
- Comprehensive Technical Synthesis Report with executive summary.
- Comparative Evaluation Matrix (Features, Performance, License, Maturity, Community Support).
- Verified Bibliography with persistent identifiers (DOIs, ArXiv IDs, official RFCs).
- State-of-the-Art (SOTA) benchmark assessment.

## 6. Step-by-Step Operating Procedure
1. **Hypothesis & Scope Definition**:
   - Formulate clear, falsifiable research questions and boundary criteria.
2. **Primary Source Discovery**:
   - Prioritize peer-reviewed literature, official RFC specifications, maintained project release notes, and authoritative benchmark studies.
   - Disregard outdated or uncredited SEO blog posts.
3. **Evidence Extraction & Verification**:
   - Extract empirical data: throughput, memory overhead, latency numbers, and hardware constraints.
   - Note the publication date, experimental methodology, and test conditions.
4. **Comparative Analysis & Trade-off Synthesis**:
   - Compare alternatives objectively using a structured multi-criteria decision matrix.
5. **Report & Citation Compilation**:
   - Format findings with formal citations, clear prose, and actionable engineering recommendations.

## 7. Repository Inspection & Planning Requirements
- Non-destructive query of project dependencies to ground research:
  ```bash
  cat package.json 2>/dev/null || cat pyproject.toml 2>/dev/null
  ```
- Preservation rule: Never fabricate citations, benchmark numbers, or author names; always verify against primary documentation.

## 8. Tool & Dependency Requirements
- Web search tools (`search_web`), URL fetchers (`read_url_content`), markdown generation.

## 9. Implementation Guidelines & Best Practices
- Distinguish between established industry standards (mature) vs experimental pre-alpha tools.
- Document research date explicitly: technology maturity shifts rapidly across quarters.
- Structure findings using the Comparative Matrix format:

```markdown
| Technology | License | Maturity (Years) | Strengths | Limitations | Optimal Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FastAPI** | MIT | 6+ (Active) | Native async, Pydantic V2 | Async discipline required | High-throughput APIs |
| **Django** | BSD-3 | 19+ (Mature) | Built-in ORM, Admin, Auth | Monolithic, heavier memory | Enterprise CRUD apps |
```

## 10. Error Handling & Recovery Procedures
- Conflicting benchmark data between sources: Document both methodologies, hardware setups, and explain the discrepancy transparently.

## 11. Security & Privacy Constraints
- Adhere to copyright and fair use guidelines; summarize and synthesize in original words rather than copying raw paper paragraphs.

## 12. Verification & Testing Requirements
- Check citation links and DOIs: Verify that every cited paper or RFC resolves to a valid URL.
- Verify that comparative tables have all cells populated without contradictory claims.

## 13. Completion Criteria
- Research answers all primary questions with evidence.
- Comparative matrix objectively contrasts competing solutions.
- Complete bibliography included with active DOIs/URLs.

## 14. Relevant Official References
- IEEE Standards & Computer Society Publications.
- ACM Digital Library & arXiv.org.
- ThoughtWorks Technology Radar Guidelines.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Designed for research workflows across 2025/2026 computer science disciplines.
