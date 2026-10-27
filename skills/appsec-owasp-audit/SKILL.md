---
name: appsec-owasp-audit
description: Master defensive Application Security (AppSec), OWASP ASVS verification, secure code review, secret scanning, injection mitigation, dependency vulnerability remediation, and defense-in-depth API hardening.
---

# Master Application Security (AppSec), OWASP ASVS & Secure Code Review

## 1. Intended Role & Domain
- **Primary Domain**: Cybersecurity, Application Defense & DevSecOps
- **Target Roles**: Application Security Engineer, Security Auditor, DevSecOps Specialist, Staff Security Architect
- **Architectural Layer**: Layer 2 (Specialized Technical Security & Defensive Standards)
- **Supported Invocations**: `/appsec-owasp-audit`, `/secure-coding-review`, `/audit`

## 2. Activation Conditions
- **Direct Triggers**: "appsec audit", "owasp asvs", "dependency vulnerability scan", "sast analysis", "secure api audit", "cve remediation", "security review", "audit vulnerability", "check OWASP", "scan for secrets", "prevent SQL injection", "XSS audit", "PR security review".
- **Contextual Inferences**: Pre-production security certification, vulnerability disclosure remediation, PR code reviews touching auth/data sinks, SOC2/ISO 27001 compliance.
- **Chained Predecessors**: `repo-audit` or code authoring workflows.

## 3. Explicit Exclusions
- Do NOT use when:
  - Performing destructive denial-of-service (DoS) or attacking external third-party targets without explicit authorization.
  - Basic non-security cosmetic CSS/styling reviews.

## 4. Required Inputs & Context
- Target codebase or specific PR diff, plus dependency lockfiles (`package-lock.json`, `poetry.lock`, `Cargo.lock`, `pom.xml`).
- Threat model context: public API, internal microservice, client-side application.
- Security scanner tools (Semgrep, Trivy, Bandit, OSV-Scanner, npm audit).

## 5. Expected Outputs & Artifacts
1. **Security Audit Ledger**: Identified findings mapped to CWE, OWASP Top 10, and CVSS v3.1 severity scores.
2. **Defensive Remediation Patches**: Parameterized queries, input sanitization, and timing-safe comparisons.
3. **Automated SAST & Dependency Pipeline**: CI/CD configuration enforcing vulnerability gates.
4. **Hardened HTTP Headers & Session Configuration**: CSP, HSTS, secure cookie policies, and CORS.

## 6. Step-by-Step Operating Procedure

### Step 1: Secret & Credential Discovery
- Scan codebase for hardcoded API keys, JWT secrets, private keys, or passwords:
  ```bash
  rg "AIzaSy|sk-[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16}"
  git log -n 5 --diff-filter=A --stat
  ```
- Preservation rule: Never commit dummy credentials or real test secrets to git repositories. Immediately advise rotation if exposed.

### Step 2: Input Validation & Injection Sinks Analysis
- Trace untrusted inputs into SQL/NoSQL databases, OS commands, HTML templates, and URL fetches:
  ```bash
  rg "execute\(f[\"']" || rg "rawQuery\("
  rg "\beval\(" || rg "child_process\.exec\("
  ```
- Enforce strict parameterization (never string interpolation) across all database queries.

### Step 3: Supply Chain & Dependency CVE Scan
- Audit lockfiles for known transitive vulnerabilities:
  ```bash
  npm audit --json 2>/dev/null || pip-audit 2>/dev/null || cargo audit 2>/dev/null || true
  ```
- Pin patched minor versions or implement compensating input validation controls.

### Step 4: Authentication, Authorization & Session Hardening
- Audit broken object-level authorization (BOLA/IDOR) on all mutating endpoints.
- Verify password hashing algorithms (Argon2id, bcrypt; reject MD5/SHA1).
- Audit cookie flags (`HttpOnly`, `Secure`, `SameSite=Strict`) and CSRF protection.
- Enforce constant-time comparison for sensitive tokens (`crypto.timingSafeEqual`).

### Step 5: Defense-in-Depth HTTP Headers & API Hardening
- Enforce strict Content Security Policy (CSP), HTTP Strict Transport Security (HSTS), and X-Content-Type-Options:

```typescript
// Express security headers via Helmet
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      objectSrc: ["'none'"],
      upgradeInsecureRequests: [],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' }
}));
```

## 7. Security & Privacy Constraints
- **Confidentiality Rule**: Treat vulnerability reports as confidential; never publish unpatched zero-days in public repositories.
- **Redaction Rule**: Redact all discovered tokens, passwords, and private IPs from output logs.

## 8. Verification & Testing Requirements
1. **SAST Scanner Verification**:
   ```bash
   semgrep --config=auto --error src/ || bandit -r src/ -ll || npm audit --audit-level=high
   ```
2. **Automated Negative Test**:
   - Write security test asserting rejection of malicious payloads (e.g. SQL injection payload, XSS tag injection, unauthorized user ID access).

## 9. Relevant Official References
- OWASP Application Security Verification Standard (ASVS v4.0.3).
- OWASP Top 10:2021 & OWASP API Security Top 10:2023.
- NIST SP 800-53: Security and Privacy Controls for Information Systems.
- OpenSSF Best Practices for Open Source Security.

## 10. Maintenance & Compatibility Notes
- Last audited: October 2026. Aligned with OWASP ASVS and modern cloud security architectures.
