---
type: Explanation
title: CLI workspaces and environment isolation
description: Choose CLI workspaces only when separate state fits the same trust boundary,
  and verify the selected state before operations.
tags:
- terraform
- workspaces
- state
status: draft
maturity: draft
audience: Engineering learners and platform practitioners
maintainer: unassigned
sources:
- id: tf-workspaces
  title: CLI workspace state model
  resource: https://developer.hashicorp.com/terraform/language/state/workspaces
- id: tf-s3-backend
  title: S3 backend and locking
  resource: https://developer.hashicorp.com/terraform/language/backend/s3
---

# CLI workspaces and environment isolation

A Terraform CLI workspace selects a separate state for the same configuration/backend. It does not automatically select a different account, provider credential, input file, or access-control boundary. HCP Terraform workspaces are a separate platform concept with configuration, runs, variables, and permissions; do not treat the names as interchangeable.[^tf-workspaces]

## Choose by trust and lifecycle

| Requirement | Better starting point |
| --- | --- |
| Short-lived copies with the same operators and permission boundary | CLI workspaces may fit. |
| Production and development require separate credentials/read access | Separate roots/backends and explicit identity controls. |
| Independent teams deploy components on different schedules | Separate state ownership and published interfaces. |
| Hosted remote execution and approvals | Evaluate the platform's workspace/run model deliberately. |

HashiCorp explicitly cautions against CLI workspaces for system decomposition or deployments requiring separate credentials/access controls.[^tf-workspaces] A name like `production` is a label, not protection. Include the selected workspace in review and the target identity in your actual environment checks.

## Inspect before changing state

```bash
terraform workspace show
terraform workspace list
terraform state list
```

What it does: identifies the selected CLI state and its tracked addresses. A newly created local workspace can report that no state file exists until its first apply. Do not interpret that specific condition as permission to import or recreate a real environment blindly; confirm whether you intended a fresh state.

With S3, the default workspace uses the configured `key`; other workspace paths incorporate the workspace prefix/name. Access policy must cover the intended paths and locking objects.[^tf-s3-backend] Do not infer the bucket/key solely from the workspace label.

## Practice in the local-only lab

The [module/workspace lab](../examples/module-workspace-lab/index.md) creates two built-in state records in `default`, selects a new `preview` workspace, confirms fresh state, applies the same configuration there, and verifies that `default` remains unchanged. Its output records the selected workspace for observation; that does not create a security boundary.

Workspace creation, selection, and deletion change the CLI's operating context. In a real repository, review backend, workspace, inputs, provider aliases, and cloud identity together before planning or applying. Automation should select these explicitly rather than inherit a developer's last local choice or `TF_WORKSPACE` setting silently.

## Cleanup and recovery

For a disposable workspace, first destroy only its intended resources and confirm the state is empty. Select another workspace before deleting the empty one. Do not use force deletion to erase a workspace that still owns infrastructure. The lab runner performs cleanup for both states and then deletes `preview`; remote workspace lifecycle and backend permissions remain environment-specific follow-ups.

## Evidence and limits

Sources reviewed on 2026-10-29. Local examples were executed with Terraform 1.17.1; the provider lab uses hashicorp/local 2.9.1. These runs cover local state/files, not cloud IAM, remote locking, backend migration, imports, or hosted execution. The guides remain drafts with unassigned ownership. Replace angle-bracket placeholders and confirm the actual root, backend, workspace, and provider identity before adapting commands.

## Related routes

- [Root/environment layouts](../project-structure/environment-layouts.md).
- [State management](state-management.md).
- [Back to this section](index.md)
- [Back to Terraform](../index.md)

[^tf-workspaces]: [CLI workspace state model](https://developer.hashicorp.com/terraform/language/state/workspaces)
[^tf-s3-backend]: [S3 backend and locking](https://developer.hashicorp.com/terraform/language/backend/s3)
