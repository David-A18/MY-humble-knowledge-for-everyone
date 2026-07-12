# CrashLoopBackOff

## Purpose

Diagnose a pod that starts, exits, and is restarted repeatedly by Kubernetes.

## Symptoms

- Pod status shows `CrashLoopBackOff`.
- Restart count increases.
- Application logs show startup failure, missing configuration, failed health checks, or process exit.

## First checks

- [ ] Confirm the namespace and workload name.
- [ ] Check current pod status.
- [ ] Inspect logs from the current and previous container instance.
- [ ] Review recent events.
- [ ] Check configuration, secrets, probes, and resource limits.

## Diagnostic commands

```bash
kubectl get pods -n <namespace>
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

## Decision sequence

1. If `kubectl logs --previous` shows an application error, fix the application configuration or image.
2. If events show failed probes, review liveness and readiness probe paths, ports, and startup timing.
3. If events show resource pressure, inspect requests, limits, and node capacity.
4. If configuration is missing, verify ConfigMaps, Secrets, environment variables, and mounted files.

## Related links

- [Kubernetes pod lifecycle documentation](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
- [Back to Kubernetes troubleshooting](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
