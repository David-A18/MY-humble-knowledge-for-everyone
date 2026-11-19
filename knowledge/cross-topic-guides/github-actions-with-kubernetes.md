---
type: How-to Guide
title: GitHub Actions with Kubernetes
description: Build an image, validate manifests, deploy to a Kubernetes cluster, and confirm the rollout from GitHub Actions, or hand deployment to GitOps.
tags: [cross-topic-guides, github-actions-with-kubernetes, kubernetes, ci-cd]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: k8s-deployment
    resource: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
    title: Kubernetes Deployments
  - id: kubectl-rollout
    resource: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/
    title: kubectl rollout
  - id: eks-kubeconfig
    resource: https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html
    title: Connect kubectl to an EKS cluster
  - id: eks-access-entries
    resource: https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html
    title: EKS access entries
  - id: gha-oidc-aws
    resource: https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws
    title: Configuring OpenID Connect in Amazon Web Services
---

# GitHub Actions with Kubernetes

A deployment pipeline turns a merged change into a running application. It
builds a container image, checks the Kubernetes manifests, updates the cluster,
and waits until the new version is actually healthy. If the new version fails,
the pipeline stops and the previous version keeps serving.

## Two ways to deploy

| Approach | How it works | Choose it when |
| --- | --- | --- |
| **Push** (this page) | The workflow authenticates to the cluster and runs `kubectl`. | You have one or a few clusters and want a simple start. |
| **GitOps** | The workflow only updates manifests in Git; Argo CD or Flux in the cluster applies them. | You want the cluster to pull changes, with no cluster credentials in CI. See [GitOps on EKS](gitops-on-eks.md). |

## The steps

1. **Build and tag the image** with the commit SHA, never a moving tag such as
   `latest`, so every deployment names exactly one image.
2. **Scan and push** the image to your registry.
3. **Validate the manifests** before they reach the cluster. See
   [manifest validation](../kubernetes/applications-and-tools/manifest-validation/index.md).
4. **Authenticate** with short-lived credentials. On EKS, GitHub's OIDC token
   becomes an AWS role, and an EKS access entry maps that role to Kubernetes
   permissions limited to the target namespace.[^gha-oidc-aws][^eks-access-entries]
5. **Deploy** the new image to the intended namespace.
6. **Wait for the rollout** and fail the job if it does not finish in time.[^kubectl-rollout]

## Example deploy job

> [!WARNING]
> This job changes a live cluster. Try it against a disposable cluster or
> namespace first, and pin each action to a full commit SHA.

```yaml
deploy:
  runs-on: ubuntu-latest
  environment: staging
  permissions:
    contents: read
    id-token: write
  steps:
    - uses: actions/checkout@<full-commit-sha> # v7.0.1
    - uses: aws-actions/configure-aws-credentials@<full-commit-sha>
      with:
        role-to-assume: arn:aws:iam::111122223333:role/deploy-web-staging
        aws-region: eu-west-1
    - name: Connect kubectl to the cluster
      run: aws eks update-kubeconfig --name staging-cluster --region eu-west-1
    - name: Check the manifests against the live API
      run: kubectl apply --dry-run=server -n web -f k8s/
    - name: Deploy
      run: |
        kubectl apply -n web -f k8s/
        kubectl set image -n web deployment/web web="registry.example.com/web:${GITHUB_SHA}"
    - name: Wait for the new version to become ready
      run: kubectl rollout status -n web deployment/web --timeout=180s
```

What it does: assumes a deploy role through OIDC, writes a kubeconfig for the
EKS cluster,[^eks-kubeconfig] checks the manifests with a server-side dry run,
applies them, points the `web` Deployment at the image built for this commit,
and waits until the new Pods are ready. A Deployment replaces Pods gradually,
so old Pods keep serving while new ones start.[^k8s-deployment]

## When the rollout fails

`kubectl rollout status` exits with an error when the timeout passes, which
fails the job. Then:

1. Look at why the new Pods are not ready:

   ```bash
   kubectl get pods -n web -l app=web
   kubectl describe deployment -n web web
   ```

   What it does: lists the Pods and shows the Deployment's events, which usually
   name the cause, such as an image that cannot be pulled or a failing
   readiness probe.

2. Return to the previous version if users are affected:

   ```bash
   kubectl rollout undo -n web deployment/web
   ```

   What it does: restores the previous Pod template in the cluster. It does not
   change Git, so revert or fix the commit too, or the next deployment repeats
   the failure.

The [Kubernetes troubleshooting guides](../kubernetes/troubleshooting/index.md)
cover each failure in detail.

## Related links

- [Local deployment learning path](local-deployment-learning-path.md) - practice deploy, break, diagnose, and roll back locally.
- [Deploying to EKS](deploying-to-eks.md)
- [EKS workload identity](eks-workload-identity.md)
- [GitHub Actions with Terraform](github-actions-with-terraform.md)
- [End-to-end deployment](end-to-end-deployment.md)
- [Back to cross-topic guides](index.md)

[^k8s-deployment]: [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
[^kubectl-rollout]: [kubectl rollout](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/)
[^eks-kubeconfig]: [Connect kubectl to an EKS cluster](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)
[^eks-access-entries]: [EKS access entries](https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html)
[^gha-oidc-aws]: [Configuring OpenID Connect in Amazon Web Services](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws)
