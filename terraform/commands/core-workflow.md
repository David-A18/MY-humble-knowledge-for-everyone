# Core Terraform workflow

## Purpose

Document the standard command flow for making and reviewing Terraform changes.

Status: Draft
Audience: Beginning platform engineer
Page type: Reference
Maintainer: Unassigned
Last substantive review: 2026-09-18
Applicable versions: Terraform CLI 1.4.0 or newer for the linked local exercise; locally executed with Terraform v1.13.1
Validation evidence: Source reviewed, statically checked, and linked local exercise executed with Terraform v1.13.1
Known limitations: This page describes command flow; use the linked exercise for a concrete local lifecycle
Next review: After the first completed local Terraform exercise run

## Command sequence

```bash
terraform fmt -recursive
terraform init
terraform validate
terraform plan
```

Expected validation output:

```text
Success! The configuration is valid.
```

## Apply changes

```bash
terraform apply
```

> [!IMPORTANT]
> Review the plan before applying. Confirm the target workspace, backend, and account context.

What it does: applies the reviewed plan to the configured backend and provider context.

## Non-interactive validation for CI

```bash
terraform fmt -recursive -check
terraform init -backend=false
terraform validate
```

What it does: checks formatting and syntax without connecting to a remote backend.

## Local practice exercise

Use [Terraform local state lifecycle](../examples/local-state-lifecycle/README.md) to run the command flow without a cloud account.

## Related links

- [Terraform CLI documentation](https://developer.hashicorp.com/terraform/cli)
- [Terraform local state lifecycle](../examples/local-state-lifecycle/README.md)
- [Back to Terraform commands](README.md)
- [Back to Terraform index](../README.md)
- [Back to root index](../../README.md)
