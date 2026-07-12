# GitHub Actions with Kubernetes

Status: Initial outline

## Purpose

Outline CI/CD workflows for validating and deploying Kubernetes workloads from GitHub Actions.

## Expected content

- Manifest validation.
- Image build and scan stages.
- Cluster authentication.
- Deployment approvals.
- Rollout validation.

## Deployment checklist

- [ ] Build and tag the image immutably.
- [ ] Validate manifests before applying.
- [ ] Authenticate with least privilege.
- [ ] Apply changes to the intended namespace.
- [ ] Verify rollout status and logs.

## Related links

- [GitHub Actions documentation](https://docs.github.com/actions)
- [Kubernetes deployments documentation](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Back to cross-topic guides](README.md)
- [Back to root index](../README.md)
