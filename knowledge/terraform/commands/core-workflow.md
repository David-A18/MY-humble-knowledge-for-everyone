---
type: How-to Guide
title: Review and apply a Terraform change
description: Check the target, validate a Terraform configuration, review a saved plan, apply that plan, and verify the result.
tags: [terraform, core-workflow, plan, apply]
status: draft
maturity: draft
audience: Beginning platform engineer
maintainer: unassigned
sources:
  - id: terraform-fmt
    resource: https://developer.hashicorp.com/terraform/cli/commands/fmt
    title: terraform fmt command
  - id: terraform-init
    resource: https://developer.hashicorp.com/terraform/cli/commands/init
    title: terraform init command
  - id: terraform-workspace-show
    resource: https://developer.hashicorp.com/terraform/cli/commands/workspace/show
    title: terraform workspace show command
  - id: terraform-validate
    resource: https://developer.hashicorp.com/terraform/cli/commands/validate
    title: terraform validate command
  - id: terraform-plan
    resource: https://developer.hashicorp.com/terraform/cli/commands/plan
    title: terraform plan command
  - id: terraform-show
    resource: https://developer.hashicorp.com/terraform/cli/commands/show
    title: terraform show command
  - id: terraform-apply
    resource: https://developer.hashicorp.com/terraform/cli/commands/apply
    title: terraform apply command
  - id: terraform-dependency-lock
    resource: https://developer.hashicorp.com/terraform/language/files/dependency-lock
    title: Terraform dependency lock file
---

# Review and apply a Terraform change

## What this guide helps you do

Use this sequence when you have already changed a Terraform configuration
and need to review what it would do before changing real infrastructure.
You will check the target, validate the files, save and inspect a plan,
apply that exact plan, and verify the result.

A **plan** is Terraform's proposed set of actions; **apply** carries
them out. A saved plan connects review to a specific proposed change.
Read [Terraform fundamentals](../fundamentals/terraform-fundamentals.md)
for the model, and [state management](../fundamentals/state-management.md)
for the record Terraform uses to track managed objects.[^terraform-plan]
[^terraform-apply]

This guide does not supply provider credentials, backend migration steps,
a cloud approval policy, or a service-specific verification test. Use the
project's runbook for those details. For a safe first run without a cloud
account, use the [local state lifecycle tutorial](../examples/local-state-lifecycle/local-state-lifecycle.md).

## Before you run a command

Work in the **root module** directory for the component you intend to
change. Identify the exact backend, Terraform workspace, cloud account
or project, provider credentials, and any approval gate. A successful
plan against the wrong target is still the wrong change.

Keep local state and saved plan files out of Git and restricted to people
allowed to inspect the infrastructure. A saved plan can contain sensitive
values even if terminal output hides them.[^terraform-plan]

| Stage | Expected evidence before moving on |
| --- | --- |
| Check target | You can name the root module, backend, workspace, and provider account or project. |
| Format and initialize | The files are formatted; initialization completed without an unexpected backend change. |
| Validate | Terraform reports valid configuration; this does not prove cloud permissions or the target. |
| Plan and review | Every create, update, replacement, and destroy is explained. |
| Apply and verify | The reviewed plan was applied, then the managed objects and user-facing service were checked. |

The following example situation is **illustrative**: a team adjusts a
staging web service's capacity. The commands below are general Terraform
commands, but no staging service, cloud account, or provider was used to
run this guide. The local tutorial was run separately with
`terraform_data`.

## 1. Check formatting and initialize

First check format without changing files:

```bash
terraform fmt -recursive -check
```

Exit status `0` means the scanned configuration is formatted. If it
lists files, run `terraform fmt -recursive`, review the file diff, and
commit the intended formatting change. The `-recursive` option includes
child directories; use a narrower target if the project requires one.
[^terraform-fmt]

Then initialize the selected root module:

```bash
terraform init
terraform workspace show
```

`terraform init` prepares modules, providers, and the configured
backend. `terraform workspace show` displays the current workspace.
Stop if initialization asks for a backend migration you did not plan,
or if the workspace or provider target differs from the intended
environment.[^terraform-init]
[^terraform-workspace-show]

Review any change to `.terraform.lock.hcl` before continuing. This
file records selected provider versions and checksums; keep the
reviewed file under version control with the configuration.
A lock-file change is a dependency change, not merely formatting.
[^terraform-lock]

## 2. Validate the configuration

```bash
terraform validate
```

Expected result: Terraform reports that the configuration is valid.
Validation checks syntax and internal consistency. It does **not**
check a particular run's input values, remote state, cloud permissions,
or whether the service will work after apply. Fix errors before planning.
[^terraform-validate]

For a pull request check that should not initialize the configured
backend, the documented validation pattern is
`terraform init -backend=false` followed by `terraform validate`.
That check still needs the modules and providers required for
validation; it is not a substitute for a backend-connected plan.
[^terraform-init][^terraform-validate]

