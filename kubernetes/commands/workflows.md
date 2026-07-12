# Kubernetes command workflows

## Purpose

Provide repeatable command sequences for common operational workflows: inspecting a workload, deploying safely, rolling back, debugging service reachability, and checking resource pressure.

## Inspect a workload

Use this when an application looks unhealthy or a deployment needs a quick status check.

```bash
kubectl get deploy,rs,pods -n app -l app.kubernetes.io/name=web
kubectl describe deployment/web -n app
kubectl get events -n app --sort-by=.lastTimestamp
kubectl logs deployment/web -n app --tail=100
```

What it does: checks the Deployment, related ReplicaSets and pods, reviews recent events, and reads recent logs.

Expected signals:

- Pods show `Running` or `Completed` when expected.
- Deployment conditions show progress and availability.
- Events do not show repeated image pull, scheduling, probe, or mount failures.

## Deploy safely

Use this for manifest-based changes when the repository or pipeline is the source of truth.

```bash
kubectl config current-context
kubectl diff -f k8s/
kubectl apply -f k8s/
kubectl rollout status deployment/web -n app
kubectl get pods -n app -l app.kubernetes.io/name=web -o wide
```

What it does: confirms the cluster, previews changes, applies manifests, waits for the rollout, and verifies pod placement and status.

> [!IMPORTANT]
> In EKS, also confirm the AWS identity behind your kubeconfig with `aws sts get-caller-identity` when access depends on assumed roles.

## Roll back a failed deployment

Use this when a Deployment rollout is failing and the previous revision is known to be safer.

```bash
kubectl rollout status deployment/web -n app
kubectl rollout history deployment/web -n app
kubectl rollout undo deployment/web -n app
kubectl rollout status deployment/web -n app
kubectl logs deployment/web -n app --tail=100
```

What it does: confirms the failed rollout, checks history, reverts to the previous revision, waits for completion, and checks logs.

> [!WARNING]
> Rollback is a live production change. Capture the failing image tag, revision, and error symptoms before reverting when incident time allows.

## Debug service reachability

Use this when pods are running but users or internal callers cannot reach the application.

```bash
kubectl get svc,endpoints,endpointslice -n app
kubectl describe svc web -n app
kubectl get pods -n app -l app.kubernetes.io/name=web -o wide
kubectl port-forward svc/web 8080:80 -n app
```

What it does: checks Service objects, endpoint population, selected pods, and local connectivity through a port-forward.

If endpoints are missing:

- Confirm the Service selector matches pod labels.
- Confirm pods are Ready.
- Review readiness probe failures in pod events.

## Check resource pressure

Use this when pods are Pending, evicted, throttled, or restarting under load.

```bash
kubectl top pods -n app
kubectl top nodes
kubectl describe pod <pod-name> -n app
kubectl describe node <node-name>
```

What it does: checks live CPU/memory metrics, pod scheduling details, and node pressure or capacity signals.

> [!NOTE]
> `kubectl top` requires the metrics API, usually provided by Metrics Server or a managed platform integration.

## Official documentation

- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Debug pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/)
- [Debug services](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/)
- [Resource management for pods and containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Amazon EKS kubeconfig](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)

## Related links

- [Back to Kubernetes commands](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
