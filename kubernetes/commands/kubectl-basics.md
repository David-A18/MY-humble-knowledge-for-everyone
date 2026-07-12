# kubectl basics

## Purpose

Collect common `kubectl` commands for inspecting Kubernetes resources.

## Quick reference

| Task | Command |
| --- | --- |
| List namespaces | `kubectl get namespaces` |
| List pods in a namespace | `kubectl get pods -n <namespace>` |
| Describe a pod | `kubectl describe pod <pod-name> -n <namespace>` |
| View recent events | `kubectl get events -n <namespace> --sort-by=.lastTimestamp` |
| Follow logs | `kubectl logs -f <pod-name> -n <namespace>` |

## Inspect pods

```bash
kubectl get pods -n default
```

Expected output:

```text
NAME                     READY   STATUS    RESTARTS   AGE
example-7d9f6c8b6-abcde  1/1     Running   0          5m
```

## Related links

- [kubectl reference](https://kubernetes.io/docs/reference/kubectl/)
- [Back to Kubernetes commands](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
