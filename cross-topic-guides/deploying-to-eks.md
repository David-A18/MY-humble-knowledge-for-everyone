# Deploying to EKS

## Purpose

Plan the moving parts of deploying applications to Amazon EKS.

## Deployment flow

| Step | Command or check | Why it matters |
| --- | --- | --- |
| Confirm AWS identity | `aws sts get-caller-identity` | Ensures the expected account and role are active. |
| Connect kubeconfig | `aws eks update-kubeconfig --region <region> --name <cluster>` | Points `kubectl` at the EKS cluster. |
| Confirm context | `kubectl config current-context` | Prevents applying to the wrong cluster. |
| Check permissions | `kubectl auth can-i update deployments -n <namespace>` | Finds access issues before deployment. |
| Preview manifests | `kubectl diff -f <path>` | Shows live changes before mutation. |
| Apply manifests | `kubectl apply -f <path>` | Updates Kubernetes resources. |
| Watch rollout | `kubectl rollout status deployment/<name> -n <namespace>` | Confirms the new version becomes available. |

## Connect and validate

```bash
aws sts get-caller-identity
aws eks update-kubeconfig --region eu-west-1 --name production-platform
kubectl config current-context
kubectl get namespaces
kubectl auth can-i update deployments -n app
```

What it does: confirms AWS identity, updates kubeconfig, checks Kubernetes context, lists namespaces, and validates deployment permission.

> [!IMPORTANT]
> EKS authentication uses AWS credentials, and Kubernetes authorization uses cluster permissions. Validate both before deployment.

## Deploy manifests

```bash
kubectl diff -f k8s/
kubectl apply -f k8s/
kubectl rollout status deployment/web -n app
kubectl get pods -n app -l app.kubernetes.io/name=web -o wide
```

What it does: previews changes, applies manifests, waits for the Deployment, and confirms the new pods.

> [!WARNING]
> `kubectl apply` mutates live resources. Confirm context, namespace, and diff output before applying production manifests.

## Deploy a new image

Use this when making an urgent image-only change outside the normal manifest flow.

```bash
kubectl set image deployment/web web=123456789012.dkr.ecr.eu-west-1.amazonaws.com/web:2026-07-12 -n app
kubectl rollout status deployment/web -n app
```

What it does: updates the `web` container image in the Deployment and waits for the rollout.

> [!WARNING]
> `kubectl set image` can create drift if manifests or GitOps are the source of truth. Prefer updating the manifest or deployment pipeline.

## Roll back

```bash
kubectl rollout history deployment/web -n app
kubectl rollout undo deployment/web -n app
kubectl rollout status deployment/web -n app
```

What it does: reviews prior revisions, rolls back to the previous revision, and waits for the rollback.

> [!WARNING]
> Rollback is a live production change. Record the failing revision and image tag before rollback when possible.

## Post-deploy verification

```bash
kubectl get deploy,rs,pods -n app -l app.kubernetes.io/name=web
kubectl logs deployment/web -n app --tail=100
kubectl get svc,ingress -n app
kubectl get events -n app --sort-by=.lastTimestamp
```

What it does: checks workload status, reads recent logs, confirms entry points, and reviews recent warning events.

## Prerequisites

- EKS cluster exists and kubeconfig access is configured.
- Container image exists in Amazon ECR or the selected registry.
- Namespace, service account, and workload IAM permissions are ready.
- Kubernetes manifests, Helm chart, or Kustomize overlay are reviewed.
- Deployment and rollback owner is known.

## Validation checklist

- [ ] Confirm cluster context.
- [ ] Confirm AWS account and assumed role.
- [ ] Confirm image tag and registry.
- [ ] Confirm namespace and service account.
- [ ] Confirm EKS Pod Identity or IRSA permissions for AWS service access.
- [ ] Run `kubectl diff` or equivalent pipeline preview.
- [ ] Check rollout status.
- [ ] Check service or ingress reachability.
- [ ] Review logs and recent events after deployment.

## Official documentation

- [Amazon EKS kubeconfig](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)
- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [kubectl rollout](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/)
- [Amazon EKS workload IAM access](https://docs.aws.amazon.com/eks/latest/userguide/service-accounts.html)

## Related links

- [Amazon EKS documentation](https://docs.aws.amazon.com/eks/)
- [Kubernetes commands](../kubernetes/commands/README.md)
- [Kubernetes command workflows](../kubernetes/commands/workflows.md)
- [EKS operations](eks-operations.md)
- [Back to cross-topic guides](README.md)
- [Back to root index](../README.md)
