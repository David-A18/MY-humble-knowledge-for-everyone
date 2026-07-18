# Kubernetes troubleshooting

Symptom-driven guides for diagnosing Kubernetes workload and cluster issues.

## Articles

| Article | Purpose |
| --- | --- |
| [CrashLoopBackOff](crashloopbackoff.md) | Diagnose pods that repeatedly crash and restart. |
| [Common solutions](common-solutions.md) | Diagnose Pending pods, image pulls, service/DNS issues, failed rollouts, and permission errors. |
| [APISIX troubleshooting](apisix.md) | Diagnose APISIX gateway, route, plugin, backend, and TLS issues. |
| [Crossplane troubleshooting](crossplane.md) | Diagnose Crossplane providers, compositions, managed resources, and deletion issues. |
| [kind troubleshooting](kind.md) | Diagnose local `kind` cluster, context, image, port, and scheduling issues. |

## Common starting commands

```bash
kubectl get pods -n <namespace> -o wide
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

What it does: checks pod state, detailed events, previous container logs, and recent namespace events.

## Official documentation

- [Debug pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/)
- [Debug services](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/)
- [Troubleshooting applications](https://kubernetes.io/docs/tasks/debug/debug-application/)

## Related links

- [Kubernetes command workflows](../commands/workflows.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
