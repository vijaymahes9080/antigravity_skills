# Universal Antigravity Skills Collection (2026â€“2040)

[![Skills Count](https://img.shields.io/badge/Skills-86%20Active-brightgreen.svg)](#architecture-overview)
[![Categories](https://img.shields.io/badge/Taxonomy-14%20Domains-blue.svg)](#14-category-taxonomy)
[![Architecture Horizon](https://img.shields.io/badge/Horizon-2026--2040-orange.svg)](#architecture-overview)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Google Antigravity](https://img.shields.io/badge/Compatible-Antigravity%202.x-blueviolet.svg)](#quick-installation)

An authoritative, production-grade collection of **86 AI Agent Skills** configured for Google Antigravity, modern agentic development environments, and the 2026â€“2040 MAJI intelligence architecture.

Every skill is structured with complete YAML frontmatter (`name`, `description`), 15-section technical depth, role definitions, activation conditions, step-by-step procedures, concrete code snippets, security constraints, and verification gates.

---

## Architecture Overview

| Dimension | Specification |
|---|---|
| **Total Skills Active** | **86** |
| **Canonical Skills** | **80** (Specialists, Master Skills, Platform Cores) |
| **Backward-Compatibility Aliases** | **6** (Seamless forwarding to master engines) |
| **Specialized Domains** | **14 Categories** |
| **Target Horizon** | 2026â€“2040 Engineering & Autonomous AI Orchestration |
| **Standard Format** | Standard Agent Skill Specification (`SKILL.md`) |

---

## 14-Category Taxonomy

| Category | Skills Count | Key Skills Included |
|---|:---:|---|
| **01. AI, ML & Deep Learning** | 4 | `image-generate`, `local-llm-integration`, `computer-vision-engineer`, `explainable-ai-xai` |
| **02. Agentic AI & Orchestration** | 3 | `ai-agent-architect`, `ai-rag-retrieval-engineering`, `multi-agent-orchestration` |
| **03. AI Infrastructure & Safety** | 2 | `ai-evaluation-safety`, `ai-inference-infrastructure` |
| **04. Frontend, UI/UX & Creative** | 27 | `design-audit`, `design-critique`, `design-systems-engineer`, `frontend-craft-design-engineering`, etc. |
| **05. Software Engineering & Languages** | 9 | `fastapi-pro`, `python-pro`, `react-nextjs-pro`, `node-typescript-pro`, `modern-cpp`, `java-modern`, etc. |
| **06. Backend, APIs & Data Platforms** | 4 | `data-engineering-pipelines`, `database-postgresql-performance-optimization`, `data-architecture-system-design`, etc. |
| **07. Cybersecurity, Privacy & Governance** | 5 | `appsec-owasp-audit`, `cybersecurity-sast-vulnerability-scan`, `privacy-engineering`, `quantum-computing-readiness`, etc. |
| **08. Cloud, DevOps & Platform Engineering** | 7 | `platform-engineering`, `finops-cloud-cost-engineering`, `docker-containerization`, `devops-ci-cd-github`, etc. |
| **09. Embedded, IoT & Edge Systems** | 2 | `edge-ai-tinyml`, `embedded-firmware-c` |
| **10. Data Science & Scientific Computing** | 1 | `reproducible-data-science` |
| **11. Testing, Debugging & Quality** | 7 | `root-cause-debugging`, `repo-audit`, `testing-playwright-browser-automation`, `testing-unit-test-generation`, etc. |
| **12. Developer Tools & Automation** | 8 | `mcp-server-developer`, `workflow-automation-scripting`, `git-release-prep`, `agy-customizations`, etc. |
| **13. Research, Docs & Communication** | 3 | `academic-report-writer`, `technical-researcher`, `writing-humanizer-prose-polish` |
| **14. Career & Professional Development** | 3 | `ats-resume-optimizer`, `github-portfolio-analyst`, `tech-interview-coach` |

> For comprehensive documentation and command triggers for all 85 skills, consult the **[Master Skills Catalog (SKILLS_CATALOG.md)](./SKILLS_CATALOG.md)**.

---

## Quick Installation

### Option 1: Global Antigravity Installation (Recommended)
Copy the `skills/` directory contents directly into your global Antigravity configuration:

- **Windows**:
  ```powershell
  Copy-Item -Recurse -Force skills\* "$HOME\.gemini\config\skills\"
  ```
- **macOS / Linux**:
  ```bash
  cp -r skills/* ~/.gemini/config/skills/
  ```

### Option 2: Project-Local Workspace Installation
To use these skills within a specific codebase:
```bash
mkdir -p .agents/skills
cp -r path/to/antigravity_skills/skills/* .agents/skills/
```

### Option 3: Cross-Platform Agent Runtimes
Compatible with Claude Desktop, Cursor, OpenCodeInterpreter, and MCP-enabled agent harnesses. Point your runner to the respective `SKILL.md` file.

---

## Repository Structure

```
antigravity_skills/
â”œâ”€â”€ .github/
â”‚   â””â”€â”€ workflows/
â”‚       â””â”€â”€ validate-skills.yml    # Continuous Integration integrity test
â”œâ”€â”€ .gitignore                     # Git hygiene filter
â”œâ”€â”€ LICENSE                        # MIT License
â”œâ”€â”€ README.md                      # Ecosystem documentation
â”œâ”€â”€ SKILLS_CATALOG.md              # Detailed reference catalog for all 86 skills
â”œâ”€â”€ skills_manifest.json           # Machine-readable inventory metadata
â””â”€â”€ skills/                        # 86 Self-contained skill directories
    â”œâ”€â”€ academic-report-writer/
    â”œâ”€â”€ ai-agent-architect/
    â”œâ”€â”€ ai-evaluation-safety/
    â”œâ”€â”€ ai-inference-infrastructure/
    â”œâ”€â”€ ...
    â””â”€â”€ writing-humanizer-prose-polish/
```

---

## Machine-Readable Automation

The repository includes [`skills_manifest.json`](./skills_manifest.json) containing structured JSON metadata for programmatic inspection, tool registration, and custom MCP integrations:
- Total skills and category distribution
- File counts and byte footprints
- Activation triggers and roles
- Direct master-to-alias resolution mappings

---

## License

This project is licensed under the [MIT License](./LICENSE) â€” free for personal, educational, and commercial agentic development.
