---
type: Troubleshooting Guide
title: Recover from Terraform state lock contention
description: Identify the lock owner, recover an orphaned lock, and verify that normal Terraform operations can resume.
tags: [terraform, state, troubleshooting]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: state-lock
    resource: https://developer.hashicorp.com/terraform/language/state/locking
    title: Terraform state locking
  - id: force-unlock
    resource: https://developer.hashicorp.com/terraform/cli/commands/force-unlock
    title: Terraform force-unlock reference
  - id: s3-locking
    resource: https://developer.hashicorp.com/terraform/language/backend/s3
    title: Terraform S3 backend reference
---

# Recover from Terraform state lock contention

A state lock prevents two Terraform operations from changing the same state at
once. If a deployment is still running and your plan reports an error acquiring
the lock, let the deployment finish before retrying.[^state-lock]

## Identify the owner

1. Record the workflow run, lock ID, operation, and timestamp. Check that your
   working directory, backend key, and workspace identify the intended state.
2. Look for the owning Terraform process or CI job. A lock's age alone gives
   no assurance that the owner has stopped.
3. If the owner is active, wait. For a busy backend, a bounded retry such as
   `terraform plan -lock-timeout=60s` lets another run finish before the plan
   gives up.
4. If the error is access denied, first check backend credentials and
   permissions. For S3 with `use_lockfile`, compare access to the state object
   and the corresponding `.tflock` object.[^s3-locking]

## Recover a lock left by your run

> [!WARNING]
> Force-unlocking while another process can still write allows concurrent
> writes. Pause queued writers and confirm your owning run has ended before
> proceeding. Use the backend's established recovery procedure.

From the initialized directory and workspace for the affected state, use the
lock ID reported by Terraform:

```bash
terraform force-unlock LOCK_ID
terraform plan -lock-timeout=30s
```

What it does: `force-unlock` removes the lock when the backend supports that
operation. The plan checks that Terraform can take a new lock and shows whether
a previous interrupted apply left changes to reconcile. Review the new plan
before applying it.[^force-unlock]

## Evidence and limits

The [disposable HTTP backend rehearsal](../../../examples/terraform/lock-recovery/README.md)
ran with Terraform 1.17.1 on Windows on 25 November 2026. A second client
reported the active lock ID. Recovery cleared the orphaned lock while
preserving the saved state byte for byte, and a subsequent apply acquired and
released a new lock. S3 and hosted backend recovery still need separate tests.

## Related links

- [Remote backends and locking](../fundamentals/remote-backends-and-locking.md)
- [Terraform troubleshooting](index.md)
- [Terraform index](../index.md)
- [Knowledge home](../../index.md)

[^state-lock]: [Terraform state locking](https://developer.hashicorp.com/terraform/language/state/locking)
[^force-unlock]: [Terraform force-unlock reference](https://developer.hashicorp.com/terraform/cli/commands/force-unlock)
[^s3-locking]: [Terraform S3 backend reference](https://developer.hashicorp.com/terraform/language/backend/s3)
