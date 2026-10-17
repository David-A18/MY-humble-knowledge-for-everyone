---
type: "Explanation"
title: "Crossplane on AWS"
description: "Understand how a Kubernetes request becomes an AWS resource, and where provider credentials, account scope, ownership, and recovery fit."
tags: [cross-topic-guides, crossplane-on-aws]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
sources:
  - id: crossplane-providers
    resource: https://docs.crossplane.io/latest/packages/providers/
    title: Crossplane - Providers
  - id: crossplane-managed
    resource: https://docs.crossplane.io/latest/managed-resources/managed-resources/
    title: Crossplane - Managed Resources
  - id: crossplane-composition
    resource: https://docs.crossplane.io/latest/composition/compositions/
    title: Crossplane - Compositions
  - id: crossplane-v2
    resource: https://docs.crossplane.io/latest/whats-new/
    title: Crossplane - What's New in v2
  - id: crossplane-activation
    resource: https://docs.crossplane.io/latest/managed-resources/managed-resource-activation-policies/
    title: Crossplane - Managed Resource Activation Policies
  - id: crossplane-v1-claims
    resource: https://docs.crossplane.io/v1.20/concepts/claims/
    title: Crossplane v1.20 - Claims
  - id: eks-pod-identity
    resource: https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html
    title: Amazon EKS - EKS Pod Identity
  - id: eks-pod-identity-flow
    resource: https://docs.aws.amazon.com/eks/latest/userguide/pod-id-how-it-works.html
    title: Amazon EKS - How EKS Pod Identity Works
  - id: eks-pod-identity-target-role
    resource: https://docs.aws.amazon.com/eks/latest/userguide/pod-id-assign-target-role.html
    title: Amazon EKS - Access AWS Resources Using EKS Pod Identity Target IAM Roles
  - id: eks-irsa
    resource: https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html
    title: Amazon EKS - IAM Roles for Service Accounts
---

# Crossplane on AWS

## What it is for

Crossplane lets a Kubernetes cluster hold **requests for external
resources**, such as an AWS bucket. A Crossplane provider turns a
Kubernetes managed resource into AWS API calls, then keeps comparing
the requested settings with what it observes. The Kubernetes object
and the AWS object are related, but they are not the same object.
[^crossplane-providers][^crossplane-managed]

This guide explains the AWS-specific boundaries. Start with
[Crossplane foundations](../kubernetes/crossplane/index.md) if
*provider*, *managed resource*, and *composition* are new terms.
Use [How an AWS resource request moves through Crossplane](../kubernetes/crossplane/aws-resource-workflow.md)
to follow the full handoff. For a hands-on install and provider test,
use the [local AWS S3 lab](../kubernetes/crossplane/local-aws-s3-lab.md).
This page does not contain an install procedure.

Think of a library request desk: a reader asks for a book, and a
librarian obtains it and records what is on the shelf. A platform
API can similarly accept a simple request while a provider handles
AWS details. The analogy ends there. Crossplane keeps reconciling
after the first request; AWS can reject changes because of IAM or
service rules; and deleting a Kubernetes request can delete an
external resource, depending on its lifecycle settings. Check those
settings before treating a request like a harmless form.
[^crossplane-managed]

## The three objects to keep separate

| Object | Where it lives | What it says |
| --- | --- | --- |
| Composite resource (XR), if your platform defines one | Kubernetes API | The user-facing request, such as a platform-defined `SecureBucket`. |
| Managed resource (MR) | Kubernetes API | The provider-specific desired AWS resource and its observed status. |
| External resource | AWS account and region | The real bucket, queue, database, or other service object. |

A **Composition** uses a function pipeline to turn an XR into one or
more Kubernetes resources. In this example, those include AWS managed
resources. The installed AWS provider supplies the relevant APIs and
runs a controller that makes AWS calls; in a cluster using selective
activation, the needed managed-resource kind must also be active. A
`ProviderConfig` tells the provider how to authenticate, and each
managed resource selects one. One provider controller can process
resources that select different credential configurations. The exact
API group, scope, schema, and credential options depend on the
installed provider package and version.
Crossplane v2 supports namespaced XRs and managed resources, but
existing v1-style APIs may still appear in a real cluster. On those
older APIs, a team may submit a **Claim** linked to an XR rather
than submitting the XR directly.
[^crossplane-composition][^crossplane-providers][^crossplane-v2][^crossplane-activation][^crossplane-v1-claims]

## Example: a team requests a bucket

This `payments` example is invented. No provider, bucket, IAM role,
Composition, GitOps controller, or request was run or checked.

