---
type: Troubleshooting Guide
title: Terraform failures and unexpected plans
description: Locate initialization, validation, state-context, dependency, and identity
  problems before using state-mutating recovery commands.
tags:
- terraform
- troubleshooting
- plans
status: draft
maturity: draft
audience: Engineering learners and platform practitioners
maintainer: unassigned
sources:
- id: tf-init
  title: terraform init
  resource: https://developer.hashicorp.com/terraform/cli/commands/init
- id: tf-plan
  title: terraform plan
  resource: https://developer.hashicorp.com/terraform/cli/commands/plan
- id: tf-moved
  title: Refactoring with moved blocks
  resource: https://developer.hashicorp.com/terraform/language/modules/develop/refactoring
- id: tf-module-providers
  title: Providers within modules
  resource: https://developer.hashicorp.com/terraform/language/modules/develop/providers
---

# Terraform failures and unexpected plans

Start with the exact failed command, root directory, CLI version, backend/workspace, dependency changes, and intended provider identity. Preserve a redacted error and plan; state and plan JSON can contain secrets. A successful format or validate check does not prove remote permissions or a safe apply.

## Inspect the context first

Run only the commands appropriate to an already-initialized working directory. A fresh or misconfigured backend can fail these checks; that is evidence to investigate, not a reason to initialize against a guessed destination.

```bash
terraform version
terraform workspace show
terraform providers
terraform state list
```

What it does: identifies the CLI, selected state, provider requirements, and tracked addresses. Confirm directory/account context outside Terraform too. A fresh local workspace can have no state file; an unexpectedly empty production state is a stop signal.

| Symptom | First question | Targeted action |
| --- | --- | --- |
| `init` cannot install a provider | Source, constraint intersection, platform/checksum, network or mirror? | Review dependency changes and signer/checksum evidence; preserve the lock. |
| Backend changed | Was migration intended or only settings changed? | Review state inventory before choosing reconfigure or migrate. |
| Missing provider configuration | Was an alias removed while state still depends on it? | Restore the required context or use a reviewed migration; do not remove state blindly. |
| Invalid `for_each` argument | Are keys known, stable, non-sensitive, and a supported collection? | Correct the key design rather than target a partial graph routinely. |
| Unexpected create/destroy after rename | Did an address change? | Evaluate a compatible `moved` block. |
| Lock failure | Is another writer active? | Coordinate with its owner; do not bypass locking. |
| Import conflict or duplicate object | Is the real object already bound elsewhere? | Inventory the intended owner/address and provider-specific import ID before mutation. |

## Diagnose dependencies and backend identity

`init -upgrade` deliberately revisits dependencies; it is not a neutral repair for every failure. `init -reconfigure` adopts settings without migrating state, whereas `-migrate-state` attempts a copy.[^tf-init] Verify the backend store and selected state before assuming resource bindings vanished.

Reusable modules must declare provider requirements and explicitly wire alternate configurations. Removing a root alias while objects still depend on it can prevent management of those objects.[^tf-module-providers] Restore the supported configuration and investigate the intended transition with the owner instead of making Terraform forget real infrastructure.

## Interpret plan differences

Compare configuration/source revision, input files, module pins, lock changes, workspace, backend location, and refreshed provider observations. A no-op code diff does not mean the cloud has not drifted; a textual refactor can still change addresses.

Use `moved` blocks for compatible address refactors and confirm the resulting actions.[^tf-moved] A real type/provider change may require a different migration. Routine `-target`, disabling refresh, or ignoring all changes can conceal incomplete configuration; targeting is intended for exceptional recovery cases.[^tf-plan]

If import is the right outcome, review the exact remote identity and intended resource address, establish that no other state owns it, and inspect the proposed import/plan before applying. This guide does not claim a cloud-backed import drill; keep provider-specific imports as focused follow-up runbooks.

## Verify recovery and close

Re-run the failed stage, inspect the full plan, and verify the intended provider-side result after any authorized apply. Record why unexpected changes disappeared; do not accept a green command achieved by removing the intended protection. For local practice, the labs verify a no-change plan after apply, a preserved-ID refactor, and complete cleanup. Remote state lock/recovery and cloud failures still need their own runtime evidence.

## Evidence and limits

Sources reviewed on 2026-10-29. Local examples were executed with Terraform 1.17.1; the provider lab uses hashicorp/local 2.9.1. These runs cover local state/files, not cloud IAM, remote locking, backend migration, imports, or hosted execution. The guides remain drafts with unassigned ownership. Replace angle-bracket placeholders and confirm the actual root, backend, workspace, and provider identity before adapting commands.

## Related routes

- [State recovery model](../fundamentals/state-management.md).
- [Backends and locking](../fundamentals/remote-backends-and-locking.md).
- [Plan exit codes](../commands/plan-exit-codes-and-ci.md).
- [Back to this section](index.md)
- [Back to Terraform](../index.md)

[^tf-init]: [terraform init](https://developer.hashicorp.com/terraform/cli/commands/init)
[^tf-plan]: [terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan)
[^tf-moved]: [Refactoring with moved blocks](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)
[^tf-module-providers]: [Providers within modules](https://developer.hashicorp.com/terraform/language/modules/develop/providers)
