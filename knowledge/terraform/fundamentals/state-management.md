---
type: "Explanation"
title: "State management"
description: "Explain how Terraform state maps configuration to real infrastructure and why state handling is operationally sensitive."
tags: [terraform, state-management]
status: stable
maturity: maintained
audience: "Beginning platform engineer"
maintainer: "Unassigned"
---

# State management

## Purpose

Explain how Terraform state maps configuration to real infrastructure and why state handling is operationally sensitive.

Status: Maintained
Audience: Beginning platform engineer
Page type: Explanation
Maintainer: Unassigned
Last substantive review: 2026-09-19
Applicable versions: Terraform CLI v1.16 state documentation; linked local exercise executed with Terraform v1.13.1
Validation evidence: Source reviewed against official Terraform state documentation; linked local exercise executed with Terraform v1.13.1
Known limitations: This page introduces state handling and does not replace backend-specific operational runbooks
Next review: 2026-12-19 or after a relevant Terraform state behavior change

## Key ideas

| Concept | Why it matters |
| --- | --- |
| State file | Records resource mappings and metadata used by Terraform operations. |
| Backend | Defines where state is stored. |
| Locking | Helps prevent concurrent writes to the same state. |
| Drift | Infrastructure differs from Terraform's recorded or desired state. |

> [!CAUTION]
> Treat state as sensitive. It can contain resource identifiers and may contain sensitive values depending on providers and configuration.

## Safe operating checklist

- [ ] Confirm the workspace or backend before planning.
- [ ] Run `terraform plan` before applying changes.
- [ ] Avoid manual state edits unless there is a documented recovery need.
- [ ] Back up state before using state mutation commands.
- [ ] Use state locking where the backend supports it.

## Useful commands

```bash
terraform state list
terraform state show <resource-address>
terraform plan
```

What it does: lists tracked resources, inspects one resource address, and compares configuration with state.

## Local practice exercise

Use [Terraform local state lifecycle](../examples/local-state-lifecycle/index.md) to create, inspect, change, and destroy a local state entry without a cloud account.

## Related links

- [Terraform state documentation](https://developer.hashicorp.com/terraform/language/state)
- [Terraform backends documentation](https://developer.hashicorp.com/terraform/language/backend)
- [Terraform local state lifecycle](../examples/local-state-lifecycle/index.md)
- [Back to Terraform fundamentals](index.md)
- [Back to Terraform index](../index.md)
- [Back to root index](../../../README.md)
