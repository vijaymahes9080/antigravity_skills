---
name: cloud-security-hardening
description: Cloud security posture management (CSPM), CIS benchmarks, IAM least-privilege policies, secret management with HashiCorp Vault/AWS Secrets Manager, and infrastructure-as-code hardening.
---

# Cloud Infrastructure Security & IAM Hardening

## 1. Intended Role & Domain
- **Primary Domain**: Cybersecurity & Cloud Engineering
- **Target Roles**: Cloud Security Engineer, Infrastructure Automation Engineer, Cloud Architect
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "cloud security", "iam hardening", "least privilege aws", "cis benchmark", "secret management vault", "terraform security scan".
- **Contextual Inferences**: Infrastructure-as-code repos (Terraform, OpenTofu, CloudFormation, Pulumi), multi-cloud IAM policy reviews.
- **Chained Predecessors**: `secure-coding-review`, `task-decomposition`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Performing application-level UI design or client-side frontend styling.
  - Local SQLite database tasks with no cloud infrastructure.

## 4. Required Inputs & Context
- Infrastructure-as-Code (IaC) manifests (`.tf`, `.yaml`, `.json`).
- Target cloud provider (AWS, Azure, GCP, Kubernetes).
- Cloud compliance frameworks (CIS Cloud Benchmarks, NIST CSF).

## 5. Expected Outputs & Artifacts
- Least-privilege IAM policies without wildcards (`*`).
- Hardened IaC templates with mandatory encryption at rest (KMS) and in transit.
- Security scan report via Checkov, tfsec, or Trivy.
- Automated secret rotation architecture.

## 6. Step-by-Step Operating Procedure
1. **IaC Static Security Analysis**:
   - Run Checkov or Trivy across Terraform / Kubernetes files to identify misconfigurations.
2. **IAM Policy Auditing & Least Privilege**:
   - Replace open `Action: "*"` and `Resource: "*"` statements with granular actions (`s3:GetObject`, `s3:PutObject`) scoped to specific ARNs.
3. **Storage & Database Encryption**:
   - Enforce customer-managed keys (CMK) via KMS for all storage buckets and database volumes.
   - Block public access on S3/blob buckets (`block_public_acls = true`).
4. **Network Segmentation & Security Groups**:
   - Audit security group ingress rules: eliminate `0.0.0.0/0` on management ports (SSH 22, RDP 3389).
5. **Secret Management Integration**:
   - Eliminate static API keys in environment variables; integrate HashiCorp Vault or Cloud Secrets Manager with dynamic token rotation.

## 7. Repository Inspection & Planning Requirements
- Non-destructive IaC scanner execution:
  ```bash
  checkov -d . --framework terraform 2>/dev/null || trivy config . 2>/dev/null || echo "Run manual IaC audit"
  ```
- Preservation rule: Never revoke production IAM permissions without validating active usage in CloudTrail to avoid service disruption.

## 8. Tool & Dependency Requirements
- Terraform / OpenTofu CLI, Checkov / tfsec / Trivy, AWS CLI / GCP gcloud CLI.

## 9. Implementation Guidelines & Best Practices
- Never allow public egress from private database subnets.
- Use IAM Roles and Service Accounts (IRSA / Workload Identity) rather than long-lived access key pairs:
  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "AllowSpecificS3BucketReadWrite",
        "Effect": "Allow",
        "Action": [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        "Resource": [
          "arn:aws:s3:::production-app-assets-2026",
          "arn:aws:s3:::production-app-assets-2026/*"
        ]
      }
    ]
  }
  ```

## 10. Error Handling & Recovery Procedures
- `AccessDeniedException` during policy tightening: Use CloudTrail event logs to identify the exact missing API call and add it surgically to the policy.

## 11. Security & Privacy Constraints
- Never commit AWS credentials, `.aws/credentials`, or terraform state files containing plaintext secrets to git.

## 12. Verification & Testing Requirements
- Execute IaC linter and security validator:
  ```bash
  terraform validate
  trivy config ./terraform/
  ```

## 13. Completion Criteria
- Zero critical or high severity misconfigurations in IaC templates.
- All S3 buckets block public access and require TLS encryption (`aws:SecureTransport`).
- IAM policies pass least-privilege verification.

## 14. Relevant Official References
- CIS AWS / Azure / GCP Foundations Benchmarks.
- AWS Well-Architected Framework: Security Pillar.
- HashiCorp Vault Security Model.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with Terraform 1.9+, OpenTofu 1.8+, and CIS Benchmark v3.0.
