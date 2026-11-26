---
type: How-to Guide
title: Find logs across Kubernetes replicas with Stern
description: Use Stern to collect a bounded log snapshot across replicas and follow a rollout from one terminal.
tags: [kubernetes, logging, stern, troubleshooting]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: stern-docs
    resource: https://github.com/stern/stern/blob/v1.35.0/README.md
    title: Stern v1.35.0 usage and options
  - id: stern-release
    resource: https://github.com/stern/stern/releases/tag/v1.35.0
    title: Stern v1.35.0 release files
  - id: kubectl-logs
    resource: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_logs/
    title: Kubernetes kubectl logs reference
  - id: kubectl-auth
    resource: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_auth/kubectl_auth_can-i/
    title: Kubernetes kubectl auth can-i reference
---

# Find logs across Kubernetes replicas with Stern

If an intermittent error can come from any replica, use Stern to bring logs
from matching Pods and containers into one terminal. During a rollout, Stern
adds matching new Pods to the stream and drops deleted Pods.[^stern-docs]

## Set up the client

Download the Stern v1.35.0 archive for your operating system and architecture
from the project's release, compare its digest with the published checksums,
then extract the binary and put it on your PATH. Use `stern --version` to
confirm which release your shell will run.[^stern-release][^stern-docs]

Use a kubeconfig context and namespace you are authorized to inspect. Make
the scope explicit with `--context` and `--namespace` in each
example.[^stern-docs]

## Gather a bounded snapshot

Replace `staging`, `payments`, and `app=checkout` with the context, namespace,
and label for the workload you want to inspect.[^stern-docs]

```bash
stern --context staging --namespace payments --selector app=checkout \
  --since 10m --tail 100 --no-follow --max-log-requests 3
```

What it does: selects Pods by label, asks for recent log lines, and exits after
collecting them. The concurrency flag limits simultaneous log requests in
snapshot mode.[^stern-docs]

## Watch a rollout

```bash
stern --context staging --namespace payments --selector app=checkout \
  --container '^api$' --since 2m --timestamps --max-log-requests 10
```

What it does: follows matching Pods while limiting the stream to the container
named `api`. With follow enabled, Stern exits with an error if the number of
concurrent log requests reaches its limit. Narrow the selection first if a
workload has more streams than expected.[^stern-docs]

## Diagnose an empty or denied result

| Symptom | First check |
| --- | --- |
| No lines | Confirm the namespace and label selector, then check whether the selected container logged within the specified time window.[^stern-docs] |
| Forbidden | Check access to list and watch Pods and read the Pod log subresource in the chosen context and namespace.[^stern-docs][^kubectl-auth] |
| Need the previous container instance | Use `kubectl logs` with the specific Pod, container, and `--previous`.[^kubectl-logs] |

## Evidence and limits

The checksum-verified Stern v1.35.0 Windows AMD64 binary reported its version
and listed the options used above. The cluster queries were reviewed against
the upstream references. No live log streams were tested.

## Related links

- [Daily kubectl commands](../commands/daily-usage.md)
- [Kubernetes observability](../observability/index.md)
- [Kubernetes applications and tools](index.md)
- [Kubernetes index](../index.md)
- [Knowledge home](../../index.md)

[^stern-docs]: [Stern v1.35.0 usage and options](https://github.com/stern/stern/blob/v1.35.0/README.md)
[^stern-release]: [Stern v1.35.0 release files](https://github.com/stern/stern/releases/tag/v1.35.0)
[^kubectl-logs]: [Kubernetes kubectl logs reference](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_logs/)
[^kubectl-auth]: [Kubernetes kubectl auth can-i reference](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_auth/kubectl_auth_can-i/)
