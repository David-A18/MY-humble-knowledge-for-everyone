# Kubernetes daily usage commands

## Purpose

Collect the `kubectl` commands used most often during daily Kubernetes and EKS work: checking context, inspecting resources, reading logs, entering containers, and temporarily forwarding traffic.

## Context and namespace

| Task | Command | When to use it |
| --- | --- | --- |
| Show current context | `kubectl config current-context` | Before touching a cluster. |
| List known contexts | `kubectl config get-contexts` | When switching between local, staging, and production clusters. |
| Switch context | `kubectl config use-context <context>` | When moving to another cluster. |
| Set default namespace | `kubectl config set-context --current --namespace=<namespace>` | When most commands target one namespace. |
| Check API access | `kubectl auth can-i <verb> <resource> -n <namespace>` | Before running an operation that may be blocked by RBAC. |

### Confirm the active context

```bash
kubectl config current-context
kubectl config view --minify --output 'jsonpath={..namespace}{"\n"}'
```

What it does: prints the active cluster context and the namespace configured on that context.

> [!IMPORTANT]
> Always confirm context before applying, deleting, scaling, or draining resources, especially when your kubeconfig contains production EKS clusters.

## Inspect resources

| Task | Command | When to use it |
| --- | --- | --- |
| List namespaces | `kubectl get namespaces` | Discover available environments or tenancy boundaries. |
| List pods | `kubectl get pods -n <namespace>` | Check workload health. |
| List pods with node/IP details | `kubectl get pods -n <namespace> -o wide` | Debug scheduling, node, or networking issues. |
| Describe a pod | `kubectl describe pod <pod> -n <namespace>` | Inspect events, probes, mounts, and container state. |
| List all common workload resources | `kubectl get deploy,rs,sts,ds,job,cronjob -n <namespace>` | Build a quick workload inventory. |
| List services and ingress | `kubectl get svc,ingress -n <namespace>` | Check application entry points. |

### Inspect pods in a namespace

```bash
kubectl get pods -n app
kubectl get pods -n app -o wide
kubectl describe pod web-7c9d8f9d6b-xm2ql -n app
```

What it does: lists pod status, adds placement details, then opens the detailed pod view with events and container state.

## Logs and events

| Task | Command | When to use it |
| --- | --- | --- |
| Show pod logs | `kubectl logs <pod> -n <namespace>` | Read the current container log. |
| Follow pod logs | `kubectl logs -f <pod> -n <namespace>` | Watch startup or live traffic behavior. |
| Show previous container logs | `kubectl logs <pod> -n <namespace> --previous` | Diagnose a restarted container. |
| Show deployment logs | `kubectl logs deployment/<deployment> -n <namespace>` | Read logs without selecting a pod manually. |
| Show sorted events | `kubectl get events -n <namespace> --sort-by=.lastTimestamp` | See recent scheduling, pull, probe, and restart events. |

### Follow logs from a deployment

```bash
kubectl logs -f deployment/web -n app --tail=100
```

What it does: follows recent logs from pods selected by the `web` Deployment.

### Check recent namespace events

```bash
kubectl get events -n app --sort-by=.lastTimestamp
```

What it does: sorts namespace events by timestamp so recent failures are easier to find.

## Exec and port-forward

| Task | Command | When to use it |
| --- | --- | --- |
| Open a shell in a pod | `kubectl exec -it <pod> -n <namespace> -- sh` | Inspect files, environment, or network from inside the container. |
| Run one command in a pod | `kubectl exec <pod> -n <namespace> -- <command>` | Check a specific value without opening a shell. |
| Forward a pod port | `kubectl port-forward pod/<pod> <local>:<remote> -n <namespace>` | Test a pod from your workstation. |
| Forward a service port | `kubectl port-forward svc/<service> <local>:<remote> -n <namespace>` | Test service routing without exposing it externally. |

### Open a shell

```bash
kubectl exec -it web-7c9d8f9d6b-xm2ql -n app -- sh
```

What it does: starts an interactive shell in the target pod.

> [!TIP]
> Some minimal images do not include `bash`. Try `sh` first unless you know the image includes another shell.

### Forward a service locally

```bash
kubectl port-forward svc/web 8080:80 -n app
```

What it does: maps `localhost:8080` on your machine to port `80` on the Kubernetes Service.

## Official documentation

- [kubectl quick reference](https://kubernetes.io/docs/reference/kubectl/quick-reference/)
- [kubectl command overview](https://kubernetes.io/docs/reference/kubectl/)
- [Organizing cluster access using kubeconfig files](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)

## Related links

- [Back to Kubernetes commands](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
