# Crossplane troubleshooting

## Purpose

Diagnose Crossplane provider, composition, managed-resource, authentication, deletion, and runtime failures.

## First checks

| Symptom | Check | Likely cause |
| --- | --- | --- |
| Resource is not ready | Conditions on the composite and managed resources. | External API error, auth failure, or invalid spec. |
| Provider cannot connect | ProviderConfig and provider logs. | Credentials, network, or role permissions. |
| Composition does not render | Composition, function, and claim events. | Schema mismatch or patch error. |
| Deletion hangs | Finalizers and provider health. | Controller cannot delete external resource. |
| Resource kind is unknown | Installed APIs and provider revisions. | Provider not healthy, API version changed, or resource not activated. |
| Drift is not corrected | Managed-resource spec, management policies, and provider support. | Field not owned, policy excludes update, or provider does not reconcile that field. |

## Start with status and events

```bash
kubectl describe <resource-kind> <name> -n <namespace>
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

What it does: shows conditions, provider messages, warning events, failed references, auth errors, and dependency failures.

Read:

- `status.conditions`
- `Reason`
- `Message`
- `LastTransitionTime`
- event timestamps
- external-name annotations
- finalizers

## Managed resource diagnostics

```bash
kubectl get managed -A
kubectl get <resource-kind> <name> -n <namespace> -o yaml
kubectl describe <resource-kind> <name> -n <namespace>
```

What it does: lists managed resources and inspects the exact spec, status, annotations, conditions, and finalizers for one resource.

## Provider installation issues

```bash
kubectl get providers.pkg.crossplane.io
kubectl get providerrevisions.pkg.crossplane.io
kubectl describe provider.pkg.crossplane.io <provider-name>
kubectl describe providerrevision.pkg.crossplane.io <revision-name>
```

What it does: checks provider package installation, active revisions, dependency resolution, package pull errors, health, and API activation.

Look for:

- Package pull failures.
- Registry authentication failures.
- Dependency resolution errors.
- Incompatible package versions.
- Unhealthy provider deployments.
- Missing or inactive managed-resource definitions.

## Provider logs

```bash
kubectl get pods -n crossplane-system
kubectl logs -n crossplane-system \
  -l pkg.crossplane.io/provider=<provider-name> \
  --tail=200
```

What it does: inspects provider controller logs.

Default provider logs may be terse. Events and conditions are often faster than logs for first diagnosis.

## Crossplane core logs

```bash
kubectl logs -n crossplane-system \
  -l app=crossplane \
  --tail=200
```

What it does: inspects Crossplane core logs for package management, composition, XRD, XR, function, and operation issues.

## Authentication failures

Common symptoms include:

```text
AccessDenied
InvalidClientTokenId
ExpiredToken
NoCredentialProviders
AssumeRoleWithWebIdentity
```

Check:

```bash
kubectl get providerconfig -A
kubectl get clusterproviderconfig
kubectl describe providerconfig <name> -n <namespace>
kubectl describe clusterproviderconfig <name>
```

What it does: confirms provider configs exist and reference the expected credential source.

For EKS Pod Identity or IRSA, also check:

- Provider pod ServiceAccount.
- Pod Identity association or IRSA annotation.
- IAM trust policy.
- EKS OIDC provider when using IRSA.
- Provider pod environment variables and projected tokens.
- CloudTrail assume-role events.

## Wrong API version or kind

Symptoms:

```text
no matches for kind
the server could not find the requested resource
```

Check:

```bash
kubectl api-resources | grep -i bucket
kubectl get crds | grep -i s3
kubectl explain bucket.s3.aws.m.upbound.io
kubectl get providerrevisions.pkg.crossplane.io
```

What it does: confirms whether the API exists, whether the provider installed it, and whether the manifest uses the current group and version.

If a Crossplane CLI command fails with a missing resource message, update the CLI and confirm it supports your installed Crossplane version.

## `Ready=False` or `Synced=False`

```bash
kubectl describe <resource-kind> <name> -n <namespace>
```

What it does: shows the detailed condition reason and message behind the short `kubectl get` output.

Common causes:

- External API validation failure.
- Missing dependency.
- Missing ProviderConfig.
- IAM denial.
- Quota or rate limit.
- Immutable field change.
- External resource already exists.
- Region or account mismatch.

## Composition failures

```bash
kubectl describe <xr-kind> <xr-name> -n <namespace>
kubectl get compositions.apiextensions.crossplane.io
kubectl get compositionrevisions.apiextensions.crossplane.io
kubectl get functions.pkg.crossplane.io
```

What it does: checks XR events, composition selection, revisions, and function health.

Render locally:

```bash
crossplane composition render \
  xr.yaml \
  composition.yaml \
  functions.yaml
```

What it does: runs the function pipeline locally so patching, transform, and generated-resource errors are visible before applying to the cluster.

## Reference resolution failures

Example reference:

```yaml
bucketRef:
  name: my-bucket
```

Check:

- The referenced resource exists.
- The reference is in the same namespace when required.
- Namespaced and cluster-scoped resources are not mixed accidentally.
- Labels match when using selectors.
- The referenced resource is ready.
- The provider supports the reference field.

## Stuck deletion

```bash
kubectl get <resource-kind> <name> -n <namespace> -o yaml
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

What it does: shows deletion timestamp, finalizers, recent failures, and provider status.

Common causes:

- External resource is not empty.
- Deletion protection is enabled.
- Dependency resources still exist.
- Provider lacks delete permission.
- Provider is unhealthy.
- ProviderConfig was deleted before the resource.
- External API is unavailable.

> [!WARNING]
> Do not remove a finalizer until you understand whether the external resource should be orphaned, manually deleted, or recovered into Crossplane control.

## Potential leaked resource

Providers may protect against duplicate resources when create results are ambiguous. If you see a message like:

```text
cannot determine creation result
```

Do this:

1. Inspect creation annotations such as `crossplane.io/external-create-pending`.
2. Search the external provider for resources created around that timestamp.
3. Confirm whether a real external resource exists.
4. Decide whether to import, delete, or retry.
5. Clear annotations only after the external state is understood.

## Pause during incident response

Pause one resource:

```bash
kubectl annotate <resource-kind> <name> \
  -n <namespace> \
  crossplane.io/paused="true" \
  --overwrite
```

What it does: stops reconciliation for one resource.

Pause Crossplane core:

```bash
kubectl scale deployment/crossplane \
  -n crossplane-system \
  --replicas=0
```

What it does: stops Crossplane core. Provider controllers may still be running, so pause providers separately if needed.

> [!IMPORTANT]
> Pausing can leave incomplete operations and stale drift. Record why reconciliation was paused and what must be checked before resuming.

## Related links

- [Crossplane](README.md)
- [Crossplane compositions](compositions.md)
- [Managed resources and lifecycle](managed-resources-and-lifecycle.md)
- [Providers and authentication](providers-and-authentication.md)
- [Production, GitOps, and operations](production-gitops-and-operations.md)
- [Crossplane references](references.md)
- [Crossplane troubleshooting documentation](https://docs.crossplane.io/latest/guides/troubleshoot-crossplane/)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
