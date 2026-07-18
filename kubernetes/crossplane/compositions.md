# Crossplane compositions

## Purpose

Use this page to understand Crossplane compositions as the boundary between platform APIs and concrete infrastructure.

## Composition design

| Layer | Owner | Responsibility |
| --- | --- | --- |
| Composite Resource Definition | Platform team | Defines the platform API shape. |
| Composition | Platform team | Maps the platform API to managed resources. |
| Composite resource claim | Application or service team | Requests infrastructure through the platform API. |
| Managed resources | Crossplane controllers | Reconcile external resources. |

## Design rules

- Keep the platform API small and stable.
- Hide provider-specific details unless users must choose them.
- Version APIs when breaking changes are needed.
- Test rendering and reconciliation before exposing a composition broadly.
- Decide how secrets and connection details flow to workloads.

## Related links

- [Crossplane](README.md)
- [Crossplane composition documentation](https://docs.crossplane.io/latest/concepts/compositions/)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
