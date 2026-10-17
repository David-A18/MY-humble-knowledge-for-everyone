# Kubernetes core objects

Status: Draft

Focused notes for the Kubernetes objects used most often in application operations.

## Articles

| Article | Purpose |
| --- | --- |
| [Stateful workloads](stateful-workloads.md) | Understand stable Pod and storage identity, claim and volume deletion policies, and the limits of a StatefulSet. |
| [Custom resources and CRDs](custom-resources-and-crds.md) | Follow a new API type from CRD to stored instance, controller action, status, and deletion. |
| [How a Kubernetes Service selects Pods](how-a-service-selects-pods.md) | Trace a label selector, readiness, EndpointSlices, and in-cluster traffic through the local `kb-web` example. |

## Expected content

- Pods and deployments.
- Ingress and external access.
- ConfigMaps and Secrets.
- PersistentVolumes and PersistentVolumeClaims.
- Jobs and CronJobs.

[Back to Kubernetes index](../index.md) | [Back to knowledge index](../../index.md)
