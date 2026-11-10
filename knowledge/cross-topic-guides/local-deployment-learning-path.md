---
type: Tutorial
title: Local deployment learning path
description: 'Complete a local Kubernetes exercise without an AWS account: deploy
  a pinned web workload, diagnose an image-pull failure, recover, and verify cleanup.'
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
- id: kind-release
  title: kind v0.30.0 release and node-image digests
  resource: https://github.com/kubernetes-sigs/kind/releases/tag/v0.30.0
- id: deployment
  title: Kubernetes Deployments
  resource: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- id: service
  title: Kubernetes Services
  resource: https://kubernetes.io/docs/concepts/services-networking/service/
- id: port-forward
  title: kubectl port-forward
  resource: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_port-forward/
- id: git-restore
  title: git restore
  resource: https://git-scm.com/docs/git-restore
- id: nginx-release
  title: nginx stable release changes
  resource: https://nginx.org/en/CHANGES-1.30
---

# Local deployment learning path

## Goal

Create a disposable kind cluster, deploy a two-replica web application, observe its Service, break a rollout with an invalid image tag, diagnose it, recover, practice Git restore, and clean up. Begin with [environment preflight](local-learning-preflight.md).

## Local Kubernetes without an AWS account

This local Kubernetes route needs a working Linux-container Docker runtime, kind, kubectl, Git, Python, and public image-registry access. It creates no AWS resource and needs no AWS credentials. Manual commands below use Bash; use [Start here](../start-here.md) to choose the Git/Kubernetes/Terraform stage you can run.

The [version contract](../kubernetes/examples/local-deployment-learning-path/lab-versions.json) pins kind v0.30.0, kubectl v1.34.1, and the release's Kubernetes v1.34.0 node digest.[^kind-release] The NGINX fixture uses a digest-pinned 1.30.6 Alpine image selected after reviewing the stable release notes.[^nginx-release] These are teaching inputs, not production readiness or a rolling latest-version promise.

## What you will create

| File | Purpose |
| --- | --- |
| [namespace.yaml](../kubernetes/examples/local-deployment-learning-path/namespace.yaml) | Task resource scope `kb-learning`. |
| [deployment.yaml](../kubernetes/examples/local-deployment-learning-path/deployment.yaml) | Two Pods with readiness probes and explicit rollout headroom. |
| [service.yaml](../kubernetes/examples/local-deployment-learning-path/service.yaml) | ClusterIP Service selecting ready web Pods. |
| [failing-image-patch.yaml](../kubernetes/examples/local-deployment-learning-path/failing-image-patch.yaml) | Strategic merge patch for an existing Deployment; not a standalone resource. |

## Concepts before commands

A Deployment maintains Pods through ReplicaSets. Labels connect the Service selector to Pods; readiness determines which normal endpoints can receive traffic. Namespace scope helps organize the exercise, but is not a security-isolation guarantee. Reconciliation keeps retrying desired state; an invalid image can remain desired even while older Pods are healthy.[^deployment][^service]

## Copy the exercise files

Run from the repository root, in a new Bash terminal:

```bash
EXERCISE_DIR=$(mktemp -d "${TMPDIR:-/tmp}/kb-local-path.XXXXXX")
cp knowledge/kubernetes/examples/local-deployment-learning-path/*.yaml "$EXERCISE_DIR/"
cp knowledge/kubernetes/examples/local-deployment-learning-path/lab-versions.json "$EXERCISE_DIR/"
cp knowledge/kubernetes/examples/local-deployment-learning-path/.gitignore "$EXERCISE_DIR/"
cd "$EXERCISE_DIR"
git init -b learning
git config user.name "Local learning fixture"
git config user.email "learner@example.invalid"
git add .
git -c commit.gpgsign=false commit -m "add local deployment exercise"
```

What it does: copies only exercise inputs into a unique scratch repository. The local identity is a synthetic teaching label and affects only this scratch copy; use your own approved local identity if appropriate. The commit command disables signing only for that disposable teaching commit. The separate kubeconfig created next is ignored by this copy's `.gitignore`.

## Protect your normal Kubernetes context

Before applying resources, this local Kubernetes tutorial creates a separate kubeconfig and passes an explicit `--context kind-kb-local` on every command. Your normal current context cannot redirect those commands to another cluster. The kubeconfig contains access material for the disposable cluster and stays ignored in the scratch repository. Keep the terminal in the exercise directory so the relative `kubeconfig` path resolves to that owned file.

## Prepare a local cluster

Check `kind get clusters` first. Stop if `kb-local` already exists; do not reuse or delete another exercise's cluster. The private kubeconfig keeps this path independent of your normal selected cluster.[^kind-start]

