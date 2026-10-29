---
type: Tutorial
title: Local Dev Container lab
description: Validate a portable environment without a hosted account.
tags:
- devops
- development-environments
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: dev-container-cli
  resource: https://containers.dev/supporting#devcontainer-cli
  title: Dev Container CLI
- id: dev-container-specification
  resource: https://containers.dev/implementors/spec/
  title: Dev Container specification
---

# Local Dev Container lab

## Purpose

Validate a portable environment without a hosted account.

Sources reviewed: 2026-10-29. See the [validation record](../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Prerequisites and files

Use a local Docker-compatible container runtime plus a Dev Container-capable editor or CLI. The sample config is in [examples/local](examples/local/index.md). It pins a Python 3.13 image tag and uses no repository credentials. The CLI example pins `@devcontainers/cli@0.80.0`.[^dev-container-cli][^dev-container-specification]

## Open locally

Open `examples/local` as the workspace folder and choose your editor's “Reopen in Container” action. Alternatively, from this series directory:

```bash
pnpm dlx @devcontainers/cli@0.80.0 read-configuration --workspace-folder examples/local
pnpm dlx @devcontainers/cli@0.80.0 up --workspace-folder examples/local
pnpm dlx @devcontainers/cli@0.80.0 exec --workspace-folder examples/local python verify.py
```

What it does: parses the configuration, starts the container, and executes the verification script. `read-configuration` does not prove the container starts. CLI/image downloads require network access; `up` and `exec` require the container runtime.

## Expected output

The verification script creates an in-memory FTS5 table and retrieves its synthetic row. Expect `Python and SQLite FTS5 ready`. Rebuild the container and rerun it to check repeatable setup. Source persists according to workspace mounting; the in-memory database is intentionally disposable.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Runtime unreachable | Runtime service/context and host permissions. |
| Image cannot pull | Registry access, tag, proxy, architecture. |
| Files not writable | Remote user and mount ownership. |
| Hook fails | Working directory and runtime command availability. |
| Different dependencies after rebuild | Floating transitive dependencies or mutable image tags. |

## Cleanup

Stop/remove only the container created for this workspace using the editor/runtime's displayed identity. Keep source mounts and unrelated images/volumes. Runtime startup was not executed on the authoring host; the configuration and Python verification are checked separately.

## Related links

- [Dev Container CLI](https://containers.dev/supporting#devcontainer-cli)
- [Dev Container specification](https://containers.dev/implementors/spec/)
- [Back to parent index](index.md)
- [Back to major area](../index.md)
- [Back to root index](../../../README.md)

[^dev-container-cli]: [Dev Container CLI](https://containers.dev/supporting#devcontainer-cli).
[^dev-container-specification]: [Dev Container specification](https://containers.dev/implementors/spec/).
