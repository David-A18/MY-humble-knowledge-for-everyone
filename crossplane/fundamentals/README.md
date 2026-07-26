# Crossplane fundamentals

## Purpose

Explain the mental model behind Crossplane: what it does, how it works, and how its Kubernetes objects map to real infrastructure.

## When to use Crossplane

Use Crossplane when you want infrastructure and platform capabilities to behave like Kubernetes APIs:

- Application teams should request infrastructure with `kubectl`, GitOps, or Kubernetes-native workflows.
- Platform teams want to publish a small internal API instead of exposing every cloud-provider field.
- Infrastructure should be reconciled continuously rather than only during a CI/CD apply job.
- Kubernetes RBAC, namespaces, events, status conditions, and controllers are already part of the operating model.

Terraform may be a better first choice when you need explicit plan review, do not operate Kubernetes as a platform control plane, or want a mature one-shot provisioning workflow with state.

## Mental model

Crossplane turns a Kubernetes cluster into a control plane for external systems.

| Concept | Meaning | Operational impact |
| --- | --- | --- |
| Desired state | The spec of a Kubernetes object. | Users declare what should exist. |
| Reconciliation | Controllers compare desired state with actual state. | Crossplane keeps trying until reality matches the object spec or reports failure. |
| Provider | A package with CRDs and controllers for an external API. | Installing a provider teaches the cluster about resources like S3 buckets or databases. |
| Managed resource | A provider-owned Kubernetes resource that maps to one external object. | Deleting or changing the Kubernetes object affects the external resource according to deletion and management policy. |
| Composite resource | A higher-level custom resource powered by Crossplane composition. | Users call a platform API instead of managing many low-level resources. |
| Composition | The implementation behind a composite resource. | Platform teams decide which real resources an abstract request creates. |
| Function | A pipeline step that produces desired composed resources. | Complex templates can be handled with Patch and Transform, Go templates, KCL, CUE, or custom code. |

## Direct managed resources

A managed resource is the most direct way to use Crossplane. The user creates a Kubernetes object from a provider API, and the provider reconciles it into an external resource.

Example:

```yaml
apiVersion: s3.aws.m.upbound.io/v1beta1
kind: Bucket
metadata:
  namespace: default
  generateName: app-logs-
spec:
  forProvider:
    region: eu-west-1
  providerConfigRef:
    name: default
    kind: ClusterProviderConfig
```

What it does: asks the AWS S3 provider to create an S3 bucket in `eu-west-1` using the cluster-wide provider configuration named `default`.

This is useful for learning and for platform teams, but it often exposes too much provider-specific detail to application teams.

## Platform APIs with XRDs, XRs, and Compositions

Crossplane's more powerful pattern is to define a custom API:

- The XRD defines the user-facing API schema, such as `AppBucket`.
- The XR is the object a user creates, such as `kind: AppBucket`.
- The Composition defines which resources the XR creates.
- Functions in the Composition pipeline generate the desired resources.
- Providers reconcile those resources into real infrastructure.

This lets a platform team publish an API like:

```yaml
apiVersion: platform.example.org/v1alpha1
kind: AppBucket
metadata:
  namespace: payments
  name: receipts
spec:
  region: eu-west-1
  environment: prod
```

What it does: lets a developer request a governed storage capability without knowing the exact S3 managed resource schema, provider config, tags, naming policy, or default security controls.

## How Crossplane differs from normal Kubernetes apps

Crossplane uses normal Kubernetes extension patterns: CRDs, controllers, status, events, RBAC, and reconciliation. The difference is that many resources it manages live outside the cluster.

| Kubernetes app controller | Crossplane provider controller |
| --- | --- |
| Reconciles pods, services, or in-cluster objects. | Reconciles cloud resources, SaaS objects, or other external APIs. |
| Status usually describes cluster-local state. | Status reports observed external state and provider errors. |
| Failure often means workload health problems. | Failure may mean cloud permissions, quota, invalid fields, region constraints, or provider API errors. |

## Important operating habits

- Treat provider credentials as production secrets.
- Use least-privilege cloud permissions for each provider configuration.
- Start with direct AWS managed resources to understand provider behavior, then hide repeated patterns behind XRDs, XRs, and Compositions.
- Prefer pipeline Compositions with Functions for new work.
- Use GitOps for Crossplane objects only after deletion policies, naming, and ownership rules are clear.
- Watch `READY`, `SYNCED`, events, and provider logs when troubleshooting.

## Related links

- [Crossplane workflow](../workflow/README.md)
- [Crossplane examples](../examples/README.md)
- [XRDs and XRs](../xrd-and-xr/README.md)
- [Compositions](../compositions/README.md)
- [Terraform vs Crossplane](../comparison/terraform-vs-crossplane.md)
- [Crossplane documentation](https://docs.crossplane.io/latest/)
- [Back to Crossplane index](../README.md)
- [Back to root index](../../README.md)
