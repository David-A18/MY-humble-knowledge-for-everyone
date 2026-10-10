---
type: Explanation
title: How a Crossplane Composition fulfills one application request
description: Follow a small WebApplication request through XRD validation, a Composition function pipeline, composed resources, revision choice, and outcome checks.
tags: [kubernetes, crossplane, compositions, platform-api, beginner]
status: draft
maturity: draft
audience: Beginning platform and infrastructure learner
maintainer: unassigned
sources:
  - id: crossplane-xrds
    resource: https://docs.crossplane.io/latest/composition/composite-resource-definitions/
    title: Crossplane - Composite Resource Definitions
  - id: crossplane-compositions
    resource: https://docs.crossplane.io/latest/composition/compositions/
    title: Crossplane - Compositions
  - id: crossplane-revisions
    resource: https://docs.crossplane.io/latest/composition/composition-revisions/
    title: Crossplane - Composition Revisions
  - id: crossplane-cli
    resource: https://docs.crossplane.io/cli/latest/command-reference/
    title: Crossplane CLI - Command Reference
  - id: kubernetes-deployment
    resource: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
    title: Kubernetes - Deployments
  - id: kubernetes-service
    resource: https://kubernetes.io/docs/concepts/services-networking/service/
    title: Kubernetes - Services
---

# How a Crossplane Composition fulfills one application request

## The idea in one minute

A **Composite Resource Definition** (XRD) defines a new request
type and its allowed fields. A **composite resource** (XR) is one
request of that type. A **Composition** selects a pipeline of
functions that returns the Kubernetes resources Crossplane should
apply for that XR.[^crossplane-xrds][^crossplane-compositions]

Think of an order form and a recipe, with a limit to the analogy.
The form checks what a customer may ask for; the recipe says how
the kitchen will prepare it. The form alone does no work, and a
recipe's output is not proof that the customer received a usable
meal. Crossplane still relies on Kubernetes and provider
controllers to reconcile the resulting resources.

