# Crossplane on AWS

## Purpose

Use this guide to run Crossplane in Kubernetes while managing AWS resources.

## Architecture

| Component | Responsibility |
| --- | --- |
| Kubernetes cluster | Hosts Crossplane and provider controllers. |
| Crossplane provider | Adds AWS resource APIs and reconciles external resources. |
| ProviderConfig | Defines AWS authentication configuration. |
| Composition | Exposes a platform API for teams. |
| AWS resources | External resources reconciled by Crossplane controllers. |

## Production checklist

- Prefer least-privilege AWS permissions for provider controllers.
- Separate platform API design from provider implementation details.
- Use GitOps for Crossplane packages and compositions.
- Monitor managed-resource conditions and provider logs.
- Define deletion policy and recovery behavior before exposing APIs.

## Related links

- [Crossplane](../kubernetes/crossplane/README.md)
- [Crossplane compositions](../kubernetes/crossplane/compositions.md)
- [Crossplane troubleshooting](../kubernetes/crossplane/troubleshooting.md)
- [Crossplane providers documentation](https://docs.crossplane.io/latest/packages/providers/)
- [Back to cross-topic guides](README.md)
- [Back to root index](../README.md)
