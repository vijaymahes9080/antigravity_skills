---
name: git-release-prep
description: Semantic versioning, changelog generation, clean git branching, PR reviews, merge conflict resolution, and release tagging. Use when preparing releases, managing git branches, or writing release notes.
---

# Git Workflow & Release Preparation

## 1. Intended Role & Domain
- **Primary Domain**: Software Development & DevOps
- **Target Roles**: DevOps Engineer, Release Manager, Git Specialist
- **Architectural Layer**: Layer 1 (Core Engineering Foundations)

## 2. Activation Conditions
- **Direct Triggers**: "prepare release", "create release notes", "generate changelog", "resolve git conflict", "git workflow", "version bump".
- **Contextual Inferences**: Milestone completion, merging feature branches into main/release branches.
- **Chained Predecessors**: Testing and verification skills.

## 3. Explicit Exclusions
- Do NOT use when:
  - Working in repositories without git version control.
  - Making simple local code edits with no git release context.

## 4. Required Inputs & Context
- Clean git working tree (or explicit list of unstaged changes).
- Target version bump (major, minor, patch) conforming to SemVer 2.0.0.
- Commit history since last release tag.

## 5. Expected Outputs & Artifacts
- `CHANGELOG.md` updated with categorized changes (Features, Fixes, Breaking Changes).
- Version updated across project manifests (`package.json`, `pyproject.toml`, `Cargo.toml`).
- Git release tag or PR description.

## 6. Step-by-Step Operating Procedure
1. **Working Tree & History Inspection**:
   - Verify that working directory is clean and all tests pass.
   - List commits since last tag:
     ```bash
     git describe --tags --abbrev=0
     git log $(git describe --tags --abbrev=0)..HEAD --oneline
     ```
2. **Semantic Version Calculation**:
   - Determine increment: Major (breaking changes), Minor (backward-compatible features), Patch (fixes).
3. **Changelog & Documentation Update**:
   - Parse conventional commits (`feat:`, `fix:`, `perf:`, `docs:`, `refactor:`) into structured sections.
4. **Manifest Synchronization**:
   - Bump version strings synchronously across all manifests and lockfiles.
5. **Git Commit & Tag Verification**:
   - Review staged diff to ensure zero unintended artifacts or secrets are committed.

## 7. Repository Inspection & Planning Requirements
- Inspect branch and remote status:
  ```bash
  git status
  git branch -vv
  git remote -v
  ```
- Preservation rule: Never force-push (`--force`) to protected main/master branches.

## 8. Tool & Dependency Requirements
- Git CLI (v2.x+).
- Node, Python, or shell utilities for version bumping.

## 9. Implementation Guidelines & Best Practices
- Follow Conventional Commits specification.
- Ensure release notes link to relevant issue/PR numbers.
- Avoid large monolithic release commits that mix bug fixes with structural rewrites.

## 10. Error Handling & Recovery Procedures
- Merge conflict: Inspect conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`), preserve both intents, and run tests before staging.
- Accidental tag on wrong commit: Delete local tag (`git tag -d vX.Y.Z`) and re-tag correct commit.

## 11. Security & Privacy Constraints
- Never commit `.env`, private keys, credentials, or local scratch artifacts during release commits.
- Ensure `.gitignore` covers build artifacts (`dist/`, `build/`, `*.pyc`).

## 12. Verification & Testing Requirements
- Confirm tag syntax:
  ```bash
  git tag -v vX.Y.Z || git tag --list "v*"
  ```
- Test build from the release commit:
  ```bash
  npm run build || python -m build || cargo build --release
  ```

## 13. Completion Criteria
- Manifests bumped to matching SemVer string.
- `CHANGELOG.md` properly formatted.
- Clean git status with release commit ready or tagged.

## 14. Relevant Official References
- Semantic Versioning 2.0.0 (semver.org).
- Conventional Commits 1.0.0 (conventionalcommits.org).

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with GitHub, GitLab, and local git workflows.
