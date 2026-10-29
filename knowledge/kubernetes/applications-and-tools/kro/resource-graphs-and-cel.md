---
type: Explanation
title: kro resource graphs and CEL
description: Design schemas and dependencies that are understandable and observable.
tags:
- kubernetes
- kro
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: resourcegraphdefinition-concepts
  resource: https://kro.run/docs/concepts/rgd/overview/
  title: ResourceGraphDefinition concepts
- id: cel-in-kro
  resource: https://kro.run/docs/concepts/rgd/cel-expressions/
  title: CEL in kro
- id: kro-source-for-pinned-release
  resource: https://github.com/kro-run/kro/tree/v0.9.4
  title: kro source for pinned release
---

# kro resource graphs and CEL

## Purpose

Design schemas and dependencies that are understandable and observable.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Definition structure

`spec.schema` declares the instance API and input/output fields. `spec.resources` contains resource IDs and templates. Expressions such as `${schema.spec.image}` read instance inputs; `${service.spec.clusterIP}` reads a reconciled resource value. kro infers dependencies from references.[^resourcegraphdefinition-concepts][^cel-in-kro][^kro-source-for-pinned-release]

CEL is a bounded expression language used to calculate values and conditions. It is not a shell, arbitrary Python, or a way to call an external API. Type checking catches many mistakes before instances reconcile.

## Small schema example

```yaml
schema:
  apiVersion: v1alpha1
  kind: WebApp
  scope: Namespaced
  spec:
    image: string | default=nginx:1.28.0-alpine
    replicas: integer | default=1 minimum=1
  status:
    endpoint: ${service.spec.clusterIP}
```

What it does: sketches the schema section inside an RGD, not a standalone Kubernetes object. It limits replica inputs and exposes an allocated Service address as status.

## Dependencies and readiness

An output reference can make a consumer wait for its producer. A resource's existence is different from application readiness: a Deployment can exist while its Pods cannot start. Declare readiness requirements appropriate to the selected API and avoid cycles. Use the release's documented `readyWhen`, conditional, and collection syntax when extending the basic lab.

Resource IDs are references inside the graph, not necessarily Kubernetes object names. Namespace and name collisions still matter. Multiple instances should generate unique resource names from instance identity.

## Failure design

Expose meaningful status rather than making users inspect every child object. Plan optional-resource behavior, missing external references, immutable updates, and timeout/error reporting. A missing CRD should be reported as a platform dependency issue, not hidden by broad retries.

Changes to schemas or generated names are API changes: test existing instances before rollout and define migration behavior explicitly.

## Related links

- [ResourceGraphDefinition concepts](https://kro.run/docs/concepts/rgd/overview/)
- [CEL in kro](https://kro.run/docs/concepts/rgd/cel-expressions/)
- [kro source for pinned release](https://github.com/kro-run/kro/tree/v0.9.4)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^resourcegraphdefinition-concepts]: [ResourceGraphDefinition concepts](https://kro.run/docs/concepts/rgd/overview/).
[^cel-in-kro]: [CEL in kro](https://kro.run/docs/concepts/rgd/cel-expressions/).
[^kro-source-for-pinned-release]: [kro source for pinned release](https://github.com/kro-run/kro/tree/v0.9.4).
