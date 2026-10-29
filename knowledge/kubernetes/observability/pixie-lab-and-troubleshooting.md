---
type: Troubleshooting Guide
title: Pixie deployment lab and troubleshooting
description: Check prerequisites and investigate synthetic HTTP traffic.
tags:
- kubernetes
- observability
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: requirements
  resource: https://docs.px.dev/installing-pixie/requirements/
  title: Requirements
- id: install-choices
  resource: https://docs.px.dev/installing-pixie/install-guides/
  title: Install choices
- id: cli
  resource: https://docs.px.dev/using-pixie/using-cli/
  title: CLI
---

# Pixie deployment lab and troubleshooting

## Purpose

Check prerequisites and investigate synthetic HTTP traffic.

Sources reviewed: 2026-10-29. See the [validation record](../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Environment gate

Use a dedicated compatible Linux-node cluster, such as a supported EKS EC2-node configuration. Check the current release/node requirements. The published matrix excludes environments such as kind and EKS Fargate; do not reuse the kind-based labs as Pixie installation recipes.[^requirements][^install-choices][^cli]

Choose an accessible hosted backend or follow the self-hosted guide. Record CLI, Vizier, PEM, kernel, and Kubernetes versions. No Pixie runtime version was validated on the authoring host.

## Installation and traffic

Obtain the CLI from official release instructions and authenticate to your chosen backend. Review the resources and privileges before deployment.

```bash
px deploy
kubectl get pods -n pl
```

What it does: deploys Pixie in the selected context and inspects its usual namespace. Confirm the namespace chosen by your options rather than hard-coding it in automation.

Deploy the web application from the [manifest regression lab](../applications-and-tools/manifest-validation/regression-lab-and-ci.md). Generate repeated requests using its curl Pod. Open cluster/HTTP views, filter to the lab namespace, and run the previous chapter's PxL query.

## Acceptance

Find the service and recent requests; verify timestamps and response codes match synthetic traffic. Introduce an unavailable target port, observe failure symptoms, restore it, and verify recovery. An empty table can mean unsupported collection rather than absent traffic.

| Symptom | Check |
| --- | --- |
| PEM cannot schedule | Node compatibility, selectors, security constraints, resources. |
| Empty HTTP table | Time window, protocol/library support, probe attachment. |
| Missing nodes | DaemonSet coverage and architecture. |
| Query error | Table schema, PxL types, backend connectivity. |
| Short history | Memory retention and resource pressure. |

## Cleanup

Use the installed CLI's documented deletion procedure for the dedicated Vizier. Inspect removal scope; preserve shared deployments. Revoke temporary tokens and remove only synthetic workloads. Review payload permissions before granting users access.

## Related links

- [Requirements](https://docs.px.dev/installing-pixie/requirements/)
- [Install choices](https://docs.px.dev/installing-pixie/install-guides/)
- [CLI](https://docs.px.dev/using-pixie/using-cli/)
- [Back to parent index](index.md)
- [Back to major area](../index.md)
- [Back to root index](../../../README.md)

[^requirements]: [Requirements](https://docs.px.dev/installing-pixie/requirements/).
[^install-choices]: [Install choices](https://docs.px.dev/installing-pixie/install-guides/).
[^cli]: [CLI](https://docs.px.dev/using-pixie/using-cli/).
