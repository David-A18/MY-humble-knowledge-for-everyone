---
type: Explanation
title: Environment layouts and state ownership
description: Choose Terraform root, module, backend, and environment boundaries by
  credentials, ownership, blast radius, and release cadence.
tags:
- terraform
- layout
- environments
status: draft
maturity: draft
audience: Engineering learners and platform practitioners
maintainer: unassigned
sources:
- id: tf-workspaces
  title: CLI workspace state model
  resource: https://developer.hashicorp.com/terraform/language/state/workspaces
- id: tf-backends
  title: Backend configuration
  resource: https://developer.hashicorp.com/terraform/language/backend
- id: tf-modules
  title: Developing modules
  resource: https://developer.hashicorp.com/terraform/language/modules/develop
---

# Environment layouts and state ownership

Organize Terraform by the unit people can safely plan, review, apply, and recover. A directory tree is useful only if it makes state ownership and operating context clear. Begin with trust boundaries and deployment cadence, then choose files and reusable modules.

## Separate composition from reuse

Illustrative layout:

```text
infrastructure/
  modules/
    network/
    application/
  roots/
    sandbox-network/
    production-network/
    production-application/
```

What it does: separates reusable module code from roots that own distinct states and runtime identities. The diagram does not provision anything and is not a rule that every team needs this many roots.

Each root should identify its backend, permitted account/project, provider aliases, input source, owner, and run/rollback process. Use a small `main.tf`, requirements/provider/backend files, explicit variables/outputs, and documentation where they improve review. All `.tf` files in a module are evaluated together; file names do not impose operation order.[^tf-modules]

## Choose the environment boundary

| Context | Recommended decision to evaluate |
| --- | --- |
| Different production credentials or state readers | Separate backend/access-control and root/run context. |
| Same operators, same credentials, temporary copies | CLI workspaces may be sufficient. |
| A shared network changes rarely; applications change often | Separate states with a deliberately published dependency contract. |
| Small single-owner local exercise | One root and local state keeps the model visible. |

CLI workspaces are not intended to replace separate credentials/access controls or system decomposition.[^tf-workspaces] A shared module can still be reused by distinct production/sandbox roots. Avoid choosing one enormous state solely to reduce file count, or one state per tiny object without a reason: both extremes add operational cost.

## Publish dependencies rather than hidden coupling

Decide how one root obtains another root's supported outputs: a service registry, parameter store, controlled configuration, or reviewed state-output mechanism. State access may expose more than the single output a caller wants. Preserve least privilege and make the producer/consumer update order explicit.

Backend configuration is not normal module input configuration. Its settings cannot be treated as arbitrary resource expressions, and credentials embedded there can persist in initialization data and plans.[^tf-backends] Use approved external identity mechanisms and version non-secret backend location metadata according to the repository's policy.

## Review and recovery evidence

A new root should have a reproducible dependency baseline, relevant validation/tests, protected plan artifacts, explicit approval for applies, and a documented state recovery owner. Capture which revision and input set produced a plan; re-plan after relevant changes rather than applying an unrelated stale artifact.

This is a layout decision guide, not an executed cloud architecture. Practice with the two local labs first. Follow-up cloud work needs real account/backend permissions, planned failure behavior, and cleanup/retention evidence. Never remove a root's state simply because its source directory is being reorganized.

## Evidence and limits

Sources reviewed on 2026-10-29. Local examples were executed with Terraform 1.17.1; the provider lab uses hashicorp/local 2.9.1. These runs cover local state/files, not cloud IAM, remote locking, backend migration, imports, or hosted execution. The guides remain drafts with unassigned ownership. Replace angle-bracket placeholders and confirm the actual root, backend, workspace, and provider identity before adapting commands.

## Related routes

- [Remote backends](../fundamentals/remote-backends-and-locking.md).
- [Module contracts](modules-and-composition.md).
- [Back to this section](index.md)
- [Back to Terraform](../index.md)

[^tf-workspaces]: [CLI workspace state model](https://developer.hashicorp.com/terraform/language/state/workspaces)
[^tf-backends]: [Backend configuration](https://developer.hashicorp.com/terraform/language/backend)
[^tf-modules]: [Developing modules](https://developer.hashicorp.com/terraform/language/modules/develop)
