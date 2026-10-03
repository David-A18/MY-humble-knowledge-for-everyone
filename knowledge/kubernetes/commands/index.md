# Kubernetes commands

Task-led `kubectl` guides for checking a target, reading workload
evidence, and making a reviewed change.

## Articles

| Article | Purpose |
| --- | --- |
| [Begin a safe kubectl inspection session](daily-usage.md) | Confirm the context and namespace, scan workloads, and choose an evidence-led next step. |
| [Review and apply a Kubernetes manifest change](common-commands.md) | Compare a reviewed Deployment file with live state, apply it, and verify rollout and user outcome. |
| [Inspect a Kubernetes API field before changing a manifest](advanced-commands.md) | Compare the field schema, live Deployment, and proposed file with a server dry run. |
| [Investigate Kubernetes resource pressure](workflows.md) | Separate scheduling requests, container limits, and node pressure using Pod and node evidence. |
| [Choose the right control path for an EKS change](eksctl-commands.md) | Identify the Kubernetes, EKS compute, or IAM owner before choosing a procedure. |
| [Inspect a Deployment with kubectl](kubectl-basics.md) | Confirm the cluster, follow a Deployment to its Pods, then read states, events, and logs. |

## Official documentation

- [kubectl quick reference](https://kubernetes.io/docs/reference/kubectl/quick-reference/)
- [kubectl reference](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands)
- [kubectl command overview](https://kubernetes.io/docs/reference/kubectl/)
- [eksctl user guide](https://docs.aws.amazon.com/eks/latest/eksctl/what-is-eksctl.html)

## Related links

- [EKS operations](../../cross-topic-guides/eks-operations.md)
- [Back to Kubernetes index](../index.md)
- [Back to root index](../../../README.md)
