# EKS human identity and Kubernetes RBAC

## Purpose

Use this guide to separate human authentication to Amazon EKS from workload identity and to bind authenticated users or groups to Kubernetes permissions safely.

## The three identity problems

| Problem | Primary mechanism | Purpose |
| --- | --- | --- |
| Workload to AWS | IRSA or EKS Pod Identity. | Pods call AWS APIs. |
| Human to AWS | IAM Identity Center or IAM federation. | People access AWS accounts and roles. |
| Human to Kubernetes | EKS access entries, IAM authentication, or external OIDC where supported. | People use `kubectl` against the cluster. |

Do not mix these together. A Pod's AWS permissions and a developer's Kubernetes RBAC permissions solve different problems.

## RBAC binding pattern

Use groups where possible. Bind a group to the smallest useful role and namespace.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-read
  namespace: payments
subjects:
  - kind: Group
    name: payments-developers
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io
```

What it does: allows members of `payments-developers` to view resources in the `payments` namespace without granting cluster-wide admin access.

## Access review commands

```bash
kubectl auth can-i get pods -n payments
kubectl auth can-i create deployments -n payments
kubectl auth can-i '*' '*' --all-namespaces
```

What it does: tests what the current Kubernetes identity can do.

## Governance checklist

- Prefer group-based bindings over individual user bindings.
- Keep cluster-admin access rare and time-bound.
- Bind developers at namespace scope when possible.
- Document which identity claim maps to Kubernetes username and groups.
- Avoid using mutable email addresses as the only stable identity.
- Review access after team changes and incident response events.
- Keep workload service accounts separate from human identities.

> [!IMPORTANT]
> Authentication proves who the caller is. Kubernetes RBAC decides what that caller can do. Both must be correct.

## Related links

- Official documentation: [Amazon EKS access entries](https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html)
- Official documentation: [Kubernetes RBAC authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [OIDC fundamentals](oidc-fundamentals.md)
- [OIDC token validation](oidc-token-validation.md)
- [EKS workload identity](../../cross-topic-guides/eks-workload-identity.md)
- [Back to identity federation](README.md)
- [Back to security index](../README.md)
- [Back to root index](../../README.md)
