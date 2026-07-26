# Crossplane

Practical Crossplane notes for building Kubernetes-native infrastructure APIs, composing cloud resources, and comparing Crossplane with Terraform.

## Index

| Section | Focus |
| --- | --- |
| [Fundamentals](fundamentals/README.md) | Crossplane mental model, providers, managed resources, XRs, XRDs, Compositions, and Functions. |
| [Workflow](workflow/README.md) | Graphical workflows for direct managed resources and composed platform APIs. |
| [Examples](examples/README.md) | Practical installation, provider, managed resource, XRD, Composition, and XR examples. |
| [XRDs and XRs](xrd-and-xr/README.md) | Custom API contracts, user-facing XR calls, Terraform module comparison, and AWS API design. |
| [Compositions](compositions/README.md) | AWS-backed Composition implementation, function pipelines, patches, revisions, and troubleshooting. |
| [Comparison](comparison/README.md) | Decision guides comparing Crossplane with Terraform. |

## What Crossplane is

Crossplane is a Kubernetes-native control plane framework. It lets platform teams expose infrastructure and application capabilities as Kubernetes APIs, then uses controllers to continuously reconcile those APIs into real resources.

In practice:

- A platform team installs Crossplane in a Kubernetes cluster.
- Providers add Kubernetes APIs for external systems such as AWS, Azure, GCP, Helm, Kubernetes, or SaaS platforms.
- Users create Kubernetes objects that describe desired infrastructure.
- Crossplane and provider controllers create, update, observe, and delete the external resources.
- Platform teams can define higher-level APIs with XRDs, let users create XRs, and implement those requests with Compositions so application teams request an AWS bucket, queue, database, or service environment without knowing every low-level cloud field.

## Core building blocks

| Building block | What it does |
| --- | --- |
| Provider | Installs APIs and controllers for an external system. |
| Managed resource | A Kubernetes object that represents one external resource, such as an S3 bucket. |
| ProviderConfig | Tells a provider how to authenticate or which account/project to use. |
| Composite resource definition | Defines a custom API schema. Usually shortened to XRD. |
| Composite resource | A user-created instance of an XRD. Usually shortened to XR. |
| Composition | Defines what resources an XR creates and how fields are mapped. |
| Function | Runs inside a Composition pipeline to generate or transform desired composed resources. |

## Crossplane v2 defaults

Crossplane v2 makes namespaced XRs and managed resources the main model. It also moves Crossplane-specific fields for XRs under `spec.crossplane`, supports composing any Kubernetes resource, and uses pipeline Compositions with Functions as the maintained Composition model.

Older Crossplane v1 patterns still appear in many examples online:

- v1 XRDs commonly used `apiextensions.crossplane.io/v1`.
- v1 used claims as namespaced proxies for cluster-scoped XRs.
- v1 supported native patch-and-transform Compositions, now replaced by Function Patch and Transform in pipeline mode.

Use v2-style namespaced XRs for new learning and new platform APIs unless you are maintaining an existing v1 control plane.

## Official documentation

- [Crossplane documentation](https://docs.crossplane.io/latest/)
- [Crossplane managed resources](https://docs.crossplane.io/latest/managed-resources/)
- [Crossplane composition](https://docs.crossplane.io/latest/composition/)
- [Crossplane packages and providers](https://docs.crossplane.io/latest/packages/)
- [Crossplane v2 changes](https://docs.crossplane.io/latest/whats-new/)

[Back to root index](../README.md)
