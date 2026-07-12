# Terraform troubleshooting

Status: Initial outline

Diagnostic workflows for Terraform failures and unexpected plans.

## Expected content

- Provider initialization failures.
- State lock failures.
- Drift investigation.
- Failed imports.
- Dependency graph surprises.

## First checks

- [ ] Confirm Terraform version.
- [ ] Confirm backend and workspace.
- [ ] Run `terraform fmt -check` and `terraform validate`.
- [ ] Inspect provider and module changes.

[Back to Terraform index](../README.md) | [Back to root index](../../README.md)