```bash
NODE_IMAGE=$(python -c 'import json; print(json.load(open("lab-versions.json"))["node_image"])')
kind create cluster --name kb-local --image "$NODE_IMAGE" --kubeconfig "$EXERCISE_DIR/kubeconfig" --wait 120s
kubectl --kubeconfig kubeconfig --context kind-kb-local cluster-info
kubectl --kubeconfig kubeconfig --context kind-kb-local wait --for=condition=Ready node --all --timeout=120s
```

What it does: creates the pinned local node and confirms API connectivity/readiness. Keep this terminal in the scratch directory for every following command. All Kubernetes mutations specify the kubeconfig and context; do not drop those flags when copying a command.

## Deploy the app

```bash
kubectl --kubeconfig kubeconfig --context kind-kb-local apply -f namespace.yaml
kubectl --kubeconfig kubeconfig --context kind-kb-local apply -f deployment.yaml
kubectl --kubeconfig kubeconfig --context kind-kb-local apply -f service.yaml
kubectl --kubeconfig kubeconfig --context kind-kb-local rollout status deployment/kb-web -n kb-learning --timeout=180s
kubectl --kubeconfig kubeconfig --context kind-kb-local get pods -n kb-learning --show-labels
kubectl --kubeconfig kubeconfig --context kind-kb-local get endpointslices -n kb-learning -l kubernetes.io/service-name=kb-web
```

What it does: creates the healthy baseline and inspects ready Pods/Service endpoints. Expect two Ready Pods with `app.kubernetes.io/name=kb-web`, and two ready Pod addresses in EndpointSlices. Do not apply the entire directory: the failing-image file is a patch reserved for a later step.

## Inspect the running app

```bash
kubectl --kubeconfig kubeconfig --context kind-kb-local exec -n kb-learning deployment/kb-web -- wget -q -O - http://kb-web.kb-learning.svc.cluster.local/
kubectl --kubeconfig kubeconfig --context kind-kb-local port-forward service/kb-web 8080:80 -n kb-learning --address=127.0.0.1
```

What it does: first requests the Service through cluster DNS/ClusterIP from an application container; expect the NGINX welcome page. Then starts a localhost port-forward. In a second terminal run `curl --fail http://127.0.0.1:8080/`, and stop forwarding with Ctrl+C before continuing.

A Service port-forward selects a Pod and forwards to it.[^port-forward] Its successful response does not prove the ClusterIP routing or DNS path; that is why the in-cluster HTTP check is separate. Neither single request proves even load distribution or every backend's behavior.

## Break the workload on purpose

```bash
kubectl --kubeconfig kubeconfig --context kind-kb-local patch deployment kb-web -n kb-learning --type=strategic --patch-file failing-image-patch.yaml
kubectl --kubeconfig kubeconfig --context kind-kb-local rollout status deployment/kb-web -n kb-learning --timeout=60s
```

What it does: changes the existing Pod template to an invalid NGINX tag. Expect a nonzero rollout status once it times out; continue to diagnosis after recording that expected failure. A timeout alone is insufficient evidence: inspect the actual image-not-found error next.

## Diagnose the failure

```bash
kubectl --kubeconfig kubeconfig --context kind-kb-local get pods -n kb-learning -o wide
kubectl --kubeconfig kubeconfig --context kind-kb-local describe deployment kb-web -n kb-learning
kubectl --kubeconfig kubeconfig --context kind-kb-local get events -n kb-learning --sort-by=.lastTimestamp
kubectl --kubeconfig kubeconfig --context kind-kb-local describe pod -n kb-learning -l app.kubernetes.io/name=kb-web
```

What it does: locates `ErrImagePull`/`ImagePullBackOff` and the registry's not-found message for the deliberate tag. A DNS failure, authentication error, or rate limit is a different failure. The explicit `maxUnavailable: 0` and `maxSurge: 1` preserve the two healthy baseline Pods while a new Pod fails, provided the baseline remains healthy and the cluster has surge capacity.[^deployment] Re-run the in-cluster HTTP request to verify old Pods still serve.

Record the command, actual waiting reason/message, rollout exit status, HTTP result, and intended recovery. For unrelated failures follow [image-pull diagnosis](../kubernetes/troubleshooting/image-pull-failures.md) or [kind diagnostics](../kubernetes/troubleshooting/kind.md).

## Recover

```bash
kubectl --kubeconfig kubeconfig --context kind-kb-local rollout undo deployment/kb-web -n kb-learning
kubectl --kubeconfig kubeconfig --context kind-kb-local rollout status deployment/kb-web -n kb-learning --timeout=120s
kubectl --kubeconfig kubeconfig --context kind-kb-local get deployment kb-web -n kb-learning -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
kubectl --kubeconfig kubeconfig --context kind-kb-local exec -n kb-learning deployment/kb-web -- wget -q -O - http://kb-web.kb-learning.svc.cluster.local/
```

