# Crossplane providers, managed resources, and compositions

## Purpose

Use this page to distinguish the Crossplane building blocks that are often confused:
providers, managed resources, composite resources, compositions, functions, and
configuration packages. It also explains how an Upbound AWS provider becomes a
Kubernetes API and how a platform team uses that API to offer a simpler feature
to its users.

## The short answer

| Object | Created or owned by | Main job | It is not |
| --- | --- | --- | --- |
| Provider | Platform operator | Install controllers and managed-resource APIs for an external system. | A reusable application or infrastructure blueprint. |
| Managed resource (MR) | Platform operator, Composition, or advanced user | Represent and reconcile one external object, such as an ECR repository. | A request for a whole platform capability. |
| XRD | Platform team | Define the schema and name of a custom platform API. | The implementation of that API. |
| XR | Platform consumer | Request one instance of the platform API. | The controller that calls AWS. |
| Composition | Platform team | Map an XR to one or more composed resources through a function pipeline. | A cloud provider integration. |
| Function | Platform team or package maintainer | Generate, transform, validate, or enrich composition output. | A provider controller. |
| Configuration package | Platform team | Distribute XRDs, Compositions, Functions, and dependencies as one versioned platform release. | A replacement for provider credentials. |

The important boundary is this: a **provider supplies the capability to manage
an external API**, while a **Composition uses that capability to implement a
product-like platform API**. A managed resource is the individual object that
the provider reconciles.

## How the pieces work together

```text
Platform operator installs Crossplane and an AWS ECR provider
                         |
                         v
Provider installs Repository and other ECR managed-resource APIs
                         |
Platform team defines an XRD and a Composition using those APIs
                         |
                         v
Application team creates an XR, for example ApplicationDelivery
                         |
                         v
Composition generates an ECR Repository and Kubernetes workload objects
                         |
                         v
The ECR provider reconciles the Repository with the AWS ECR API
```

Kubernetes stores desired state for every object in this flow. The provider
controller, not `kubectl`, authenticates and calls AWS. Crossplane core runs
the composition pipeline; the provider controller reconciles the managed
resource it produces.

## What a provider is

A provider is an OCI package installed through a Crossplane `Provider` object.
It adds Kubernetes API types for the external resources it supports and starts
controller pods that continuously reconcile those APIs with the external
service. Providers are responsible for authentication, observation, external
API calls, and controller logic.

For example, the Upbound AWS ECR provider is a service-focused provider package
from the AWS provider family. Its available managed resources and exact schema
are determined by the installed package version. The marketplace is the source
for package provenance and resource discovery; the cluster is the source of
truth for the fields a manifest may use.

### Provider installation lifecycle

| Stage | What Crossplane does | What to verify |
| --- | --- | --- |
| Package requested | Reads `spec.package` from the `Provider` object. | Pin a reviewed version or digest. |
| Revision installed | Pulls the OCI package and creates a `ProviderRevision`. | `INSTALLED` and package events. |
| APIs activated | Makes provider managed-resource APIs available. | `kubectl api-resources` and activation policy. |
| Runtime starts | Creates the provider controller deployment and service account. | Pods, runtime configuration, and workload identity. |
| Reconciliation begins | Watches MRs and calls the external API through a ProviderConfig. | `HEALTHY`, conditions, and logs. |

### Install an ECR provider deliberately

Use the current package location, a reviewed version or digest, and the
provider's compatibility information from the official marketplace. Do not
substitute a version from an old example.

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-aws-ecr
spec:
  package: xpkg.upbound.io/upbound/provider-aws-ecr:<reviewed-version-or-digest>
  revisionActivationPolicy: Manual
```

What it does: asks Crossplane to install an ECR provider package but leaves
activation of a newly installed revision under operator control. `Manual` is a
useful production choice when a provider upgrade might change CRDs or provider
behavior; teams may choose automatic activation after testing.

> [!IMPORTANT]
> A package name, API group, resource kind, and field can differ by provider
> family and version. Consult the [Upbound AWS ECR provider](https://marketplace.upbound.io/providers/upbound/provider-aws-ecr), then validate the installed API before applying a resource manifest.

### Inspect package health and the installed schema

```bash
kubectl get providers.pkg.crossplane.io
kubectl get providerrevisions.pkg.crossplane.io
kubectl get pods -n crossplane-system
kubectl api-resources | grep -i ecr
kubectl explain repository.ecr.aws.m.upbound.io.spec.forProvider
```

What it does: checks package installation and runtime health, then discovers
the API resource and its accepted fields in the current cluster. If the final
command fails, do not guess the API group or schema; inspect the package
revision, provider documentation, and API discovery output first.

## What a managed resource is

A managed resource is a provider-defined Kubernetes object that represents one
external object. An ECR `Repository`, an S3 `Bucket`, and an EC2 `VPC` are
examples. A managed resource usually contains desired external settings in
`spec.forProvider`, a `providerConfigRef` that selects credentials and account
targeting, and observed state in `status`.

### Direct managed resource example

```yaml
apiVersion: ecr.aws.m.upbound.io/v1beta1
kind: Repository
metadata:
  name: payments-api
  namespace: payments
