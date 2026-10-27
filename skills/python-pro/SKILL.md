---
name: python-pro
description: Master Python 3.12+ and Python 3.13 features, modern type hinting (PEP 695 type parameter syntax), async/await concurrency, high-performance package management with uv, and pytest suites.
---

# Modern Python 3.12+ Architecture & Engineering

## 1. Intended Role & Domain
- **Primary Domain**: Software Development & Backend Architecture
- **Target Roles**: Python Developer, Backend Developer, Data Platform Engineer
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "python", "modern python", "python 3.12", "python type hints", "uv package manager", "pytest", "asyncio python", "structural pattern matching".
- **Contextual Inferences**: Repositories containing `pyproject.toml`, `requirements.txt`, `setup.py`, Python virtual environments.
- **Chained Predecessors**: `task-decomposition`, `repo-audit`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Working purely in JavaScript/TypeScript, Go, Rust, or C/C++ without Python.
  - Basic bash scripting where Python is not installed.

## 4. Required Inputs & Context
- Python 3.10+ (recommended Python 3.12+).
- Project packaging configuration (`pyproject.toml` using Hatch, Poetry, Flit, or Setuptools).
- Package manager (uv, pip, or poetry).

## 5. Expected Outputs & Artifacts
- Strongly typed Python modules utilizing modern type syntax (`type Point = tuple[float, float]`).
- Asynchronous task processing using `asyncio.TaskGroup` (Python 3.11+).
- Pyproject configuration with Ruff linter/formatter and Pytest runner.
- Automated unit test suite with high coverage.

## 6. Step-by-Step Operating Procedure
1. **Environment & Runtime Verification**:
   - Verify Python runtime: `python --version` (ensure >= 3.11 for `TaskGroup` and >= 3.12 for PEP 695).
2. **Package Management & Tooling Setup**:
   - Use `uv` for 10x-100x faster dependency resolution and virtual environment creation.
3. **Type Annotations & Structural Pattern Matching**:
   - Utilize native generic syntax (`def get_first[T](items: list[T]) -> T: ...`).
   - Use `match / case` statements for clean domain dispatch.
4. **Structured Concurrency with TaskGroup**:
   - Replace legacy `asyncio.gather()` with `async with asyncio.TaskGroup() as tg:` to ensure deterministic error propagation and cancellation.
5. **Testing & Static Analysis**:
   - Run Ruff for formatting/linting and Pytest with `-v --strict-markers`.

## 7. Repository Inspection & Planning Requirements
- Non-destructive package check:
  ```bash
  python --version
  cat pyproject.toml 2>/dev/null || cat requirements.txt 2>/dev/null
  ```
- Preservation rule: Avoid legacy Python 2/3 compatibility shims (`six`, `__future__`); write pure modern Python.

## 8. Tool & Dependency Requirements
- Python 3.11/3.12+, `uv` or `pip`, `pytest`, `ruff`, `mypy`.

## 9. Implementation Guidelines & Best Practices
- Always use `asyncio.TaskGroup` for concurrent subtasks to avoid leaking background tasks on exception:

```python
import asyncio
from typing import Sequence

# PEP 695 type alias syntax (Python 3.12+)
type UserID = int
type UserRecord = dict[str, str | int]

async def fetch_profile(user_id: UserID) -> UserRecord:
    await asyncio.sleep(0.01)
    return {"id": user_id, "name": f"User_{user_id}"}

async def fetch_all_users(user_ids: Sequence[UserID]) -> list[UserRecord]:
    results = []
    # Structured concurrency with TaskGroup
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch_profile(uid)) for uid in user_ids]
    return [t.result() for t in tasks]
```

## 10. Error Handling & Recovery Procedures
- `ExceptionGroup` handling: In Python 3.11+, use `except* ValueError as eg:` syntax to catch specific exceptions from TaskGroups.

## 11. Security & Privacy Constraints
- Prevent Arbitrary Code Execution: Never use `pickle` for untrusted deserialization; use Pydantic or `json`.
- Prevent Path Traversal: Validate file paths with `Path.resolve()` against a base directory.

## 12. Verification & Testing Requirements
- Run type checker and linter:
  ```bash
  ruff check src/
  mypy src/ --strict
  ```
- Run Pytest:
  ```bash
  pytest tests/ -v
  ```

## 13. Completion Criteria
- Zero type errors under strict mypy/pyright.
- Zero Ruff linting or formatting errors.
- 100% passing tests in Pytest suite.

## 14. Relevant Official References
- Python 3.12 What's New & PEP 695 (Type Parameter Syntax).
- Ruff Linter Documentation (docs.astral.sh/ruff).
- UV Package Manager Documentation (docs.astral.sh/uv).

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with Python 3.11, 3.12, and 3.13.
