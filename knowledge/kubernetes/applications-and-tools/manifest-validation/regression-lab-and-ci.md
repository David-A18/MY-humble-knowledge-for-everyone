---
type: Tutorial
title: Kubernetes routing regression lab and CI
description: Prove why a valid Service manifest still needs an end-to-end request
  test.
tags:
- kubernetes
- manifest-validation
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: helm-chart-tests
  resource: https://helm.sh/docs/topics/chart_tests/
  title: Helm chart tests
- id: chainsaw-project
  resource: https://kyverno.github.io/chainsaw/0.2.15/reference/commands/chainsaw_test/
  title: Chainsaw project
- id: kind
  resource: https://kind.sigs.k8s.io/
  title: kind
---

# Kubernetes routing regression lab and CI

Prove why valid YAML and a healthy Deployment do not establish working Service traffic. This exercise changes one Service target port, detects the change before deployment, observes the failed request after deployment, restores service, and verifies cleanup.

## Prerequisites and boundary

Use a disposable Linux amd64 Docker environment, Python 3.10+ and Git. The supplied installer supports Linux amd64 only; Windows has executed source-only tool evidence, while the authoring host has no usable Docker/kind runtime. Do not point these mutation tests at an existing cluster.

The [version manifest](examples/lab-versions.json) pins kind 0.30.0, kubectl 1.34.1, Kubernetes 1.34.0/node digest, dyff 1.12.0, kubeconform 0.8.0, Conftest 0.71.1 and Chainsaw 0.2.15. These are a fixed teaching baseline, not a claim of latest releases. The Deployment pins NGINX 1.30.6 Alpine by registry digest.

Downloads require GitHub, Kubernetes release endpoints, a schema repository and container registries. The installer verifies stored release SHA256 values obtained from official release metadata/checksum files; it does not verify detached publisher signatures. Record Docker/Python/tool versions from your actual run.

## Install and run from the repository root

In Bash, choose a new empty tools directory and activate an isolated Python environment:

```bash
python -m venv /tmp/kb-manifest-venv
source /tmp/kb-manifest-venv/bin/activate
python -m pip install PyYAML==6.0.3
tools_dir=$(mktemp -d)
python knowledge/kubernetes/applications-and-tools/manifest-validation/examples/install-tools.py --directory "$tools_dir"
export PATH="$tools_dir:$PATH"
python knowledge/kubernetes/applications-and-tools/manifest-validation/examples/test-fixtures.py
python knowledge/kubernetes/applications-and-tools/manifest-validation/examples/validate-offline.py --report /tmp/kb-manifest-offline.json
python knowledge/kubernetes/applications-and-tools/manifest-validation/examples/validate-cluster.py --report /tmp/kb-manifest-cluster.json
```

What it does: creates a task-owned Python environment, installs checksum-pinned Linux executables into an empty directory, then runs fixture, actual source-tool and live-cluster checks. Choose a different task-owned venv path if that path already exists. The cluster runner always creates a unique kind cluster and private temporary kubeconfig; it does not reuse the current user context or mutate tracked manifests.

The fixture test checks declared labels and numeric port relationships only. `containerPort: 80` is metadata; it does not make a process listen on port 80. The actual HTTP checks provide separate behavioral evidence.

## Explain the observed layers

| Stage | Required result |
| --- | --- |
| Text/semantic diff | Git detects reordered text; dyff reports equal mappings; changed `targetPort: 81` is a semantic difference. |
| Schema and policy | Wrong routing remains schema valid and policy compliant; invalid replicas, missing custom schema and missing owner label fail their specific checks. |
| Rendering | Pinned kubectl's Kustomize renders both Deployment and Service. |
| Baseline | Deployment becomes available, EndpointSlice has one ready endpoint on port 80, and Service DNS/HTTP returns the NGINX page. |
| Prospective comparison | Baseline/reordered return 0; changed target port returns 1; a deliberately failing external diff returns an error >1. Diff leaves live port 80 unchanged. |
| Regression | Apply port 81, wait for EndpointSlice convergence, verify the Deployment and localhost HTTP remain healthy, then observe a failed Service-IP HTTP connection. |
| Drift and repair | Desired-good versus live-broken returns a difference; restore the good object, verify Service DNS/HTTP and zero diff. |
| Chainsaw | The same declarative apply/assert/request test passes with the good Service and fails at HTTP with the broken Service; both test namespaces are removed. |
| Cleanup | Lab namespace, unique kind cluster and its node containers are absent. |

