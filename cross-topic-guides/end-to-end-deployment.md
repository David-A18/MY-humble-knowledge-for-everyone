# End-to-end deployment

Status: Initial outline

## Purpose

Map a complete delivery path from source control to running cloud infrastructure and application validation.

## Expected content

- Repository structure.
- CI validation.
- Infrastructure provisioning.
- Application deployment.
- Post-deployment checks.
- Rollback and incident notes.

## High-level flow

1. Create a reviewed pull request.
2. Run automated validation.
3. Provision or update infrastructure.
4. Build and publish application artifacts.
5. Deploy to the target environment.
6. Validate health, logs, metrics, and user-facing behavior.

## Related links

- [Git index](../git/README.md)
- [Terraform index](../terraform/README.md)
- [Kubernetes index](../kubernetes/README.md)
- [AWS index](../aws/README.md)
- [Back to cross-topic guides](README.md)
- [Back to root index](../README.md)
