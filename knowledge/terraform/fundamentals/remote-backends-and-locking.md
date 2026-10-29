---
type: Explanation
title: Remote backends and state locking
description: Design shared Terraform state storage and distinguish backend initialization,
  migration, locking, and recovery responsibilities.
tags:
- terraform
- backends
- s3
- locking
status: draft
maturity: draft
audience: Engineering learners and platform practitioners
maintainer: unassigned
sources:
- id: tf-backends
  title: Backend configuration
  resource: https://developer.hashicorp.com/terraform/language/backend
- id: tf-s3-backend
  title: S3 backend and locking
  resource: https://developer.hashicorp.com/terraform/language/backend/s3
- id: tf-init
  title: terraform init
  resource: https://developer.hashicorp.com/terraform/cli/commands/init
---

# Remote backends and state locking

A backend defines where Terraform stores state and which state-operation behavior is available. Provider configuration manages resources; backend authentication reaches the state store. These identities and permissions can differ. A remote store is not proof that state is encrypted, access-controlled, versioned, or locked correctly.[^tf-backends]

## Define the operational contract

Document the root owner, backend type/location, selected workspace, read/write identities, locking mechanism, audit/retention rules, backup recovery, and who may authorize migration. Credentials supplied directly in backend arguments or `-backend-config` can persist in initialization data and saved plans; use the backend's intended external credential mechanism.[^tf-backends]

The following is a source-reviewed S3 illustration, **not part of the executed local labs**. Its bucket and IAM/KMS setup must already exist in an authorized environment; do not apply a fake bucket name copied from documentation.

```hcl
terraform {
  backend "s3" {
    bucket       = "replace-with-authorized-state-bucket"
    key          = "platform/learning/terraform.tfstate"
    region       = "eu-west-1"
    encrypt      = true
    use_lockfile = true
  }
}
```

What it does: selects S3 state storage and opts into its lock-file mechanism. Enable suitable bucket versioning, restrict state access, and evaluate the actual encryption/KMS policy. Current documentation marks DynamoDB-based locking deprecated. Lock-object permissions include operations needed to create and remove the `.tflock` object; do not confuse them with permissions to delete the state object.[^tf-s3-backend]

## Initialization is not migration

| Operation | Intent | Safety boundary |
| --- | --- | --- |
| `init -backend=false` | Prepare dependencies for validation without backend initialization | Does not prove backend permission or state correctness. |
| `init -reconfigure` | Adopt backend settings without migrating existing state | Can point at a different/empty state; not a copy operation. |
| `init -migrate-state` | Attempt to copy existing state into the changed backend | Requires a reviewed inventory, backup, exclusive writers, and migration verification. |

HashiCorp distinguishes reconfiguration from state migration explicitly.[^tf-init] Do not delete `.terraform/` and repeatedly initialize until a warning disappears. Confirm which state holds the real resource bindings first.

For migration, freeze writers, record every relevant workspace/state, take protected backups, establish destination permissions/locking, and review prompts before copying. Then verify bindings/lineage and a no-surprise plan at the destination before allowing writes again. Keep an owner-approved recovery path; copying an older snapshot back blindly can discard newer changes.

## Lock failures and recovery

A lock failure may mean another valid writer is active, not a corrupt state. Inspect the owner/run and timestamps with the backend operator. Prefer waiting or safely terminating the owning run under its incident process. Neither `-lock=false` nor manual deletion of a live lock is a routine repair. Force-unlock belongs to a confirmed stale-lock recovery with exclusive ownership and evidence.

No remote backend, cloud bucket, migration, or competing-writer drill was executed in this revision. Use the [state guide](state-management.md) for the general model and add backend-specific runtime evidence before calling an operational procedure tested. Remove only task-owned sandbox backend resources after consumers/state retention requirements have been resolved; never treat a real state bucket as disposable lab output.

## Evidence and limits

Sources reviewed on 2026-10-29. Local examples were executed with Terraform 1.17.1; the provider lab uses hashicorp/local 2.9.1. These runs cover local state/files, not cloud IAM, remote locking, backend migration, imports, or hosted execution. The guides remain drafts with unassigned ownership. Replace angle-bracket placeholders and confirm the actual root, backend, workspace, and provider identity before adapting commands.

## Related routes

- [Dependency lock file](providers-and-dependency-locking.md) — provider selection, not concurrency.
- [Failure diagnosis](../troubleshooting/failures-and-unexpected-plans.md).
- [Back to this section](index.md)
- [Back to Terraform](../index.md)

[^tf-backends]: [Backend configuration](https://developer.hashicorp.com/terraform/language/backend)
[^tf-s3-backend]: [S3 backend and locking](https://developer.hashicorp.com/terraform/language/backend/s3)
[^tf-init]: [terraform init](https://developer.hashicorp.com/terraform/cli/commands/init)