What it does: restores the previous Pod template, waits for the rollout, checks the pinned image, and requests HTTP again. `rollout undo` changes live Deployment state; it does not rewrite a Git file. This exercise has no GitOps controller to overwrite that manual recovery.

## Practice Git recovery

Edit the scratch `deployment.yaml` image value, then inspect and stage only that file:

```bash
git diff -- deployment.yaml
git add deployment.yaml
git diff --staged -- deployment.yaml
git restore --staged deployment.yaml
git diff -- deployment.yaml
git restore deployment.yaml
git status --short
```

What it does: unstages the edited file while retaining its contents, then deliberately discards that scratch edit and restores the tracked baseline.[^git-restore] After the first restore the unstaged diff should remain; after the second it should be empty. This changes the scratch file, not the live cluster. Do not practice discarding valuable edits in your normal checkout.

Restoring `deployment.yaml` does not roll back the live Kubernetes Deployment or change Terraform state. The following Terraform exercise tracks its own local `terraform_data` object and does not manage this cluster. Use the Kubernetes recovery step for a live Pod-template rollback, and keep each tool's source/state boundary explicit.

## Clean up

Confirm this is still the task-owned `kind-kb-local` context and `kb-learning` namespace. The deletion removes every resource in that namespace.

```bash
kubectl --kubeconfig kubeconfig --context kind-kb-local delete namespace kb-learning --wait=true --timeout=120s
kubectl --kubeconfig kubeconfig --context kind-kb-local get namespace kb-learning --ignore-not-found -o name
kind delete cluster --name kb-local --kubeconfig "$EXERCISE_DIR/kubeconfig"
kind get clusters
```

What it does: waits for namespace deletion, confirms no namespace result, then deletes the owned cluster and checks its name is absent. Do not count a connection error as successful deletion. The scratch repository/kubeconfig can be removed later after retaining exercise evidence; verify its actual path before any recursive cleanup.

## Understanding checks

- Which selector joins the Service to ready Pods, and what did EndpointSlices show?
- Why did a port-forward response not prove cluster DNS or load balancing?
- Which message distinguished the invalid tag from a network outage?
- Why did older Pods continue serving, and which rollout setting requires extra capacity?
- Which changes belong to live Kubernetes state, the Git index, the working tree, and Terraform state?
- Which checks establish namespace and cluster deletion?

## Validation evidence and next step

Official sources and fixture digests reviewed on 2026-11-10. An older revision recorded a rootless local run with Docker 29.8.0; that historical record is not a fresh execution of these revised inputs. The [automated runner](../kubernetes/examples/local-deployment-learning-path/validate-lab.py) and [CI workflow](../../.github/workflows/local-learning-journey.yml) check actual deployment, Service HTTP, port-forward, image-not-found failure, rollback and cleanup for each tested revision. Inspect its exact commit's result before treating those checks as executed. The authoring Windows host could not run Kubernetes.

Execution recorded on 2026-11-10: [the successful run for content revision c7d9d02](https://github.com/David-A18/MY-humble-knowledge-for-everyone/actions/runs/42794513544) used Linux amd64, Docker 29.4.2, kind v0.30.0, kubectl v1.34.1 and Kubernetes v1.34.0. All six runtime assertions passed, including both HTTP paths, the intended failure with old Pods serving, restored image/endpoints/HTTP, namespace deletion, and removal of the kind cluster/node containers. The runner used the pinned node and NGINX digests shown in the inputs. This is hosted execution evidence, not independent beginner or rootless/desktop validation.

Continue with the [Terraform local state lifecycle](../terraform/examples/local-state-lifecycle/local-state-lifecycle.md). Independent beginner testing, native Windows/WSL/rootless repetition, cloud load balancers, IAM and persistent storage remain outside this walkthrough's current evidence.

## Related links

- [Start here](../start-here.md)
- [Kubernetes fundamentals](../kubernetes/fundamentals/index.md)
- [Git undo and recovery](../git/troubleshooting/undo-and-recovery.md)
- [Exercise files and validation](../kubernetes/examples/local-deployment-learning-path/index.md)
- [Back to cross-topic guides](index.md)

[^kind-start]: [kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/).
[^kind-release]: [kind v0.30.0 release and node-image digests](https://github.com/kubernetes-sigs/kind/releases/tag/v0.30.0).
[^deployment]: [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).
[^service]: [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/).
[^port-forward]: [kubectl port-forward](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_port-forward/).
[^git-restore]: [git restore](https://git-scm.com/docs/git-restore).
[^nginx-release]: [nginx stable release changes](https://nginx.org/en/CHANGES-1.30).
