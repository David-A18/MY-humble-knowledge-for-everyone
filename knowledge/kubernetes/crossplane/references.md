---
type: Reference
title: Find the right Crossplane source for your question
description: Choose the official Crossplane, provider, or AWS documentation that answers a specific API, deployment, identity, or troubleshooting question.
tags: [kubernetes, crossplane, references, beginner]
status: draft
maturity: draft
audience: Beginning platform and infrastructure learner
maintainer: unassigned
sources:
  - id: crossplane-docs
    resource: https://docs.crossplane.io/latest/
    title: Crossplane - Documentation
  - id: crossplane-managed
    resource: https://docs.crossplane.io/latest/managed-resources/managed-resources/
    title: Crossplane - Managed Resources
  - id: crossplane-compositions
    resource: https://docs.crossplane.io/latest/composition/compositions/
    title: Crossplane - Compositions
  - id: crossplane-cli
    resource: https://docs.crossplane.io/cli/latest/command-reference/
    title: Crossplane CLI - Command Reference
  - id: crossplane-troubleshoot
    resource: https://docs.crossplane.io/latest/guides/troubleshoot-crossplane/
    title: Crossplane - Troubleshoot Crossplane
  - id: upbound-marketplace
    resource: https://marketplace.upbound.io/
    title: Upbound - Marketplace
  - id: aws-eks-identity
    resource: https://docs.aws.amazon.com/eks/latest/userguide/service-accounts.html
    title: AWS - IAM roles for EKS workloads
---

# Find the right Crossplane source for your question

## Start with the question

A reference page is a map, not another deployment recipe. If a
`SecureBucket` request exists but no bucket appears, first ask
whether the problem is in the XR, the composed managed resource,
the provider, or AWS. Then open the source for that boundary.
The [first-failure guide](troubleshooting.md) explains how to
find it.

