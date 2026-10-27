---
name: ats-resume-optimizer
description: Optimize software engineering resumes against target job descriptions for Applicant Tracking Systems (ATS), keyword frequency matching, Google XYZ impact bullet formatting, and structural readability.
---

# ATS Resume Optimization & Job Description Analysis

## 1. Intended Role & Domain
- **Primary Domain**: Career & Professional Development
- **Target Roles**: ATS Resume Optimizer, Job Description Analyst, Career Transition Coach
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "optimize resume", "ats score", "match job description", "resume review", "tailor resume", "bullet points xyz formula", "ats resume check".
- **Contextual Inferences**: Candidates preparing job applications, optimizing technical portfolios, analyzing job postings for core competencies.
- **Chained Predecessors**: None.

## 3. Explicit Exclusions
- Do NOT use when:
  - Falsifying candidate experience, inventing fake credentials, or inserting invisible white-text keyword stuffing.
  - Reviewing non-career software codebases.

## 4. Required Inputs & Context
- Existing resume text (Markdown, plain text, or extracted PDF content).
- Target Job Description (JD) text including responsibilities and requirements.
- Candidate's genuine background constraints and verified technical accomplishments.

## 5. Expected Outputs & Artifacts
- Job Description Competency Breakdown (Hard Skills, Soft Skills, Tools, Domain Expertise).
- ATS Keyword Relevance & Gap Analysis Scorecard.
- Tailored Resume Draft formatted in clean Markdown with quantified impact bullets.
- Actionable improvement summary explaining specific positioning adjustments.

## 6. Step-by-Step Operating Procedure
1. **Job Description Keyword & Entity Extraction**:
   - Parse the target JD to extract high-frequency technical keywords, required frameworks, cloud platforms, and architecture patterns.
2. **Current Resume Baseline & Gap Analysis**:
   - Compare candidate's existing experience against the JD keyword ledger.
   - Categorize gaps: Missing keywords for actual skills possessed vs unpossessed domain experience.
3. **Google XYZ Bullet Point Transformation**:
   - Rewrite bullet points using the formula: "Accomplished [X], as measured by [Y], by doing [Z]".
   - Ensure every bullet begins with a strong active verb (e.g. *Architected, Engineered, Optimized, Reduced, Accelerated*).
4. **ATS Formatting & Structural Sanitization**:
   - Eliminate parsing hazards: multi-column tables, graphics, text boxes, and non-standard header names.
   - Use standard header titles: `Summary`, `Technical Skills`, `Professional Experience`, `Education`, `Projects`.
5. **Keyword Density & Authenticity Verification**:
   - Ensure relevant keywords appear organically 2-4 times across experience and skills sections without stuffing.

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection: Read provided resume and JD files.
- Preservation rule: Never invent employment history, degrees, or years of experience. Authenticity is non-negotiable.

## 8. Tool & Dependency Requirements
- Text parser, Markdown formatter, word frequency counter.

## 9. Implementation Guidelines & Best Practices
- Quantify impact: Replace vague statements ("Improved API performance") with quantified metrics ("Reduced API p99 latency by 45% (from 850ms to 460ms) by implementing Redis caching and indexing PostgreSQL foreign keys").
- Standardize the Technical Skills section into categorized tags:
  - **Languages**: Python, TypeScript, Go, SQL.
  - **Frameworks & Libraries**: FastAPI, React 19, Next.js, PyTorch.
  - **Cloud & DevOps**: AWS (ECS, S3, IAM), Docker, GitHub Actions, Terraform.
  - **Databases & Tools**: PostgreSQL, Redis, Qdrant, Git, Linux.

## 10. Error Handling & Recovery Procedures
- Candidate lacks a mandatory requirement: Do not fabricate experience. Instead, highlight adjacent transferable skills (e.g. if GCP is required and candidate has AWS, emphasize deep cloud architecture principles).

## 11. Security & Privacy Constraints
- Sanitize personal contact info (phone numbers, physical home addresses) if saving resume reports to public or shared workspaces.

## 12. Verification & Testing Requirements
- Calculate ATS keyword coverage ratio:
  - Target: >= 80% coverage of core technical keywords.
- Verify that every work experience entry contains: Role Title, Company Name, Dates (Month Year), and 3-5 quantified bullet points.

## 13. Completion Criteria
- Fully optimized resume draft generated in clean, ATS-compliant Markdown.
- Keyword match report highlights matched vs unaddressed terms.
- 100% of bullet points contain active verbs and metrics.

## 14. Relevant Official References
- Google Careers: "Resume Tips: How to write an effective resume".
- National Association of Colleges and Employers (NACE) Career Readiness Competencies.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Optimized for modern ATS parsers (Workday, Greenhouse, Lever, Ashby).
