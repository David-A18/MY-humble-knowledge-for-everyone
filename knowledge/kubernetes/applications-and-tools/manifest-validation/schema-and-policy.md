---
type: Reference
title: Schema and policy validation
description: Reject malformed objects and organization-specific violations before
  deployment.
tags:
- kubernetes
- manifest-validation
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: kubeconform
  resource: https://github.com/yannh/kubeconform
  title: kubeconform
- id: conftest
  resource: https://www.conftest.dev/
  title: Conftest
- id: kubernetes-api-deprecation
  resource: https://kubernetes.io/docs/reference/using-api/deprecation-guide/
  title: Kubernetes API deprecation
---

# Schema and policy validation

## Purpose

Reject malformed objects and organization-specific violations before deployment.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Complementary checks

kubeconform validates resources against JSON schemas for a selected Kubernetes version. It does not check whether the application works or every admission rule will accept it. CRDs need matching custom schemas; skipping missing schemas can silently bypass your most important checks.[^kubeconform][^conftest][^kubernetes-api-deprecation]

Conftest evaluates structured configuration against Rego policies. It expresses requirements such as allowed registries, denied privileged containers, or required labels. In-cluster admission still enforces policy for every client.

```bash
kubeconform -strict -summary -kubernetes-version 1.34.0 examples/app.yaml
conftest test examples/app.yaml --policy examples/policy
```

What it does: validates the sample's schema and evaluates its policy. Pin kubeconform, schema revision, and Conftest in your own CI toolchain; the fixture uses core APIs. Run from this series directory.

## Useful negative tests

- Use an invalid type, such as a string where `replicas` requires an integer: schema validation must fail.
- Set a Service selector to the wrong label: schemas may still pass; behavior tests must fail.
- Remove the required ownership label: policy validation must fail.
- Add a CRD object with no registered schema: explicitly report missing validation coverage.

## Policy operations

Treat policy bundles like code: version them, test allowed and denied fixtures, document exceptions, and keep readable failure messages. An offline policy pass is insufficient when admission evaluates additional cluster context.

If validation fails only in CI, compare schema downloads, tool versions, working directories, and rendered inputs. Avoid upgrading schemas automatically without checking removed APIs and changed defaults.

## Related links

- [kubeconform](https://github.com/yannh/kubeconform)
- [Conftest](https://www.conftest.dev/)
- [Kubernetes API deprecation](https://kubernetes.io/docs/reference/using-api/deprecation-guide/)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^kubeconform]: [kubeconform](https://github.com/yannh/kubeconform).
[^conftest]: [Conftest](https://www.conftest.dev/).
[^kubernetes-api-deprecation]: [Kubernetes API deprecation](https://kubernetes.io/docs/reference/using-api/deprecation-guide/).