spec:
  forProvider:
    region: <aws-region>
    name: payments-api
    imageTagMutability: IMMUTABLE
  providerConfigRef:
    name: payments-aws
```

What it does: directly asks the installed ECR provider to reconcile one AWS
ECR repository. The example is useful for an operator or an advanced team that
is intentionally allowed to use AWS-specific APIs.

> [!NOTE]
> This is an API shape example, not a promise that every installed provider
> version exposes the same fields. Use `kubectl explain` before applying it.

### Managed-resource lifecycle

```text
Desired MR stored in Kubernetes
        |
Provider reads ProviderConfig credentials and endpoint settings
        |
Provider observes the external object
        |
Provider creates, updates, or only observes according to its policy and schema
        |
Provider records external identity, conditions, and observed status
```

An MR does not become ready just because `kubectl apply` succeeded. Read its
`status.conditions`, events, provider logs, and external service state. See
[Managed resources and lifecycle](managed-resources-and-lifecycle.md) for
import, drift, references, management policies, finalizers, and safe deletion.

## What a Composition is

A Composition is platform-owned implementation logic for an XR. It selects a
function pipeline that creates the desired composed resources. Those resources
may be provider MRs, ordinary Kubernetes resources, or a mixture of both.

For example, a `SecureRepository` XR can expose only a name and a region. Its
Composition can create an ECR repository with the organization’s preferred
tags, mutability setting, lifecycle policy, and access controls. Consumers ask
for a feature; the platform owns how it is delivered.

| Question | Direct MR | Composition-backed XR |
| --- | --- | --- |
| Who selects cloud-provider fields? | The resource author. | The platform implementation. |
| How many resources are created? | Usually one. | One or many. |
| Is the user API provider-specific? | Usually yes. | It can be stable and intent-focused. |
| Who controls defaults and guardrails? | The MR author plus policy. | The platform team plus policy. |
| Who calls AWS? | The provider controller. | Still the provider controller for each generated MR. |

> [!IMPORTANT]
> A Composition never replaces a provider. Without a provider that understands
> the generated ECR `Repository` resource, Crossplane cannot reconcile it with
> AWS. Without a Composition, a provider still supports direct managed
> resources.

## Functions and configuration packages

Composition Functions add programmable or reusable behavior to a Composition
pipeline. Use a declarative function such as Patch and Transform for fixed
resource templates. Use a tested templating or language function when the API
needs dynamic generation, loops, richer validation, or complex data shaping.

A Configuration package bundles a platform API and its dependencies into a
versioned OCI release. It commonly contains XRDs and Compositions and declares
the provider and Function packages it needs. This allows a platform team to
promote a reviewed capability between environments without making application
teams install individual providers.

| Need | Use |
| --- | --- |
| Connect Crossplane to AWS ECR | Provider plus ProviderConfig. |
| Create one AWS-specific repository | Direct managed resource. |
| Offer a standardized secure repository to teams | XRD, XR, Composition, and provider-managed resources. |
| Generate a variable number of resources | Composition Function. |
| Ship the whole platform capability | Configuration package. |

## ProviderConfig ownership

ProviderConfig objects decide which credentials and target account a provider
uses. They are not interchangeable with the provider package or Composition.

| Configuration type | Scope | Good use |
| --- | --- | --- |
| `ProviderConfig` | Namespace | Tenant, team, or environment-specific AWS identity. |
| `ClusterProviderConfig` | Cluster | Deliberately shared platform identity. |

Keep application consumers from selecting privileged provider configs unless
that choice is part of the platform contract. Combine Kubernetes RBAC,
namespaces, provider IAM roles, admission policy, and AWS guardrails to limit
blast radius.

## Choosing the right level of abstraction

Start with a direct MR when learning a provider, importing a small number of
resources, or exposing cloud-specific controls is intentional. Create an XR and
Composition when the same safe pattern will be requested repeatedly and users
should not need to understand every provider field. Package the capability when
it needs to be consistently installed and promoted across control planes.

The [Application delivery platform API](application-delivery-platform-api.md)
uses this model to generate an ECR repository and Kubernetes delivery resources
from one request.

## Related links

- [Application delivery platform API](application-delivery-platform-api.md)
- [Providers and authentication](providers-and-authentication.md)
- [Managed resources and lifecycle](managed-resources-and-lifecycle.md)
- [Crossplane compositions](compositions.md)
- [Crossplane component model](component-model.md)
- [Crossplane providers documentation](https://docs.crossplane.io/latest/packages/providers/)
- [Crossplane compositions documentation](https://docs.crossplane.io/latest/composition/compositions/)
- [Upbound AWS ECR provider](https://marketplace.upbound.io/providers/upbound/provider-aws-ecr)
- [Back to Crossplane index](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
