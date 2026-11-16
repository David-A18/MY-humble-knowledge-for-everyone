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
- id: peer-authentication
  resource: https://istio.io/latest/docs/reference/config/security/peer_authentication/
  title: Istio PeerAuthentication
- id: authorization-policy
  resource: https://istio.io/latest/docs/reference/config/security/authorization-policy/
  title: Istio AuthorizationPolicy
---

# Istio mTLS and JWT security lab

Use a disposable sidecar mesh to see which layer rejects a request. The lab keeps the web server and URL constant while changing the client service account, the HTTP credential and the transport policy.

## Prerequisites

Use Linux amd64 with Docker, Python 3.13 and Bash. The version file pins Istio 1.32.0, kind 0.30.0, kubectl 1.34.1 and a Kubernetes 1.34.0 node image by digest. Istio's support matrix lists Kubernetes 1.34 for Istio 1.32. Check compatibility before substituting versions. [^supported-releases]

The runner installs the minimal sidecar control plane into a new cluster. It uses a separate kubeconfig and verifies enrollment of both mesh clients and the server. A third client runs in a namespace with injection disabled. [^istio-install]

## Run the lab

From the repository root, use an isolated Python environment and run the following in Bash.

```bash
python -m pip install cryptography==46.0.3
tools_dir=$(mktemp -d)
python knowledge/kubernetes/applications-and-tools/manifest-validation/examples/install-tools.py \
  --directory "$tools_dir" \
  --versions knowledge/kubernetes/applications-and-tools/istio/examples/lab-versions.json
export PATH="$tools_dir:$PATH"
python knowledge/kubernetes/applications-and-tools/istio/examples/validate-mesh.py
```

What it does: installs the checksum-pinned executables, creates a uniquely named cluster and runs the staged request checks. The two fixture images use digests. The JWT generator uses a fresh RSA key in memory and embeds its public JWKS in the policies. The runner passes the synthetic bearer token through stdin and retains only outcomes and version data in its report. The temporary directory holds the private kubeconfig, generated policies and short-lived token for the duration of the run.

## Read the access matrix

| Phase | Client and credential | Expected observation |
| --- | --- | --- |
| Baseline | Allowed, denied and plaintext clients with no JWT | Each returns HTTP 200 before the policies apply. |
| STRICT peer authentication | Allowed mesh client with no JWT | HTTP 200 over mesh mTLS. |
| STRICT peer authentication | Uninjected client against the same Service | Connection rejected before an HTTP response. |
| Add request authentication | Allowed client with valid JWT, missing JWT, then malformed JWT | HTTP 200, 200, then 401. |
| Add authorization | Allowed client with a valid JWT | HTTP 200. |
| Add authorization | Denied client with the same valid JWT | HTTP 403. |
| Add authorization | Allowed client without a JWT | HTTP 403. |
| Add authorization | Allowed client with a malformed JWT | HTTP 401. |

PeerAuthentication STRICT requires a mesh peer on the tested inbound path. Keep a working mesh request in this phase so an outage cannot satisfy the negative case. The same plaintext client first reaches the Service and then receives a transport failure with HTTP code 000. A generic timeout or an API error fails the transport assertion. [^peer-authentication]

RequestAuthentication validates a presented token and permits a request without one to continue to authorization. The ALLOW rule selects the server and requires both the mTLS principal of the allowed service account and a verified request principal. The same token sent by the other service account therefore receives 403. [^jwt-authentication-task][^authorization-policy]

## Diagnose and clean up

Start with the phase that failed. If the baseline fails, inspect readiness, sidecar injection and Service DNS. If a result changes after a policy is applied, inspect the destination proxy's configuration sync, the policy selector and the target namespace. For a JWT 401, check the issuer, audience, expiration and JWKS. For a 403 with a valid token, compare the peer and request principals with the same authorization rule. Keep bearer tokens out of shell traces, proxy diagnostics and retained reports.

The runner deletes both lab namespaces and verifies their absence. It attempts cluster deletion in its cleanup block and checks the kind inventory and Docker containers for the task cluster. If the process is terminated before cleanup runs, verify the printed cluster name and remove only that cluster.

## Validation

Reviewed the install, release-support and policy references on 2026-11-16. The GitHub Actions workflow runs the same request checks with pinned tools on Ubuntu 24.04. The access matrix above lists expected results until a successful run is recorded. Ambient policy placement and production rollout are covered separately.

- [Examples and version pins](examples/index.md)
- [Istio security lab workflow](../../../../.github/workflows/istio-security-lab.yml)
- [Troubleshooting and rollout](troubleshooting-and-rollout.md)
- [Back to Istio](index.md) | [Back to Kubernetes](../../index.md)

[^istio-install]: [Istio install with istioctl](https://istio.io/latest/docs/setup/install/istioctl/).
[^supported-releases]: [Istio supported releases](https://istio.io/latest/docs/releases/supported-releases/).
[^jwt-authentication-task]: [Istio authentication policy examples](https://istio.io/latest/docs/tasks/security/authentication/authn-policy/).
[^peer-authentication]: [Istio PeerAuthentication](https://istio.io/latest/docs/reference/config/security/peer_authentication/).
[^authorization-policy]: [Istio AuthorizationPolicy](https://istio.io/latest/docs/reference/config/security/authorization-policy/).
