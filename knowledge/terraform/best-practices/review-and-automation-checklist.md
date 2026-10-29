---
type: How-to Guide
title: Review and automate Terraform changes
description: Apply concrete review gates to Terraform dependencies, operating context,
  plans, tests, secrets, and cleanup.
tags:
- terraform
- ci
- review
status: draft
maturity: draft
audience: Engineering learners and platform practitioners
maintainer: unassigned
sources:
- id: tf-lock-file
  title: Provider dependency lock file
  resource: https://developer.hashicorp.com/terraform/language/files/dependency-lock
- id: tf-plan
  title: terraform plan
  resource: https://developer.hashicorp.com/terraform/cli/commands/plan
- id: tf-tests
  title: Terraform test files
  resource: https://developer.hashicorp.com/terraform/language/tests
- id: tf-test-cli
  title: terraform test and cleanup
  resource: https://developer.hashicorp.com/terraform/cli/commands/test
- id: tf-sensitive
  title: Sensitive and ephemeral data
  resource: https://developer.hashicorp.com/terraform/language/manage-sensitive-data
---

# Review and automate Terraform changes

Use this checklist when preparing a Terraform change for review or automation. The goal is an explainable change to the intended state, with evidence proportional to its impact. Formatting and validation are necessary checks, not deployment approval.

## Establish the baseline

- Identify the root owner, source revision, backend/workspace, and target provider identity.
- Review input changes, module pins, provider constraints, and `.terraform.lock.hcl` changes.
- Separate configuration changes from dependency upgrades when that makes their effects easier to assess.
- Keep `.terraform/`, state, plans, crash logs, and credentials out of source commits.

The provider lock file covers provider selections/checksums, while remote module version selection needs its own pinning/review.[^tf-lock-file] Avoid deleting a lock simply because another machine's initialization fails; diagnose the actual platform, mirror, or checksum issue.

## Run checks with clear scope

From the intended root, this prepares static validation without contacting its backend. Provider/module downloads may still use the network:

```bash
terraform fmt -recursive -check
terraform init -backend=false -input=false -lockfile=readonly
terraform validate
```

What it does: checks style, installs reviewed dependencies for validation, and checks internal consistency. A new project without a suitable lock may need a deliberate initialization/lock-generation step first. This is not proof of backend access, cloud policy, cost, or live resource behavior.

Run relevant contract tests in their declared environment. Terraform tests default to apply operations unless `command = plan` is specified; tests can create real resources.[^tf-tests] Confirm test identity/scope and inspect cleanup diagnostics. The supplied labs use built-in state records or one local file and run only in disposable copies; do not generalize that safety property to arbitrary modules.[^tf-test-cli]

## Review the full plan

Check creates, updates, replacements, destroys, address moves, unknown values, and output changes. Ask whether every action matches the intended change and whether provider defaults or newly selected dependencies explain differences. Code formatting is not enough to evaluate them.

For automated planning, distinguish detailed exit codes: `0` means no diff, `2` means a successful plan with changes, and `1` means error. Only treat the documented successful states as success; do not append unconditional `|| true`.[^tf-plan] Use the [CI command example](../commands/plan-exit-codes-and-ci.md).

## Protect artifacts and the apply boundary

Treat saved plans and machine-readable outputs as sensitive. Redaction does not remove values from state/plans, and JSON/raw output can reveal them.[^tf-sensitive] Restrict artifact readers/retention, keep untrusted pull requests away from privileged credentials, and approve the exact intended plan/revision under the platform's change process.

After apply, verify resource/application behavior and the intended permission boundary. A subsequent no-op plan is useful but does not replace workload health or failover tests. Retain the minimal redacted evidence needed for recovery, then remove disposable resources through their owning state before deleting local state/artifacts. The local lab runners verify destruction and empty state automatically for their bundled examples.

## Evidence and limits

Sources reviewed on 2026-10-29. Local examples were executed with Terraform 1.17.1; the provider lab uses hashicorp/local 2.9.1. These runs cover local state/files, not cloud IAM, remote locking, backend migration, imports, or hosted execution. The guides remain drafts with unassigned ownership. Replace angle-bracket placeholders and confirm the actual root, backend, workspace, and provider identity before adapting commands.

## Related routes

- [Environment layout](../project-structure/environment-layouts.md).
- [Core workflow](../commands/core-workflow.md).
- [Back to this section](index.md)
- [Back to Terraform](../index.md)

[^tf-lock-file]: [Provider dependency lock file](https://developer.hashicorp.com/terraform/language/files/dependency-lock)
[^tf-plan]: [terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan)
[^tf-tests]: [Terraform test files](https://developer.hashicorp.com/terraform/language/tests)
[^tf-test-cli]: [terraform test and cleanup](https://developer.hashicorp.com/terraform/cli/commands/test)
[^tf-sensitive]: [Sensitive and ephemeral data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data)
