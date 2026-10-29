---
type: Explanation
title: Ona workflows, security, and operations
description: Use existing-organization environments and background workflows with
  explicit boundaries.
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
- id: automations
  resource: https://ona.com/docs/ona/automations/overview
  title: Automations
- id: secrets
  resource: https://ona.com/docs/ona/configuration/secrets/overview
  title: Secrets
- id: runner-infrastructure
  resource: https://ona.com/docs/ona/runners/overview
  title: Runner infrastructure
---

# Ona workflows, security, and operations

## Purpose

Use existing-organization environments and background workflows with explicit boundaries.

Sources reviewed: 2026-10-29. See the [validation record](../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Existing-organization workflow

Confirm access to an existing organization and supported runner. Connect the repository using approved source-control permissions, configure the Dev Container, open an environment, and run the same verification used locally. Check current hosting and runner requirements before relying on older Gitpod instructions.[^current-ona-overview][^automations][^secrets][^runner-infrastructure]

For a first background workflow, choose a bounded task such as identifying broken documentation links. Define its trigger, allowed repositories, commands, output, and review boundary. Have it produce a proposed change and validation evidence; configure publication behavior explicitly.

## Automations

Current Ona documents manual, time-based, webhook, and pull-request triggers. Prompts and deterministic commands can be combined into a workflow. Automations, environment tasks/services, and image lifecycle hooks have different purposes; avoid launching the same service multiple times through different layers.

## Identity and data

Scope user/project/organization secrets according to actual need. Prefer short-lived federation where supported over static credentials. Inspect source-control write permissions, network egress, runner cloud permissions, and persistence. Logs, support bundles, generated patches, and image layers can expose sensitive data.

## Operations checklist

- Pin and record runner/configuration/toolchain versions.
- Monitor startup failures, automation failures, queueing, budgets, and orphaned environments.
- Define stop/delete behavior and data retention before cleanup.
- Test repository access revocation and member offboarding.
- Review agent permissions and command guardrails independently of editor access.

## Troubleshooting

Separate source authentication, runner availability, image build, lifecycle hooks, secret injection, and application errors. Collect redacted support evidence only after reproducing on the intended revision. An environment that opens successfully can still have incorrect tool versions or unauthorized background tasks.

Hosted execution was not performed during authoring; readers need the documented existing-organization access and should verify current availability.

## Related links

- [Current Ona overview](https://ona.com/docs/ona/getting-started)
- [Automations](https://ona.com/docs/ona/automations/overview)
- [Secrets](https://ona.com/docs/ona/configuration/secrets/overview)
- [Runner infrastructure](https://ona.com/docs/ona/runners/overview)
- [Back to parent index](index.md)
- [Back to major area](../index.md)
- [Back to root index](../../../README.md)

[^current-ona-overview]: [Current Ona overview](https://ona.com/docs/ona/getting-started).
[^automations]: [Automations](https://ona.com/docs/ona/automations/overview).
[^secrets]: [Secrets](https://ona.com/docs/ona/configuration/secrets/overview).
[^runner-infrastructure]: [Runner infrastructure](https://ona.com/docs/ona/runners/overview).
