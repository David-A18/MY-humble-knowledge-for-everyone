---
type: How-to Guide
title: Prepare the local learning environment
description: Choose the Git, Kubernetes, or Terraform stage and check shell, runtime,
  target isolation, versions, and cleanup before starting.
tags:
- learning
- local-development
- beginner
status: draft
maturity: draft
audience: Beginning platform engineer
maintainer: unassigned
sources:
- id: kind-start
  title: kind quick start
  resource: https://kind.sigs.k8s.io/docs/user/quick-start/
- id: kind-known
  title: kind host/runtime issues
  resource: https://kind.sigs.k8s.io/docs/user/known-issues/
- id: kubeconfig
  title: Kubernetes kubeconfig contexts
  resource: https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/
- id: git-config
  title: git config
  resource: https://git-scm.com/docs/git-config
---

# Prepare the local learning environment

Use this preflight before [Start here](../start-here.md) or the [local deployment exercise](local-deployment-learning-path.md). The stages have different prerequisites; a missing container runtime need not block Git or Terraform practice.

## Choose the stage you can run

| Stage | Tools needed | Completion evidence |
| --- | --- | --- |
| Git recovery | Git and Python for the optional checker | Unstaging preserves an edit; restoring recovers the tracked file; HEAD stays unchanged. |
| Kubernetes | Bash, a working Linux-container Docker runtime, kind, compatible kubectl, registry access | Ready Pods/endpoints, HTTP, diagnosed bad-image rollout, recovery, and deleted task resources. |
| Terraform | Terraform 1.4+; Python for the optional checker | One local state object, reviewed update, expected output, and empty managed state after destroy. |

Manual tutorial commands use Bash on Linux/macOS or a configured WSL2 Linux environment. Native PowerShell users can run the Python Git and Terraform checkers; those were exercised on Windows. This revision's Kubernetes automation runs in Linux CI. A successful hosted run does not prove Docker Desktop, WSL integration, or rootless operation on your own host.[^kind-known]

## Check installed clients and the runtime separately

```bash
git --version
python --version
docker version
docker info
kind version
kubectl version --client
terraform version
```

What it does: records the tools needed for your selected stage. Skip tools for stages you are not running. A Docker client version without a reachable server is insufficient; do not proceed to cluster creation until the Linux-container runtime works under your normal account. `kubectl --client` needs no cluster.

Use official installation instructions and organization-approved setup. For kind, check architecture, Docker/WSL/rootless prerequisites, available CPU/RAM/disk, VPN/subnet interactions, and registry reachability.[^kind-start][^kind-known] The old guide's approximate resource recommendation was not a verified minimum for every host; allow enough capacity for the control plane, two ready Pods, and one surge Pod.

## Keep a reproducible teaching baseline

The [version contract](../kubernetes/examples/local-deployment-learning-path/lab-versions.json) fixes kind v0.30.0, kubectl v1.34.1 and a digest-pinned Kubernetes v1.34.0 node image. This is a repeatable historical teaching baseline, not a recommendation to deploy an old Kubernetes patch in production. Choose upgrades deliberately and rerun the walkthrough. The workload image is pinned in [deployment.yaml](../kubernetes/examples/local-deployment-learning-path/deployment.yaml).

The [CI workflow](../../.github/workflows/local-learning-journey.yml) validates kind/kubectl downloads against published HTTPS checksums and records the runner's Docker/Kubernetes versions. It does not verify detached signatures or establish that the host's entire supply chain is trusted.

## Confirm targets before mutation

Read the dedicated cluster name and scratch-directory instructions before running any `apply`, `patch`, `undo`, or deletion. The Kubernetes tutorial uses a separate kubeconfig and an explicit context; a changed global current-context cannot redirect its commands.[^kubeconfig] Stop if its fixed manual cluster name already exists. The automated runner chooses a new name and refuses reuse.

Use unique task-owned directories for Git/Terraform. Run `git rev-parse --show-toplevel` in an existing repository when unsure where you are; the tutorial's `git init` belongs only in its new scratch copy. Configure commit identity locally there if needed, rather than changing global identity just to make the exercise pass.[^git-config]

## Common stops and recovery routes

| Stop | Next action |
| --- | --- |
| Command not found or denied execution | Fix the approved installation/permission path; a source review cannot substitute for running the client. |
| Docker server unavailable | Repair the selected runtime/WSL integration before kind creation. |
| Existing `kb-local` cluster | Inspect its owner/data and choose another owned exercise; do not delete it blindly. |
| Image pull fails during healthy deployment | Check the actual registry/network error before the deliberate bad-image test. |
| Git asks for author identity/signing | Use local teaching-repository configuration; keep real signing policy in your normal repositories. |
| Port 8080 occupied | Choose an unused localhost port and use the same port in the HTTP check. |
| Terraform wants a cloud provider/backend | Stop: the beginner fixture uses only built-in `terraform_data` and local state. |

Continue with [kind diagnostics](../kubernetes/troubleshooting/kind.md), [image-pull diagnosis](../kubernetes/troubleshooting/image-pull-failures.md), or [Terraform diagnosis](../terraform/troubleshooting/failures-and-unexpected-plans.md) as applicable. Preserve the exact failure and versions; do not label a timeout or infrastructure error as the tutorial's expected application failure.

## Evidence and handoff

Sources reviewed on 2026-11-10. Git 2.55.0.windows.2 and Terraform 1.17.1 local runners were executed during authoring. Kubernetes execution belongs to the exact revision's hosted workflow record; this Windows host has no Docker/kind runtime and its installed kubectl is denied execution. Independent beginner testing and platform-specific setup remain open.

[Back to Start here](../start-here.md) | [Back to cross-topic guides](index.md)

[^kind-start]: [kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/).
[^kind-known]: [kind host/runtime issues](https://kind.sigs.k8s.io/docs/user/known-issues/).
[^kubeconfig]: [Kubernetes kubeconfig contexts](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/).
[^git-config]: [git config](https://git-scm.com/docs/git-config).
