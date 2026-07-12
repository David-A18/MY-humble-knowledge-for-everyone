# Kubernetes best practices

Status: Initial outline

Operational practices for safer and more reliable Kubernetes workloads.

## Expected content

- Resource requests and limits.
- Probes and graceful shutdown.
- Namespace and RBAC hygiene.
- Deployment strategies.
- Secrets handling.

## Starter checklist

- [ ] Define resource requests for production workloads.
- [ ] Use readiness probes for traffic eligibility.
- [ ] Keep liveness probes conservative.
- [ ] Avoid running containers as root when possible.

[Back to Kubernetes index](../README.md) | [Back to root index](../../README.md)
