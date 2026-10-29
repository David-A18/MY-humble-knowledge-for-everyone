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

## Purpose

Inspect semantic changes before making API calls.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Render the actual deployment inputs

```bash
helm template demo ./chart -f values-prod.yaml > proposed.yaml
kubectl kustomize overlays/prod > proposed-overlay.yaml
dyff between baseline.yaml proposed.yaml
```

What it does: materializes configuration and compares YAML structures. Use a baseline produced from the previous Git revision using identical tool versions. File names here refer to your application repository.

For a Helm-managed release, `helm diff upgrade` compares release manifests against a proposed upgrade. Review plugin version compatibility with your Helm major version; the plugin is a separate executable dependency.

```bash
helm diff upgrade demo ./chart --values values-prod.yaml --detailed-exitcode
```

What it does: displays an upgrade preview and enables the plugin's distinct difference exit code. Consult the pinned plugin's help rather than reusing kubectl's exit-code contract.

## Formatting versus behavior

The [fixtures](examples/index.md) include reordered and changed Service JSON documents. JSON is valid YAML. Compare the original with its reordered equivalent: no semantic field changes should appear. Compare the original with the bad target port: `targetPort` must appear.

```bash
dyff between examples/service.json examples/service-reordered.json
dyff between examples/service.json examples/service-broken.json
```

What it does: demonstrates formatting tolerance and a routing change. Run from this series directory. A tool may still display document ordering differently; inspect whether the actual field value changed.

## Review beyond text

Watch for removed resources, immutable fields, renamed selectors, dropped RBAC rules, changed storage classes, and modified defaults after chart upgrades. Rendering may not evaluate server-side lookups identically to a real upgrade.

> [!WARNING]
> Helm values and rendered Secret objects can expose credentials. Review redaction options in the pinned tool and never publish unfiltered diffs.

Source references: [^dyff-documentation][^helm-diff-documentation]

## Related links

- [dyff documentation](https://github.com/homeport/dyff)
- [Helm Diff documentation](https://github.com/databus23/helm-diff)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^dyff-documentation]: [dyff documentation](https://github.com/homeport/dyff).
[^helm-diff-documentation]: [Helm Diff documentation](https://github.com/databus23/helm-diff).
