---
name: fastapi-pro
description: Build high-performance async APIs with FastAPI, SQLAlchemy 2.0 async, and Pydantic V2. Master microservices, WebSockets, background tasks, and OpenAPI 3.1 documentation.
---

# FastAPI & Async API Engineering

## 1. Intended Role & Domain
- **Primary Domain**: Software Development & Backend Engineering
- **Target Roles**: Backend and API Developer, Python Developer, Full-Stack Developer
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "fastapi", "async python api", "sqlalchemy async", "pydantic v2", "build rest api in python", "openapi 3.1".
- **Contextual Inferences**: Repositories containing `fastapi`, `uvicorn`, `pydantic` in `pyproject.toml` or `requirements.txt`.
- **Chained Predecessors**: `task-decomposition`, `repo-audit`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Developing synchronous Django or Flask monolithic template applications.
  - Non-Python backend frameworks (e.g. Node.js, Go, Spring Boot).

## 4. Required Inputs & Context
- API endpoints specification or entity models.
- Database connection configuration (PostgreSQL asyncpg, SQLite aiosqlite).
- Python environment with Python 3.10+ (preferred 3.12+).

## 5. Expected Outputs & Artifacts
- Production-grade FastAPI router modules (`APIRouter`).
- Pydantic V2 request/response schemas with strict validation.
- Async database models and session dependency injection (`Depends`).
- Automated pytest integration test suite with `httpx.AsyncClient`.

## 6. Step-by-Step Operating Procedure
1. **Environment & Dependency Verification**:
   - Verify Python version and installed packages: `fastapi`, `uvicorn[standard]`, `pydantic>=2.0`, `sqlalchemy>=2.0`.
2. **Schema Definition (Pydantic V2)**:
   - Create schemas in `schemas/` with `ConfigDict(from_attributes=True)` for ORM compatibility.
3. **Database & Session Management**:
   - Configure async engine (`create_async_engine`) and session factory (`async_sessionmaker`).
   - Implement `get_db` generator with `async with` context manager.
4. **Router & Business Logic Implementation**:
   - Implement handlers in `routers/` using dependency injection for auth, database, and background tasks.
5. **Testing & OpenAPI Validation**:
   - Test endpoints with `httpx.AsyncClient` using `lifespan` handler.
   - Inspect OpenAPI schema at `/docs` or `/openapi.json`.

## 7. Repository Inspection & Planning Requirements
- Non-destructive dependency check:
  ```bash
  python -c "import fastapi, pydantic, sqlalchemy; print(fastapi.__version__, pydantic.__version__, sqlalchemy.__version__)"
  ```
- Preservation rule: Do not mix synchronous blocking calls (e.g. `requests.get()`, `time.sleep()`) inside `async def` endpoints.

## 8. Tool & Dependency Requirements
- Python 3.10+, `uvicorn`, `httpx`, `pytest-asyncio`.

## 9. Implementation Guidelines & Best Practices
- Never execute blocking I/O in async endpoints. Use `asyncio.to_thread` for legacy synchronous libraries.
- Use Pydantic's `@field_validator` and `@model_validator(mode='after')` for business rule enforcement.
- Always return typed responses using `response_model=...` to prevent data leakage.

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=List[ItemResponse])
async def list_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ItemModel).limit(100))
    return result.scalars().all()
```

## 10. Error Handling & Recovery Procedures
- `RuntimeError: Task attached to a different loop`: Ensure database engine and sessions are initialized per lifespan/request.
- Database disconnection: Configure `pool_pre_ping=True` and connection pooling in SQLAlchemy engine.

## 11. Security & Privacy Constraints
- Protect sensitive data: Never return password hashes in response models.
- Enforce CORS policy: Do not use `allow_origins=["*"]` with `allow_credentials=True` in production.
- Implement rate limiting with `slowapi` or Redis middleware on public routes.

## 12. Verification & Testing Requirements
- Execute async tests:
  ```bash
  pytest tests/ -v -m asyncio
  ```
- Verify OpenAPI documentation:
  ```bash
  python -c "from main import app; import json; json.dump(app.openapi(), open('openapi.json', 'w'))"
  ```

## 13. Completion Criteria
- Endpoints respond with correct HTTP status codes (200, 201, 400, 404, 422).
- Zero blocking calls in async loop.
- Pytest suite passes 100%.

## 14. Relevant Official References
- FastAPI Official Docs (fastapi.tiangolo.com).
- Pydantic V2 Migration & Documentation (docs.pydantic.dev).
- SQLAlchemy 2.0 Asyncio Guide (docs.sqlalchemy.org).

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with FastAPI 0.115+ and Python 3.12/3.13.
