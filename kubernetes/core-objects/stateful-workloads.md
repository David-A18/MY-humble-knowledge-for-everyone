# Stateful workloads

## Purpose

Use this page to understand Kubernetes objects and storage decisions for stateful workloads.

## Workload choices

| Object | Use it for | Watch for |
| --- | --- | --- |
| Deployment | Stateless replicas. | Pods are interchangeable. |
| StatefulSet | Pods needing stable identity or ordered rollout. | It does not create database replication by itself. |
| PersistentVolumeClaim | Request storage for a Pod. | Storage lifecycle may outlive Pods. |
| StorageClass | Defines dynamic provisioning behavior. | Binding mode affects scheduling and zone placement. |

## Design reminders

- A StatefulSet gives Pods stable names and identities.
- Persistent storage does not automatically provide backup, replication, or application-level high availability.
- Use `WaitForFirstConsumer` when storage placement should align with Pod scheduling.
- Test restore and scale-down behavior before running stateful systems in production.

## Related links

- [Stateful vs. stateless on AWS](../../cloud/aws/architecture/stateful-vs-stateless.md)
- [Kubernetes StatefulSet documentation](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
- [Back to Kubernetes core objects](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
