---
name: site-reliability-sre
description: Site Reliability Engineering (SRE), Service Level Indicators (SLIs), Service Level Objectives (SLOs), error budgets, Prometheus metrics, Grafana alerting rules, and blameless incident postmortems.
---

# Site Reliability Engineering (SRE) & Observability

## 1. Intended Role & Domain
- **Primary Domain**: Infrastructure, Operations & Reliability
- **Target Roles**: Site Reliability Engineer (SRE), DevOps Engineer, Systems Administrator
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "sre", "sli slo", "error budget", "prometheus alerting", "grafana dashboard", "postmortem", "incident response", "system reliability".
- **Contextual Inferences**: Production outages, high latency alerts, designing reliability targets for microservices.
- **Chained Predecessors**: `repo-audit`, `root-cause-debugging`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Performing manual local coding or styling fixes without production infrastructure or metrics context.
  - Designing low-level chip firmware without networked service infrastructure.

## 4. Required Inputs & Context
- Target service architecture and critical user journeys (CUJs).
- Metrics system (Prometheus, OpenTelemetry, Datadog, CloudWatch).
- Target availability tiers (e.g. 99.9% or 99.95% monthly availability).

## 5. Expected Outputs & Artifacts
- Formal SLI/SLO specification document with error budget policy.
- Prometheus Alerting Rules YAML file (`alerts.yaml`) with multi-window burn rate alerts.
- Grafana dashboard definition (JSON) visualizing SLI trends and burn rate.
- Blameless incident postmortem template with causal timeline.

## 6. Step-by-Step Operating Procedure
1. **Critical User Journey (CUJ) Identification**:
   - Define exact user-visible transactions (e.g., checkout completion, API search latency).
2. **SLI Metric Specification**:
   - Availability SLI: `count(successful_requests) / count(total_valid_requests)`.
   - Latency SLI: `count(requests_faster_than_threshold) / count(total_valid_requests)`.
3. **SLO Target & Error Budget Definition**:
   - Establish target (e.g. 99.9% over rolling 30-day window = 0.1% error budget = 43.2 minutes downtime/month).
4. **Multi-Window Multi-Burn-Rate Alerting**:
   - Configure alerts that fire on 14.4x burn rate (2% budget consumed in 1 hour) and 6x burn rate (5% consumed in 6 hours).
5. **Dashboard & Postmortem Workflow**:
   - Create Grafana visualization and establish error budget freeze policy when budget is exhausted.

## 7. Repository Inspection & Planning Requirements
- Non-destructive Prometheus and OpenTelemetry check:
  ```bash
  grep -ri "prometheus" src/ 2>/dev/null || find . -name "*alert*.yaml"
  ```
- Preservation rule: Avoid pager fatigue; do not configure paging alerts on non-actionable warnings or transient spikes.

## 8. Tool & Dependency Requirements
- Prometheus 2.45+, Alertmanager, Grafana, OpenTelemetry SDKs.

## 9. Implementation Guidelines & Best Practices
- Never alert on raw CPU or RAM thresholds alone (cause-based alerting); alert on user impact (SLO burn rate).
- Multi-window alerting formula:
  ```yaml
  groups:
    - name: slo_alerts
      rules:
        - alert: HighErrorRateBurnRate
          expr: (
              sum(rate(http_requests_total{status=~"5.."}[1h])) 
              / sum(rate(http_requests_total[1h]))
            ) > (1 - 0.999) * 14.4
          for: 2m
          labels:
            severity: page
          annotations:
            summary: "Service error budget burning at 14.4x rate (2% budget consumed in 1h)"
  ```

## 10. Error Handling & Recovery Procedures
- Missing telemetry data: Implement fallback zero-fill counters in PromQL (`or vector(0)`) to prevent alerts from breaking on sparse traffic.
- Alert storming during outage: Configure `inhibit_rules` in Alertmanager to suppress downstream leaf-service alerts when root gateway is down.

## 11. Security & Privacy Constraints
- Metric labels must NEVER contain PII, user email addresses, or unhashed account IDs (cardinality explosion and privacy violation).

## 12. Verification & Testing Requirements
- Validate Prometheus alert syntax using `promtool`:
  ```bash
  promtool check rules alerts.yaml
  ```
- Unit test alert triggers against simulated PromQL time series.

## 13. Completion Criteria
- SLIs and SLOs formally defined with mathematical precision.
- Promtool validates alert syntax with zero errors.
- Blameless postmortem template in place.

## 14. Relevant Official References
- Google SRE Book & SRE Workbook (Beyer, Jones, Petoff, Murphy).
- The Site Reliability Workbook: Implementing SLOs.
- Prometheus Alerting Best Practices (prometheus.io).

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with OpenTelemetry 1.30+ and Prometheus 2.50+.
