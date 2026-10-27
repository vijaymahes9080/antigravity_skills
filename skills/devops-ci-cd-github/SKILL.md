---
name: devops-ci-cd-github
description: Production GitHub Actions CI/CD workflows, reusable workflows, matrix builds, automated test & lint gates, container publishing, and zero-downtime deployment pipelines.
---

# GitHub Actions CI/CD & Pipeline Automation

## 1. Intended Role & Domain
- **Primary Domain**: DevOps & Cloud Infrastructure
- **Target Roles**: DevOps Engineer, CI/CD Automation Engineer, Release Engineer
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "github actions", "ci cd pipeline", "automated testing workflow", "matrix build", "publish docker image", "continuous integration", "github workflow".
- **Contextual Inferences**: Repositories needing automated PR validation, lint checks, build artifacts, or deployment.
- **Chained Predecessors**: `task-decomposition`, `git-release-prep`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Repository uses dedicated alternative runners (GitLab CI, Jenkins, CircleCI) with explicit instructions not to use GitHub Actions.
  - Making simple manual local edits with no CI/CD pipeline scope.

## 4. Required Inputs & Context
- Target branch strategy (e.g. `main`, `release/*`, `develop`).
- Language runtime and package managers (Node, Python, Rust, Go, Java).
- Required automated checks (lint, type-check, unit tests, security scan, docker build).

## 5. Expected Outputs & Artifacts
- Production-grade `.github/workflows/ci.yml` and `.github/workflows/cd.yml`.
- Reusable composite actions (`.github/actions/setup-environment`).
- Caching strategy for package dependencies (`actions/cache`).
- Pipeline status badges and branch protection guidelines.

## 6. Step-by-Step Operating Procedure
1. **Trigger & Permissions Scoping**:
   - Limit workflow triggers to relevant branches and paths to save CI runner minutes.
   - Enforce least-privilege token permissions (`permissions: contents: read`).
2. **Matrix Build & Environment Setup**:
   - Configure multi-OS (Ubuntu, macOS, Windows) or multi-runtime (Node 18/20/22, Python 3.10/3.12) matrices.
3. **Dependency Caching**:
   - Implement deterministic caching using hash of lockfiles (`package-lock.json`, `poetry.lock`, `Cargo.lock`).
4. **Automated Testing & Coverage Gates**:
   - Run linters, type checks, and tests sequentially with fail-fast options.
   - Upload test coverage artifacts.
5. **Continuous Delivery & Release**:
   - Build and sign container images (Docker Buildx with OIDC GitHub token) and push to registry (GHCR/Docker Hub).

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection of existing workflows:
  ```bash
  ls -la .github/workflows/ 2>/dev/null || echo "No workflows found"
  ```
- Preservation rule: Never commit hardcoded secrets or plaintext tokens into workflow files; always use `${{ secrets.SECRET_NAME }}`.

## 8. Tool & Dependency Requirements
- GitHub Actions runners, Docker Buildx, actionlint CLI for YAML linting.

## 9. Implementation Guidelines & Best Practices
- Pin actions to full-length commit SHAs rather than mutable branch tags for supply chain security:
  ```yaml
  name: CI Pipeline

  on:
    push:
      branches: [main]
    pull_request:
      branches: [main]

  permissions:
    contents: read

  jobs:
    test:
      name: Lint & Test
      runs-on: ubuntu-latest
      steps:
        - name: Checkout Code
          uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1

        - name: Setup Node.js
          uses: actions/setup-node@60edb5dd545a775178f5252478332d7967a14e9d # v4.0.2
          with:
            node-version: 22
            cache: 'npm'

        - name: Install Dependencies
          run: npm ci

        - name: Run Type Check & Lint
          run: npm run lint && npx tsc --noEmit

        - name: Execute Tests
          run: npm test -- --coverage
  ```

## 10. Error Handling & Recovery Procedures
- Cache invalidation issues: Add a cache key version prefix (`v1-${{ hashFiles('package-lock.json') }}`) so cache can be busted manually.
- Flaky tests breaking CI: Isolate flaky tests into quarantine suites while investigating root causes.

## 11. Security & Privacy Constraints
- Prevent script injection in pull request triggers: Never directly interpolate untrusted context values like `${{ github.event.pull_request.title }}` inside `run:` shell commands.
- Use GitHub Environments for deployment secrets with required human reviewers.

## 12. Verification & Testing Requirements
- Validate syntax using `actionlint`:
  ```bash
  actionlint .github/workflows/*.yml
  ```
- Test locally using `act` (if Docker is available) to simulate runner execution.

## 13. Completion Criteria
- GitHub Actions YAML files parse cleanly with zero syntax warnings.
- Least-privilege permissions explicitly declared.
- Caching and test gates configured properly.

## 14. Relevant Official References
- GitHub Actions Official Documentation (docs.github.com/en/actions).
- OpenSSF Scorecard & Supply Chain Security Guidelines.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with GitHub Actions v4 ecosystem and Ubuntu 24.04 runners.
