---
type: Tutorial
title: Local provider alias and lock-file lab
description: Install a pinned signed provider, pass a declared alias into a child
  module, create one local artifact, and verify cleanup.
tags:
- terraform
- lab
- providers
- dependency-locking
status: draft
maturity: draft
audience: Engineering learners and platform practitioners
maintainer: unassigned
sources:
- id: tf-providers
  title: Provider configuration
  resource: https://developer.hashicorp.com/terraform/language/block/provider
- id: tf-module-providers
  title: Providers within modules
  resource: https://developer.hashicorp.com/terraform/language/modules/develop/providers
- id: tf-lock-file
  title: Provider dependency lock file
  resource: https://developer.hashicorp.com/terraform/language/files/dependency-lock
- id: local-file
  title: local_file v2.9.1
  resource: https://raw.githubusercontent.com/hashicorp/terraform-provider-local/v2.9.1/docs/resources/file.md
---

# Local provider alias and lock-file lab

Use this lab after the provider-free module exercise to see a real installed provider and explicit alias wiring. The pinned `hashicorp/local` 2.9.1 provider creates one non-sensitive JSON file inside a temporary directory. No cloud credentials are required.

## Prerequisites

Use Python 3.10+, Terraform 1.6+ within the declared `< 2.0.0` constraint, and network access to the Terraform registry/provider release endpoints. The authoring baseline is Python 3.13.17, Terraform 1.17.1, local provider 2.9.1, Windows amd64. Terraform reported the downloaded provider signed by HashiCorp. Lock preparation included Windows amd64 and Linux amd64 packages. Repository CI executes both local labs on Linux; inspect the exact commit's run for that platform's evidence.

## Run in an isolated copy

The runner creates its own temporary copy, uses a dedicated empty Terraform CLI configuration, and installs the reviewed lock without updating it. It writes and then destroys only its local teaching artifact.

```bash
python knowledge/terraform/examples/provider-alias-lab/validate-lab.py --terraform terraform
```

What it does: checks formatting, initializes with `-lockfile=readonly`, validates, saves/applies a one-create plan, checks the artifact and provider configuration, verifies a no-change plan, destroys the file, and confirms empty state before removing the copy.

## Follow the provider mapping

```text
root required_providers: hashicorp/local = 2.9.1
root configuration: local.artifacts
module providers mapping: local.writer = local.artifacts
child declaration: configuration_aliases = [local.writer]
child resource: provider = local.writer
```

What it does: separates the installed provider identity/version from configuration names at each module boundary.[^tf-providers][^tf-module-providers] Both names refer to the caller's configured local provider, not two different provider versions.

| File | Role |
| --- | --- |
| [Root](main.tf) | Exact version, root alias, child mapping, temporary artifact path. |
| [Child](child/main.tf) | Required provider/alias and `local_file` resource. |
| [Dependency lock](.terraform.lock.hcl) | Reviewed selected provider and package checksums. |
| [Runner](validate-lab.py) | Isolated plan/apply/verification/destruction. |

The lock file records provider selections, not module versions or state concurrency.[^tf-lock-file] The module is a local path included in the same source revision. No backend lock is being demonstrated.

## Expected results and troubleshooting

Expect one local file create, a parsed JSON object with `secret: false`, and a subsequent plan returning no changes. The plan configuration should map the child's resource to `local.artifacts`. Cleanup removes the file and leaves no managed state entries.

If initialization fails, inspect network/proxy, platform, provider constraint, and checksum diagnostics before changing the lock. This runner deliberately ignores user CLI mirror settings; a restricted environment may need an approved adapted copy rather than broader network access. If module wiring fails, compare both the expected child alias and root mapping.

The local provider detects a file missing on another machine as a recreate candidate.[^local-file] This lab therefore does not model shared artifact storage or cloud permission isolation. File permissions and filesystem behavior are platform-specific; no cross-platform runtime claim is made.

## Cleanup

Successful execution destroys the task-owned local file before deleting its temporary state/copy. Keep the source lock file; it is an intended dependency artifact. Do not run the example directly in a shared working directory with an existing `artifact.json`, and never repurpose a real state directory as this lab's cleanup target.

## Evidence and limits

Sources reviewed on 2026-10-29. Local examples were executed with Terraform 1.17.1; the provider lab uses hashicorp/local 2.9.1. These runs cover local state/files, not cloud IAM, remote locking, backend migration, imports, or hosted execution. The guides remain drafts with unassigned ownership. Replace angle-bracket placeholders and confirm the actual root, backend, workspace, and provider identity before adapting commands.

## Related routes

- [Provider model](../../fundamentals/providers-and-dependency-locking.md).
- [Provider-free module lab](../module-workspace-lab/index.md).
- [Back to this section](index.md)
- [Back to Terraform](../../index.md)

[^tf-providers]: [Provider configuration](https://developer.hashicorp.com/terraform/language/block/provider)
[^tf-module-providers]: [Providers within modules](https://developer.hashicorp.com/terraform/language/modules/develop/providers)
[^tf-lock-file]: [Provider dependency lock file](https://developer.hashicorp.com/terraform/language/files/dependency-lock)
[^local-file]: [local_file v2.9.1](https://raw.githubusercontent.com/hashicorp/terraform-provider-local/v2.9.1/docs/resources/file.md)
