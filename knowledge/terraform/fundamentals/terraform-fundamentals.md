---
type: Explanation
title: Terraform fundamentals
description: Understand Terraform configuration, providers, resources, state, planning, application, and safe local practice before managing real infrastructure.
tags: [terraform, fundamentals, infrastructure-as-code, beginner]
status: draft
maturity: draft
audience: Beginning platform engineer
maintainer: unassigned
sources:
  - id: terraform-language
    resource: https://developer.hashicorp.com/terraform/language
    title: Terraform language documentation
  - id: terraform-providers
    resource: https://developer.hashicorp.com/terraform/language/providers
    title: Terraform providers
  - id: terraform-resources
    resource: https://developer.hashicorp.com/terraform/language/resources
    title: Terraform resources
  - id: terraform-state
    resource: https://developer.hashicorp.com/terraform/language/state
    title: Terraform state documentation
stale_after: 2026-12-20
---

# Terraform fundamentals

## Purpose

Understand the Terraform model before using it to manage cloud or shared infrastructure. Terraform describes desired infrastructure in configuration files, compares that declaration with its state and provider observations, then proposes changes before applying them.

## The core model

| Part | Purpose | Why it matters |
| --- | --- | --- |
| Configuration | HCL files that declare the intended infrastructure. | It is the reviewable desired state in version control. |
| Provider | A plugin that talks to a cloud, SaaS service, or other API. | Provider versions and credentials determine what Terraform can manage. |
| Resource | A managed infrastructure object declared in configuration. | Its address connects configuration, state, and a real object. |
| State | Terraform's record of resource bindings and metadata. | It lets Terraform plan changes and must be protected as potentially sensitive data. |
| Plan | A proposed change set. | Review it before any apply to confirm scope and target. |
| Apply | The action that asks providers to make the planned changes. | It can create, modify, or destroy real infrastructure. |

## The safe workflow

1. Write or review configuration and provider requirements.
2. Run `terraform init` after adding or changing providers or modules.
3. Run `terraform fmt -check` and `terraform validate`.
4. Run `terraform plan` in the intended workspace and account context.
5. Review every proposed create, change, and destroy action.
6. Apply only the reviewed plan.
7. Record outputs and verify the provider-side result.
8. Destroy disposable resources and confirm state no longer tracks them.

> [!WARNING]
> `terraform apply` and `terraform destroy` can alter real infrastructure. A passing `validate` command proves syntax and internal consistency, not that the selected account, workspace, backend, cost, or permissions are correct.

## Learn without a cloud account

Use [Terraform local state lifecycle](../examples/local-state-lifecycle/local-state-lifecycle.md). It uses the built-in `terraform_data` resource, so you can practice initialization, planning, state inspection, change review, and cleanup without cloud credentials.

## Related links

- [Core Terraform workflow](../commands/core-workflow.md)
- [Terraform state management](state-management.md)
- [Terraform local state lifecycle](../examples/local-state-lifecycle/local-state-lifecycle.md)
- [Back to Terraform fundamentals](index.md)
- [Back to Terraform index](../index.md)
- [Back to knowledge index](../../index.md)
