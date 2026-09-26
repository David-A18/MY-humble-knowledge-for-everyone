---
type: "How-to Guide"
title: "Core Terraform workflow"
description: "Document the standard command flow for making and reviewing Terraform changes."
tags: [terraform, core-workflow]
status: stable
maturity: maintained
audience: "Beginning platform engineer"
maintainer: unassigned
sources:
  - id: terraform-cli
    resource: https://developer.hashicorp.com/terraform/cli
    title: Terraform CLI documentation
  - id: terraform-fmt
    resource: https://developer.hashicorp.com/terraform/cli/commands/fmt
    title: terraform fmt reference
  - id: terraform-init
    resource: https://developer.hashicorp.com/terraform/cli/commands/init
    title: terraform init reference
  - id: terraform-validate
    resource: https://developer.hashicorp.com/terraform/cli/commands/validate
    title: terraform validate reference
  - id: terraform-plan
    resource: https://developer.hashicorp.com/terraform/cli/commands/plan
    title: terraform plan reference
  - id: terraform-apply
    resource: https://developer.hashicorp.com/terraform/cli/commands/apply
    title: terraform apply reference
  - id: terraform-providers-lock
    resource: https://developer.hashicorp.com/terraform/cli/commands/providers/lock
    title: terraform providers lock reference
  - id: terraform-dependency-lock
    resource: https://developer.hashicorp.com/terraform/language/files/dependency-lock
    title: Terraform dependency lock file documentation
stale_after: 2026-12-21
---

# Core Terraform workflow

## Purpose

Document the standard command flow for making and reviewing Terraform changes.

Status: Maintained
Audience: Beginning platform engineer
Page type: Reference
Maintainer: Unassigned
Last substantive review: 2026-09-21
Applicable versions: Terraform CLI v1.16 fmt, init, validate, plan, apply, providers lock, and dependency lock documentation; linked local exercise previously executed with Terraform v1.13.1
Validation evidence: Source reviewed against official HashiCorp Terraform documentation on 2026-09-21. Terraform CLI is not installed in this workspace, so this pass did not re-execute the local exercise.
Known limitations: This page describes the core command workflow and review gates. Provider-specific credentials, backend migration, remote execution, policy checks, and cloud-side permissions still require environment runbooks.
Next review: 2026-12-21 or after a relevant Terraform CLI workflow, provider lock, plan, or apply behavior change

## Workflow model

Terraform's daily CLI workflow has two jobs: prepare the working directory,
then review and execute an intended change.[^terraform-cli] The command
sequence should make each state transition visible before anything changes
infrastructure.

```text
format -> initialize -> validate -> plan -> review -> apply
```

Use this page from the root module directory, the directory that contains the
`.tf` files for the stack or component you are changing.

## Before You Run Commands

- Confirm the repository branch and working directory.
- Confirm the target workspace, backend, cloud account, subscription, or
  project.
- Confirm how credentials are provided and whether they are read-only,
  planning-capable, or apply-capable.
- Review the provider lock file change, if `.terraform.lock.hcl` changed.
- Keep state files, saved plan files, local override files, and provider cache
  directories out of normal source commits unless the project explicitly says
  otherwise.

## Format Configuration

```bash
terraform fmt -recursive
```

What it does: rewrites Terraform configuration files into Terraform's canonical
format. HashiCorp documents `terraform fmt` as opinionated and intentionally
focused on consistent style.[^terraform-fmt]

Expected result: the command prints files it changed, or prints nothing when
everything already matches the canonical format.

For CI, check formatting without rewriting files:

```bash
terraform fmt -recursive -check
```

Expected result: exit status `0` when files are formatted. A non-zero result
means the contributor should run `terraform fmt -recursive` locally and commit
the formatting change.

## Initialize the Working Directory

```bash
terraform init
```

What it does: initializes a directory containing Terraform configuration. It
downloads modules and providers, configures the backend, and creates or updates
local initialization files. HashiCorp documents `terraform init` as the first
command to run after writing or cloning a configuration, and safe to run more
than once.[^terraform-init]

Expected result: Terraform reports successful initialization, and the working
directory contains `.terraform/` plus `.terraform.lock.hcl` when providers are
selected.

> [!IMPORTANT]
> Commit `.terraform.lock.hcl` when provider selections change. Terraform uses
> this dependency lock file to remember selected provider versions and verify
> package checksums on later runs.[^terraform-dependency-lock]

For CI syntax validation that should not access the configured backend:

```bash
terraform init -backend=false
```

What it does: installs the plugins and modules needed for validation without
configuring or contacting the backend. The Terraform validate documentation
recommends this pattern for validation-only initialization.[^terraform-validate]

## Validate Syntax and Internal Consistency

```bash
terraform validate
```

What it does: checks whether the configuration is syntactically valid and
internally consistent. It does not validate remote state, provider APIs, cloud
permissions, or whether the values for a specific run will work.[^terraform-validate]

Expected validation output:

```text
Success! The configuration is valid.
```

If it fails: fix syntax, type, attribute, or module wiring errors before
running a plan.

## Create and Review a Plan

```bash
terraform plan
```

