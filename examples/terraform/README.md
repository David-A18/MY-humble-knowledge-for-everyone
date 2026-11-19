# Terraform examples

Use disposable local copies. These examples practice state, modules, aliases, and files without cloud provisioning.

## Routes

| Guide | Outcome |
| --- | --- |
| [First local state lifecycle](local-state-lifecycle/README.md) | The beginner init/plan/apply/inspect/change/destroy route. |
| [Modules and workspaces](module-workspace-lab/README.md) | Validated inputs, stable keys, tests, ID-preserving refactor, and two local states. |
| [Provider aliases and lock file](provider-alias-lab/README.md) | Pinned local provider, explicit child mapping, a local artifact, and cleanup. |

## Evidence and follow-ups

The section was reviewed on 2026-10-29. Local execution uses Terraform 1.17.1; cloud-backed imports, remote locks/migration, hosted CI credentials, and provider-specific failure drills remain follow-up evidence. The guides identify their individual scope and lifecycle status.

[Back to Terraform](../../knowledge/terraform/index.md)
