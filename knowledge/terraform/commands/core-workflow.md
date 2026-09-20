---
type: "How-to Guide"
title: "Core Terraform workflow"
description: "Document the standard command flow for making and reviewing Terraform changes."
tags: [terraform, core-workflow]
status: stable
maturity: maintained
audience: "Beginning platform engineer"
maintainer: "Unassigned"
---

# Core Terraform workflow

## Purpose

Document the standard command flow for making and reviewing Terraform changes.

Status: Maintained
Audience: Beginning platform engineer
Page type: Reference
Maintainer: Unassigned
Last substantive review: 2026-09-19
Applicable versions: Terraform CLI v1.16 documentation; linked local exercise executed with Terraform v1.13.1
Validation evidence: Source reviewed against official Terraform init, plan, and apply documentation; linked local exercise executed with Terraform v1.13.1
Known limitations: This page describes command flow; provider-specific backend, credential, and policy behavior still require environment runbooks
Next review: 2026-12-19 or after a relevant Terraform CLI workflow change

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

Use [Terraform local state lifecycle](../examples/local-state-lifecycle/index.md) to run the command flow without a cloud account.

## Related links

- [Terraform CLI documentation](https://developer.hashicorp.com/terraform/cli)
- [Terraform local state lifecycle](../examples/local-state-lifecycle/index.md)
- [Back to Terraform commands](index.md)
- [Back to Terraform index](../index.md)
- [Back to root index](../../../README.md)