What it does: compares configuration, state, input values, provider refresh
results, and selected planning options to show proposed infrastructure changes.
A normal plan does not carry out the changes.[^terraform-plan]

Expected result: the plan clearly shows whether Terraform proposes adds,
changes, replacements, destroys, output changes, or no changes. Stop and
investigate any action you cannot explain.

For automation or a two-step reviewed workflow, save the plan:

```bash
terraform plan -out=tfplan
terraform show tfplan
```

> [!IMPORTANT]
> Treat saved plan files as sensitive. HashiCorp documents that saved plan
> files contain the full configuration, planned values, plan options, and input
> variables, including sensitive values in cleartext when they are part of the
> plan.[^terraform-plan]

What it does: writes the exact reviewed plan to `tfplan`, then shows it for
review. Store, share, and delete saved plans according to the same rules you
would use for sensitive operational artifacts.

## Apply a Reviewed Change

```bash
terraform apply
```

What it does: creates a fresh plan, prompts for approval, and then performs the
approved operations.[^terraform-apply]

For a saved plan:

```bash
terraform apply tfplan
```

What it does: applies the exact saved plan file without asking for interactive
confirmation. Passing the plan file is treated as approval, and additional
planning options cannot be supplied at apply time.[^terraform-apply]

> [!WARNING]
> Use `-auto-approve` only in automation that already produced and reviewed a
> plan through an explicit approval gate. Terraform can delete resources when
> the approved plan says to delete them.

Expected result: Terraform reports completed resource actions and writes
updated state through the configured backend.

## Provider Lock File Review

Provider selections and checksums live in `.terraform.lock.hcl`. Terraform
creates or updates this file during `terraform init`, and HashiCorp recommends
including it in version control so provider dependency changes can be reviewed
like configuration changes.[^terraform-dependency-lock]

When a team needs to pre-populate provider checksums for multiple operating
systems or architecture targets, use:

```bash
terraform providers lock \
  -platform=linux_amd64 \
  -platform=darwin_arm64 \
  -platform=windows_amd64
```

What it does: fetches provider dependency information from upstream registries
and updates the dependency lock file for the requested platforms. Review the
command output before committing the updated lock file because Terraform cannot
decide whether provider signers satisfy your local trust policy.[^terraform-providers-lock]

## CI Validation Sequence

Use this sequence for pull-request checks that should verify formatting and
configuration consistency without accessing a remote backend:

```bash
terraform fmt -recursive -check
terraform init -backend=false
terraform validate
```

What it does: checks formatting, installs local validation dependencies without
backend initialization, and validates the configuration. This does not prove
cloud credentials, backend access, policy checks, cost impact, or apply
success.

Use a real backend-connected `terraform plan` in a protected environment when
the review needs provider behavior, state refresh, or permission validation.

## Common Stop Signals

| Signal | Why to stop |
| --- | --- |
| Unexpected destroy or replacement | The change may delete or recreate real infrastructure. Confirm whether it is intended. |
| Backend or workspace looks wrong | The same configuration can affect a different environment when pointed at a different backend or workspace. |
| Provider lock file changes unexpectedly | Provider versions or checksums changed and need dependency review. |
| Saved plan contains sensitive inputs | The plan artifact needs restricted storage and cleanup. |
| `validate` passes but `plan` fails | Static consistency is not enough; the run context, provider, backend, or input values still need correction. |

## Local practice exercise

Use [Terraform local state lifecycle](../examples/local-state-lifecycle/index.md) to run the command flow without a cloud account.

## Related links

- [Terraform CLI documentation](https://developer.hashicorp.com/terraform/cli)
- [terraform fmt reference](https://developer.hashicorp.com/terraform/cli/commands/fmt)
- [terraform init reference](https://developer.hashicorp.com/terraform/cli/commands/init)
- [terraform validate reference](https://developer.hashicorp.com/terraform/cli/commands/validate)
- [terraform plan reference](https://developer.hashicorp.com/terraform/cli/commands/plan)
- [terraform apply reference](https://developer.hashicorp.com/terraform/cli/commands/apply)
- [terraform providers lock reference](https://developer.hashicorp.com/terraform/cli/commands/providers/lock)
- [Terraform dependency lock file](https://developer.hashicorp.com/terraform/language/files/dependency-lock)
- [Terraform state management](../fundamentals/state-management.md)
- [Terraform local state lifecycle](../examples/local-state-lifecycle/index.md)
- [Back to Terraform commands](index.md)
- [Back to Terraform index](../index.md)
- [Back to root index](../../../README.md)

[^terraform-cli]: Official Terraform CLI documentation, source record `terraform-cli`.
[^terraform-fmt]: Official Terraform fmt command reference, source record `terraform-fmt`.
[^terraform-init]: Official Terraform init command reference, source record `terraform-init`.
[^terraform-validate]: Official Terraform validate command reference, source record `terraform-validate`.
[^terraform-plan]: Official Terraform plan command reference, source record `terraform-plan`.
[^terraform-apply]: Official Terraform apply command reference, source record `terraform-apply`.
[^terraform-providers-lock]: Official Terraform providers lock command reference, source record `terraform-providers-lock`.
[^terraform-dependency-lock]: Official Terraform dependency lock file documentation, source record `terraform-dependency-lock`.
