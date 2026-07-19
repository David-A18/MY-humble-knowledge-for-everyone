# Crossplane managed resources and lifecycle

## Purpose

Use this page to understand direct managed resources, reconciliation fields, references, import behavior, pause controls, and deletion safety in Crossplane.

Managed resources are the provider-defined Kubernetes APIs that represent external resources. An AWS S3 `Bucket`, an AWS EC2 `Instance`, a Google Cloud GKE `Cluster`, or another provider resource becomes a Kubernetes object with desired state, observed state, conditions, and lifecycle metadata.

## Managed resource shape

Most managed resources follow this pattern:

```yaml
apiVersion: s3.aws.m.upbound.io/v1beta1
kind: Bucket
metadata:
  name: platform-lab-bucket
  namespace: default
spec:
  forProvider:
    region: eu-west-1
    tags:
      Environment: lab
      ManagedBy: crossplane
  providerConfigRef:
    name: default
    kind: ClusterProviderConfig
  managementPolicies:
    - "*"
```

What it does: declares a provider-owned resource with desired settings under `spec.forProvider`, an explicit provider config reference, and full management permissions.

| Field | Use | Notes |
| --- | --- | --- |
| `apiVersion` and `kind` | Select the provider API endpoint. | Verify against the installed provider version. |
| `metadata.name` | Kubernetes object name. | May differ from the real external name. |
| `metadata.namespace` | Tenant or environment boundary for namespaced APIs. | Crossplane v2 favors namespaced managed resources. |
| `spec.forProvider` | Desired external configuration. | Crossplane normally reconciles drift back to these values. |
| `spec.initProvider` | Creation-time values. | Later changes are not continuously enforced. |
| `providerConfigRef` | Provider authentication and connection choice. | Avoid relying on implicit defaults in production. |
| `managementPolicies` | Allowed actions. | Provider support can vary. |
| `status.atProvider` | Observed external state. | Do not edit status. |
| `status.conditions` | Readiness and reconciliation status. | First place to inspect failures. |

## Reconciliation flow

```text
kubectl apply -f resource.yaml
        |
Kubernetes stores the managed resource
        |
Provider controller observes the resource
        |
Provider authenticates through ProviderConfig
        |
Provider observes, creates, updates, or deletes the external resource
        |
Provider writes status, conditions, and external-name data
```

`kubectl apply` returning successfully only means Kubernetes accepted the object. It does not mean the external resource is ready.

### Watch readiness

```bash
kubectl get buckets.s3.aws.m.upbound.io -n default -w
```

What it does: watches the managed-resource summary columns until the provider reports readiness.

Expected output resembles:

```text
NAME                  SYNCED   READY   EXTERNAL-NAME
platform-lab-bucket   True     True    platform-lab-bucket
```

### Inspect full status

```bash
kubectl get bucket.s3.aws.m.upbound.io platform-lab-bucket \
  -n default \
  -o yaml
```

What it does: shows `status.atProvider`, `status.conditions`, external-name annotations, creation annotations, finalizers, and the exact stored spec.

## Desired and observed state

| Location | Meaning | Reader habit |
| --- | --- | --- |
| `spec.forProvider` | Settings Crossplane should enforce. | Treat as desired state. |
| `spec.initProvider` | Settings used during create, then ignored for ongoing enforcement. | Use for fields an autoscaler or external system should later own. |
| `status.atProvider` | Real observed provider state. | Read it; do not patch it. |
| `status.conditions` | Structured readiness and sync state. | Read `type`, `status`, `reason`, and `message`. |

> [!IMPORTANT]
> Provider schemas define which fields exist, which are required, and which are immutable. Always verify with the installed provider, not an old blog post or video.

### Discover installed schema

```bash
kubectl api-resources | grep -i bucket
kubectl explain bucket.s3.aws.m.upbound.io.spec.forProvider
```

What it does: confirms the resource kind and shows the provider schema currently installed in the cluster.

## References between managed resources

Provider resources often need identifiers from other resources. Prefer Kubernetes-native references when they are available.

