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
  - id: terraform-plan
    resource: https://developer.hashicorp.com/terraform/cli/commands/plan
    title: Terraform plan and saved plans
  - id: terraform-data
    resource: https://developer.hashicorp.com/terraform/language/resources/terraform-data
    title: Built-in terraform_data resource
stale_after: 2026-12-19
---

# Terraform local state lifecycle

## Goal

Learn Terraform's local workflow by initializing a small configuration, validating it, creating local state, changing an input, reviewing the plan, applying the change, inspecting state, and destroying the managed object.

This exercise does not require a cloud account. It uses Terraform's built-in `terraform_data` resource, which stores data in Terraform state without creating external infrastructure.[^terraform-data]

## Prerequisites

- Terraform 1.4.0 or newer.
- Git and a terminal.
- A disposable local directory.
- Bash for manual commands below, or Python 3.10+ for the cross-platform validation runner.

This tutorial was previously executed with Terraform v1.13.1. Its local init/validate/plan/apply/change/destroy lifecycle was rechecked on 2026-10-29 with Terraform 1.17.1 in a disposable directory. It remains `draft`; the local execution is not a maintainer approval or cloud/backend validation.

On 2026-11-10 the [new lifecycle runner](validate-lab.py) executed the actual fixture with Terraform 1.17.1 and Python 3.13.17 on Windows: create, no-change status, in-place update with stable object ID, non-persisted CLI input, destroy and empty managed state. The linked [preflight](../../../cross-topic-guides/local-learning-preflight.md) explains stage and shell requirements. This Terraform project does not create or control the kind cluster from the earlier exercise.

## Files

| File | Purpose |
| --- | --- |
| [main.tf](main.tf) | Defines variables, local values, a `terraform_data` resource, and outputs. |
| [.gitignore](.gitignore) | Keeps local state, cache, plans, and override files out of Git. |

## Prepare an isolated copy

From the repository root:

```bash
EXERCISE_DIR=$(mktemp -d "${TMPDIR:-/tmp}/kb-terraform-local.XXXXXX")
cp knowledge/terraform/examples/local-state-lifecycle/main.tf "$EXERCISE_DIR/"
cp knowledge/terraform/examples/local-state-lifecycle/.gitignore "$EXERCISE_DIR/"
cd "$EXERCISE_DIR"
git init -b learning
git config user.name "Local learning fixture"
git config user.email "learner@example.invalid"
git add .
git -c commit.gpgsign=false commit -m "add terraform local state exercise"
```

What it does: creates a unique disposable working directory so Terraform state and cache files stay out of the knowledge-base checkout. The synthetic local author identity and per-command signing override apply only to this teaching repository/commit. Use your own approved local identity if appropriate.

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

What it does: illustrates successful static validation; it does not prove the selected state, backend, or any real cloud account is safe.

## Review the first plan

```bash
terraform plan -out=create.tfplan
```

What it does: shows that Terraform will create one `terraform_data.release` object in local state and stores the plan in `create.tfplan`. Review its actual create/change/destroy actions before applying.[^terraform-plan]

Expected condition: the plan says `1 to add, 0 to change, 0 to destroy`.

## Apply and inspect state

```bash
terraform apply create.tfplan
terraform output
terraform state list
terraform state show terraform_data.release
```

What it does: applies the saved plan, displays output values, lists tracked state addresses, and shows the stored object.

Expected condition: `terraform_data.release` appears in state.

## Make a deliberate change

```bash
terraform plan -var='release_version=1.1.0' -out=change.tfplan
terraform apply change.tfplan
terraform output release_summary
```

What it does: reviews and saves a version update, applies that saved plan, then inspects the updated output. A saved plan contains the chosen input; applying it does not prompt for a second interactive plan approval. Treat saved plans as potentially sensitive artifacts.[^terraform-plan]

Expected condition: the plan shows `terraform_data.release` changing in place and the output includes `version = "1.1.0"`.

The command-line `-var` does not rewrite `main.tf`. A later plan with the same override should show no change; a plan using only the original defaults proposes returning to `1.0.0`. Decide how real configuration will persist in versioned inputs before assuming that apply changed the source of truth. The runner explicitly tests this distinction.

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
| `*.tfplan` or `tfplan` | Saved plan artifacts. | Ignored because plans can include sensitive data. |

Empty managed state after destroy does not erase local state snapshots, backups, or saved plans. Keep the scratch directory until the exercise report is complete; remove only that verified task-owned directory under the applicable retention policy. No source checkout or shared state should be removed as tutorial cleanup.

## Repeatable validation

Run from the repository root with Terraform on PATH:

```bash
python knowledge/terraform/examples/local-state-lifecycle/validate-lab.py
```

What it does: copies the exact local fixture into a temporary directory, clears inherited Terraform overrides for this child process, verifies create/update/plan/state behavior, destroys the local object, and removes the temporary copy. An unexpected result exits nonzero. The [local learning CI workflow](../../../../.github/workflows/local-learning-journey.yml) runs the same lifecycle on Linux with Terraform 1.17.1.

## Understanding checks

- Which command created the local state file?
- Which command showed the exact address `terraform_data.release`?
- Why is state ignored even though this exercise has no secrets?
- What does the plan report before apply, after the version change, and after destroy?

## Next local exercises

- [Module and workspace lab](../module-workspace-lab/index.md) — learn typed contracts, stable keys, tests, refactors, and separate local states.
- [Provider alias lab](../provider-alias-lab/index.md) — learn an installed provider and child alias mapping with a local artifact.

## Related links

- [Start here](../../../start-here.md)
- [Core Terraform workflow](../../commands/core-workflow.md)
- [State management](../../fundamentals/state-management.md)
- [Back to Terraform local state lifecycle](index.md)
- [Back to Terraform examples](../index.md)
- [Back to Terraform index](../../index.md)
- [Back to knowledge index](../../../index.md)

[^terraform-plan]: [Terraform plan and saved plans](https://developer.hashicorp.com/terraform/cli/commands/plan).
[^terraform-data]: [Built-in terraform_data resource](https://developer.hashicorp.com/terraform/language/resources/terraform-data).
