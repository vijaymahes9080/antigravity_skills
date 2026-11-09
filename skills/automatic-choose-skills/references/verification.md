# Automatic Choose Skills: Verification Reference

This document provides the checklist and verification procedures to ensure that skill selection and orchestration satisfy user requirements accurately.

---

## 1. Skill Selection Quality Audit

Before commencing execution, verify the selection against these 5 checks:
- [ ] **Necessity Check**: Is every selected skill strictly required to complete the user's task?
- [ ] **Sufficiency Check**: Does the combination of skills cover all requested deliverables (e.g., frontend + backend + testing)?
- [ ] **No Keyword Hallucination**: Was each skill verified against actual installed files or the environment index?
- [ ] **Clear Sequencing**: Is there a deterministic execution sequence avoiding circular dependencies?
- [ ] **User Tool Alignment**: Does the selection respect the user's requested frameworks, languages, and constraints?

---

## 2. Multi-Skill Execution Verification Checklist

After completing the task, verify:
- [ ] **Deliverables Complete**: All files, endpoints, components, or documents requested by the user are fully created.
- [ ] **Tests Executed**: Verification commands or unit tests specified by the domain skills were executed and passed.
- [ ] **Skill Invariants Respected**: Runbook instructions from each activated skill were followed faithfully.
- [ ] **Clean Reporting**: If the task was substantial, the concise selection report was provided; if straightforward, unnecessary verbosity was omitted.
