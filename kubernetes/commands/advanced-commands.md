# Kubernetes advanced commands

## Purpose

Collect advanced `kubectl` commands for structured output, API discovery, server-side operations, debugging, node maintenance, and authorization checks.

## API discovery and structured output

| Task | Command | When to use it |
| --- | --- | --- |
| List API resources | `kubectl api-resources` | Discover resource names, short names, and scopes. |
| Explain resource fields | `kubectl explain <resource>.<field>` | Check manifest schema from the cluster API. |
| Print JSONPath output | `kubectl get <resource> -o jsonpath='<path>'` | Extract one field for scripts or checks. |
| Use custom columns | `kubectl get <resource> -o custom-columns=<columns>` | Create readable views without external tools. |

### Explain a manifest field

```bash
kubectl explain deployment.spec.strategy
```

What it does: shows the API description for the Deployment rollout strategy field.

### Extract node names from pods

```bash
kubectl get pods -n app -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.nodeName}{"\n"}{end}'
```

What it does: prints each pod name and the node where it is scheduled.

## Dry runs and server-side apply

| Task | Command | When to use it |
| --- | --- | --- |
| Client dry run | `kubectl apply -f <file> --dry-run=client` | Validate local command construction. |
| Server dry run | `kubectl apply -f <file> --dry-run=server` | Ask the API server to validate without persisting. |
| Server-side apply | `kubectl apply --server-side -f <file>` | Let the API server track field ownership. |
| Force field conflicts | `kubectl apply --server-side --force-conflicts -f <file>` | Take ownership during controlled migrations. |

### Validate with the API server

```bash
kubectl apply -f k8s/deployment.yaml --dry-run=server
```

What it does: sends the object to the API server for validation without creating or updating it.

### Use server-side apply

```bash
kubectl apply --server-side -f k8s/
```

What it does: applies manifests using server-side field management.

> [!WARNING]
> `--force-conflicts` can overwrite fields owned by another manager. Use it only when you know which controller or workflow should own those fields.

## Debug workloads

| Task | Command | When to use it |
| --- | --- | --- |
| Create a debug container | `kubectl debug -it <pod> -n <namespace> --image=<image> --target=<container>` | Inspect a pod with a helper image. |
| Copy a pod for debug | `kubectl debug <pod> -n <namespace> --copy-to=<name> --container=<container> -- sh` | Investigate without changing the original pod. |
| Run a temporary pod | `kubectl run <name> --rm -it --image=<image> -- sh` | Test DNS, network, or tooling from inside the cluster. |
| Check resource usage | `kubectl top pod -n <namespace>` | Inspect CPU and memory when metrics are installed. |

### Start a temporary network debug pod

```bash
kubectl run net-debug --rm -it --restart=Never --image=curlimages/curl -- sh
```

What it does: starts an interactive temporary pod and removes it when the shell exits.

### Add an ephemeral debug container

```bash
kubectl debug -it web-7c9d8f9d6b-xm2ql -n app --image=busybox:1.36 --target=web -- sh
```

What it does: attaches a temporary debug container to the selected pod.

> [!NOTE]
> Ephemeral containers depend on cluster support and RBAC permissions. Some locked-down production clusters restrict this operation.

## Node maintenance

| Task | Command | When to use it |
| --- | --- | --- |
| Mark node unschedulable | `kubectl cordon <node>` | Stop new pods from scheduling on a node. |
| Drain node | `kubectl drain <node> --ignore-daemonsets --delete-emptydir-data` | Evict workloads before maintenance. |
| Re-enable scheduling | `kubectl uncordon <node>` | Return a node to service. |
| Show node details | `kubectl describe node <node>` | Inspect pressure, capacity, taints, and events. |

### Drain a node for maintenance

```bash
kubectl cordon ip-10-0-12-34.ec2.internal
kubectl drain ip-10-0-12-34.ec2.internal --ignore-daemonsets --delete-emptydir-data
```

What it does: prevents new scheduling and evicts eligible pods from the node.

> [!WARNING]
> `kubectl drain` can disrupt applications. Confirm PodDisruptionBudgets, replica counts, and maintenance windows before draining shared or production nodes.

## Authorization checks

| Task | Command | When to use it |
| --- | --- | --- |
| Check a verb/resource | `kubectl auth can-i <verb> <resource> -n <namespace>` | Confirm whether your identity can perform an action. |
| Check as another user | `kubectl auth can-i <verb> <resource> --as=<user>` | Validate RBAC from another identity. |
| List own permissions | `kubectl auth can-i --list -n <namespace>` | Review namespace-level access. |

### Check deployment update permission

```bash
kubectl auth can-i update deployments -n app
```

What it does: asks the API server whether the current identity can update Deployments in the `app` namespace.

## Official documentation

- [kubectl explain](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_explain/)
- [Server-side apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/)
- [Debug running pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)
- [Safely drain a node](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/)
- [Authorization overview](https://kubernetes.io/docs/reference/access-authn-authz/authorization/)

## Related links

- [Back to Kubernetes commands](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
