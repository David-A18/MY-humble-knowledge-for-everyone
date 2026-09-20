# Local deployment learning path files

Status: Draft
Audience: Beginning platform engineer
Page type: Tutorial support files
Maintainer: Unassigned
Last substantive review: 2026-09-19
Applicable versions: Docker 29.8.0 rootless daemon, kind v0.30.0, Kubernetes v1.34.0 node image, kubectl v1.34.1 client, and stable Deployment, Service, and Namespace APIs
Validation evidence: Applied during the end-to-end local deployment learning path run; the failing image manifest was corrected after Kubernetes rejected the earlier incomplete patch
Known limitations: These files are intentionally small and local; they are not production manifests
Next review: After KB-14 reader testing or by 2026-12-19

## Purpose

This directory contains the exact Kubernetes manifests used by the [local deployment learning path](../../../cross-topic-guides/local-deployment-learning-path.md).

## Files

| File | Purpose |
| --- | --- |
| [namespace.yaml](namespace.yaml) | Isolates the exercise resources. |
| [deployment.yaml](deployment.yaml) | Creates a two-replica `nginx` Deployment. |
| [service.yaml](service.yaml) | Creates a ClusterIP Service for the web Pods. |
| [failing-image-patch.yaml](failing-image-patch.yaml) | Applies an invalid image tag to create a diagnosable rollout failure. |

## Related links

- [Local deployment learning path](../../../cross-topic-guides/local-deployment-learning-path.md)
- [Back to Kubernetes examples](../index.md)
- [Back to Kubernetes index](../../index.md)
- [Back to root index](../../../../README.md)
