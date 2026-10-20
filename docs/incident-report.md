# Incident Report: Deliberate Infrastructure Drift
## Summary
A controlled change was made to the Terraform-managed
S3 drift-test bucket outside the normal workflow.
## Expected state
DriftTest = expected
## Actual state
DriftTest = unexpected
## Detection
The scheduled/manual Terraform plan identified
a difference between configuration and actual AWS state.
## Remediation
The approved Terraform plan was applied to restore
the declared configuration.
## Verification
A subsequent Terraform plan showed no remaining changes.
## Lessons learned
- Console changes can create configuration drift.
- Automated detection needs explicit exit-code handling.
- Detection and remediation are separate decisions.
- The state bucket must be protected from experiments.
## Evidence
- Initial Terraform plan
- AWS Console showing the changed tag
- Terraform apply result
- Final verification plan
