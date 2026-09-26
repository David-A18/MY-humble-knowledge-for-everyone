---
type: "Explanation"
title: "End-to-end deployment"
description: "Map a complete delivery path from source control to running cloud infrastructure and application validation."
tags: [cross-topic-guides, end-to-end-deployment]
status: draft
maturity: initial-outline
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

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

- [Git index](../git/index.md)
- [Terraform index](../terraform/index.md)
- [Kubernetes index](../kubernetes/index.md)
- [AWS index](../cloud/aws/index.md)
- [Back to cross-topic guides](index.md)
- [Back to root index](../../README.md)
