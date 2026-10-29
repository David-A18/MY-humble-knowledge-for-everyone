# Terraform fundamentals

Start with the model, then distinguish resource identity, provider dependencies, and shared-state operating context.

## Routes

| Guide | Outcome |
| --- | --- |
| [Terraform fundamentals](terraform-fundamentals.md) | Configuration, providers, resources, state, plan, apply, and first local practice. |
| [State management](state-management.md) | Bindings, sensitive state, drift, inspection, and recovery limits. |
| [Providers and dependency locking](providers-and-dependency-locking.md) | Requirements, aliases, module wiring, package selections, and upgrade review. |
| [CLI workspaces](cli-workspaces-and-environment-isolation.md) | Separate state versus separate credentials and access controls. |
| [Remote backends and locking](remote-backends-and-locking.md) | Backend identity, S3 lock files, initialization, migration, and unexecuted remote boundaries. |

## Evidence and follow-ups

The section was reviewed on 2026-10-29. Local execution uses Terraform 1.17.1; cloud-backed imports, remote locks/migration, hosted CI credentials, and provider-specific failure drills remain follow-up evidence. The guides identify their individual scope and lifecycle status.

[Back to Terraform](../index.md)
