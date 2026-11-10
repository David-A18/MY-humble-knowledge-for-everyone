---
type: Explanation
title: Compare rendered Kubernetes YAML
description: Inspect semantic changes before making API calls.
tags:
- kubernetes
- manifest-validation
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: dyff-documentation
  resource: https://github.com/homeport/dyff
  title: dyff documentation
- id: helm-diff-documentation
  resource: https://github.com/databus23/helm-diff
  title: Helm Diff documentation
---

# Compare rendered Kubernetes YAML

Compare the objects that will reach Kubernetes, then inspect what each field means. A template patch can be small while the rendered change affects every environment; a key-order rewrite can be large while the parsed objects remain equal.

## Render a reproducible baseline

For an application repository, record both Git revisions, render tool versions, dependency locks, release/namespace, values, overlays and target API capabilities. Render the previous and proposed revisions with the same inputs except the intended change. Never silently use today's chart dependencies for yesterday's baseline.

```bash
helm template demo ./chart -f values-prod.yaml > proposed.yaml
kubectl kustomize overlays/prod > proposed-overlay.yaml
dyff between --set-exit-code baseline.yaml proposed.yaml
```

What it does: illustrates Helm and Kustomize rendering in your application repository, then compares one selected baseline/proposal. The chart/overlay names are placeholders, not supplied lab paths. dyff's `--set-exit-code` makes differences return 1; without it, readable output alone is not a reliable failure gate.[^dyff-documentation]

Helm rendering with API lookups, server capabilities or install/upgrade branches needs the appropriate mode and inputs. An offline render does not reproduce every server-assisted operation. A Kustomize overlay must include the patches, replacements and generator inputs for the actual target environment.

## Run the supplied formatting and routing comparisons

Run from this series directory with the pinned dyff 1.12.0 baseline:

```bash
git diff --no-index -- examples/service.json examples/service-reordered.json
dyff between --set-exit-code examples/service.json examples/service-reordered.json
dyff between --set-exit-code examples/service.json examples/service-broken.json
```

What it does: the Git comparison returns 1 for changed text, dyff returns 0 for equal parsed mappings, and the final dyff comparison returns 1 and names the `targetPort` change from 80 to 81. These expected nonzero commands need explicit handling in a `set -e` script. JSON documents are valid YAML inputs.

The [offline runner](examples/validate-offline.py) asserts these results using the real executables, rather than replacing a diff tool with Python object equality. It also checks schema/policy outcomes. A structural difference is evidence to review, not automatic proof that a change should be rejected.

## Review a Helm upgrade

```bash
helm diff upgrade demo ./chart --values values-prod.yaml --detailed-exitcode --suppress-secrets
```

What it does: previews a proposed upgrade for a Helm release and suppresses Secret objects. This remains an application-repository example; the lab does not install Helm or the plugin. Pin a compatible Helm/plugin pair and inspect its help before adopting it. With the documented detailed-status mode, Helm Diff uses 2 for detected changes; that differs from kubectl/dyff's difference status 1. Do not apply one tool's status mapping to every command.[^helm-diff-documentation]

Ordinary upgrade comparison starts from Helm's stored release manifests. The plugin's three-way mode also uses live state and computes the prospective patch. Record which question the chosen mode answers. A release preview and `helm template` are not interchangeable evidence, especially with lookups or admission.

## Review additions, deletions and sensitive output

Check object identity, removed resources, renamed selectors, image digests, RBAC rules, immutable fields, storage classes, generated names and chart defaults. Do not hide a broad subtree because one default is noisy. Keep the underlying rendered files available in a protected job if reviewers need to understand the summary.

Rendered data may contain credentials in Secret objects and ordinary fields. `--suppress-secrets` does not sanitize an arbitrary ConfigMap, annotation, URL or log. Use synthetic fixtures here; review artifact retention, access and redaction before applying the pattern to a real repository.

## Troubleshooting and evidence

If output differs unexpectedly, first compare renderer versions and all inputs; then object identity and generator behavior. If only mapping order changed, check the semantic result. If a CRD list moves, verify its actual order semantics before suppressing it.

Sources reviewed on 2026-11-10. Git 2.55.0.windows.2 and dyff 1.12.0 comparisons were executed locally. Kustomize execution belongs to the hosted [routing lab](regression-lab-and-ci.md#validation-boundary). Helm/plugin commands remain unexecuted guidance. Cleanup of these source-only comparisons requires only task-owned rendered files; do not delete cluster resources for a render-only exercise.

- [Live drift](live-drift.md) | [Schema and policy](schema-and-policy.md)
- [Back to series](index.md) | [Back to Kubernetes](../../index.md)

[^dyff-documentation]: [dyff documentation and exit-status integration](https://github.com/homeport/dyff).
[^helm-diff-documentation]: [Helm Diff options and comparison modes](https://github.com/databus23/helm-diff).
