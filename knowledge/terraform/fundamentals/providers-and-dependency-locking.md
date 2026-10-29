---
type: Explanation
title: Providers and dependency locking
description: Distinguish provider requirements, configured aliases, module wiring,
  and reviewed dependency selections.
tags:
- terraform
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

# Providers and dependency locking

A provider is a plugin implementing resource/data-source operations. A provider requirement names its source and acceptable versions; a provider configuration supplies a particular context such as a region or endpoint. Multiple aliases configure the same installed provider version in different contexts, rather than installing one version per alias.[^tf-providers]

## Keep the responsibilities separate

| Item | Meaning | Where it belongs |
| --- | --- | --- |
| `required_providers` | Source identity and version constraint | Each module that uses the provider. |
| `provider` block | Configuration and optional alias | Normally the root, which owns runtime identity. |
| Module `providers` map | Maps caller configurations to child names | The module call. |
| Child `configuration_aliases` | Declares alternate names the child expects | The child's provider requirement. |
| `.terraform.lock.hcl` | Selected provider versions and package checksums | Reviewed with the root configuration. |

Default configuration inheritance does not replace a child's provider requirements. Aliases need deliberate wiring. Keep provider configuration blocks out of reusable child modules so the caller can control context and lifecycle.[^tf-module-providers]

In the [local provider lab](../examples/provider-alias-lab/index.md), the root configures `local.artifacts` and maps it to the child's declared `local.writer` alias. The child uses that configuration to write one non-sensitive JSON artifact. This verifies wiring without suggesting that a label changes AWS identity.

## Review selection and upgrade behavior

The provider lock file records provider selections/checksums, not remote module versions. Pin registry module versions or immutable Git revisions separately. Commit the root lock file; exclude `.terraform/`, state, and plans.[^tf-lock-file]

Run the following from the provider lab's **disposable copy**. These commands download provider metadata/packages but create no cloud resources:

```bash
terraform init -input=false -lockfile=readonly
terraform providers
terraform validate
```

What it does: installs the reviewed locked selection, shows provider requirements, and checks configuration/module consistency. Expected result: `hashicorp/local` 2.9.1 installs successfully using the supplied lock and the child alias resolves. A checksum or constraint mismatch is a dependency-review signal, not a reason to delete the lock file automatically.

Use `init -upgrade` only as a deliberate dependency change, inspect the resulting lock diff and release notes, and run relevant plans/tests. Checksums prove package consistency; they do not prove the provider's code, signer, or permissions meet your security policy. Cross-platform teams should populate/check the platforms they actually use. The teaching lock includes Windows amd64 and Linux amd64 checksum preparation. Authoring execution used Windows; the repository CI also runs both local labs on Linux, with results tied to each commit.

## Operational limits and cleanup

Do not place credentials in provider blocks or assume the backend uses the provider's credentials. A provider alias with only an empty configuration can be valid for the local provider; cloud providers may require a real region and identity.

The local-file resource can appear missing on another machine, creating a legitimate recreate diff.[^local-file] This is a teaching example, not shared deployment storage. Destroy its task-owned artifact before removing its disposable state; keep the reviewed lock file as source.

## Evidence and limits

Sources reviewed on 2026-10-29. Local examples were executed with Terraform 1.17.1; the provider lab uses hashicorp/local 2.9.1. These runs cover local state/files, not cloud IAM, remote locking, backend migration, imports, or hosted execution. The guides remain drafts with unassigned ownership. Replace angle-bracket placeholders and confirm the actual root, backend, workspace, and provider identity before adapting commands.

## Related routes

- [Backend state locking](remote-backends-and-locking.md) — a different kind of lock.
- [Environment layout](../project-structure/environment-layouts.md).
- [Back to this section](index.md)
- [Back to Terraform](../index.md)

[^tf-providers]: [Provider configuration](https://developer.hashicorp.com/terraform/language/block/provider)
[^tf-module-providers]: [Providers within modules](https://developer.hashicorp.com/terraform/language/modules/develop/providers)
[^tf-lock-file]: [Provider dependency lock file](https://developer.hashicorp.com/terraform/language/files/dependency-lock)
[^local-file]: [local_file v2.9.1](https://raw.githubusercontent.com/hashicorp/terraform-provider-local/v2.9.1/docs/resources/file.md)
