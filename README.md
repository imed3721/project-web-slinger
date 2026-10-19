# Web-Slinger: Secure DevOps and Infrastructure Automation

[![CI Test](https://img.shields.io/badge/CI-GitHub_Actions-blue)](../../actions)
[![Container](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Infrastructure](https://img.shields.io/badge/Infrastructure-Terraform-7B42BC?logo=terraform&logoColor=white)](https://developer.hashicorp.com/terraform)
[![Orchestration](https://img.shields.io/badge/Orchestration-Kubernetes-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)

Web-Slinger is a DevOps learning project demonstrating automated testing, secure container delivery, infrastructure as code, Kubernetes deployment verification, and infrastructure drift detection using GitHub Actions and AWS.

The project brings application code, infrastructure configuration, Kubernetes manifests, automated workflows, and test evidence together in one repository.

**Repository:** [imed3721/project-web-slinger](https://github.com/imed3721/project-web-slinger)

## Project objectives

- Automate application checks through continuous integration (CI).
- Package the Python application as a Docker image.
- Scan container images for known vulnerabilities before publishing.
- Authenticate GitHub Actions to AWS using OpenID Connect (OIDC).
- Publish versioned container images to Amazon Elastic Container Registry (ECR).
- Deploy Kubernetes manifests to a temporary test cluster and verify application readiness.
- Introduce and repair deliberate Kubernetes configuration drift.
- Manage AWS infrastructure using Terraform and an S3 remote state backend.
- Detect Terraform infrastructure drift and verify recovery.
- Provide documented evidence of successful workflow executions.

## Technology stack

| Technology | Purpose |
|---|---|
| Python | Application runtime |
| Docker | Container image build and packaging |
| GitHub Actions | Automated CI/CD workflows |
| Trivy | Container vulnerability scanning |
| AWS IAM and OIDC | Short-lived AWS authentication for workflows |
| Amazon ECR | Container image registry |
| Terraform | Infrastructure as code and drift detection |
| Amazon S3 | Remote Terraform state storage |
| Kubernetes | Application deployment and health verification |
| kind | Temporary Kubernetes cluster for automated tests |
| Bash and kubectl | Automated drift testing and cluster verification |
| GitHub Actions artifacts | Retention of workflow evidence |

## Repository structure

```text
project-web-slinger/
├── app/
│   ├── app.py
│   └── Dockerfile
├── docs/
│   ├── architecture.md
│   └── images/
├── infra/
│   └── Terraform configuration
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   └── service.yaml
├── scripts/
│   └── drift-test.sh
├── .github/
│   └── workflows/
│       ├── CI workflow
│       ├── Terraform workflows
│       ├── release.yml
│       └── terraform-destroy.yml
└── README.md
```

*This is a logical overview; adjust the listed workflow names and files to match the repository's actual contents.*

## Continuous integration and delivery

### 1. CI Test

The CI workflow checks the application and its configuration automatically when its configured trigger conditions are met.

**Purpose:** Catch errors early and provide repeatable evidence that automated checks have run.

**Evidence:** See [CI Test evidence](#workflow-evidence).

### 2. Terraform Infrastructure

Terraform defines and manages AWS resources as code. The project uses an S3 backend to store Terraform state remotely and supports automated formatting, validation, planning, and controlled application of infrastructure changes.

The intended workflow separates unprivileged code checks from AWS-backed operations:

- Pull requests: formatting and configuration validation without AWS credentials.
- Trusted branch: AWS authentication through OIDC and Terraform planning.
- Protected environment: approval before applying infrastructure changes.

### 3. Secure container release

The release workflow is designed to:

1. Build a Docker image on the GitHub Actions runner.
2. Scan the image with Trivy.
3. Enforce a vulnerability policy.
4. Publish an approved image to Amazon ECR.
5. Record the source commit, image tag, and image digest.
6. Deploy the scanned image to a temporary Kubernetes test cluster.
7. Verify rollout readiness and run drift-recovery tests.

The configured example policy blocks releases for fixable HIGH and CRITICAL vulnerabilities. Unfixed vulnerabilities and approved exceptions should still be reviewed and documented.

### 4. Kubernetes deployment verification

Kubernetes manifests describe the application's namespace, Deployment, and Service.

The automated test verifies that:

- The Deployment rolls out successfully.
- Two replicas are desired and ready.
- The application passes its configured readiness and liveness probes.
- The cluster can recover from a deliberate replica-count change.

**Important:** The release workflow uses a temporary kind cluster on the GitHub Actions runner. It verifies deployment behaviour but does not, by itself, establish a persistent production deployment on Amazon EKS.

### 5. Kubernetes drift detection

The drift test deliberately scales the Deployment away from its declared replica count, uses `kubectl diff` to detect the discrepancy, reapplies the Kubernetes manifest, and checks that the desired replica count is restored.

This demonstrates the difference between the desired configuration stored in Git and the live configuration running in Kubernetes.

### 6. AWS infrastructure drift

The Terraform drift workflow compares the declared infrastructure configuration with the state and infrastructure observed by Terraform.

For the controlled drift exercise, a managed test resource's tag is changed from its expected value. Terraform planning should identify the difference, and the manual recovery workflow can apply the reviewed plan and verify that no further changes are reported.

Scheduled detection should report drift without automatically applying changes unless that behaviour has been explicitly designed and approved.

### 7. Controlled Terraform destruction

The separate Terraform destroy workflow is manually triggered. It generates a destruction plan, publishes a short-lived review artifact, and uses a protected GitHub environment before applying the saved plan.

This is a destructive operation. Review every planned deletion and confirm that resources and data are safe to remove before approving it.

## Workflow evidence

Screenshots of successful GitHub Actions executions provide visual evidence of the project's automated checks and infrastructure tests.

Save the screenshots in `docs/images/` and update the filenames below to match the files you upload.

### CI Test

![CI Test workflow evidence](docs/images/ci-test.png)

*Evidence of the CI Test workflow and its completed checks.*

### Terraform Infrastructure

![Terraform Infrastructure workflow evidence](docs/images/terraform-infrastructure.png)

*Evidence of Terraform formatting, validation, planning, or infrastructure workflow execution, as shown in the screenshot.*

### Web-Slinger Release and Kubernetes Test

![Web-Slinger release workflow evidence](docs/images/web-slinger-release.png)

*Evidence of the container release, vulnerability scan, image publication, and Kubernetes verification steps that are visible in the run.*

### Test Kubernetes drift

![Kubernetes drift test evidence](docs/images/kubernetes-drift.png)

*Evidence of detecting the deliberate replica-count difference and restoring the declared Kubernetes configuration.*

### AWS infrastructure drift

![AWS infrastructure drift evidence](docs/images/aws-infrastructure-drift.png)

*Evidence of Terraform identifying the controlled infrastructure change and, where shown, successful recovery.*

## Security considerations

- Use GitHub OIDC rather than long-lived AWS access keys.
- Apply least-privilege IAM permissions to each workflow role.
- Keep AWS-backed Terraform operations away from untrusted pull requests.
- Protect the main branch and require review of infrastructure changes.
- Require environment approval before destructive or sensitive operations.
- Scan images before publication and review security findings.
- Use immutable image tags and record image digests for traceability.
- Protect Terraform state and review changes before applying them.
- Never commit credentials, secret values, or sensitive state files to Git.

A successful workflow indicates that its configured checks passed; it is not a guarantee that the application or infrastructure is completely secure.

## Architecture

See [docs/architecture.md](docs/architecture.md) for the Mermaid architecture diagram and an explanation of the application, release, infrastructure, and drift-detection flows.

## Learning outcomes

This project demonstrates practical DevOps skills in:

- CI/CD workflow design and debugging.
- Docker image construction and vulnerability scanning.
- AWS IAM, OIDC federation, and least-privilege permissions.
- Container registry publishing and artifact traceability.
- Kubernetes deployment, probes, replica verification, and drift recovery.
- Terraform state management, planning, drift detection, and controlled destruction.
- Automated evidence collection and technical documentation.

## Future improvements

- Pin third-party GitHub Actions to verified full commit SHAs.
- Add automated Python unit tests and coverage reporting where appropriate.
- Retain machine-readable vulnerability scan reports and a software bill of materials (SBOM).
- Document the vulnerability exception and remediation process.
- Add stronger policy checks for Terraform plans.
- Introduce a persistent deployment environment only when required, with separate access controls and approval gates.

---

**Maintainer:** [imed3721](https://github.com/imed3721)

**Project:** Web-Slinger — DevOps, Infrastructure as Code, and Kubernetes learning project.
