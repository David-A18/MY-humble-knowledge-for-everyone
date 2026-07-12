# Kubernetes common commands

## Purpose

Collect common `kubectl` commands for applying manifests, comparing changes, managing rollouts, scaling workloads, deleting resources, filtering output, and exporting useful views.

## Apply and compare changes

| Task | Command | When to use it |
| --- | --- | --- |
| Preview manifest changes | `kubectl diff -f <file-or-dir>` | Before applying declarative configuration. |
| Apply manifests | `kubectl apply -f <file-or-dir>` | Create or update resources from YAML. |
| Apply with pruning label | `kubectl apply -f <dir> -l <selector>` | Keep a labeled resource set aligned with files. |
| View live YAML | `kubectl get <type>/<name> -n <namespace> -o yaml` | Inspect the server-side object. |

### Preview and apply a manifest directory

```bash
kubectl diff -f k8s/
kubectl apply -f k8s/
```

What it does: shows the difference between local manifests and live objects, then applies the desired state.

> [!IMPORTANT]
> `kubectl apply` changes live cluster resources. Review the target context, namespace, and diff first.

## Rollouts

| Task | Command | When to use it |
| --- | --- | --- |
| Check rollout status | `kubectl rollout status deployment/<name> -n <namespace>` | Wait for a Deployment to finish updating. |
| View rollout history | `kubectl rollout history deployment/<name> -n <namespace>` | See previous revisions. |
| Undo last rollout | `kubectl rollout undo deployment/<name> -n <namespace>` | Revert the latest Deployment revision. |
| Restart pods safely | `kubectl rollout restart deployment/<name> -n <namespace>` | Trigger new pods without changing the image or manifest. |

### Watch deployment rollout

```bash
kubectl rollout status deployment/web -n app
```

What it does: waits until the `web` Deployment completes or reports a rollout failure.

### Roll back a deployment

```bash
kubectl rollout history deployment/web -n app
kubectl rollout undo deployment/web -n app
kubectl rollout status deployment/web -n app
```

What it does: reviews revisions, reverts to the previous revision, and watches the rollback complete.

> [!WARNING]
> A rollback changes production behavior immediately. Confirm the image, configuration, and incident context before running it.

## Scale and delete

| Task | Command | When to use it |
| --- | --- | --- |
| Scale a deployment | `kubectl scale deployment/<name> --replicas=<count> -n <namespace>` | Temporarily change capacity. |
| Delete one resource | `kubectl delete <type>/<name> -n <namespace>` | Remove a known object. |
| Delete resources from files | `kubectl delete -f <file-or-dir>` | Tear down a manifest-managed resource set. |
| Delete completed jobs | `kubectl delete job <name> -n <namespace>` | Clean up old one-off work. |

### Temporarily scale a deployment

```bash
kubectl scale deployment/web --replicas=4 -n app
kubectl rollout status deployment/web -n app
```

What it does: changes desired replicas for the Deployment and waits for the new pods to become available.

> [!TIP]
> If GitOps or another controller owns the workload, make the replica change in the source of truth or expect the controller to revert it.

### Delete a resource

```bash
kubectl delete job/db-migration-20260712 -n app
```

What it does: deletes the named Job and the pods owned by that Job.

> [!WARNING]
> `kubectl delete` removes live resources. Check owner references and persistent storage behavior before deleting workloads or PVCs.

## Select and format output

| Task | Command | When to use it |
| --- | --- | --- |
| Filter by label | `kubectl get pods -l app=<name> -n <namespace>` | Find resources that belong to one app. |
| Filter by field | `kubectl get pods --field-selector=status.phase=Running -n <namespace>` | Find resources by supported object fields. |
| Print names only | `kubectl get pods -n <namespace> -o name` | Feed resources into scripts or review concise output. |
| Print JSON | `kubectl get deployment/<name> -n <namespace> -o json` | Inspect structured data with tools. |
| Print custom columns | `kubectl get pods -n <namespace> -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName` | Build readable operational views. |

### Find pods for one application

```bash
kubectl get pods -n app -l app.kubernetes.io/name=web
```

What it does: lists only pods that match the recommended application label.

### Show pod placement

```bash
kubectl get pods -n app -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName,PHASE:.status.phase
```

What it does: prints pod name, node, and phase in a compact table.

## Official documentation

- [kubectl reference](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands)
- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Recommended labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/)

## Related links

- [Back to Kubernetes commands](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
