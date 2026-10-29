---
type: Tutorial
title: Local kro application-composition lab
description: Create and operate a WebApp API that composes a Deployment and Service.
tags:
- kubernetes
- kro
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: pinned-kro-installation-instructions
  resource: https://kro.run/docs/getting-started/Installation/
  title: Pinned kro installation instructions
- id: kro-v0-9-4-examples
  resource: https://github.com/kro-run/kro/tree/v0.9.4/examples
  title: kro v0.9.4 examples
---

# Local kro application-composition lab

## Purpose

Create and operate a WebApp API that composes a Deployment and Service.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Prerequisites

Use a disposable kind cluster, kubectl, Helm 3, and kro **0.9.4**. The application image is pinned in the supplied [fixtures](examples/index.md). The release API is still `v1alpha1`; test compatibility before upgrades. Run from this series directory.[^pinned-kro-installation-instructions][^kro-v0-9-4-examples]

> [!WARNING]
> Installation modifies cluster-wide components and APIs. Confirm the current context is the disposable lab cluster before proceeding.

## Install and define the API

```bash
helm install kro oci://registry.k8s.io/kro/charts/kro --namespace kro-system --create-namespace --version 0.9.4
kubectl apply -f examples/webapp-rgd.yaml
kubectl get resourcegraphdefinition webapp
kubectl api-resources | grep -i webapp
```

What it does: installs a pinned controller and requests a generated API. Inspect definition conditions and wait for `webapps.kro.run` discovery before applying instances.

```bash
kubectl create namespace kro-lab
kubectl apply -n kro-lab -f examples/webapp.yaml
kubectl rollout status deployment/demo -n kro-lab --timeout=120s
kubectl get webapp,deploy,service -n kro-lab
kubectl port-forward -n kro-lab service/demo 8080:80
```

What it does: creates one higher-level instance and waits for its generated workload. In a second terminal, `curl --fail http://localhost:8080` should return the nginx page. Port forwarding stays in the foreground; stop it before cleanup.

## Observe reconciliation

Change `spec.replicas` in `webapp.yaml` to 2 and reapply. Verify the generated Deployment converges to two replicas. Change the image to a deliberately invalid tag and inspect instance, Deployment, and Pod conditions; restore the pinned image and verify recovery.

Do not manually maintain a second desired copy of the generated Deployment through GitOps. GitOps should own the WebApp instance while kro owns its children.

## Cleanup

> [!WARNING]
> Deleting an instance removes its managed workload resources according to controller lifecycle behavior. Use only the disposable namespace.

```bash
kubectl delete -n kro-lab -f examples/webapp.yaml
kubectl get deployment,service -n kro-lab
kubectl delete namespace kro-lab
```

What it does: tests deletion through the parent API before removing the namespace. Remove the RGD/controller only after all dependent lab instances are gone and only if the installation is dedicated to this lab.

## Related links

- [Pinned kro installation instructions](https://kro.run/docs/getting-started/Installation/)
- [kro v0.9.4 examples](https://github.com/kro-run/kro/tree/v0.9.4/examples)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^pinned-kro-installation-instructions]: [Pinned kro installation instructions](https://kro.run/docs/getting-started/Installation/).
[^kro-v0-9-4-examples]: [kro v0.9.4 examples](https://github.com/kro-run/kro/tree/v0.9.4/examples).