## 3. Save and inspect the plan

```bash
terraform plan -out=tfplan
terraform show tfplan
```

Terraform reads the current managed objects where possible, compares
them with configuration and state, and saves the proposed actions in
`tfplan`. `terraform show` displays that saved plan for review.
Planning itself does not perform the proposed changes.[^terraform-plan]
[^terraform-show]

For the illustrative staging capacity change, expect only the
particular service resources and output changes that the team
intended. Do not approve by relying on a total such as "one to
change." Read the resource addresses, symbols, changed attributes,
replacement reasons, and any destroy actions.

> [!WARNING]
> Stop if the plan targets the wrong account or workspace, proposes
> an unexplained replacement or deletion, or changes more resources
> than expected. Investigate configuration, state, provider inputs,
> and the remote objects before applying.

Treat `tfplan` and its displayed details as sensitive. Keep the file
out of Git, restrict any CI artifact, and remove it according to the
project's retention policy. The plan file includes configuration,
input values, plan options, and potentially cleartext sensitive
values.[^terraform-plan]

## 4. Apply the plan you reviewed

Only after the required human or automated approval gate has passed:

```bash
terraform apply tfplan
```

Passing a saved plan is itself approval to Terraform: it does **not**
show a new interactive approval prompt. It applies that plan, rather
than calculating an unrelated fresh plan. If the context or intended
change has shifted since review, make and review a **new** plan instead.
[^terraform-apply]

A plain `terraform apply` is a different path: it creates a fresh
plan and asks for approval. Read that newly generated plan in full;
an earlier speculative `terraform plan` is not the one being applied.
[^terraform-apply][^terraform-plan]

Expected result: Terraform reports the resource actions it completed
and updates state through the configured backend. An apply error may
leave some actions completed; do not blindly rerun or manually edit
state. Inspect the reported operations and the next plan with the
project's recovery procedure.

## 5. Check Terraform and the service

```bash
terraform plan
```

A no-change plan is useful evidence that configuration, state, and the
provider's current view agree at this moment. It does not prove that
the staging web service is healthy for users. Run the project's
service-specific checks, such as a request through the actual entry
point, and record the observed result.[^terraform-plan]

If the final plan proposes more changes, investigate the difference
before another apply. If the service fails, use its operational
runbook; a green Terraform apply alone cannot identify every
application failure.

## Common stop signals

| Signal | Next action |
| --- | --- |
| Unexpected backend, workspace, or account | Stop and identify the selected target before planning or applying. |
| Provider lock file changed unexpectedly | Review the chosen provider version and checksum change before committing it. |
| `validate` passes but `plan` fails | Check run inputs, backend access, provider/API behavior, and remote permissions; validation did not test them. |
| Plan includes an unexplained destroy or replacement | Inspect the exact address and cause. Seek the project's review before approving. |
| Apply partly completed | Inspect state, remote objects, and a new plan with the recovery runbook; do not assume rollback occurred. |

## Check your understanding

1. Why is `terraform validate` not enough to approve a change?
2. What does `terraform apply tfplan` do with the approval prompt?
3. Why might a plain `terraform apply` differ from a plan you saw earlier?
4. What would prove that a service works for users after Terraform
   reports a successful apply?

## Official documentation for deeper study

- [Format configuration](https://developer.hashicorp.com/terraform/cli/commands/fmt)
  and [initialize a directory](https://developer.hashicorp.com/terraform/cli/commands/init).
- [Validate configuration](https://developer.hashicorp.com/terraform/cli/commands/validate)
  and [review a plan](https://developer.hashicorp.com/terraform/cli/commands/plan).
- [Inspect a saved plan](https://developer.hashicorp.com/terraform/cli/commands/show)
  and [apply it](https://developer.hashicorp.com/terraform/cli/commands/apply).
- [Understand the provider dependency lock file](https://developer.hashicorp.com/terraform/language/files/dependency-lock).

[Back to Terraform commands](index.md) |
[Back to Terraform index](../index.md) |
[Back to knowledge index](../../index.md)

[^terraform-fmt]: [terraform fmt command](https://developer.hashicorp.com/terraform/cli/commands/fmt).
[^terraform-init]: [terraform init command](https://developer.hashicorp.com/terraform/cli/commands/init).
[^terraform-workspace-show]: [terraform workspace show command](https://developer.hashicorp.com/terraform/cli/commands/workspace/show).
[^terraform-validate]: [terraform validate command](https://developer.hashicorp.com/terraform/cli/commands/validate).
[^terraform-plan]: [terraform plan command](https://developer.hashicorp.com/terraform/cli/commands/plan).
[^terraform-show]: [terraform show command](https://developer.hashicorp.com/terraform/cli/commands/show).
[^terraform-apply]: [terraform apply command](https://developer.hashicorp.com/terraform/cli/commands/apply).
[^terraform-lock]: [Terraform dependency lock file](https://developer.hashicorp.com/terraform/language/files/dependency-lock).
