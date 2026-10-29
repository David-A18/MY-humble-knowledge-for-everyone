---
type: Tutorial
title: Local modules, keys, refactors, and workspaces lab
description: Execute a provider-free Terraform module contract, reject invalid inputs,
  preserve IDs during a refactor, and compare isolated CLI states.
tags:
- terraform
- lab
- modules
- workspaces
status: draft
maturity: draft
audience: Engineering learners and platform practitioners
maintainer: unassigned
sources:
- id: tf-tests
  title: Terraform test files
  resource: https://developer.hashicorp.com/terraform/language/tests
- id: tf-for-each
  title: for_each reference
  resource: https://developer.hashicorp.com/terraform/language/meta-arguments/for_each
- id: tf-moved
  title: Refactoring with moved blocks
  resource: https://developer.hashicorp.com/terraform/language/modules/develop/refactoring
- id: tf-workspaces
  title: CLI workspace state model
  resource: https://developer.hashicorp.com/terraform/language/state/workspaces
---

# Local modules, keys, refactors, and workspaces lab

This lab builds on the [first local state exercise](../local-state-lifecycle/index.md). It uses built-in `terraform_data` records and no cloud API or downloaded provider. You will observe typed module inputs/outputs, stable keys, expected validation failures, address refactoring, and separate CLI workspace states.

## Prerequisites and isolation

Use Python 3.10+ and Terraform 1.6+ within the declared `< 2.0.0` constraint. The executed baseline is Python 3.13.17 and Terraform 1.17.1 on Windows amd64. Terraform's archive was checked against HashiCorp's published SHA256 list; the detached checksum signature was not verified in this run.

Run the bundled runner from the repository root. It resolves Terraform on PATH or accepts an explicit executable path. It copies only the bundled exercise into a fresh temporary directory and clears inherited Terraform CLI/workspace settings for that copy.

```bash
python knowledge/terraform/examples/module-workspace-lab/validate-lab.py --terraform terraform
```

What it does: formats/checks, initializes, validates, runs three Terraform tests, plans/applies local state, checks key/refactor behavior, compares workspaces, destroys both states' managed records, and removes the temporary copy. It does not change this checkout or provision external resources.

## Understand the files

| File | Learning purpose |
| --- | --- |
| [Root configuration](main.tf) | Validated environment/services inputs, keyed module calls, public outputs. |
| [Child module](child/main.tf) | Derived record stored in a built-in resource. |
| [Contract tests](tests/contract.tftest.hcl) | One apply contract and two expected input failures. |
| [Added-service inputs](add-service.tfvars.example) | Add a third stable key without replacing existing records. |
| [Execution runner](validate-lab.py) | Performs the isolated end-to-end exercise and checks the results. |

Terraform tests default to apply unless specified otherwise. Here the one apply test creates local state-only records, while invalid inputs are checked in plan runs with `expect_failures`.[^tf-tests] Do not assume tests in a cloud module are equally local.

## Expected observations

| Stage | Evidence the runner checks |
| --- | --- |
| Contract | Two service keys and expected values; production label/fractional replicas rejected. |
| Initial apply | Two managed creates, then a no-change plan. |
| Add `batch` | One additional create; `api` and `worker` are not replaced. |
| Rename child resource | Two prior-address entries, no create/delete actions, unchanged object IDs after apply. |
| New `preview` workspace | Starts without prior state; same configuration creates independent records. |
| Return to `default` | Existing state remains unchanged. |
| Cleanup | Both workspaces have no managed objects; empty `preview` is deleted. |

Stable `for_each` keys make individual identity reviewable.[^tf-for-each] The runner's refactor uses a `moved` block in its temporary child copy, rather than silently editing bindings.[^tf-moved] CLI workspace separation is state separation within the same trust boundary.[^tf-workspaces]

## Investigate failures

If Terraform is missing or does not meet the version constraint, select the intended executable. On contract failures, read the named assertion or variable error. A new local workspace reporting `No state file was found` is expected before its first apply; the runner distinguishes that message from unrelated errors.

The runner fails if creates/replacements, preserved IDs, or cleanup differ from expectations. Its summary is not a cloud deployment attestation. Do not copy production credentials or backend blocks into this lab to broaden it.

## Cleanup

Successful execution destroys the local records before its temporary directory is removed. No external resources remain. For manual practice, make a separate disposable copy, follow the same workspace cleanup order, and confirm empty state before deleting files; never run these cleanup steps in an unrelated root.

## Evidence and limits

Sources reviewed on 2026-10-29. Local examples were executed with Terraform 1.17.1; the provider lab uses hashicorp/local 2.9.1. These runs cover local state/files, not cloud IAM, remote locking, backend migration, imports, or hosted execution. The guides remain drafts with unassigned ownership. Replace angle-bracket placeholders and confirm the actual root, backend, workspace, and provider identity before adapting commands.

## Related routes

- [Module contracts](../../project-structure/modules-and-composition.md).
- [Provider alias lab](../provider-alias-lab/index.md).
- [Back to this section](index.md)
- [Back to Terraform](../../index.md)

[^tf-tests]: [Terraform test files](https://developer.hashicorp.com/terraform/language/tests)
[^tf-for-each]: [for_each reference](https://developer.hashicorp.com/terraform/language/meta-arguments/for_each)
[^tf-moved]: [Refactoring with moved blocks](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)
[^tf-workspaces]: [CLI workspace state model](https://developer.hashicorp.com/terraform/language/state/workspaces)
