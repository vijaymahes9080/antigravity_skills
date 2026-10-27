---
name: task-deployable-dockerize
description: Convert an existing arbitrary software project into a self-contained, reproducible, and deployable Dockerized application with zero host dependency requirements. [Consolidated Master Skill: docker-containerization]
---

# Task Workflow: Convert Existing Project to Deployable Container

> [!NOTE]
> **Consolidated Master Workflow**: This skill has been consolidated into [docker-containerization](../docker-containerization/SKILL.md). All multi-stage container builds, zero-host-dependency application packaging, `.dockerignore` generation, and non-root security hardening are executed through the master `docker-containerization` engine.

## Supported Invocations
- `/task-deployable-dockerize` (Maintained for full backward compatibility)
- `/docker-containerization` (Direct Master Skill invocation)
- `/docker` (Common alias)

## Core Capabilities Executed
When invoked via `/task-deployable-dockerize`, Antigravity activates the unified master containerization workflow defined in [docker-containerization](../docker-containerization/SKILL.md):
1. **Entry Point & Environment Variable Inventory**: Auto-detect startup scripts and config keys.
2. **Comprehensive `.dockerignore` Generation**: Prevent caches, node_modules, and secrets from entering image layers.
3. **Multi-Stage Build Construction**: Builder stage for compilation + minimal distroless/slim runtime image.
4. **Non-Root Hardening**: Explicit non-root UID/GID and signal handling.
5. **Docker Compose & Healthcheck Runbook**: Multi-service local verification.

Please refer to [docker-containerization/SKILL.md](../docker-containerization/SKILL.md) for full execution steps and verification gates.
