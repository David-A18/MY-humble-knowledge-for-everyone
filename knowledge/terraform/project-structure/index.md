# Terraform project structure

Choose reusable contracts and state/run boundaries by ownership, credentials, and change cadence.

## Routes

| Guide | Outcome |
| --- | --- |
| [Modules and composition](modules-and-composition.md) | Root/child responsibilities, source pinning, provider mapping, and moved addresses. |
| [Environment layouts](environment-layouts.md) | Roots, shared modules, state ownership, environment isolation, and dependency contracts. |

## Evidence and follow-ups

The section was reviewed on 2026-10-29. Local execution uses Terraform 1.17.1; cloud-backed imports, remote locks/migration, hosted CI credentials, and provider-specific failure drills remain follow-up evidence. The guides identify their individual scope and lifecycle status.

[Back to Terraform](../index.md)
