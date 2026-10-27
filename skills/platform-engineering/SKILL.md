---
name: platform-engineering
description: Architect and operate Internal Developer Platforms (IDPs), Backstage service catalogs, self-service infrastructure APIs, golden paths, developer experience (DevEx) metrics, DORA tracking, and platform orchestration.
---

# Platform Engineering & Internal Developer Platforms (IDP)

## 1. Intended Role & Domain
- **Primary Domain**: Cloud, DevOps & Platform Eng.
- **Target Roles**: Platform Engineer, DevEx Lead, Cloud Infrastructure Architect
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "platform engineering", "internal developer platform", "idp", "backstage catalog", "golden path", "self-service infrastructure", "scorecards", "devex", "dora metrics", "developer portal".
- **Contextual Inferences**: Reducing cognitive load on product engineering teams, providing standardized self-service provisioning, implementing service ownership standards.
- **Chained Predecessors**: `devops-ci-cd-github`, `docker-containerization`, `site-reliability-sre`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Writing business application logic for an isolated microservice.
  - Designing client-side web UI designs -> use `/frontend-interface-design-system`.

## 4. Required Inputs & Context
- Target cloud provider (AWS, GCP, Azure, Hybrid K8s).
- Service catalog platform (Spotify Backstage, Port, Cortex, Kratix).
- Infrastructure-as-Code tooling (Terraform, OpenTofu, Crossplane, Helm).
- Target engineering teams and desired self-service capabilities (e.g., spin up new Postgres DB, provision new microservice template).

## 5. Expected Outputs & Artifacts
- Service definition schema (`catalog-info.yaml`) with ownership, dependencies, and lifecycle tags.
- Software template (`template.yaml`) implementing an approved golden path.
- Self-service infrastructure orchestration (Crossplane composite resource or Terraform module).
- Platform scorecard configuration defining security, testing, and operational maturity gates.

## 6. Step-by-Step Operating Procedure
1. **Golden Path & Template Definition**:
   - Architect standardized templates encoding best-practice Docker, CI/CD, telemetry, and security defaults.
2. **Service Catalog Registration**:
   - Establish declarative `catalog-info.yaml` definitions for every microservice, API, and resource.
3. **Self-Service Infrastructure Automation**:
   - Expose infrastructure primitives via declarative Custom Resource Definitions (CRDs) or platform APIs.
4. **Scorecards & Operational Readiness**:
   - Define automated maturity rules: SonarQube quality gate passing, Sentry error monitoring active, PagerDuty on-call mapped.
5. **DORA & DevEx Telemetry**:
   - Instrument deployment frequency, lead time for changes, change failure rate, and time to restore service (MTTR).

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection of existing platform and deployment files:
  ```bash
  find . -name "catalog-info.yaml" -o -name "*template*.yaml" -o -name "*crossplane*" 2>/dev/null
  ```
- Preservation rule: Ensure golden path templates produce reproducible, secure repositories with zero manual configuration steps.

## 8. Tool & Dependency Requirements
- Backstage / Port, Crossplane, Terraform / OpenTofu, Kubernetes 1.28+, GitHub Actions / ArgoCD.

## 9. Implementation Guidelines & Best Practices
- Declarative Backstage software template implementing an approved Node.js microservice golden path:

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: modern-microservice-golden-path
  title: Production-Ready Microservice
  description: Scaffolds a new TypeScript microservice with GitHub Actions, Docker, Prometheus telemetry, and OWASP audit gates.
  tags:
    - nodejs
    - typescript
    - golden-path
spec:
  owner: platform-team
  type: service
  parameters:
    - title: Service Configuration
      required:
        - component_id
        - owner
      properties:
        component_id:
          title: Service Identifier
          type: string
          description: Unique slug for the microservice (e.g. billing-service)
        owner:
          title: Owning Team
          type: string
          description: GitHub team slug responsible for this service
  steps:
    - id: fetch-base
      name: Fetch Base Skeleton
      action: fetch:template
      input:
        url: ./skeleton
        values:
          component_id: ${{ parameters.component_id }}
          owner: ${{ parameters.owner }}
    - id: publish-github
      name: Publish to GitHub
      action: publish:github
      input:
        repoUrl: github.com?owner=my-org&repo=${{ parameters.component_id }}
        defaultBranch: main
        repoVisibility: private
    - id: register-catalog
      name: Register in Service Catalog
      action: catalog:register
      input:
        catalogInfoUrl: https://github.com/my-org/${{ parameters.component_id }}/blob/main/catalog-info.yaml
  output:
    links:
      - title: Repository
        url: ${{ steps['publish-github'].output.remoteUrl }}
```

## 10. Error Handling & Recovery Procedures
- Template rendering failures: Validate Jinja2/Nunjucks syntax with local validation tools before committing templates.
- Crossplane provisioning timeout: Check cloud provider IAM roles and underlying VPC subnet quotas.

## 11. Security & Privacy Constraints
- Restrict platform template access using RBAC.
- Ensure all generated golden paths enforce non-root container user execution and secret management via HashiCorp Vault or AWS Secrets Manager.

## 12. Verification & Testing Requirements
- Test scaffold template execution end-to-end in CI sandbox.
- Confirm generated `catalog-info.yaml` parses without schema warnings in the Backstage entity validator.

## 13. Completion Criteria
- Developer can provision a production-compliant service in under 5 minutes without opening an infrastructure ticket.
- Service catalog tracks ownership and health status accurately.

## 14. Relevant Official References
- Team Topologies (Skelton & Pais).
- CNCF Platform Engineering Maturity Model.
- Backstage Software Catalog & Scaffolder Specification.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with Backstage 1.30+, Crossplane 1.16+, and modern cloud Kubernetes providers.
