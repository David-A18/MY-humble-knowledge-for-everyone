---
type: Troubleshooting Guide
title: Design and troubleshoot Crossplane XRDs and Compositions
description: Decide between direct managed resources and platform APIs, handle older claim-based examples, and fix broken XRD, Composition, and XR links.
tags: [kubernetes, crossplane, xrd-composition-and-xr-calls, troubleshooting]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
---

# Design and troubleshoot Crossplane XRDs and Compositions

Use this page when you design a Crossplane platform API or when an XR does not create what you expect. It is part of [Crossplane XRDs, Compositions, and XR calls](xrd-composition-and-xr-calls.md).

## Direct managed resources versus platform APIs

You can use Crossplane without XRDs and Compositions.

Direct managed resource:

```yaml
apiVersion: s3.aws.m.upbound.io/v1beta1
kind: Bucket
metadata:
  name: payments-audit-logs
  namespace: payments
spec:
  forProvider:
    region: eu-west-1
  providerConfigRef:
    name: default
    kind: ClusterProviderConfig
```

What it does: asks the AWS provider to manage one S3 bucket directly.

Platform API:

```yaml
apiVersion: platform.example.org/v1alpha1
kind: AuditLogStore
metadata:
  name: payments
  namespace: payments
spec:
  region: eu-west-1
  retentionDays: 365
  classification: regulated
```

What it does: asks the platform API for an audit log store. The Composition may create a bucket, encryption configuration, lifecycle rules, access policy, monitoring alarms, and Kubernetes connection data behind the scenes.

Use direct managed resources when the consumer should know the provider API. Use XRDs and Compositions when the platform should expose intent and hide implementation.

## Claims and older Crossplane examples

In older Crossplane material, you may see claims or composite resource claims. A claim was a namespaced user-facing object that created or bound to a cluster-scoped XR behind it.

In Crossplane v2, namespaced XRs are the default model, so the usual beginner mental model is simpler:

```text
User creates XR -> Crossplane runs Composition -> composed resources reconcile
```

If you are reading old examples, translate carefully:

| Older or legacy wording | Modern mental model |
| --- | --- |
| Claim | User-facing request object, often replaced by a namespaced XR in v2 designs. |
| XR | Composite resource that the Composition acts on. |
| XRD with `claimNames` | Legacy compatibility pattern rather than the default v2 starting point. |

## Design advice

- Name the XRD after the product API, not after every resource it creates.
- Keep the XR spec small: expose intent, not every provider field.
- Use XRD schema for required fields, enums, simple validation, and defaults.
- Use multiple Compositions when one API needs multiple implementations.
- Use `defaultCompositionRef` when most users should not choose implementation details.
- Use `enforcedCompositionRef` when users must not bypass the standard implementation.
- Use `compositionRef` only when the user or GitOps layer is allowed to choose a specific implementation.
- Put provider credentials in `ProviderConfig` or `ClusterProviderConfig`, not in the XR.
- Patch only the XR fields that the platform API intentionally supports.
- Expose useful status back to the XR so users do not need to inspect every composed resource.
- Treat Composition changes like production code because existing XRs may adopt new CompositionRevisions.

## Troubleshooting the relationship

| Symptom | Likely cause | Next step |
| --- | --- | --- |
| `kubectl apply` rejects the XR kind | The XRD is missing, not established, or the XR `apiVersion`/`kind` does not match it. | Run `kubectl get xrd` and `kubectl api-resources \| grep platform.example.org`. |
| XR exists but no composed resources appear | No compatible Composition was selected or the function pipeline failed. | Describe the XR and inspect `Synced`, events, `compositionRef`, and function logs. |
| XR selected the wrong implementation | Multiple Compositions match and defaults/selectors are unclear. | Set `defaultCompositionRef`, `enforcedCompositionRef`, `compositionRef`, or clearer Composition labels. |
| Composition is ignored | `compositeTypeRef` does not match the XRD's group, version, or kind. | Compare `Composition.spec.compositeTypeRef` with the XR `apiVersion` and `kind`. |
| A Composition update changed existing resources unexpectedly | XRs followed new CompositionRevisions automatically. | Use `defaultCompositionUpdatePolicy: Manual` or XR-level `compositionUpdatePolicy: Manual` for production APIs. |

### Inspect the API and selection

```bash
kubectl get xrd
kubectl describe xrd platformnetworks.platform.example.org
kubectl get compositions
kubectl describe composition platformnetwork-aws-private
kubectl get platformnetworks -n payments
kubectl describe platformnetwork payments-network -n payments
```

What it does: checks that the API exists, the Composition points at the right XR type, and the XR selected a Composition and produced resource references.

## Related links

- [Crossplane XRDs, Compositions, and XR calls](xrd-composition-and-xr-calls.md)
- [Back to index](index.md)