The runner prints eight source-tool assertions and thirteen cluster assertions with actual versions. A failure stops acceptance; it must not be relabeled as the expected regression merely because any command returned nonzero. For example, the negative Chainsaw result must include the actual `wget` request failure, not a parsing or cluster-setup error.

## Inspect the implementation

The [cluster runner](examples/validate-cluster.py) uses explicit `--kubeconfig`/context for kubectl and a child-process-only `KUBECONFIG` for Chainsaw. Server-side apply and diff share the lab's field manager. It waits for the target-port change to reach EndpointSlices before probing, allows bounded data-plane convergence, and checks backend localhost HTTP independently.[^kind][^chainsaw-project]

The [Chainsaw test](examples/chainsaw-test.yaml) applies the two fixtures, asserts availability and executes a real HTTP request. A temporary copy substitutes only the broken Service for the negative run. No Chainsaw controller or CRD is installed; Chainsaw is the test runner. Helm's `helm.sh/hook: test` Pod/Job mechanism is an alternative for packaged charts; `helm test` succeeds only when its hook workloads succeed. This lab does not install Helm or execute chart hooks.[^helm-chart-tests]

## CI and diagnostics

The enabled [Manifest validation lab workflow](../../../../.github/workflows/manifest-validation-lab.yml) runs the same commands on Ubuntu 24.04/Python 3.13 for pull requests and `develop`/`main`. A [reference workflow copy](examples/ci-workflow.yaml) preserves the original example route; inspect the enabled workflow for authoritative behavior.

On failure, inspect the named assertion, exact tool versions and original command diagnostic. Schema-download errors are not invalid replicas. Missing images, DNS/network setup or RBAC failures are not the intended Service regression. The runner prints synthetic-cluster Pods/events on errors and attempts cluster removal in `finally`; a cleanup failure remains a failed result.

A clean diff against the deliberately broken file would only mean live state matches that broken intent. A successful port-forward selects a Pod and does not exercise the Service ClusterIP path; this suite uses in-cluster Service DNS/IP requests instead. Admission, GitOps reconciliation, Helm release upgrades, NetworkPolicy, multi-node and real application dependencies require their own tests.

## Security and cleanup

Use synthetic fixtures and a disposable Docker host. There are no cloud credentials, production contexts or application secrets in this exercise. The lab creates cluster-admin credentials for its private cluster, never prints their contents, and removes the temporary kubeconfig with its directory.

Reports contain synthetic names and versions. Remove only your own reports, empty-tool-directory installation and venv after retaining needed evidence; do not run a broad cleanup against shared directories. Successful runtime acceptance includes absence checks for namespaces, cluster inventory and labeled node containers. If the host terminates the process before `finally`, inspect the exact printed `kb-manifest-…` cluster name before manually deleting that task-owned cluster.

## Validation boundary

Sources reviewed on 2026-11-10. Python 3.13.17/PyYAML 6.0.3 on Windows executed the existing fixture test and all eight actual source-tool checks. Python/YAML parsing is checked for the cluster runner, but is not cluster execution evidence. Hosted cluster execution is pending until a specific successful workflow result is recorded here; inspect the exact revision's CI before claiming it passed.

No cloud account, shared cluster, Helm/Helm Diff release or GitOps controller was exercised. Native Windows/WSL/macOS repetition, external-diff implementations, CRD admission and independent reader sessions remain follow-ups.

- [Example files](examples/index.md)
- [Live drift contract](live-drift.md) | [Schema/policy coverage](schema-and-policy.md)
- [Back to series](index.md) | [Back to Kubernetes](../../index.md)

[^helm-chart-tests]: [Helm chart tests](https://helm.sh/docs/topics/chart_tests/).
[^chainsaw-project]: [Chainsaw 0.2.15 commands and timeouts](https://kyverno.github.io/chainsaw/0.2.15/reference/commands/chainsaw_test/).
[^kind]: [kind documentation](https://kind.sigs.k8s.io/).
