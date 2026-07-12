# Kubernetes tricks

Small command patterns and techniques for faster Kubernetes investigation.

## Productivity patterns

| Task | Command | When to use it |
| --- | --- | --- |
| Shorten `kubectl` | `alias k=kubectl` | Reduce typing in interactive shells. |
| Show current context | `kubectl config current-context` | Confirm the target cluster quickly. |
| Set namespace once | `kubectl config set-context --current --namespace=<namespace>` | Avoid repeating `-n <namespace>`. |
| Sort events | `kubectl get events --sort-by=.lastTimestamp` | Read recent failures in order. |
| Show more pod details | `kubectl get pods -o wide` | Include node and pod IP details. |
| Show labels | `kubectl get pods --show-labels` | Debug selectors and ownership. |

### Create a short alias

```bash
alias k=kubectl
```

What it does: lets you type `k get pods` instead of `kubectl get pods` in the current shell.

> [!TIP]
> Add the alias to your shell profile only after you are comfortable reading and running the full command.

### Set the namespace for the current context

```bash
kubectl config set-context --current --namespace=app
```

What it does: changes the default namespace for the active context so future namespaced commands target `app`.

## Useful filters

| Task | Command | When to use it |
| --- | --- | --- |
| Select by label | `kubectl get pods -l app.kubernetes.io/name=<name>` | Find one app's resources. |
| Select running pods | `kubectl get pods --field-selector=status.phase=Running` | Filter by supported object fields. |
| Print names only | `kubectl get pods -o name` | Use concise output for review or scripts. |
| Print selected fields | `kubectl get pods -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName` | Build a quick table. |

### Find pods by recommended label

```bash
kubectl get pods -n app -l app.kubernetes.io/name=web
```

What it does: returns only pods labeled as the `web` application.

### Build a compact pod table

```bash
kubectl get pods -n app -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName,IP:.status.podIP
```

What it does: prints a focused table with pod name, node, and pod IP.

## API discovery

| Task | Command | When to use it |
| --- | --- | --- |
| List resource types | `kubectl api-resources` | Discover names, short names, and scope. |
| List API versions | `kubectl api-versions` | Check available API groups. |
| Explain a resource | `kubectl explain deployment` | Learn the schema from the cluster. |
| Explain a nested field | `kubectl explain deployment.spec.template.spec.containers` | Check manifest structure while writing YAML. |

### Explain a Kubernetes field

```bash
kubectl explain deployment.spec.template.spec.containers
```

What it does: asks the API server for schema help about containers inside a Deployment pod template.

## Temporary access

| Task | Command | When to use it |
| --- | --- | --- |
| Temporary debug pod | `kubectl run debug --rm -it --restart=Never --image=busybox:1.36 -- sh` | Test DNS or networking inside the cluster. |
| Forward a service | `kubectl port-forward svc/<service> <local>:<remote> -n <namespace>` | Test without exposing public ingress. |
| Follow deployment logs | `kubectl logs -f deployment/<name> -n <namespace>` | Watch an app without selecting pod names. |

### Start a temporary debug shell

```bash
kubectl run debug --rm -it --restart=Never --image=busybox:1.36 -- sh
```

What it does: starts a short-lived pod for cluster-internal checks and deletes it after the shell exits.

## Official documentation

- [kubectl quick reference](https://kubernetes.io/docs/reference/kubectl/quick-reference/)
- [kubectl explain](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_explain/)
- [Labels and selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)

## Related links

- [Kubernetes daily usage commands](../commands/daily-usage.md)
- [Advanced Kubernetes commands](../commands/advanced-commands.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
