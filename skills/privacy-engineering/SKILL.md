---
name: privacy-engineering
description: Privacy-by-design architecture, automated PII discovery and masking, differential privacy, synthetic data generation, GDPR/CCPA/DPDP regulatory compliance, cryptographic anonymization, and Privacy Impact Assessments (PIAs).
---

# Privacy Engineering & Privacy-by-Design Architecture

## 1. Intended Role & Domain
- **Primary Domain**: Cybersecurity, Privacy & Gov.
- **Target Roles**: Privacy Engineer, Data Protection Officer Technical Lead, Security & Governance Architect
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "privacy engineering", "pii masking", "gdpr compliance", "ccpa", "dpdp", "differential privacy", "synthetic data", "privacy impact assessment", "data anonymization", "consent management".
- **Contextual Inferences**: Handling sensitive personal data (names, emails, SSNs, health data, financial records), designing privacy-preserving data pipelines, responding to Data Subject Access Requests (DSARs).
- **Chained Predecessors**: `appsec-owasp-audit`, `cybersecurity-sast-vulnerability-scan`, `database-postgresql-performance-optimization`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Performing routine network packet firewall configuration without personal data context.
  - Basic frontend aesthetic styling without data privacy forms.

## 4. Required Inputs & Context
- Data schemas, API request/response models, database DDLs.
- Applicable legal regulations (GDPR EU, CCPA/CPRA California, DPDP India, HIPAA US).
- Data flow architecture (ingestion -> storage -> processing -> analytics -> third-party sharing).

## 5. Expected Outputs & Artifacts
- Automated PII scanning and redaction utility (`pii_masking.py`).
- Declarative data retention and deletion job (implementing Right to be Forgotten / DSAR).
- Technical Privacy Impact Assessment (`pia_assessment.md`) mapping data minimization.
- Synthetic data generation pipeline for non-production environments.

## 6. Step-by-Step Operating Procedure
1. **Data Discovery & PII Classification**:
   - Classify fields into tiers: Direct Identifiers (SSN, Email, Name), Quasi-Identifiers (ZIP, DOB, Gender), Sensitive Attributes (Health, Biometric).
2. **Privacy-by-Design & Data Minimization**:
   - Enforce collection minimization: do not collect personal data fields without documented business justification.
3. **Cryptographic Anonymization & Pseudonymization**:
   - Replace direct identifiers with keyed cryptographic HMACs or tokenized UUIDs.
   - Implement k-Anonymity and l-Diversity on analytical data exports.
4. **Differential Privacy Implementation**:
   - Inject calibrated mathematical noise (Laplace or Gaussian mechanisms) into analytical query results to prevent linkage attacks.
5. **Automated DSAR & Erasure Automation**:
   - Implement cascading data deletion pipelines satisfying the 30-day GDPR Right to be Forgotten SLA.
6. **Logging & Telemetry Scrubbing**:
   - Sanitize application logs, Sentry error traces, and telemetry pipelines to prevent accidental PII leakage.

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection of data models and logger configurations:
  ```bash
  grep -rnE "(ssn|passport|email|phone|birthdate|credit_card)" . 2>/dev/null
  ```
- Preservation rule: Never store raw encryption keys in the same physical database table as the encrypted personal data.

## 8. Tool & Dependency Requirements
- Python 3.11+, Microsoft Presidio, Diffprivlib, Faker, SQLAlchemy 2.0, PostgreSQL pgcrypto.

## 9. Implementation Guidelines & Best Practices
- High-performance automated PII detection and redaction engine for application logging and text streams:

```python
import re
from typing import Dict, Any, List

class PrivacyShield:
    def __init__(self):
        self.patterns = {
            "EMAIL": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
            "PHONE_US": re.compile(r"(?:\+?1[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})"),
            "SSN": re.compile(r"\d{3}-\d{2}-\d{4}"),
            "CREDIT_CARD": re.compile(r"(?:\d{4}[- ]?){3}\d{4}")
        }

    def redact_text(self, text: str) -> str:
        scrubbed = text
        for pii_type, pattern in self.patterns.items():
            scrubbed = pattern.sub(f"[REDACTED_{pii_type}]", scrubbed)
        return scrubbed

    def mask_record(self, record: Dict[str, Any], sensitive_fields: List[str]) -> Dict[str, Any]:
        sanitized = record.copy()
        for field in sensitive_fields:
            if field in sanitized and sanitized[field]:
                val = str(sanitized[field])
                if "@" in val:
                    parts = val.split("@")
                    sanitized[field] = f"{parts[0][:2]}***@{parts[1]}"
                else:
                    sanitized[field] = f"***{val[-4:]}" if len(val) >= 4 else "***"
        return sanitized

# Example usage
if __name__ == "__main__":
    shield = PrivacyShield()
    log_line = "User vijay.kumar@example.com logged in with phone 555-123-4567 and SSN 123-45-6789."
    print("Scrubbed Log:", shield.redact_text(log_line))
```

## 10. Error Handling & Recovery Procedures
- PII false negatives: Maintain customizable regex patterns and regex overrides for regional identifiers (e.g. India Aadhaar, UK NHS number).
- Erasure cascade failure: Ensure foreign keys use `ON DELETE CASCADE` or soft-delete pseudonymization flags.

## 11. Security & Privacy Constraints
- All pseudonymization secret salts must be rotated annually and stored in a Hardware Security Module (HSM).

## 12. Verification & Testing Requirements
- Zero unmasked PII strings in test log exports.
- Automated tests verify that synthetic data generation maintains statistical distribution without leaking original identities.

## 13. Completion Criteria
- PII discovery and redaction active across all request logging middleware.
- Technical Privacy Impact Assessment document completed.
- DSAR deletion verification automated.

## 14. Relevant Official References
- ISO/IEC 27701: Privacy Information Management System.
- NIST Privacy Framework: A Tool for Improving Privacy through Enterprise Risk Management.
- European Data Protection Board (EDPB) Guidelines on Data Protection by Design.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Aligned with GDPR, CCPA/CPRA, and India DPDP Act.
