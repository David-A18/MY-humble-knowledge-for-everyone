---
type: How-to Guide
title: Plan exit codes and CI boundaries
description: Handle Terraform plan result codes correctly and preserve the distinction
  between static validation, real plans, tests, and apply approval.
tags:
- terraform
- plan
- ci
status: draft
maturity: draft
audience: Engineering learners and platform practitioners
maintainer: unassigned
sources:
- id: tf-plan
  title: terraform plan
  resource: https://developer.hashicorp.com/terraform/cli/commands/plan
- id: tf-tests
  title: Terraform test files
  resource: https://developer.hashicorp.com/terraform/language/tests
- id: tf-test-cli
  title: terraform test and cleanup
  resource: https://developer.hashicorp.com/terraform/cli/commands/test
---

# Plan exit codes and CI boundaries

Use `terraform plan -detailed-exitcode` when automation must distinguish a no-change result from a proposed change. The option changes the exit-status contract: `0` is successful with no diff, `1` is an error, and `2` is successful with changes.[^tf-plan]

## Capture status without masking errors

This Bash fragment belongs in a protected planning environment with the intended backend/workspace, inputs, and credentials already selected. It does not apply anything. The saved plan must be private because it can contain sensitive data.

```bash
set -euo pipefail
plan_status=0
terraform plan -input=false -no-color -detailed-exitcode -out=reviewed.tfplan || plan_status=$?
case "$plan_status" in
  0) echo "Plan succeeded: no changes." ;;
  2) echo "Plan succeeded: changes require review." ;;
  *) echo "Plan failed with status $plan_status." >&2; exit "$plan_status" ;;
esac
```

What it does: preserves command errors while accepting both documented successful plan outcomes. `set -e` would otherwise abort on exit `2` before the script can classify it. The `||` capture is deliberate; unconditional success would hide a failed plan. In PowerShell, capture `$LASTEXITCODE` immediately after the native command and branch on the same values.

Expected behavior: an initial local-lab plan returns `2`, its post-apply no-op plan returns `0`, and a deliberately invalid input rejects planning with `1`. A positive exit-code classification does not authorize apply or prove all application behavior.

## Match the check to the claim

| Stage | Useful evidence | Does not prove |
| --- | --- | --- |
| Format | Canonical HCL formatting | Correct resource behavior. |
| Initialize without backend + validate | Dependency installation and internal consistency | Remote state access or cloud authorization. |
| Plan against the intended environment | Proposed resource and state changes | Successful apply, later drift, or application health. |
| Contract tests | Tested configuration outcomes and expected failures | Every provider/platform failure mode. |
| Apply and verification | Observed execution and selected runtime behavior | An indefinite guarantee of future health. |

Terraform test run blocks can execute `plan` or `apply`, and default to apply.[^tf-tests] A test stage using privileged credentials can create real resources; keep it scoped and verify cleanup. Terraform reports resources it could not destroy, which require follow-up rather than a green-looking log summary.[^tf-test-cli]

## Keep plan and apply connected

Associate the plan with its source revision, inputs, dependency lock, state/workspace, and identity context. Re-plan after relevant changes; do not apply a stale plan simply because a previous review was approved. Applying a saved plan does not repeat an interactive approval prompt, so automation must enforce its own explicit change gate.

The local runners use saved plans only inside their isolated teaching copies and automatically destroy the local objects. The CLI's `0`, `1`, and `2` outcomes were exercised locally; this Bash fragment was source reviewed, not executed in a hosted pipeline. Hosted credentials, artifact permissions, cloud APIs, and remote locks were not exercised. Remove only lab-owned plan files after evidence retention and close temporary sessions.

## Evidence and limits

Sources reviewed on 2026-10-29. Local examples were executed with Terraform 1.17.1; the provider lab uses hashicorp/local 2.9.1. These runs cover local state/files, not cloud IAM, remote locking, backend migration, imports, or hosted execution. The guides remain drafts with unassigned ownership. Replace angle-bracket placeholders and confirm the actual root, backend, workspace, and provider identity before adapting commands.

## Related routes

- [Module/workspace tests](../examples/module-workspace-lab/index.md).
- [Review checklist](../best-practices/review-and-automation-checklist.md).
- [Back to this section](index.md)
- [Back to Terraform](../index.md)

[^tf-plan]: [terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan)
[^tf-tests]: [Terraform test files](https://developer.hashicorp.com/terraform/language/tests)
[^tf-test-cli]: [terraform test and cleanup](https://developer.hashicorp.com/terraform/cli/commands/test)