| Your question | Start with | What to confirm |
| --- | --- | --- |
| What changed in v2? | [What's new in Crossplane v2](https://docs.crossplane.io/latest/whats-new/) | Whether the example uses namespaced v2 or legacy cluster-scoped APIs. |
| How do I install Crossplane? | [Install Crossplane](https://docs.crossplane.io/latest/get-started/install/) | Supported Kubernetes and Helm versions, chart options, and ready Pods. |
| Which API defines the request? | [Composite Resource Definitions](https://docs.crossplane.io/latest/composition/composite-resource-definitions/) | XRD group, scope, schema, and served versions. |
| How does a request choose an implementation? | [Composite Resources](https://docs.crossplane.io/latest/composition/composite-resources/) and [Compositions](https://docs.crossplane.io/latest/composition/compositions/) | Selected Composition, function pipeline, composed-resource references, and conditions. |
| How does one AWS object map to Kubernetes? | [Managed Resources](https://docs.crossplane.io/latest/managed-resources/managed-resources/) | `forProvider`, `atProvider`, external name, references, conditions, and management policies. |
| Which provider API and field actually exist? | [Providers](https://docs.crossplane.io/latest/packages/providers/), [Managed Resource Definitions](https://docs.crossplane.io/latest/managed-resources/managed-resource-definitions/), and the [Upbound Marketplace](https://marketplace.upbound.io/) for Upbound packages | Installed package version, active CRD, group, kind, scope, and provider field schema. |
| Why is a provider kind missing? | [Managed Resource Activation Policies](https://docs.crossplane.io/latest/managed-resources/managed-resource-activation-policies/) and [disabling unused managed resources](https://docs.crossplane.io/latest/guides/disabling-unused-managed-resources/) | Installed MRDs, activation policy, and whether a default broad policy is still active. |
| How do I preview desired composed objects? | [Compositions: test a composition](https://docs.crossplane.io/latest/composition/compositions/#test-a-composition) and [CLI command reference](https://docs.crossplane.io/cli/latest/command-reference/) | Exact CLI syntax, function inputs, and Docker or development runtime. |
| Where do I begin troubleshooting? | [Troubleshoot Crossplane](https://docs.crossplane.io/latest/guides/troubleshoot-crossplane/) | Object scope, conditions, Reason, Message, events, and the responsible controller. |

The current documentation uses `latest`, which can move as
Crossplane releases change. Record the **installed package and
CLI versions** before copying a command or manifest. The provider
package and activated Kubernetes CRD are the final authority for a
field in your cluster; a marketplace example for another version
is a starting point.[^crossplane-managed][^crossplane-cli]

## Choose a source for common design work

| Design question | Official source | What it teaches |
| --- | --- | --- |
| How do fixed templates and patches work? | [Function Patch and Transform](https://docs.crossplane.io/latest/guides/function-patch-and-transform/) | Patch direction, transforms, and readiness checks. |
| How do I create a variable number of resources? | [Crossplane Compositions](https://docs.crossplane.io/latest/composition/compositions/) and the [Go templating function README](https://github.com/crossplane-contrib/function-go-templating) | Function pipelines, desired state, list iteration, and composed-resource identity. |
| How do I package a platform API? | [Configurations](https://docs.crossplane.io/latest/packages/configurations/) | Package dependencies, installation, and revisions. |
| How do I manage a change to a Composition? | [Composition revisions](https://docs.crossplane.io/latest/composition/composition-revisions/) | Revision creation and XR update policy. |
| How do I stop deletion while a dependent resource exists? | [Usages](https://docs.crossplane.io/latest/managed-resources/usages/) | Dependency-based deletion protection and ordering. |
| How do I bring in an existing AWS resource? | [Import existing resources](https://docs.crossplane.io/latest/guides/import-existing-resources/) | Observe-first import and external identity. |
| How do I run Crossplane through GitOps? | [Crossplane with Argo CD](https://docs.crossplane.io/latest/guides/crossplane-with-argo-cd/) | Sync ordering, health assessment, and tracking considerations. |
| How do I upgrade safely? | [Upgrade Crossplane](https://docs.crossplane.io/latest/guides/upgrade-crossplane/) | Version-specific upgrade procedure and compatibility checks. |

A function can generate a desired Kubernetes object without
proving that an external API will accept it. `crossplane composition
render` previews desired output; a live managed resource and its
provider conditions show a later stage. Keep the checks separate.
[^crossplane-compositions][^crossplane-managed]

## Follow the provider and AWS boundary

A provider package adds APIs and a controller. Its
`ProviderConfig` selects authentication settings for a
managed resource. The controller's runtime identity must be
allowed to perform the AWS action. The AWS object can still
be rejected for naming, Region, quota, or service-policy
reasons.[^crossplane-managed]

| Question | Source |
| --- | --- |
| Which AWS S3 managed-resource kinds does my chosen package offer? | [Upbound AWS S3 provider](https://marketplace.upbound.io/providers/upbound/provider-aws-s3), then the installed CRDs. |
| How does the provider authenticate? | [Upbound provider authentication](https://docs.upbound.io/manuals/packages/providers/authentication/) and the chosen provider package documentation. |
| Should EKS use Pod Identity or IRSA for the provider Pod? | [AWS EKS workload IAM overview](https://docs.aws.amazon.com/eks/latest/userguide/service-accounts.html), [Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html), and [IRSA](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html). Check provider runtime compatibility. |
| Does AWS allow the requested bucket name? | [AWS S3 bucket naming rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html). |
| Did the provider call AWS? | [AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html), alongside provider conditions and logs. |

A successful call made from a developer laptop uses that laptop's
AWS identity. It does not establish which identity the provider
Pod uses. Read the [provider identity explanation](providers-and-authentication.md)
before diagnosing an authorization failure.

## Use this repository's teaching routes

- [How an AWS resource request moves through Crossplane](aws-resource-workflow.md)
  follows the request from Kubernetes to AWS and an application check.
- [How a Crossplane managed resource changes over time](managed-resources-and-lifecycle.md)
  explains drift, pause, import, and deletion.
- [Choose how Crossplane repeats and connects resources](deployment-patterns-and-references.md)
  explains fixed templates, loops, and references.
- [Create and remove one S3 bucket with Crossplane](local-aws-s3-lab.md) contains the hands-on
  sandbox path. Check its draft status and evidence before running it.

The original [processed source notes](../../../sources/processed/crossplane-complete-study-guide.md)
record earlier research. Use the official sources above for current
API and operational claims.

[^crossplane-managed]: Crossplane, [Managed Resources](https://docs.crossplane.io/latest/managed-resources/managed-resources/).
[^crossplane-cli]: Crossplane CLI, [Command Reference](https://docs.crossplane.io/cli/latest/command-reference/).
[^crossplane-compositions]: Crossplane, [Compositions](https://docs.crossplane.io/latest/composition/compositions/).
