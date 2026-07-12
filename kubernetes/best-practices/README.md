# Kubernetes best practices

Operational practices for safer and more reliable Kubernetes workloads.

## Workload reliability

| Practice | Why it matters |
| --- | --- |
| Set CPU and memory requests | Helps the scheduler place pods and supports capacity planning. |
| Set limits intentionally | Prevents noisy-neighbor behavior, but avoid unrealistic memory limits. |
| Use readiness probes | Keeps traffic away from pods that are not ready. |
| Use startup probes for slow apps | Prevents liveness probes from killing applications during normal startup. |
| Keep liveness probes conservative | Avoids restart loops caused by temporary dependency failures. |
| Handle graceful shutdown | Lets pods finish requests during rollout or node maintenance. |

### Inspect resource requests and limits

```bash
kubectl describe pod <pod-name> -n app
```

What it does: shows container requests, limits, probe configuration, events, and recent state transitions.

## Deployment safety

| Practice | Why it matters |
| --- | --- |
| Use declarative manifests | Keeps desired state reviewable and repeatable. |
| Review `kubectl diff` before apply | Shows live changes before mutation. |
| Watch rollout status | Catches failed rollouts quickly. |
| Keep rollback commands ready | Reduces recovery time during incidents. |
| Avoid manual drift | Prevents GitOps or IaC systems from fighting one-off changes. |

### Deploy with a verification loop

```bash
kubectl diff -f k8s/
kubectl apply -f k8s/
kubectl rollout status deployment/web -n app
kubectl get pods -n app -l app.kubernetes.io/name=web -o wide
```

What it does: previews the change, applies it, waits for rollout completion, and checks the resulting pods.

> [!WARNING]
> `kubectl apply`, `scale`, `delete`, and `rollout undo` mutate live resources. Confirm context and namespace before running them.

## Access and isolation

| Practice | Why it matters |
| --- | --- |
| Use namespaces intentionally | Separates environments, teams, or application groups. |
| Grant least-privilege RBAC | Limits blast radius for users, services, and automation. |
| Prefer service accounts per workload | Makes workload permissions explicit. |
| Avoid default service account privileges | Reduces accidental access from pods. |
| Use NetworkPolicies where supported | Restricts east-west pod traffic. |

### Check permissions before operating

```bash
kubectl auth can-i update deployments -n app
```

What it does: checks whether the current identity can update Deployments in the `app` namespace.

## Secrets and configuration

| Practice | Why it matters |
| --- | --- |
| Store non-sensitive config in ConfigMaps | Keeps application configuration separate from images. |
| Store sensitive values in Secrets or external secret tooling | Avoids hardcoding credentials in manifests or images. |
| Restrict Secret access with RBAC | Secret read access can expose credentials. |
| Rotate credentials deliberately | Reduces impact from leaked or stale credentials. |

### Inspect Secret metadata only

```bash
kubectl get secret -n app
kubectl describe secret <secret-name> -n app
```

What it does: lists Secret objects and metadata without printing secret values.

> [!WARNING]
> Avoid printing Secret data in shared terminals, logs, screenshots, or tickets.

## EKS-specific habits

| Practice | Why it matters |
| --- | --- |
| Confirm AWS identity | EKS authentication depends on AWS credentials or assumed roles. |
| Prefer EKS access entries for cluster access | Centralizes IAM principal access through EKS APIs. |
| Use Pod Identity or IRSA for AWS service access | Grants workloads fine-grained AWS permissions. |
| Review EKS add-on ownership | Avoids unmanaged drift in VPC CNI, CoreDNS, kube-proxy, and controllers. |
| Track cost by namespace and labels | Supports EKS cost visibility and allocation. |

### Confirm identity before EKS work

```bash
aws sts get-caller-identity
kubectl config current-context
kubectl auth can-i get pods -n app
```

What it does: confirms the AWS identity, active Kubernetes context, and namespace-level Kubernetes permission.

## Starter checklist

- [ ] Define resource requests for production workloads.
- [ ] Use readiness probes for traffic eligibility.
- [ ] Keep liveness probes conservative.
- [ ] Avoid running containers as root when possible.
- [ ] Confirm context and namespace before mutations.
- [ ] Use workload-specific service accounts.
- [ ] Keep labels consistent for ownership, selection, and cost reporting.
- [ ] Keep rollback and diagnostics commands close to deployment workflows.

## Official documentation

- [Resource management for pods and containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Configure liveness, readiness, and startup probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [RBAC good practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/)
- [Good practices for Kubernetes Secrets](https://kubernetes.io/docs/concepts/security/secrets-good-practices/)
- [Amazon EKS Best Practices Guide](https://docs.aws.amazon.com/eks/latest/best-practices/introduction.html)

## Related links

- [Kubernetes command workflows](../commands/workflows.md)
- [Kubernetes on AWS](../../cross-topic-guides/kubernetes-on-aws.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
