# Crossplane troubleshooting

## Purpose

Diagnose Crossplane provider, composition, and managed-resource failures.

## First checks

| Symptom | Check | Likely cause |
| --- | --- | --- |
| Resource is not ready | Conditions on the composite and managed resources. | External API error, auth failure, or invalid spec. |
| Provider cannot connect | ProviderConfig and provider logs. | Credentials, network, or role permissions. |
| Composition does not render | Composition, function, and claim events. | Schema mismatch or patch error. |
| Deletion hangs | Finalizers and provider health. | Controller cannot delete external resource. |

## Diagnostic commands

```bash
kubectl describe <resource-kind> <name>
kubectl get managed -A
kubectl logs -n crossplane-system deploy/<provider-controller>
```

What it does: inspects conditions, managed resources, and provider controller logs.

## Related links

- [Crossplane](../applications-and-tools/crossplane.md)
- [Crossplane compositions](../applications-and-tools/crossplane-compositions.md)
- [Crossplane documentation](https://docs.crossplane.io/latest/)
- [Back to Kubernetes troubleshooting](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
