# Local deployment learning path files

Status: Draft
Audience: Beginning platform engineer
Page type: Tutorial support files
Maintainer: Unassigned
Last substantive review: 2026-09-18
Applicable versions: kubectl v1.37.0 client; stable Kubernetes API shapes for Deployment, Service, and Namespace
Validation evidence: Statically checked as Markdown and linked from the local learning path; cluster execution blocked because `kind` could not connect to a Docker daemon at `/var/run/docker.sock`
Known limitations: These files are intentionally small and local; they are not production manifests
Next review: After the first completed author run

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
- [Back to Kubernetes examples](../README.md)
- [Back to Kubernetes index](../../README.md)
- [Back to root index](../../../README.md)
