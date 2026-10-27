---
name: docker-containerization
description: Master production containerization, multi-stage Dockerfiles, minimal distroless/alpine images, non-root security hardening, zero-host-dependency packaging, Docker Compose orchestration, and container health checks.
---

# Master Docker Containerization & Deployable Application Packaging

## 1. Intended Role & Domain
- **Primary Domain**: Cloud Engineering, DevOps & Application Packaging
- **Target Roles**: Cloud Engineer, DevOps Engineer, Platform Engineer, Infrastructure Automation Specialist
- **Architectural Layer**: Layer 2 (Specialized Technical Standards & Packaging Workflows)
- **Supported Invocations**: `/docker-containerization`, `/task-deployable-dockerize`, `/docker`

## 2. Activation Conditions
- **Direct Triggers**: "dockerfile", "docker containerization", "docker compose", "multi-stage build", "distroless", "container hardening", "dockerize app", "convert project to deployable application", "make project deployable", "package app for production".
- **Contextual Inferences**: Converting arbitrary source code into reproducible, zero-host-dependency OCI container images; configuring local multi-service development stacks; preparing apps for Kubernetes, ECS, or GCP Cloud Run.
- **Chained Predecessors**: `task-decomposition` or build manifests.

## 3. Explicit Exclusions
- Do NOT use when:
  - Deploying directly to bare-metal microcontroller firmware without container runtimes.
  - Basic client-only standalone GUI apps without server hosting.

## 4. Required Inputs & Context
- Application source repository, entry point files, and package manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `pom.xml`, etc.).
- Target deployment platform (Kubernetes, AWS ECS, GCP Cloud Run, Docker Compose).
- Runtime environment variables and required backing services (PostgreSQL, Redis, RabbitMQ).

## 5. Expected Outputs & Artifacts
1. **Production Multi-Stage Dockerfile**: Builder stage + lean non-root runtime base (Distroless or Alpine/Debian slim).
2. **Comprehensive `.dockerignore`**: Strict exclusion of `.git`, local `node_modules`, `venv`, logs, caches, and secrets.
3. **`docker-compose.yml`**: Multi-service local testing orchestration with health checks and volume persistence.
4. **`.env.example`**: Complete template documenting all required runtime environment variables.
5. **Container Security Audit Report**: Trivy / Docker Scout vulnerability scan output.

## 6. Step-by-Step Operating Procedure

### Step 1: Entry Point & Dependency Discovery
- Inspect package manifests to identify build tools, runtime requirements, and startup commands:
  ```bash
  cat package.json 2>/dev/null || cat pyproject.toml 2>/dev/null || cat Cargo.toml 2>/dev/null
  ```
- Inventory environment variables:
  ```bash
  rg -o "(process\.env\.[A-Z0-9_]+|os\.environ\.get\(['\"][A-Z0-9_]+['\"]\)|System\.getenv\(['\"][A-Z0-9_]+['\"]\))"
  ```

### Step 2: Comprehensive `.dockerignore` Generation
- Create `.dockerignore` preventing secret/cache leakage:
  ```
  .git
  .github
  node_modules
  __pycache__
  *.pyc
  venv
  .env*
  !*.example
  dist
  target
  *.log
  tmp
  ```

### Step 3: Multi-Stage Build Construction (Cache-Optimized)
- Order instructions from least-frequently changed to most-frequently changed.
- Stage 1 (Builder): Install compiler/build dependencies, compile artifacts, prune devDependencies.
- Stage 2 (Runner): Copy only minimal runtime artifacts into clean base (e.g. `gcr.io/distroless` or `alpine`).

```dockerfile
# Multi-stage Node.js example
FROM node:22-bookworm-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build && npm prune --production

FROM gcr.io/distroless/nodejs22-debian12
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./package.json

USER nonroot:nonroot
EXPOSE 3000
ENV NODE_ENV=production
CMD ["dist/index.js"]
```

```dockerfile
# Multi-stage Python example
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src
ENV PATH=/root/.local/bin:$PATH
USER 10001
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 4: Non-Root Hardening & Signal Handling
- Enforce dedicated non-root UID/GID (`USER nonroot` or `USER 10001`).
- Use `exec` syntax (`CMD ["executable", "arg"]`) to guarantee PID 1 receives SIGTERM signals.
- Configure `HEALTHCHECK` with interval (30s), timeout (3s), and retries (3).

### Step 5: Docker Compose Orchestration & Smoke Testing
- Configure `docker-compose.yml` linking application to backing databases/caches.
- Execute local build, startup, and health endpoint assertions.

## 7. Security & Hardening Rules
- **Zero Root Rule**: Never run production containers as `root`.
- **Zero Secret Baking**: Never embed API keys or passwords in `ENV` or build `ARG` directives. Use Buildx secret mounts (`--mount=type=secret`).
- **Read-Only Root Filesystem**: Configure `--read-only` where feasible with writable `/tmp` tmpfs.

## 8. Verification & Testing Requirements
1. **Image Build Test**:
   ```bash
   docker build -t deployable-app:local .
   ```
2. **Container Startup & Health Verification**:
   ```bash
   docker run -d --name test-run -p 8080:8000 deployable-app:local
   sleep 3
   curl -f http://localhost:8080/health || curl -f http://localhost:8080/
   docker stop test-run && docker rm test-run
   ```
3. **Vulnerability Scan**:
   ```bash
   trivy image --severity HIGH,CRITICAL deployable-app:local || true
   ```

## 9. Relevant Official References
- Docker Best Practices for Image Construction (docs.docker.com).
- CIS Docker Benchmark v1.6.0.
- 12-Factor App Methodology (12factor.net).

## 10. Maintenance & Compatibility Notes
- Last audited: October 2026. Aligned with Docker Engine 26+, Buildx 0.14+, and OCI image specification v1.1.
