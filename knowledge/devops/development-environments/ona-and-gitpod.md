---
type: Explanation
title: Ona and Gitpod explained
description: Understand the evolution from cloud development environments to the current
  Ona platform.
tags:
- devops
- development-environments
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: current-ona-overview
  resource: https://ona.com/docs/ona/getting-started
  title: Current Ona overview
- id: classic-payg-sunset
  resource: https://ona.com/stories/gitpod-classic-payg-sunset
  title: Classic PAYG sunset
- id: classic-migration-history
  resource: https://ona.com/stories/migrating-from-classic-to-ona
  title: Classic migration history
---

# Ona and Gitpod explained

## Purpose

Understand the evolution from cloud development environments to the current Ona platform.

Sources reviewed: 2026-10-29. See the [validation record](../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Product history and availability

Gitpod became known for reproducible cloud development environments tied to repositories. Ona evolved from Gitpod and describes its current platform in terms of background software-engineering agents, projects, environments, runners, and automations.[^current-ona-overview][^classic-payg-sunset][^classic-migration-history]

As checked on **2026-10-29**, Ona's getting-started page says new customer signup is closed; existing customers and members joining existing organizations can continue. Do not assume a new reader can create an account. The 2025 Gitpod Classic PAYG sunset notice had a specific timeline and excluded Enterprise customers from that same schedule; it is not a universal shutdown date for every installation.

## What it can be used for

- Consistent toolchains and faster onboarding.
- Isolated development/test environments for branches or tasks.
- Interactive work through supported editors.
- Background code-maintenance workflows with bounded access.
- Organization-managed compute, identity, secrets, and policy.

| Term | Meaning |
| --- | --- |
| Project | Repository/workflow configuration and team context. |
| Environment | A running workspace with its development toolchain. |
| Runner | Infrastructure executing workloads in the supported hosting model. |
| Agent | Software that acts on a task using configured tools and permissions. |
| Automation | Triggered workflow of prompts/commands with operational controls. |

## Choose by requirement

Use a local Dev Container when a portable environment is enough. Evaluate hosted environments when centralized compute, isolation, onboarding, or background execution justifies operational and access dependencies. Existing Ona organizations must also assess runner support, residency, connectivity, and cost.

The supplied local lab needs no Ona account. Hosted instructions describe existing-organization workflows and must be checked against the organization's current version and policies.

## Related links

- [Current Ona overview](https://ona.com/docs/ona/getting-started)
- [Classic PAYG sunset](https://ona.com/stories/gitpod-classic-payg-sunset)
- [Classic migration history](https://ona.com/stories/migrating-from-classic-to-ona)
- [Back to parent index](index.md)
- [Back to major area](../index.md)
- [Back to root index](../../../README.md)

[^current-ona-overview]: [Current Ona overview](https://ona.com/docs/ona/getting-started).
[^classic-payg-sunset]: [Classic PAYG sunset](https://ona.com/stories/gitpod-classic-payg-sunset).
[^classic-migration-history]: [Classic migration history](https://ona.com/stories/migrating-from-classic-to-ona).
