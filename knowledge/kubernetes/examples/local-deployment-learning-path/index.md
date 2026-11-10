# Local deployment learning path files

Use these task-owned teaching inputs with the [local deployment walkthrough](../../../cross-topic-guides/local-deployment-learning-path.md). The version contract pins tools/node image, the Deployment pins its workload digest, and the runners distinguish file recovery, API state, HTTP, and cleanup. Exact runtime evidence belongs to the tested commit's CI result; these are not production manifests.

## Purpose

This directory contains the exact Kubernetes manifests used by the [local deployment learning path](../../../cross-topic-guides/local-deployment-learning-path.md).

## Files

| File | Purpose |
| --- | --- |
| [namespace.yaml](namespace.yaml) | Isolates the exercise resources. |
| [deployment.yaml](deployment.yaml) | Creates a two-replica `nginx` Deployment. |
| [service.yaml](service.yaml) | Creates a ClusterIP Service for the web Pods. |
| [failing-image-patch.yaml](failing-image-patch.yaml) | Strategic merge patch for an existing Deployment; use `kubectl patch`, not standalone `apply`. |
| [lab-versions.json](lab-versions.json) | Fixed kind, kubectl and release node-image contract. |
| [.gitignore](.gitignore) | Keeps the task kubeconfig and Python bytecode out of the teaching repository. |
| [validate-git-recovery.py](validate-git-recovery.py) | Exercises staged/unstaged recovery in a disposable Git copy. |
| [validate-lab.py](validate-lab.py) | Creates a unique kind cluster, verifies Service/port-forward HTTP, image-not-found failure, rollback and owned cleanup. |

The [CI workflow](../../../../.github/workflows/local-learning-journey.yml) also runs the beginner Terraform lifecycle. Read the [preflight](../../../cross-topic-guides/local-learning-preflight.md) before manual or automated cluster execution. Independent reader testing and platform-specific runtime repetition remain open.

## Related links

- [Local deployment learning path](../../../cross-topic-guides/local-deployment-learning-path.md)
- [Back to Kubernetes examples](../index.md)
- [Back to Kubernetes index](../../index.md)
- [Back to root index](../../../../README.md)
