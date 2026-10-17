# Kubernetes troubleshooting

Symptom-driven guides for diagnosing Kubernetes workload and cluster issues.

## Articles

| Article | Purpose |
| --- | --- |
| [Diagnose CrashLoopBackOff](crashloopbackoff.md) | Read the last container failure, previous logs, and events before changing the workload. |
| [Find the first failing Kubernetes boundary](common-solutions.md) | Match Pod, image, readiness, Service, and access symptoms to evidence before changing resources. |
| [Trace an APISIX 404 to its first failed handoff](apisix.md) | Separate entry, route-match, controller, and backend causes of a 404. |
| [Diagnose a local image pull in kind](kind.md) | Confirm the local cluster and Pod image before loading a built image; route other kind symptoms by evidence. |

## Start with the symptom

Use [the first-boundary guide](common-solutions.md) to confirm the
cluster, read the affected Pod or Service, and choose a focused
investigation. Previous container logs are useful when a container
restarted; they are not a universal first check.

## Official documentation

- [Debug pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/)
- [Debug services](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/)
- [Troubleshooting applications](https://kubernetes.io/docs/tasks/debug/debug-application/)

## Related links

- [Investigate Kubernetes resource pressure](../commands/workflows.md)
- [Back to Kubernetes index](../index.md)
- [Back to knowledge index](../../index.md)