Read [How Crossplane's components turn a request into a resource](component-model.md)
first for the wider request path. This page focuses on the
**XR-to-composed-resources handoff**.

## One invented WebApplication request

Imagine a platform team offers `WebApplication`. The caller may
choose an image and a replica count. The platform team wants each
request to yield a Kubernetes Deployment and Service. The example
is invented; the previous long YAML on this page was not run in
a cluster or rendered for verification.

| Layer | In this example | Who owns it |
| --- | --- | --- |
| XRD | Declares `WebApplication` and validates fields such as `image` and `replicas`. | Platform team. |
| XR | Requests `image: example/web:v1` and `replicas: 2` for one app. | Application team or its GitOps controller. |
| Composition | Selects a compatible function pipeline for `WebApplication`. | Platform team. |
| Function result | Describes the desired Deployment and Service. | Function logic chosen and reviewed by the platform team. |
| Composed resources | Kubernetes objects applied by Crossplane and reconciled by their normal controllers. | Crossplane and Kubernetes controllers. |

```mermaid
flowchart LR
  request["WebApplication XR<br/>image and replicas"] --> validate["XRD schema<br/>validates request"]
  validate --> select["Crossplane selects<br/>Composition"]
  select --> fn["Function pipeline<br/>returns desired objects"]
  fn -->|"Crossplane applies"| output["Deployment + Service<br/>Kubernetes"]
  output --> runtime["Pods and network path<br/>Kubernetes controllers"]
  runtime --> check["Application request<br/>user outcome"]
```

Text alternative: an application team submits one WebApplication
XR. The XRD supplies the API schema. Crossplane chooses a
Composition and runs its function steps to obtain desired
Deployment and Service objects. Kubernetes controllers work to
make Pods and a Service path available. A separate application
request checks whether users can actually use the app.

The exact Deployment and Service fields matter: selectors must
match Pod labels, images must pull, and Pods must become ready.
An attractive XR name does not supply those details
automatically. Current Crossplane v2 can compose ordinary
Kubernetes resources as well as provider managed resources.
[^crossplane-compositions][^kubernetes-deployment][^kubernetes-service]

## The pipeline is implementation, not the user API

Crossplane calls the functions listed in a Composition in order.
Each step sees the result accumulated so far and can return
desired composed resources. One function might template the
Deployment and Service; another might determine readiness. The
pipeline's function packages must be installed and healthy for
the Composition to work.[^crossplane-compositions]

| Question | Where to look |
| --- | --- |
| Is `replicas` allowed to be zero or greater than five? | The XRD schema and any admission rules.[^crossplane-xrds] |
| How does `image` reach the Deployment? | The selected Composition and function inputs/output.[^crossplane-compositions] |
| Which name and labels does the Service use? | The function's rendered desired objects, then the applied Service and Deployment.[^crossplane-compositions][^kubernetes-service] |
| Does the app answer a request? | The actual app route and response, beyond XR and Pod status. |

The XRD can reject invalid **request shape** early. It cannot
guarantee the image exists, that the function emits correct
selectors, or that a backend serves a correct response. Those
need later checks.

## Changing the recipe changes existing requests

When a Composition changes, Crossplane creates a
`CompositionRevision`. Its documentation describes an
`Automatic` update policy that follows the latest revision and
a `Manual` policy that requires an XR's revision reference to
be changed deliberately. A team needs to know which policy its
XRs use before changing a Composition; a new template can alter
or remove real resources.[^crossplane-revisions]

For the invented WebApplication, imagine changing the Service
port. The platform team should compare the old and new desired
objects, decide which XRs receive the revision, test the
resulting Service path, and prepare recovery for affected
applications. Merely seeing the new Composition accepted by
Kubernetes would be weak evidence of a successful rollout.

## Check a Composition in layers

| Check | What it can establish | What remains unproven |
| --- | --- | --- |
| XRD schema validation | The request type and fields are accepted. | The function output and runtime behavior. |
| Local Composition render | With a chosen XR, Composition, and Function packages, the CLI can show desired output for review.[^crossplane-cli] | External API permissions, controller reconciliation, and live traffic. |
| Kubernetes/API and controller observation | The generated objects were admitted and their controllers report conditions. | The application's real user path. |
| Disposable integration exercise | The rendered resources can reconcile in a representative cluster. | Production traffic, scale, and every failure mode. |
| User-path check | A representative request reaches the application and produces the expected response. | Every future request or rollout. |

The Crossplane CLI's [Composition render command](https://docs.crossplane.io/cli/latest/command-reference/)
supports an XR, Composition, and Function inputs. This page
does not supply a working file set or claim that the old
WebApplication YAML rendered successfully.[^crossplane-cli]

For a provider-backed example, use
[How one Crossplane request becomes an AWS network](aws-vpc-platform-api.md). For how the
resulting managed resources evolve, use
[How a Crossplane managed resource changes over time](managed-resources-and-lifecycle.md).

## Check your understanding

1. Which object decides whether an XR may contain a `replicas`
   field, and which object decides what resources that value
   changes?
2. Why can the same `WebApplication` XR produce different
   desired resources after a Composition revision?
3. What does a local render show, and which live results does
   it leave untested?
4. Why is an XR's ready condition not a full application
   success test?

## Explore further

- [Composite Resource Definitions](https://docs.crossplane.io/latest/composition/composite-resource-definitions/)
  explains API schema and versions.[^crossplane-xrds]
- [Compositions](https://docs.crossplane.io/latest/composition/compositions/)
  explains pipeline steps and composed resources.
  [^crossplane-compositions]
- [Composition Revisions](https://docs.crossplane.io/latest/composition/composition-revisions/)
  explains update policies.[^crossplane-revisions]
- [Crossplane CLI command reference](https://docs.crossplane.io/cli/latest/command-reference/)
  documents local rendering.[^crossplane-cli]
- [Back to Crossplane](index.md).

[^crossplane-xrds]: [Crossplane, Composite Resource Definitions](https://docs.crossplane.io/latest/composition/composite-resource-definitions/), source record `crossplane-xrds`.
[^crossplane-compositions]: [Crossplane, Compositions](https://docs.crossplane.io/latest/composition/compositions/), source record `crossplane-compositions`.
[^crossplane-revisions]: [Crossplane, Composition Revisions](https://docs.crossplane.io/latest/composition/composition-revisions/), source record `crossplane-revisions`.
[^crossplane-cli]: [Crossplane CLI, Command Reference](https://docs.crossplane.io/cli/latest/command-reference/), source record `crossplane-cli`.
[^kubernetes-deployment]: [Kubernetes, Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), source record `kubernetes-deployment`.
[^kubernetes-service]: [Kubernetes, Services](https://kubernetes.io/docs/concepts/services-networking/service/), source record `kubernetes-service`.
