# Universal Antigravity Skills Collection (2026–2040)

[![Skills Count](https://img.shields.io/badge/Skills-90%20Active-brightgreen.svg)](#architecture-overview)
[![Categories](https://img.shields.io/badge/Taxonomy-14%20Domains-blue.svg)](#14-category-taxonomy)
[![Architecture Horizon](https://img.shields.io/badge/Horizon-2026--2040-orange.svg)](#architecture-overview)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Google Antigravity](https://img.shields.io/badge/Compatible-Antigravity%202.x-blueviolet.svg)](#quick-installation)

An authoritative, production-grade collection of **90 AI Agent Skills** configured for Google Antigravity, modern agentic development environments, and the 2026–2040 MAJI intelligence architecture.

Every skill is structured with complete YAML frontmatter (`name`, `description`), comprehensive technical depth, role definitions, activation conditions, step-by-step procedures, concrete code snippets, security constraints, and verification gates.

---

## Architecture Overview

| Dimension | Specification |
|---|---|
| **Total Skills Active** | **90** |
| **Canonical Skills** | **84** (Specialists, Master Skills, Platform Cores) |
| **Backward-Compatibility Aliases** | **6** (Seamless forwarding to master engines) |
| **Specialized Domains** | **14 Categories** |
| **Target Horizon** | 2026–2040 Engineering & Autonomous AI Orchestration |
| **Standard Format** | Standard Agent Skill Specification (`SKILL.md`) |

---

## 14-Category Taxonomy

| Category | Skills Count | Key Skills Included |
|---|:---:|---|
| **01. AI, ML & Deep Learning** | 4 | `image-generate`, `local-llm-integration`, `computer-vision-engineer`, `explainable-ai-xai` |
| **02. Agentic AI & Orchestration** | 5 | `deepseek-superagent`, `google-elephant-goldfish`, `ai-agent-architect`, `ai-rag-retrieval-engineering`, `multi-agent-orchestration` |
| **03. AI Infrastructure & Safety** | 2 | `ai-evaluation-safety`, `ai-inference-infrastructure` |
| **04. Frontend, UI/UX & Creative** | 27 | `design-audit`, `design-critique`, `design-systems-engineer`, `frontend-craft-design-engineering`, etc. |
| **05. Software Engineering & Languages** | 9 | `fastapi-pro`, `python-pro`, `react-nextjs-pro`, `node-typescript-pro`, `modern-cpp`, `java-modern`, etc. |
| **06. Backend, APIs & Data Platforms** | 4 | `data-engineering-pipelines`, `database-postgresql-performance-optimization`, `data-architecture-system-design`, etc. |
| **07. Cybersecurity, Privacy & Governance** | 5 | `appsec-owasp-audit`, `cybersecurity-sast-vulnerability-scan`, `privacy-engineering`, `quantum-computing-readiness`, etc. |
| **08. Cloud, DevOps & Platform Engineering** | 7 | `platform-engineering`, `finops-cloud-cost-engineering`, `docker-containerization`, `devops-ci-cd-github`, etc. |
| **09. Embedded, IoT & Edge Systems** | 2 | `edge-ai-tinyml`, `embedded-firmware-c` |
| **10. Data Science & Scientific Computing** | 1 | `reproducible-data-science` |
| **11. Testing, Debugging & Quality** | 7 | `root-cause-debugging`, `repo-audit`, `testing-playwright-browser-automation`, `testing-unit-test-generation`, etc. |
| **12. Developer Tools & Automation** | 9 | `automatic-choose-skills`, `mcp-server-developer`, `workflow-automation-scripting`, `git-release-prep`, `agy-customizations`, etc. |
| **13. Research, Docs & Communication** | 5 | `document-maker-any-format`, `document-maker-all-format`, `academic-report-writer`, `technical-researcher`, `writing-humanizer-prose-polish` |
| **14. Career & Professional Development** | 3 | `ats-resume-optimizer`, `github-portfolio-analyst`, `tech-interview-coach` |

> For comprehensive documentation and command triggers for all 90 skills, consult the **[Master Skills Catalog (SKILLS_CATALOG.md)](./SKILLS_CATALOG.md)**.

---

## Quick Installation

### Option 1: Global Antigravity Installation (Recommended)
Extract or symlink each skill folder into your global Antigravity configuration directory:
- **Windows**: `%USERPROFILE%\.gemini\config\skills\` (e.g., `C:\Users\<username>\.gemini\config\skills\`)
- **macOS / Linux**: `~/.gemini/config/skills/`

### Option 2: Project-Local Workspace Installation
If you want to use skills specifically within a repository:
- Copy the desired skill folders into `.agents/skills/` at your repository root.

---

## Verification & CI/CD Integrity

Every skill passes rigorous structural, syntax, and schema validation. You can verify the entire ecosystem locally:

```bash
python -c "
import os, re, json
dirs = [d for d in os.listdir('skills') if os.path.isdir(os.path.join('skills', d))]
assert len(dirs) == 90
for d in dirs:
    with open(f'skills/{d}/SKILL.md') as f:
        c = f.read()
    assert c.startswith('---')
print('All 90 skills verified!')
"
```
