# State management

## Purpose

Explain how Terraform state maps configuration to real infrastructure and why state handling is operationally sensitive.

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

## Related links

- [Terraform state documentation](https://developer.hashicorp.com/terraform/language/state)
- [Terraform backends documentation](https://developer.hashicorp.com/terraform/language/backend)
- [Back to Terraform fundamentals](README.md)
- [Back to Terraform index](../README.md)
- [Back to root index](../../README.md)
