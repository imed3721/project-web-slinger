# Web-Slinger Operational Runbook
## 1. CI tests fail
1. Open GitHub Actions.
2. Select the failed workflow run.
3. Open the failed step.
4. Read the first meaningful error.
5. Correct the source or test.
6. Rerun the checks.
## 2. AWS OIDC authentication fails
1. Check the AWS role ARN in GitHub variables.
2. Check the IAM OIDC provider.
3. Check the role's trust policy.
4. Verify repository and branch conditions.
5. Check that the workflow has id-token: write.
Never solve an authentication failure by adding
permanent AWS access keys to the repository.
## 3. ECR publishing fails
1. Check the ECR repository name and Region.
2. Check the image-publishing role permissions.
3. Check whether the image tag already exists.
4. Inspect the failing Docker push step.
## 4. Kubernetes deployment fails
1. Inspect the Deployment and pod status.
2. Read container logs.
3. Check image availability.
4. Check the port and health probes.
5. Correct the underlying issue and rerun the test.
## 5. Terraform detects drift
1. Inspect the proposed plan.
2. Identify the out-of-band change.
3. Decide whether the change is authorised.
4. Restore the intended configuration through
an approved process.
5. Run another plan to verify the result.
## 6. Terraform state problems
1. Stop concurrent infrastructure changes.
2. Inspect the error and S3 object history.
3. Verify backend configuration and IAM access.
4. Recover only through a documented procedure.
5. Never delete the state bucket to fix a plan error.
