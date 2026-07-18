# Crossplane

## Purpose

Use this page to understand Crossplane as a Kubernetes-native control plane for external infrastructure.

## Mental model

Crossplane extends the Kubernetes API with providers and custom resources. A Crossplane provider maps Kubernetes resources to external APIs such as AWS. Crossplane reconciles desired state from Kubernetes into external infrastructure.

| Concept | Meaning |
| --- | --- |
| Provider | Package that adds APIs and controllers for an external system. |
| Managed resource | Kubernetes representation of one external resource. |
| ProviderConfig | Authentication and connection configuration for a provider. |
| Composite resource | Platform-level API exposed to users. |
| Composition | Template that maps a composite resource to managed resources. |

## When Crossplane fits

- Platform teams want to publish internal infrastructure APIs.
- Developers should request infrastructure through Kubernetes-style resources.
- Drift correction and reconciliation are desired operating behaviors.

## Articles

| Article | Purpose |
| --- | --- |
| [Compositions](compositions.md) | Design platform APIs with Crossplane compositions. |
| [Troubleshooting](troubleshooting.md) | Diagnose providers, compositions, managed resources, and deletion issues. |

## Related links

- [Crossplane compositions](compositions.md)
- [Crossplane on AWS](../../cross-topic-guides/crossplane-on-aws.md)
- [Crossplane troubleshooting](troubleshooting.md)
- [Crossplane documentation](https://docs.crossplane.io/latest/)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
