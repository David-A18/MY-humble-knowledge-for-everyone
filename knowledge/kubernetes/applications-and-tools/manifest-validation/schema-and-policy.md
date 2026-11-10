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

Use schemas to reject malformed objects, policies to enforce selected requirements, and runtime checks to verify behavior. A schema-valid Service can select the wrong Pods or target the wrong port; a required ownership label says nothing about connectivity.

## Know which contract is checked

kubeconform validates objects against JSON schemas for a selected Kubernetes version. Strict mode rejects fields absent from those schemas and duplicate keys. It does not reproduce every API validation rule, admission webhook, RBAC decision or controller operation. A schema download failure is a coverage error, not an invalid manifest.[^kubeconform]

Conftest evaluates structured inputs against Rego. This section's policy requires `metadata.labels.team`; it is a small teaching rule, not a production policy bundle. It does not enforce admission in a cluster, authenticate an owner or check all security settings.[^conftest]

## Run the complete source-only exercise

From the repository root, install the [pinned versions](examples/lab-versions.json) and PyYAML 6.0.3 as described in the [lab](regression-lab-and-ci.md), then run:

```bash
python knowledge/kubernetes/applications-and-tools/manifest-validation/examples/validate-offline.py
```

What it does: invokes actual Git, dyff 1.12.0, kubeconform 0.8.0 and Conftest 0.71.1. It requires no kubeconfig or cluster. Schema requests use immutable repository revision `9367d1ce1c88b8bbf6ee06d0e80510f26394913f` and Kubernetes 1.34.0; the schema cache and mutated files live in a temporary directory.

| Fixture or mutation | Expected result |
| --- | --- |
| Deployment, correct Service, reordered Service, wrong-port Service | All four are schema valid; none skipped. |
| Deployment `replicas: "two"` | Invalid type; failure must identify replicas, not a network error. |
| Unknown `TeachingWidget` custom object | Missing schema is an error; no `-ignore-missing-schemas`. |
| Labeled Deployment and both Service variants | Ownership policy passes, including the wrong-port Service. |
| Remove Deployment ownership label | Policy fails with the ownership-rule message. |

The runner also checks textual and semantic differences; see [rendered comparison](rendered-yaml-comparison.md). These are eight bounded tool assertions, not eight proof points for production readiness.

## Inspect an individual command

From the series directory:

```bash
kubeconform -strict -summary -kubernetes-version 1.34.0 -schema-location 'https://raw.githubusercontent.com/yannh/kubernetes-json-schema/9367d1ce1c88b8bbf6ee06d0e80510f26394913f/{{.NormalizedKubernetesVersion}}-standalone{{.StrictSuffix}}/{{.ResourceKind}}{{.KindSuffix}}.json' examples/app.yaml examples/service-broken.json
conftest test examples/app.yaml examples/service-broken.json --policy examples/policy
```

What it does: pins the schema source as well as the target API version and shows why both tools accept the wrong-port fixture. A subsequent HTTP test is expected to detect the regression. Use the runner for controlled negative mutations and count assertions instead of manually editing the tracked files.

## Make coverage explicit

Treat invalid, error and skipped counts separately. An empty render, skipped kind or unknown CRD must not become a silent pass. A complete pipeline should also assert the expected object inventory for its environment.

Custom resources need schemas matching the installed CRD version. Converting or sourcing a schema is separate from installing a CRD; validate structural requirements and test actual admission/controller behavior in a compatible cluster. Kubernetes version pins do not automatically pin every controller's schema or guarantee that a removed API remains served.[^kubeconform][^kubernetes-api-deprecation]

## Operate policy as code

Keep policy versions, positive/negative fixtures, exceptions and clear messages together. Review whether a check applies to top-level objects, Pod templates, generated resources or admission context; a top-level label rule does not establish Pod-label completeness. Rego syntax/runtime compatibility matters: the pinned Conftest uses OPA 1.21.1 and this example imports Rego v1.

When CI differs from a workstation, compare tool versions, schema revision/downloads, working directory and rendered inputs. Do not use broad missing-schema exclusions or disable TLS verification to obtain a green check. Protect real rendered inputs and reports because policy findings can quote sensitive fields.

## Evidence and cleanup

Sources reviewed on 2026-11-10. All eight real offline tool checks passed locally on Windows with Python 3.13.17 and PyYAML 6.0.3. The [runtime lab](regression-lab-and-ci.md#validation-boundary) carries separate Linux/cluster evidence. Temporary mutations/cache are removed by the runner; tracked fixtures remain unchanged. The installer writes only to an explicitly supplied empty tools directory, which you may remove after the lab.

- [Policy files](examples/policy/index.md)
- [Back to series](index.md) | [Back to Kubernetes](../../index.md)

[^kubeconform]: [kubeconform strict validation, schema locations and custom-resource support](https://github.com/yannh/kubeconform).
[^conftest]: [Conftest structured input and Rego rules](https://www.conftest.dev/).
[^kubernetes-api-deprecation]: [Kubernetes API deprecation guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/).