1. A platform team has already created an EKS management cluster
   and installed Crossplane, an AWS provider, and a reviewed
   `SecureBucket` platform API.
2. The payments team submits an XR asking for a bucket in its
   namespace. The platform must map that request to an approved
   credential configuration and region. GitOps *may* apply it from Git;
   GitOps is optional and does not itself create the AWS bucket.
3. Crossplane selects a compatible Composition. It creates the
   provider-specific managed resources for the bucket and whatever
   additional controls that Composition actually defines.
4. The provider reads each MR and its selected `ProviderConfig`, gets
   credentials, and calls the appropriate AWS API. Those credentials
   determine which account owns the bucket; the MR specifies the
   region. AWS authorizes or rejects the call.
5. The provider reports observed state back to the MR. The team
   still needs an application-level check before claiming the
   bucket is usable for its real workload.
   [^crossplane-composition][^crossplane-managed]

```mermaid
flowchart TB
  team["Payments request"] --> xr["SecureBucket XR<br/>Kubernetes"]
  git["GitOps, if used"] -. "applies request" .-> xr
  xr --> comp["Crossplane<br/>Composition"]
  comp --> mr["AWS managed resource<br/>Kubernetes"]
  mr -. "providerConfigRef" .-> cfg["ProviderConfig<br/>credential choice"]
  cfg -. "read by" .-> provider["AWS provider<br/>controller"]
  mr -- "desired region" --> provider
  identity["Provider Pod identity<br/>if selected"] -. "AWS credentials" .-> provider
  provider -- "authorized AWS API call" --> aws["Bucket<br/>target account + region"]
  aws -. "observed state" .-> provider
  provider -. "status" .-> mr
```

Text alternative: the team's request becomes a Kubernetes XR. A
Composition turns it into an AWS managed resource. The managed
resource names a credential configuration and a region. That
configuration can select the provider Pod's AWS identity or another
supported credential source. The provider calls AWS in the target
account and region, then reports what it observes to the
managed resource. An optional
GitOps controller applies the request to Kubernetes; it does not
replace Crossplane or the AWS provider.

The name `SecureBucket` describes a **platform promise**, not a
native Crossplane or AWS kind. It is secure only if its actual
Composition, IAM policy, AWS configuration, and tests enforce
the promised properties. Do not infer encryption, public-access
blocking, logging, or retention from the name alone.

## Four boundaries a platform must choose

| Boundary | Decision to make | What can go wrong |
| --- | --- | --- |
| Bootstrap | Which tool creates the first cluster, network, and provider identity? | Crossplane cannot recover the cluster it runs in if that failed cluster is the only bootstrap tool. |
| AWS identity | Which provider Pod identity and selected credentials can make the call in the intended account? | A valid Kubernetes request can be rejected by AWS, or a broad role can affect unintended resources or accounts. |
| API exposure | Which users may create XRs, MRs, or `ProviderConfig` references? | A narrow user-facing XR is ineffective if users can bypass it and select a privileged provider config directly. |
| Resource ownership | Which controller may update and delete each external resource? | Terraform and Crossplane can repeatedly overwrite one another, or a deletion can remove state the team meant to retain. |

For bootstrap, Terraform, CloudFormation, CDK, or another operator
managed tool may create the first EKS cluster and IAM foundation.
Afterward, Crossplane can own selected resources whose lifecycle
the team has explicitly assigned to it. This is a design choice,
not a requirement to use a particular bootstrap product.

