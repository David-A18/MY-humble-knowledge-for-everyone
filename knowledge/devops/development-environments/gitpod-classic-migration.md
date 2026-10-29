---
type: Explanation
title: Gitpod Classic configuration migration
description: Translate legacy environment behavior without assuming old configuration
  remains current.
tags:
- devops
- development-environments
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: 2025-migration-guidance
  resource: https://ona.com/stories/migrating-from-classic-to-ona
  title: 2025 migration guidance
- id: current-dev-container-configuration
  resource: https://ona.com/docs/ona/configuration/devcontainer/overview
  title: Current Dev Container configuration
- id: current-task-service-schema
  resource: https://ona.com/docs/ona/reference/ona-config-schema
  title: Current task/service schema
---

# Gitpod Classic configuration migration

## Purpose

Translate legacy environment behavior without assuming old configuration remains current.

Sources reviewed: 2026-10-29. See the [validation record](../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Historical versus current formats

Gitpod Classic used `.gitpod.yml` for images, tasks, ports, and editor configuration. The 2025 migration documentation described moving to Dev Containers plus `.gitpod/automations.yml` and a historical `gitpod env migrate` command. Current Ona documentation also describes tasks/services through `.ona/config.yaml` and separate automation features.[^2025-migration-guidance][^current-dev-container-configuration][^current-task-service-schema]

Treat the 2025 command/output as historical migration context, not an instruction to install an obsolete CLI or assume a file is supported today. Follow the current organization/runner documentation when producing the final configuration.

## Inventory first

Record image packages, runtime versions, init/start tasks, long-running services, forwarded ports, extensions, workspace persistence, secrets, network requirements, and source-control access. Distinguish developer setup from background agent automation.

| Legacy intent | Migration destination |
| --- | --- |
| Development image/toolchain | Dev Container image/build and features. |
| Initial dependency setup | Appropriate Dev Container lifecycle command. |
| Long-running task/service | Current Ona task/service configuration or local explicit command. |
| Port behavior | Dev Container/platform port configuration. |
| Secrets and environment values | Current user/project/organization secret mechanism. |
| Background workflow | Current Ona Automation, after reviewing permissions/triggers. |

## Validate behavior

Open a fresh environment, install dependencies, execute tests, start required services, inspect forwarded-port access, stop/restart, and rebuild. Verify which files persist and that credentials do not leak into images or logs. Account, organization, billing, settings, and secrets are separate migration concerns; do not assume they transfer automatically.

## Rollback

Retain the reviewed legacy config in version history and document the new environment's prerequisites. A config conversion is not proof of a successful migration. Do not remove the old operational route until the replacement passes the team's actual development tasks.

## Related links

- [2025 migration guidance](https://ona.com/stories/migrating-from-classic-to-ona)
- [Current Dev Container configuration](https://ona.com/docs/ona/configuration/devcontainer/overview)
- [Current task/service schema](https://ona.com/docs/ona/reference/ona-config-schema)
- [Back to parent index](index.md)
- [Back to major area](../index.md)
- [Back to root index](../../../README.md)

[^2025-migration-guidance]: [2025 migration guidance](https://ona.com/stories/migrating-from-classic-to-ona).
[^current-dev-container-configuration]: [Current Dev Container configuration](https://ona.com/docs/ona/configuration/devcontainer/overview).
[^current-task-service-schema]: [Current task/service schema](https://ona.com/docs/ona/reference/ona-config-schema).
