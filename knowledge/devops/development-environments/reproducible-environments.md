---
type: Explanation
title: Reproducible development environments
description: Make a repository's toolchain and startup behavior explicit.
tags:
- devops
- development-environments
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: dev-container-specification
  resource: https://containers.dev/implementors/spec/
  title: Dev Container specification
- id: ona-container-configuration
  resource: https://ona.com/docs/ona/configuration/devcontainer/overview
  title: Ona container configuration
---

# Reproducible development environments

## Purpose

Make a repository's toolchain and startup behavior explicit.

Sources reviewed: 2026-10-29. See the [validation record](../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## The layers

A development image provides OS packages and language runtimes. Dev Container configuration chooses the image/build, editor integration, users, ports, and lifecycle commands. The workspace contains source and local state. Platform configuration adds hosting, secrets, tasks/services, and organization policy.[^dev-container-specification][^ona-container-configuration]

An environment definition is executable configuration: lifecycle hooks, package installation, and extensions can execute code with the environment's permissions. Review changes before opening an untrusted repository.

## Reproducibility choices

Pin runtime/image versions, record dependency locks, minimize interactive setup, and keep secrets outside the repository. Image tags can move; production-grade reproducibility should record image digests and verified update processes.

Separate one-time setup, per-start services, and explicit user commands. Rebuilding a container is different from restarting it; neither should silently destroy source or inject production credentials.

```json
{
  "name": "Knowledge-base Python lab",
  "image": "mcr.microsoft.com/devcontainers/python:1-3.13-bookworm",
  "remoteUser": "vscode",
  "postCreateCommand": "python -c \"import sqlite3; print(sqlite3.sqlite_version)\""
}
```

What it does: selects a Python environment and checks SQLite during initial creation. It does not add cloud credentials, mount a Docker socket, or launch a hosted service.

## Acceptance criteria

A new user can open the repository, run a stated validation command, rebuild, and obtain the same required tools. Test ports, user/file permissions, persistent data, offline/network assumptions, and secret injection separately.

For team operation, assign image/dependency ownership and update frequency. Cache/prebuild support can improve startup time but should not bypass verification of the source revision or leak secrets into shared image layers.

## Related links

- [Dev Container specification](https://containers.dev/implementors/spec/)
- [Ona container configuration](https://ona.com/docs/ona/configuration/devcontainer/overview)
- [Back to parent index](index.md)
- [Back to major area](../index.md)
- [Back to root index](../../../README.md)

[^dev-container-specification]: [Dev Container specification](https://containers.dev/implementors/spec/).
[^ona-container-configuration]: [Ona container configuration](https://ona.com/docs/ona/configuration/devcontainer/overview).
