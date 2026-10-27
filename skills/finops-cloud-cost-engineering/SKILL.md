---
name: finops-cloud-cost-engineering
description: Cloud financial operations (FinOps), FOCUS framework compliance, compute rightsizing, Reserved/Spot Instance optimization, storage tiering, architectural unit cost economics, and real-time anomaly alerting.
---

# FinOps & Cloud Cost Optimization Engineering

## 1. Intended Role & Domain
- **Primary Domain**: Cloud, DevOps & Platform Eng.
- **Target Roles**: FinOps Practitioner, Cloud Cost Optimization Engineer, SRE Financial Architect
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "finops", "cloud cost optimization", "reduce aws bill", "focus specification", "rightsizing compute", "spot instances", "reserved instance coverage", "storage tiering", "unit cost economics", "cost anomaly alerting".
- **Contextual Inferences**: Auditing cloud infrastructure spend, reducing Kubernetes cluster costs, designing architectures for minimal operational expenditure (OpEx).
- **Chained Predecessors**: `site-reliability-sre`, `cloud-security-hardening`, `docker-containerization`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Performing microservice application code debugging unrelated to cloud resource allocation.
  - Designing visual user interfaces.

## 4. Required Inputs & Context
- Target cloud platform (AWS, GCP, Azure, Kubernetes, Datadog, Snowflake).
- Current billing data, CUR (Cost and Usage Report), or Infracost breakdown.
- Performance SLA thresholds (ensuring cost cuts do not compromise latency or availability).

## 5. Expected Outputs & Artifacts
- Cost optimization ledger (`finops_remediation_ledger.md`) with concrete dollar savings estimates.
- Infrastructure-as-Code cost regression gate (`infracost.yml` for GitHub Actions).
- Kubernetes resource rightsizing recommendations (requests/limits calibration).
- Automated storage lifecycle policy configurations (S3 Glacier / GCS Coldline).

## 6. Step-by-Step Operating Procedure
1. **Cost & Usage Discovery (FOCUS Framework)**:
   - Normalize cloud spend into FinOps Open Cost and Usage Specification (FOCUS) standard schemas: BilledCost, EffectiveCost, ResourceId, ServiceName.
2. **Compute Rightsizing & Utilization Audit**:
   - Identify zombie resources: unattached EBS volumes, idle load balancers, orphaned snapshots.
   - Profile CPU/Memory utilization: identify instances with < 15% average CPU for down-scaling.
3. **Commitment & Purchasing Strategy**:
   - Calibrate commitment coverage: Compute Savings Plans and Reserved Instances for steady-state baseline.
   - Transition stateless batch, CI/CD, and non-critical worker workloads to Spot/Preemptible instances.
4. **Storage Tiering & Lifecycle Automation**:
   - Establish lifecycle rules: transition objects from Standard to Infrequent Access (IA) at 30 days, Glacier Flexible at 90 days, Deep Archive at 180 days.
5. **Architectural Unit Cost Modeling**:
   - Calculate unit cost metrics (e.g., Cost per Active User, Cost per Query, Cost per API Call).
6. **Continuous CI/CD Cost Guardrails**:
   - Integrate Infracost pull request checks blocking unexpected monthly cloud spend spikes.

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection of Terraform / CloudFormation infrastructure manifests:
  ```bash
  find . -name "*.tf" -o -name "kustomization.yaml" -o -name "*values*.yaml" 2>/dev/null
  ```
- Preservation rule: Never downgrade production database instances during peak operational hours.

## 8. Tool & Dependency Requirements
- Infracost, OpenCost / Kubecost, AWS Cost Explorer CLI, Terraform / OpenTofu.

## 9. Implementation Guidelines & Best Practices
- Automated GitHub Actions CI workflow enforcing Infracost cost regression gates on PRs:

```yaml
name: Cloud Cost Guardrail
on: [pull_request]

jobs:
  infracost:
    name: Infracost Financial Gate
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Infracost
        uses: infracost/actions/setup@v3
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}

      - name: Generate Baseline Cost
        run: |
          infracost breakdown --path=.             --format=json             --out-file=/tmp/infracost-base.json

      - name: Post Cost Comment to PR
        run: |
          infracost comment github --path=/tmp/infracost-base.json             --repo=$GITHUB_REPOSITORY             --github-token=${{ secrets.GITHUB_TOKEN }}             --pull-request=${{ github.event.pull_request.number }}             --behavior=update
```

## 10. Error Handling & Recovery Procedures
- Spot Instance termination notices: Implement AWS Node Termination Handler or graceful pre-drain hooks in Kubernetes.
- Inaccurate cost estimates: Reconcile synthetic Infracost estimates against actual monthly cloud billing exports.

## 11. Security & Privacy Constraints
- Protect cloud billing reports: CUR files contain business metrics and resource ARNs; restrict bucket access.

## 12. Verification & Testing Requirements
- Validate that rightsized Kubernetes pods do not trigger OOMKill events under peak synthetic load.
- Confirm automated lifecycle policies transition test objects accurately.

## 13. Completion Criteria
- Minimum 20% identifiable cloud spend reduction opportunities cataloged with implementation steps.
- Automated PR cost check active in repository.
- Unit economic cost KPI established.

## 14. Relevant Official References
- FinOps Foundation Framework & FOCUS Specification (finops.org).
- AWS Well-Architected Framework: Cost Optimization Pillar.
- Google Cloud Architecture Framework: Cost Optimization.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with AWS, GCP, Azure, and Kubernetes OpenCost standards.
