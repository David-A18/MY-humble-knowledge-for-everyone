# Kubernetes tricks

Small shortcuts can save typing, but they should not hide the target
cluster or namespace. Start with a task-led guide below; use a shortcut
only after you understand what its full command does.

## Choose a task

| Need | Start here | Why |
| --- | --- | --- |
| Check where `kubectl` will read | [Begin a safe kubectl inspection session](../commands/daily-usage.md) | Confirm context and namespace before reading workload evidence. |
| Find a field for a manifest | [Inspect a Kubernetes API field before changing a manifest](../commands/advanced-commands.md) | Separate the API schema, stored object, and proposed file. |
| Trace a Deployment to its Pods | [Inspect a Deployment with kubectl](../commands/kubectl-basics.md) | Use the actual selector and read states, events, and logs. |
| Investigate a user-facing failure | [Find the first failing Kubernetes boundary](../troubleshooting/common-solutions.md) | Locate the first failed handoff before choosing a fix. |
| Compare and apply a reviewed file | [Review and apply a Kubernetes manifest change](../commands/common-commands.md) | Inspect the diff, then verify both rollout and user outcome. |
| Examine CPU or memory symptoms | [Investigate Kubernetes resource pressure](../commands/workflows.md) | Distinguish scheduling, container limits, and node pressure. |

## Two safe shortcuts for reading

To see Pods on their nodes without changing the cluster:

```bash
kubectl config current-context
kubectl get pods -n <namespace> -o wide
```

The first command shows the active context name. Confirm its cluster
mapping and replace `<namespace>` with the intended namespace before
the second command. The wide view adds details such as node and Pod
IP; it does not explain a failing Pod by itself.
[The inspection guide](../commands/daily-usage.md) shows the next
evidence to read.

To see the labels that selectors can match:

```bash
kubectl get pods -n <namespace> --show-labels
```

A label's presence does not prove that a Service selects a healthy
endpoint. Compare the Service selector and EndpointSlice conditions
using the [failure-boundary guide](../troubleshooting/common-solutions.md).

A shell alias such as `alias k=kubectl` only changes what you type
in that shell. It does not select a safer cluster. Changing the
default namespace of a context, creating a debug Pod, forwarding
a port, or changing workload state needs its own target and
permission check; use the task guide or official procedure first.

## Official documentation

- [kubectl quick reference](https://kubernetes.io/docs/reference/kubectl/quick-reference/)
- [kubectl get](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/)
- [Labels and selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)

[Back to Kubernetes index](../index.md).
