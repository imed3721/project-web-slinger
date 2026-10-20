# Web-Slinger Threat Model
## Assets
- AWS account and IAM roles
- Terraform state in S3
- Container images in ECR
- GitHub source code and workflow definitions
- Deployment evidence
## Threats and mitigations
### Stolen AWS credentials
Mitigation: Use GitHub OIDC and temporary credentials.
### Untrusted workflow
Mitigation: Restrict OIDC trust to the intended repository
and protected branch. Minimise workflow permissions.
### Overwritten container image
Mitigation: Use immutable ECR tags and Git commit identifiers.
### Vulnerable container image
Mitigation: Scan images before release and define a
vulnerability policy.
### Infrastructure drift
Mitigation: Run Terraform plans on a schedule and test
drift detection deliberately.
### Lost Terraform state
Mitigation: Enable S3 versioning and state locking.
Document recovery procedures.
### Unexpected AWS spending
Mitigation: Minimise resources, configure billing alerts,
inspect billing, and document cleanup steps.
## Remaining risks
- A compromised trusted workflow could still misuse its role.
- A temporary Kubernetes test does not prove EKS compatibility.
- Billing alerts do not guarantee a hard spending limit.
- Vulnerability scanners cannot detect every vulnerability.
