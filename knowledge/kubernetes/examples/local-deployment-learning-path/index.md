# Local deployment learning path files

Status: Draft
Audience: Beginning platform engineer
Page type: Tutorial support files
Maintainer: Unassigned
Last content review: 2026-10-12 (static review; no current cluster run)
Earlier run versions: Docker 29.8.0, kind v0.30.0, Kubernetes v1.34.0 node image, and kubectl v1.34.1 client
Validation evidence: A previous version was run end to end on 2026-09-19. The current strategic merge patch and revised command sequence have not been run in a cluster.
Known limitations: These files are intentionally small and local; they are not production manifests
Next review: After KB-14 reader testing or by 2026-12-19

## Purpose

This directory contains the manifests for the [local deployment learning path](../../../cross-topic-guides/local-deployment-learning-path.md). The current files still need an end-to-end cluster run.

## Files

| File | Purpose |
| --- | --- |
| [namespace.yaml](namespace.yaml) | Groups the exercise resources under one name; it does not by itself isolate network traffic. |
| [deployment.yaml](deployment.yaml) | Creates a two-replica `nginx` Deployment. |
| [service.yaml](service.yaml) | Creates a ClusterIP Service for the web Pods. |
| [failing-image-patch.yaml](failing-image-patch.yaml) | Applies a nonexistent image tag to create a diagnosable rollout failure. |

## Related links

- [Local deployment learning path](../../../cross-topic-guides/local-deployment-learning-path.md)
- [Back to Kubernetes examples](../index.md)
- [Back to Kubernetes index](../../index.md)
- [Back to knowledge index](../../../index.md)