| Reference style | Example | When to use it |
| --- | --- | --- |
| External identifier | `vpcId: vpc-0123456789abcdef0` | Importing or linking to a resource not represented as a Kubernetes object. |
| Name reference | `vpcIdRef.name: platform-vpc` | Linking to another managed resource by Kubernetes name. |
| Selector | `vpcIdSelector.matchLabels` | Selecting by labels when names differ by environment. |
| Controller reference | `matchControllerRef: true` | Linking resources composed by the same XR. |

### Reference by name

```yaml
apiVersion: ec2.aws.m.upbound.io/v1beta1
kind: Subnet
metadata:
  name: app-private-a
  namespace: platform
spec:
  forProvider:
    region: eu-west-1
    cidrBlock: 10.0.1.0/24
    vpcIdRef:
      name: platform-vpc
```

What it does: asks the provider to resolve the real VPC ID from the managed resource named `platform-vpc`.

## External names and import

Crossplane maps the Kubernetes object to the real provider object with:

```yaml
metadata:
  annotations:
    crossplane.io/external-name: real-provider-identifier
```

Examples include S3 bucket names, VPC IDs, database identifiers, ARNs, or provider-specific IDs.

### Observe an existing resource

```yaml
apiVersion: s3.aws.m.upbound.io/v1beta1
kind: Bucket
metadata:
  name: existing-logs-bucket
  namespace: platform
  annotations:
    crossplane.io/external-name: existing-company-logs
spec:
  managementPolicies:
    - Observe
  forProvider:
    region: eu-west-1
  providerConfigRef:
    name: default
    kind: ClusterProviderConfig
```

What it does: lets Crossplane observe an existing external bucket without creating, updating, or deleting it.

> [!WARNING]
> Import and observe-only behavior depends on provider support and exact schema. Test in a sandbox before using it for production resources.

## Management policies

`managementPolicies` define which actions the provider may take.

| Policy | Meaning |
| --- | --- |
| `*` | Full provider-supported control. |
| `Observe` | Observe the external resource. |
| `Create` | Create the external resource if missing. |
| `Update` | Update provider-owned fields. |
| `Delete` | Delete the external resource when the managed resource is deleted. |
| `LateInitialize` | Populate unspecified spec fields from provider defaults. |

### Prevent Crossplane from deleting an external resource

```yaml
managementPolicies:
  - Observe
  - Create
  - Update
  - LateInitialize
```

What it does: allows observation, creation, updates, and late initialization, but omits deletion permission.

> [!IMPORTANT]
> Providers decide which management policies they support. Confirm behavior with `kubectl explain`, provider documentation, and a sandbox test.

## Pause and manual reconciliation

### Pause one resource

```bash
kubectl annotate bucket.s3.aws.m.upbound.io platform-lab-bucket \
  -n default \
  crossplane.io/paused="true" \
  --overwrite
```

What it does: pauses reconciliation for a single managed resource.

### Request reconciliation

```bash
kubectl annotate bucket.s3.aws.m.upbound.io platform-lab-bucket \
  -n default \
  crossplane.io/reconcile-requested-at="$(date +%s)" \
  --overwrite
```

What it does: asks the provider to reconcile the resource soon, which is useful after a manual drift test.

## Deletion and finalizers

When a managed resource is deleted, Kubernetes marks it for deletion and waits for Crossplane finalizers. The provider must delete or detach the external resource before the Kubernetes object can disappear.

Common deletion blockers:

- External resource is not empty.
- AWS deletion protection is enabled.
- Dependencies are still attached.
- Provider lacks delete permissions.
- ProviderConfig or credentials were removed too early.
- Provider pod is unhealthy.

> [!WARNING]
> Do not remove Crossplane finalizers just to clear a stuck object. First decide whether orphaning the external resource is acceptable and document the recovery path.

## Related links

- [Crossplane](README.md)
- [Deployment patterns and references](deployment-patterns-and-references.md)
- [Providers and authentication](providers-and-authentication.md)
- [Crossplane troubleshooting](troubleshooting.md)
- [Crossplane references](references.md)
- [Managed resources documentation](https://docs.crossplane.io/latest/managed-resources/managed-resources/)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
