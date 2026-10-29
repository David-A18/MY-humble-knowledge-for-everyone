---
type: Troubleshooting Guide
title: Image pull failures
description: Distinguish image naming, authorization, registry connectivity, and local
  cache failures before a container starts.
tags:
- kubernetes
- troubleshooting
- images
- registry
status: draft
maturity: draft
audience: Platform engineers with basic kubectl knowledge
maintainer: unassigned
sources:
- id: images
  title: Images
  resource: https://kubernetes.io/docs/concepts/containers/images/
- id: private-images
  title: Pull an Image from a Private Registry
  resource: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
---

# Image pull failures

Use this guide for `ErrImagePull` or `ImagePullBackOff`. The runtime has not successfully obtained the requested image; application logs may not exist. Backoff delays retries but does not identify the cause.[^images]

## Read the exact registry error

```bash
kubectl describe pod <pod> -n <namespace>
kubectl get pod <pod> -n <namespace> -o jsonpath='{.spec.nodeName}{"\n"}{.spec.containers[*].image}{"\n"}{.spec.initContainers[*].image}{"\n"}{.spec.imagePullSecrets}{"\n"}'
```

What it does: reads the failing image, assigned node, pull events, and credential references, including init-container images. Check the waiting state for the specific container. Expect a concrete error such as unauthorized, manifest unknown, timeout, certificate failure, rate limit, or no compatible platform.

| Error / observation | Check before changing anything |
| --- | --- |
| Image/tag/digest not found | Exact registry, repository, spelling, published tag, and digest. |
| Unauthorized / denied | Registry permission and credential source used by that node/runtime. |
| `FailedToRetrieveImagePullSecret` | Referenced Secret name and namespace. |
| Timeout / name-resolution failure | Node-to-registry DNS, routing, proxy, firewall, and registry health. A laptop pull does not prove node connectivity. |
| Certificate validation failure | Registry chain and approved runtime trust configuration; do not disable TLS verification globally. |
| No matching platform | Whether the image index includes the node's OS/architecture. |
| Local image works on one node only | Per-node cache and pull policy; use the [kind guide](kind.md) for local clusters. |

## Inspect credential wiring without dumping credentials

```bash
kubectl get serviceaccount <service-account> -n <namespace> -o jsonpath='{.imagePullSecrets}{"\n"}'
kubectl get secret <pull-secret> -n <namespace> -o jsonpath='{.type}{"\n"}'
```

What it does: checks the ServiceAccount's pull-secret references and the Secret type, without printing `.dockerconfigjson`. Image-pull Secrets must be in the Pod's namespace. Inspect the existing Pod's references too; changing a ServiceAccount does not rewrite an already-created Pod.[^private-images]

The application's AWS workload identity and the identity that pulls its image are different paths. Do not add broad application IAM permissions to fix a node/runtime registry error. Managed-node credential providers or serverless execution roles may supply registry credentials instead of an `imagePullSecret`; identify your environment's mechanism.

## Recover and verify

Correct the image reference or credential source through the owning configuration. Prefer a reviewed immutable digest when reproducibility matters. Store registry credentials using your established secret-management process; never commit them or paste token-bearing commands into a shared terminal log.

After correction, wait for a retry or a reviewed workload rollout. Expect the container to transition to running and then Ready; `ImagePullBackOff` disappearing does not prove application health. `IfNotPresent` with a mutable tag can leave nodes running cached content, and `Never` fails without a local image.[^images] Confirm the actual `imageID` when investigating inconsistent versions. Remove temporary credential objects only if created for a disposable test and no longer referenced.

## Evidence and scope

Source review: 2026-10-29. Commands are adaptable diagnostic examples; replace angle-bracket placeholders before running. No live cluster walkthrough was executed for this revision. Record client/server and controller versions during reproduction. Keep diagnostic logs private and redact credentials, customer data, and internal addresses before sharing.

## Related routes

- [Secret-management patterns](../applications-and-tools/platform-tooling/secret-management.md).
- [CrashLoopBackOff](crashloopbackoff.md) — continue if the image starts but exits.
- [Back to troubleshooting](index.md)
- [Back to Kubernetes](../index.md)

[^images]: [Images](https://kubernetes.io/docs/concepts/containers/images/)
[^private-images]: [Pull an Image from a Private Registry](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)
