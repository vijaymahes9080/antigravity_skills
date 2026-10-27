---
name: secure-coding-review
description: Static analysis, OWASP Top 10 mitigation, secret scanning, SQLi/XSS/SSRF prevention, and least-privilege verification. Use when reviewing code for security vulnerabilities, conducting PR audits, or hardening endpoints. [Consolidated Master Skill: appsec-owasp-audit]
---

# Task Workflow: Secure Coding & Vulnerability Review

> [!NOTE]
> **Consolidated Master Workflow**: This skill has been consolidated into [appsec-owasp-audit](../appsec-owasp-audit/SKILL.md). All static code analysis, OWASP ASVS verification, secret scanning, injection mitigation, and defense-in-depth API hardening are executed through the master `appsec-owasp-audit` engine.

## Supported Invocations
- `/secure-coding-review` (Maintained for full backward compatibility)
- `/appsec-owasp-audit` (Direct Master Skill invocation)
- `/audit` (Common alias)

## Core Capabilities Executed
When invoked via `/secure-coding-review`, Antigravity activates the unified master security review workflow defined in [appsec-owasp-audit](../appsec-owasp-audit/SKILL.md):
1. **Secret & Credential Discovery**: High-entropy regex scanning for leaked API keys, tokens, and private keys.
2. **Input Validation & Injection Sinks**: Tracing untrusted inputs into database queries (SQLi/NoSQLi), OS commands, and HTML templates.
3. **Authentication & Session Analysis**: Token expiration, password hashing algorithms (Argon2id, bcrypt), and CSRF protection.
4. **Access Control & BOLA/IDOR Review**: Object-level permissions and role checks on mutating routes.
5. **Defensive API Hardening**: Helmet HTTP headers (CSP, HSTS), parameterized ORM queries, and timing-safe token comparisons.

Please refer to [appsec-owasp-audit/SKILL.md](../appsec-owasp-audit/SKILL.md) for full execution steps and verification gates.
