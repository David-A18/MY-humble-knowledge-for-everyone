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
  resource: https://github.com/kyverno/chainsaw
  title: Chainsaw project
- id: kind
  resource: https://kind.sigs.k8s.io/
  title: kind
---

# Kubernetes routing regression lab and CI

## Purpose

Prove why a valid Service manifest still needs an end-to-end request test.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Prerequisites and files

Use a disposable kind cluster, Bash, kubectl, and the [example files](examples/index.md). The application listens on port 80. `service-broken.json` intentionally targets port 81. Runtime execution was not possible on the authoring host.[^helm-chart-tests][^chainsaw-project][^kind]

## Establish working behavior

```bash
kubectl create namespace manifest-lab
kubectl apply -n manifest-lab -f examples/app.yaml
kubectl apply -n manifest-lab -f examples/service.json
kubectl rollout status deployment/web -n manifest-lab --timeout=120s
kubectl run probe -n manifest-lab --image=curlimages/curl:8.12.1 --restart=Never --command -- curl --fail --connect-timeout 5 --max-time 10 http://web
kubectl wait pod/probe -n manifest-lab --for=jsonpath='{.status.phase}'=Succeeded --timeout=60s
kubectl delete pod probe -n manifest-lab
```

What it does: deploys a web server and checks an actual Service request. Expect a completed probe. Checking only Deployment availability would not cover Service routing.

## Introduce and detect the regression

```bash
kubectl apply -n manifest-lab -f examples/service-broken.json
kubectl run probe-bad -n manifest-lab --image=curlimages/curl:8.12.1 --restart=Never --command -- curl --fail --connect-timeout 5 --max-time 10 http://web
kubectl logs -n manifest-lab probe-bad --pod-running-timeout=60s
kubectl get pod probe-bad -n manifest-lab -o jsonpath='{.status.containerStatuses[0].state.terminated.exitCode}{"\n"}'
```

What it does: changes a schema-valid target port and exposes the failed connection. Wait for termination before asserting a nonzero exit code. Restore `service.json` and repeat the successful probe before cleanup.

## CI sequence

A [GitHub Actions example](examples/ci-workflow.yaml) runs the offline contract and positive/negative HTTP tests on disposable kind infrastructure. It is a reviewable example and was not executed on hosted CI during authoring.

Render all environments; run schema/policy checks; compare rendered artifacts; apply to a disposable cluster; wait for readiness; execute behavioral tests; collect redacted events/logs; always clean up. The supplied [offline test](examples/test-fixtures.py) catches fixture routing and label errors without a cluster; it does not replace the request test.

For Helm, package a test Pod using `helm.sh/hook: test` and run `helm test` after rollout. For declarative multi-step integration tests, Chainsaw **0.2.15** can apply fixtures, assert resource conditions, execute commands, and clean up. Keep namespaces isolated and assert both desired state and a real request. Review the supplied [Chainsaw example](examples/chainsaw-test.yaml).

> [!WARNING]
> Cleanup deletes all lab resources: verify context and delete only `manifest-lab`. Retain shared controllers and CRDs.

## Related links

- [Helm chart tests](https://helm.sh/docs/topics/chart_tests/)
- [Chainsaw project](https://github.com/kyverno/chainsaw)
- [kind](https://kind.sigs.k8s.io/)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^helm-chart-tests]: [Helm chart tests](https://helm.sh/docs/topics/chart_tests/).
[^chainsaw-project]: [Chainsaw project](https://github.com/kyverno/chainsaw).
[^kind]: [kind](https://kind.sigs.k8s.io/).
