---
type: Tutorial
title: Istio mTLS and JWT security lab
description: Reproduce workload authorization, mandatory JWTs, and plaintext rejection
  on a disposable cluster.
tags:
- kubernetes
- istio
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: istio-install
  resource: https://istio.io/latest/docs/setup/install/istioctl/
  title: Istio install
- id: supported-releases
  resource: https://istio.io/latest/docs/releases/supported-releases/
  title: Supported releases
- id: jwt-authentication-task
  resource: https://istio.io/latest/docs/tasks/security/authentication/authn-policy/
  title: JWT authentication task
---

# Istio mTLS and JWT security lab

## Purpose

Reproduce workload authorization, mandatory JWTs, and plaintext rejection on a disposable cluster.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Prerequisites

Use Bash, a disposable kind cluster, and `istioctl` **1.31.0** with its matching control plane. Confirm the release's Kubernetes support matrix before choosing your kind node image. Python **3.13** plus `cryptography==46.0.3` generates a disposable signing key in memory. No private key is written or committed. This is a sidecar lab, not an ambient installation.[^istio-install][^supported-releases][^jwt-authentication-task]

Run from this series directory. Download and verify tools using their official release instructions rather than piping unreviewed installer scripts into a shell.

> [!WARNING]
> Installation modifies cluster-wide components and APIs. Confirm the current context is the disposable lab cluster before proceeding.

## Install and enroll

```bash
istioctl install --set profile=demo -y
kubectl create namespace istio-lab
kubectl label namespace istio-lab istio-injection=enabled
kubectl apply -n istio-lab -f examples/workloads.yaml
kubectl wait pod -n istio-lab --all --for=condition=Ready --timeout=180s
python -m venv /tmp/istio-jwt-env
/tmp/istio-jwt-env/bin/python -m pip install cryptography==46.0.3
/tmp/istio-jwt-env/bin/python examples/jwt-lab.py /tmp/istio-jwt-lab
kubectl apply -f /tmp/istio-jwt-lab/policies.json
```

What it does: installs a disposable mesh, injects proxies, generates a one-hour synthetic JWT/public JWKS, and applies STRICT mTLS plus combined workload/JWT authorization. Generated output is outside Git. On Windows use the virtual environment's `Scripts/python.exe` and a local temporary directory.

## Verify the access matrix

```bash
TOKEN=$(cat /tmp/istio-jwt-lab/token.txt)
kubectl exec -n istio-lab allowed -c client -- curl -sS -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" http://web
kubectl exec -n istio-lab denied -c client -- curl -sS -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" http://web
kubectl exec -n istio-lab allowed -c client -- curl -sS -o /dev/null -w '%{http_code}\n' http://web
kubectl exec -n istio-lab allowed -c client -- curl -sS -o /dev/null -w '%{http_code}\n' -H 'Authorization: Bearer invalid' http://web
```

What it does: sends identical requests with distinct identities or credentials. Expect respectively **200, 403, 403, 401** once proxy configuration has converged. Valid JWT alone does not authorize the `denied` service account. Do not enable shell tracing or print bearer tokens.

## Test non-mesh plaintext

```bash
kubectl create namespace plaintext-lab
kubectl run plain -n plaintext-lab --image=curlimages/curl:8.12.1 --restart=Never --command -- curl --fail --connect-timeout 5 --max-time 10 http://web.istio-lab.svc.cluster.local
kubectl logs -n plaintext-lab plain --pod-running-timeout=60s
```

What it does: attempts a connection without a mesh proxy. Expect a transport failure/nonzero termination rather than application HTTP 200 under STRICT policy. Wait for Pod termination and inspect its exit code before recording the result.

## Debug and clean up

Use `istioctl analyze`, inspect server proxy logs and synchronized policy, and confirm every injected Pod has the proxy container. A stale token can cause 401; regenerate the lab output and reapply its matching public key.

> [!WARNING]
> These commands delete lab workloads. Verify context first. Delete only `istio-lab` and `plaintext-lab`; uninstall Istio or delete the kind cluster only if you created that entire installation for this lab.

```bash
kubectl delete namespace istio-lab plaintext-lab
```

What it does: removes the lab's namespaced policies and workloads. Delete generated token files from the temporary directory when finished.

## Related links

- [Istio install](https://istio.io/latest/docs/setup/install/istioctl/)
- [Supported releases](https://istio.io/latest/docs/releases/supported-releases/)
- [JWT authentication task](https://istio.io/latest/docs/tasks/security/authentication/authn-policy/)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^istio-install]: [Istio install](https://istio.io/latest/docs/setup/install/istioctl/).
[^supported-releases]: [Supported releases](https://istio.io/latest/docs/releases/supported-releases/).
[^jwt-authentication-task]: [JWT authentication task](https://istio.io/latest/docs/tasks/security/authentication/authn-policy/).
