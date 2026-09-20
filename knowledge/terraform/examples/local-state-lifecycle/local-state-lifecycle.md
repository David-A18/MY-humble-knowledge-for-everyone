---
type: Tutorial
title: Terraform local state lifecycle
description: Learn Terraform initialization, validation, planning, local state inspection, change review, and cleanup without a cloud account.
tags: [terraform, tutorial, state, beginner]
status: draft
maturity: draft
audience: Beginning platform engineer
maintainer: unassigned
sources:
  - id: terraform-cli
    resource: https://developer.hashicorp.com/terraform/cli
    title: Terraform CLI documentation
  - id: terraform-state
    resource: https://developer.hashicorp.com/terraform/language/state
    title: Terraform state documentation
stale_after: 2026-12-19
---

# Terraform local state lifecycle

## Goal

Learn Terraform's local workflow by initializing a small configuration, validating it, creating local state, changing an input, reviewing the plan, applying the change, inspecting state, and destroying the managed object.

This exercise does not require a cloud account. It uses Terraform's built-in `terraform_data` resource, which stores data in Terraform state without creating external infrastructure.

## Prerequisites

- Terraform 1.4.0 or newer.
- Git and a terminal.
- A disposable local directory.

This tutorial was previously executed with Terraform v1.13.1. It remains `draft` until a maintainer records a new structured verification entry.

## Files

| File | Purpose |
| --- | --- |
| [main.tf](main.tf) | Defines variables, local values, a `terraform_data` resource, and outputs. |
| [.gitignore](.gitignore) | Keeps local state, cache, plans, and override files out of Git. |

## Prepare an isolated copy

From the repository root:

```bash
mkdir -p /tmp/kb-terraform-local
cp knowledge/terraform/examples/local-state-lifecycle/main.tf /tmp/kb-terraform-local/
cp knowledge/terraform/examples/local-state-lifecycle/.gitignore /tmp/kb-terraform-local/
cd /tmp/kb-terraform-local
git init
git add .
git commit -m "add terraform local state exercise"
```

What it does: creates a disposable working directory so Terraform state and cache files do not appear in the knowledge-base checkout.

## Initialize and validate

```bash
terraform version
terraform init
terraform fmt -check
terraform validate
```

What it does: records the Terraform version, initializes the working directory, checks formatting, and validates the configuration.

Expected validation output:

```text
Success! The configuration is valid.
```

## Review the first plan

```bash
terraform plan -out=tfplan
```

What it does: shows that Terraform will create one `terraform_data.release` object in local state and stores the plan in `tfplan`.

Expected condition: the plan says `1 to add, 0 to change, 0 to destroy`.

## Apply and inspect state

```bash
terraform apply tfplan
terraform output
terraform state list
terraform state show terraform_data.release
```

What it does: applies the saved plan, displays output values, lists tracked state addresses, and shows the stored object.

Expected condition: `terraform_data.release` appears in state.

## Make a deliberate change

```bash
terraform plan -var='release_version=1.1.0'
terraform apply -var='release_version=1.1.0'
terraform output release_summary
```

What it does: changes only the input value recorded in state, then applies and inspects the updated output.

Expected condition: the plan shows `terraform_data.release` changing in place and the output includes `version = "1.1.0"`.

## Clean up

> [!WARNING]
> `terraform destroy` removes objects tracked by this exercise's state. This exercise is local-only, but the same command can delete real infrastructure in other Terraform projects.

```bash
terraform destroy
terraform state list
```

What it does: removes the local `terraform_data.release` object from state, then confirms no managed objects remain.

Expected condition: `terraform state list` prints no managed resources.

## State files to notice

| File or directory | Meaning | Git handling |
| --- | --- | --- |
| `.terraform/` | Local plugin and module working directory. | Ignored. |
| `terraform.tfstate` | Local state file for this exercise. | Ignored because state can contain sensitive values in real projects. |
| `terraform.tfstate.backup` | Previous local state snapshot. | Ignored. |
| `tfplan` | Saved plan artifact. | Ignored because plans can include sensitive data. |

## Understanding checks

- Which command created the local state file?
- Which command showed the exact address `terraform_data.release`?
- Why is state ignored even though this exercise has no secrets?
- What does the plan report before apply, after the version change, and after destroy?

## Related links

- [Start here](../../../start-here.md)
- [Core Terraform workflow](../../commands/core-workflow.md)
- [State management](../../fundamentals/state-management.md)
- [Back to Terraform local state lifecycle](index.md)
- [Back to Terraform examples](../index.md)
- [Back to Terraform index](../../index.md)
- [Back to knowledge index](../../../index.md)
