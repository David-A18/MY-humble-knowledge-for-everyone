# State management

## Purpose

Explain how Terraform state maps configuration to real infrastructure and why state handling is operationally sensitive.

Status: Draft
Audience: Beginning platform engineer
Page type: Explanation
Maintainer: Unassigned
Last substantive review: 2026-09-18
Applicable versions: Terraform CLI 1.4.0 or newer for the linked local exercise; locally executed with Terraform v1.13.1
Validation evidence: Source reviewed, statically checked, and linked local exercise executed with Terraform v1.13.1
Known limitations: This page introduces state handling and does not replace backend-specific operational runbooks
Next review: After the first completed local Terraform exercise run

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

Use [Terraform local state lifecycle](../examples/local-state-lifecycle/README.md) to create, inspect, change, and destroy a local state entry without a cloud account.

## Related links

- [Terraform state documentation](https://developer.hashicorp.com/terraform/language/state)
- [Terraform backends documentation](https://developer.hashicorp.com/terraform/language/backend)
- [Terraform local state lifecycle](../examples/local-state-lifecycle/README.md)
- [Back to Terraform fundamentals](README.md)
- [Back to Terraform index](../README.md)
- [Back to root index](../../README.md)
