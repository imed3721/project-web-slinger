# Web-Slinger: Secure DevOps & Infrastructure Automation

[![CI](https://img.shields.io/badge/CI-GitHub_Actions-blue?logo=githubactions&logoColor=white)](../../actions)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform&logoColor=white)](https://developer.hashicorp.com/terraform)
[![Kubernetes](https://img.shields.io/badge/Orchestration-Kubernetes-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![AWS](https://img.shields.io/badge/Cloud-AWS-232F3E?logo=amazonaws&logoColor=white)](https://aws.amazon.com/)

**Web-Slinger** is a hands-on DevOps project exploring secure software delivery, infrastructure as code, Kubernetes deployment verification, and infrastructure drift detection.

The project brings application code, automated workflows, container security checks, Kubernetes manifests, Terraform configuration, and execution evidence together in one GitHub repository.

**Repository:** [imed3721/project-web-slinger](https://github.com/imed3721/project-web-slinger)

## Contents

- [Project objectives](#project-objectives)
- [Technology stack](#technology-stack)
- [Repository structure](#repository-structure)
- [CI/CD and infrastructure workflows](#cicd-and-infrastructure-workflows)
- [Workflow evidence](#workflow-evidence)
- [Security and operational considerations](#security-and-operational-considerations)
- [Architecture](#architecture)
- [Learning outcomes](#learning-outcomes)
- [Future improvements](#future-improvements)

## Project objectives

- Automate application checks through continuous integration (CI).
- Package the Python application as a Docker image.
- Scan container images for known vulnerabilities before publication.
- Authenticate GitHub Actions to AWS using OpenID Connect (OIDC).
- Publish versioned container images to Amazon Elastic Container Registry (ECR).
- Deploy Kubernetes manifests to a temporary test cluster and verify rollout health.
- Introduce, detect, and repair deliberate Kubernetes configuration drift.
- Manage AWS infrastructure with Terraform and remote state stored in Amazon S3.
- Detect infrastructure drift and verify recovery through Terraform plans.
- Capture workflow logs, screenshots, and artifacts to document implementation and testing.

## Technology stack

| Technology | Role in the project |
|---|---|
| Python | Application runtime |
| Docker | Container image construction |
| GitHub Actions | CI/CD automation and workflow orchestration |
| Trivy | Container vulnerability scanning |
| AWS IAM and OIDC | Federated authentication and access control |
| Amazon ECR | Container image registry |
| Terraform | Infrastructure as code and drift detection |
| Amazon S3 | Remote Terraform state storage |
| Kubernetes | Deployment, health checks, and desired-state management |
| kind | Temporary Kubernetes cluster for automated tests |
| Bash and kubectl | Test automation and Kubernetes verification |
| GitHub Actions artifacts | Retention of selected workflow evidence |

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
├── screenshots/
├── .github/
│   └── workflows/
│       ├── CI workflow
│       ├── Terraform workflows
│       ├── release.yml
│       └── terraform-destroy.yml
└── README.md
```

*The structure above highlights the main project components. Workflow filenames and Terraform files should reflect the actual files present in the repository.*

## CI/CD and infrastructure workflows

### 1. Continuous integration — CI Test

The CI workflow automates the configured application and configuration checks when its trigger conditions are met.

**Objective:** Identify errors early and provide repeatable evidence that checks have run.

**Evidence:** See [CI Test](#ci-test).

### 2. Infrastructure as code — Terraform

Terraform defines the AWS resources managed by the project and provides a repeatable way to plan and apply infrastructure changes.

The project uses an Amazon S3 backend for remote Terraform state and separates code validation from AWS-backed operations.

The intended security model is:

- **Pull requests:** Run formatting and configuration checks without AWS credentials.
- **Trusted branch:** Authenticate through OIDC and generate an infrastructure plan.
- **Protected environment:** Require review and approval before sensitive changes are applied.

Terraform plans can reveal configuration differences and proposed infrastructure changes. They should be reviewed before application.

**Evidence:** See [Terraform Infrastructure](#terraform-infrastructure).

### 3. Secure container release — Web-Slinger Release and Kubernetes Test

The release workflow combines container construction, vulnerability scanning, image publication, and Kubernetes verification.

The intended release sequence is:

1. Build the Docker image on the GitHub Actions runner.
2. Scan the image using Trivy.
3. Apply the configured vulnerability policy.
4. Publish an approved image to Amazon ECR.
5. Record the source commit, image tag, and image digest.
6. Load the scanned image into the temporary Kubernetes test cluster.
7. Verify deployment readiness and exercise Kubernetes drift recovery.

The example policy blocks releases when fixable HIGH or CRITICAL vulnerabilities are found. Unfixed findings and exceptions still require review and a documented remediation or acceptance decision.

**Evidence:** See [Web-Slinger Release and Kubernetes Test](#web-slinger-release-and-kubernetes-test).

### 4. Kubernetes deployment verification

The Kubernetes manifests define the application's namespace, Deployment, and Service.

The release workflow checks that:

- The Deployment rollout completes successfully.
- The expected two replicas become ready.
- Configured readiness and liveness probes are present and used by Kubernetes.
- The test environment can detect and recover from a deliberate replica-count change.

**Environment boundary:** The release workflow uses a temporary kind cluster on the GitHub Actions runner. This demonstrates deployment and recovery behaviour; it does not establish a persistent production deployment on Amazon EKS.

### 5. Kubernetes drift detection and recovery

The Kubernetes drift test deliberately changes the Deployment's replica count from the declared value.

The test then uses `kubectl diff` to detect the difference, reapplies the desired manifest, waits for rollout completion, and verifies that the declared replica count has been restored.

This demonstrates the relationship between the desired configuration in Git and the live configuration in Kubernetes.

**Evidence:** See [Test Kubernetes drift](#test-kubernetes-drift).

### 6. AWS infrastructure drift detection

The Terraform drift workflow checks for differences between the declared configuration and the infrastructure represented by Terraform state and provider observations.

The controlled exercise changes a managed test resource's tag from its expected value. Terraform planning should identify the difference. The recovery workflow can apply the reviewed plan and verify that no further changes are reported.

Scheduled detection should report discrepancies rather than automatically changing infrastructure unless automatic remediation has been deliberately designed, reviewed, and authorised.

**Evidence:** See [AWS infrastructure drift](#aws-infrastructure-drift).

### 7. Controlled Terraform destruction

The separate Terraform destroy workflow is manually triggered. It generates a destruction plan, stores a short-lived plan artifact for review, and uses a protected GitHub environment before applying the saved plan.

Destroy operations are potentially irreversible. Review every proposed deletion, confirm the resources are safe to remove, and ensure important data and Terraform state are protected before approving the operation.

## Workflow evidence

The screenshots below document selected GitHub Actions executions for the project's CI, infrastructure, release, and drift-testing workflows.

The screenshots are retained in the repository's `screenshots/` directory. The links below point to specific repository revisions so the evidence remains traceable to the version captured.

### CI Test

![CI Test workflow execution](https://github.com/imed3721/project-web-slinger/blob/4e81b682a5b5abf85a1a32fee17cb94f2814dc71/screenshots/Screenshot%202026-10-19%20204139.png)

![CI Test workflow checks](https://github.com/imed3721/project-web-slinger/blob/4e81b682a5b5abf85a1a32fee17cb94f2814dc71/screenshots/Screenshot%202026-10-19%20204153.png)

*Evidence of the CI workflow execution and the checks visible in the captured run.*

### Terraform Infrastructure

![Terraform infrastructure workflow](https://github.com/imed3721/project-web-slinger/blob/3eee9af07f45979f011cefe11452f757bcd0f5b1/screenshots/Screenshot%202026-10-19%20212749.png)

![Terraform validation evidence](https://github.com/imed3721/project-web-slinger/blob/3eee9af07f45979f011cefe11452f757bcd0f5b1/screenshots/Screenshot%202026-10-19%20212808.png)

![Terraform plan evidence](https://github.com/imed3721/project-web-slinger/blob/3eee9af07f45979f011cefe11452f757bcd0f5b1/screenshots/Screenshot%202026-10-19%20212814.png)

*Evidence of Terraform workflow execution and the configuration or planning results visible in the screenshots.*

### Web-Slinger Release and Kubernetes Test

![Container release workflow](https://github.com/imed3721/project-web-slinger/blob/03e3f39fa917b8aad51e6a5ffdbab6c13217dc71/screenshots/Screenshot%202026-10-19%20at%2023.14.09.png)

![Container build and scan evidence](https://github.com/imed3721/project-web-slinger/blob/03e3f39fa917b8aad51e6a5ffdbab6c13217dc71/screenshots/Screenshot%202026-10-19%20at%2023.14.19.png)

![Container publication evidence](https://github.com/imed3721/project-web-slinger/blob/03e3f39fa917b8aad51e6a5ffdbab6c13217dc71/screenshots/Screenshot%202026-10-19%20at%2023.14.25.png)

![Kubernetes test workflow](https://github.com/imed3721/project-web-slinger/blob/03e3f39fa917b8aad51e6a5ffdbab6c13217dc71/screenshots/Screenshot%202026-10-19%20at%2023.14.32.png)

![Kubernetes deployment evidence](https://github.com/imed3721/project-web-slinger/blob/03e3f39fa917b8aad51e6a5ffdbab6c13217dc71/screenshots/Screenshot%202026-10-19%20at%2023.14.40.png)

![Kubernetes readiness verification](https://github.com/imed3721/project-web-slinger/blob/03e3f39fa917b8aad51e6a5ffdbab6c13217dc71/screenshots/Screenshot%202026-10-19%20at%2023.14.45.png)

![Release test execution](https://github.com/imed3721/project-web-slinger/blob/03e3f39fa917b8aad51e6a5ffdbab6c13217dc71/screenshots/Screenshot%202026-10-19%20at%2023.17.29.png)

![Release workflow result](https://github.com/imed3721/project-web-slinger/blob/03e3f39fa917b8aad51e6a5ffdbab6c13217dc71/screenshots/Screenshot%202026-10-19%20at%2023.19.50.png)

*Evidence of the release workflow stages and results visible in the recorded executions.*

### Test Kubernetes drift

![Kubernetes drift test setup](https://github.com/imed3721/project-web-slinger/blob/d567c4abaf59600bdb27f872657e3a5d1631ec44/screenshots/Screenshot%202026-10-19%20at%2023.34.51.png)

![Kubernetes drift detection](https://github.com/imed3721/project-web-slinger/blob/d567c4abaf59600bdb27f872657e3a5d1631ec44/screenshots/Screenshot%202026-10-19%20at%2023.35.04.png)

![Kubernetes configuration difference](https://github.com/imed3721/project-web-slinger/blob/d567c4abaf59600bdb27f872657e3a5d1631ec44/screenshots/Screenshot%202026-10-19%20at%2023.36.34.png)

![Kubernetes drift recovery](https://github.com/imed3721/project-web-slinger/blob/d567c4abaf59600bdb27f872657e3a5d1631ec44/screenshots/Screenshot%202026-10-19%20at%2023.36.42.png)

![Kubernetes restored configuration](https://github.com/imed3721/project-web-slinger/blob/d567c4abaf59600bdb27f872657e3a5d1631ec44/screenshots/Screenshot%202026-10-19%20at%2023.36.50.png)

*Evidence of the Kubernetes drift test and the results captured during recovery.*

### AWS infrastructure drift

![AWS infrastructure drift workflow](https://github.com/imed3721/project-web-slinger/blob/3f829b74181d5ed5cfe565077872479b9e61212d/screenshots/Screenshot%202026-10-19%20at%2023.42.14.png)

![Terraform drift detection](https://github.com/imed3721/project-web-slinger/blob/3f829b74181d5ed5cfe565077872479b9e61212d/screenshots/Screenshot%202026-10-19%20at%2023.42.38.png)

![Terraform infrastructure change](https://github.com/imed3721/project-web-slinger/blob/3f829b74181d5ed5cfe565077872479b9e61212d/screenshots/Screenshot%202026-10-19%20at%2023.57.44.png)

![Terraform drift plan](https://github.com/imed3721/project-web-slinger/blob/3f829b74181d5ed5cfe565077872479b9e61212d/screenshots/Screenshot%202026-10-19%20at%2023.57.53.png)

![Terraform drift verification](https://github.com/imed3721/project-web-slinger/blob/3f829b74181d5ed5cfe565077872479b9e61212d/screenshots/Screenshot%202026-10-19%20at%2023.58.01.png)

![Terraform recovery workflow](https://github.com/imed3721/project-web-slinger/blob/3f829b74181d5ed5cfe565077872479b9e61212d/screenshots/Screenshot%202026-10-19%20at%2023.58.10.png)

![Terraform infrastructure verification](https://github.com/imed3721/project-web-slinger/blob/3f829b74181d5ed5cfe565077872479b9e61212d/screenshots/Screenshot%202026-10-19%20at%2023.58.38.png)

![Terraform workflow result](https://github.com/imed3721/project-web-slinger/blob/3f829b74181d5ed5cfe565077872479b9e61212d/screenshots/Screenshot%202026-10-19%20at%2023.58.52.png)

![Final infrastructure drift evidence](https://github.com/imed3721/project-web-slinger/blob/3f829b74181d5ed5cfe565077872479b9e61212d/screenshots/Screenshot%202026-10-19%20at%2023.59.26.png)

![Final Terraform verification](https://github.com/imed3721/project-web-slinger/blob/3f829b74181d5ed5cfe565077872479b9e61212d/screenshots/Screenshot%202026-10-20%20at%2000.02.32.png)

![Terraform recovery confirmation](https://github.com/imed3721/project-web-slinger/blob/3f829b74181d5ed5cfe565077872479b9e61212d/screenshots/Screenshot%202026-10-20%20at%2000.02.38.png)

![Infrastructure drift test result](https://github.com/imed3721/project-web-slinger/blob/3f829b74181d5ed5cfe565077872479b9e61212d/screenshots/Screenshot%202026-10-20%20at%2000.02.49.png)

![Terraform final state check](https://github.com/imed3721/project-web-slinger/blob/3f829b74181d5ed5cfe565077872479b9e61212d/screenshots/Screenshot%202026-10-20%20at%2000.02.58.png)

![Infrastructure verification result](https://github.com/imed3721/project-web-slinger/blob/3f829b74181d5ed5cfe565077872479b9e61212d/screenshots/Screenshot%202026-10-20%20at%2000.03.05.png)

*Evidence of the controlled Terraform drift exercise, planning output, and verification steps captured in the workflow runs.*

## Security and operational considerations

- **Federated authentication:** Use GitHub OIDC and temporary credentials instead of long-lived AWS access keys.
- **Least privilege:** Scope IAM permissions to the specific resources and operations required by each workflow.
- **Trusted execution:** Keep AWS-backed Terraform operations away from untrusted pull-request contexts.
- **Review and approval:** Protect the main branch and require review before sensitive infrastructure changes.
- **Destructive operations:** Require explicit approval and careful inspection of Terraform destruction plans.
- **Container security:** Run vulnerability scans before publishing and document remediation or exception decisions.
- **Traceability:** Use unique image tags and record image digests and source commits.
- **State protection:** Restrict access to Terraform state, plans, and workflow artifacts.
- **Secret management:** Never commit credentials, access tokens, or sensitive state files to the repository.

A passing workflow confirms only that its configured checks passed. It does not guarantee that the application or infrastructure is completely secure.

## Architecture

The architecture diagram explains the relationship between CI, container scanning and publication, Kubernetes verification, Terraform operations, and evidence collection.

See [docs/architecture.md](docs/architecture.md).

## Learning outcomes

Web-Slinger provides practical experience with:

- CI/CD workflow development and troubleshooting.
- Docker image building and vulnerability scanning.
- AWS IAM, OIDC federation, and permission scoping.
- Amazon ECR image publication and provenance tracking.
- Kubernetes manifests, probes, replica verification, and drift recovery.
- Terraform state management, planning, drift detection, and controlled destruction.
- Automated evidence collection and technical documentation.

## Future improvements

Potential next steps include:

- Pin third-party GitHub Actions to verified full commit SHAs.
- Add Python unit tests, coverage reporting, and dependency checks.
- Retain machine-readable Trivy reports and generate a software bill of materials (SBOM).
- Document vulnerability exceptions, remediation ownership, and review dates.
- Add policy checks for Terraform plans before approval.
- Improve evidence organisation with concise captions and direct workflow-run links.
- Introduce a persistent deployment environment only if needed, with separate permissions and approval controls.

---

**Maintainer:** [imed3721](https://github.com/imed3721)

**Project:** Web-Slinger — Secure DevOps, Infrastructure as Code, and Kubernetes verification.