For identity on EKS, **Pod Identity** can associate the provider Pod's
service account with an IAM role if its agent and the provider's AWS
SDK credential path support it. The first role is in the cluster's
AWS account. An association can also name a target role in another
account; EKS then chains the two roles. **IRSA** instead uses an IAM
role trust policy, a cluster OIDC provider, and a service-account web
identity token. Crossplane's package manager creates the provider
service account; a `DeploymentRuntimeConfig` can set its name or
annotations when the identity setup needs them. First check which
service account the provider actually uses. Then check the *provider
Pod's* effective identity and permissions. Running `aws sts
get-caller-identity` in your own shell proves only your shell's
identity.[^eks-pod-identity][^eks-pod-identity-flow][^eks-pod-identity-target-role][^eks-irsa][^crossplane-providers]

The selected `ProviderConfig` is a separate choice from the provider
Pod's starting identity. A provider can serve multiple teams and use
different configurations for their MRs. Check the actual provider's
credential options before deciding whether a configuration uses the
Pod's credentials, a secret, or another supported path. For the AWS
bucket example, the credentials used for the call determine the account;
the MR's `spec.forProvider.region` specifies the region. Neither is
inferred safely from the team's namespace alone.[^crossplane-providers]

For API exposure, the AWS provider described in current Crossplane
documentation supports namespaced `ProviderConfig` and
cluster-wide `ClusterProviderConfig`. A managed resource that sets
`providerConfigRef` must name its kind and name. If it omits that
reference, the documented default is the cluster-wide
`ClusterProviderConfig` named `default`. A namespaced MR can select
a cluster-wide configuration, so a user who can create MRs must not
be able to select more powerful credentials than intended. Kubernetes
RBAC and admission rules must limit who can create MRs and which
credential references they can use.
Verify these APIs against the provider you install.
[^crossplane-providers]

For ownership, Crossplane's `managementPolicies` can limit actions
such as `Observe`, `Create`, `Update`, and `Delete` **when the installed
provider supports them**. The default `*` grants full control. If
GitOps prunes a removed XR, its composed MR may be deleted too; if the
MR permits `Delete`, the provider may then delete the AWS resource.
Removing a file alone has no such effect without a controller that
applies the deletion. Check the actual lifecycle configuration and
recovery plan before exposing the XR. Avoid two active tools writing
the same AWS fields.
[^crossplane-managed]

## If the bucket does not appear

Trace the first failed handoff instead of repeating the request:

1. Was the XR admitted, and did a compatible Composition produce
   the expected MR?
2. Is the provider installed and healthy, is the MR kind active, and
   does the MR name the intended `ProviderConfig`?
3. Did the provider use the credentials selected by its
   `ProviderConfig`? If that path uses Pod Identity or IRSA, did the
   provider Pod receive the expected AWS identity? Inspect the MR's
   conditions and events, provider Pod logs, and relevant AWS
   CloudTrail events; your laptop identity is not evidence for the Pod.
4. Did AWS deny the call, reject a setting, or create the resource
   in a different account or region?
5. If the MR reports ready, does the application using the bucket
   actually have its *own* required access? Provider identity and
   application identity are separate.

See [Find the first failing Crossplane handoff](../kubernetes/crossplane/troubleshooting.md)
for the operational commands. A failed provider can leave a
Kubernetes request present while the external AWS resource is
absent or stale. Even `Ready=True` on the MR is not an
application-level access test.

## Check your understanding

1. Which object is the actual AWS bucket, and which objects exist
   only in Kubernetes?
2. Why might Git show an approved `SecureBucket` request while
   AWS has no bucket?
3. Whose AWS identity matters for creation: your terminal's,
   the provider Pod's, or the application Pod's?
4. What must you decide before deleting an XR or managed resource
   that represents important data?

## Deeper study

- [Crossplane providers](https://docs.crossplane.io/latest/packages/providers/)
  for installed APIs, runtime, and configuration.
- [Crossplane managed resources](https://docs.crossplane.io/latest/managed-resources/managed-resources/)
  for desired state, observed state, and lifecycle controls.
- [Crossplane compositions](https://docs.crossplane.io/latest/composition/compositions/)
  for the XR-to-MR translation.
- [EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html)
  and [target IAM roles](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-assign-target-role.html),
  plus [IRSA](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html)
  for workload credential paths.
- [How an AWS resource request moves through Crossplane](../kubernetes/crossplane/aws-resource-workflow.md)
  for the request-to-AWS handoffs.

[Back to cross-topic guides](index.md)

[^crossplane-providers]: [Crossplane - Providers](https://docs.crossplane.io/latest/packages/providers/).
[^crossplane-managed]: [Crossplane - Managed Resources](https://docs.crossplane.io/latest/managed-resources/managed-resources/).
[^crossplane-composition]: [Crossplane - Compositions](https://docs.crossplane.io/latest/composition/compositions/).
[^crossplane-v2]: [Crossplane - What's New in v2](https://docs.crossplane.io/latest/whats-new/).
[^crossplane-activation]: [Crossplane - Managed Resource Activation Policies](https://docs.crossplane.io/latest/managed-resources/managed-resource-activation-policies/).
[^crossplane-v1-claims]: [Crossplane v1.20 - Claims](https://docs.crossplane.io/v1.20/concepts/claims/).
[^eks-pod-identity]: [Amazon EKS - Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html).
[^eks-pod-identity-flow]: [Amazon EKS - How Pod Identity Works](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-how-it-works.html).
[^eks-pod-identity-target-role]: [Amazon EKS - Access AWS Resources Using EKS Pod Identity Target IAM Roles](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-assign-target-role.html).
[^eks-irsa]: [Amazon EKS - IAM Roles for Service Accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html).
