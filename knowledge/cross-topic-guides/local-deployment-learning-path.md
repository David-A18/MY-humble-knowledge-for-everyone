---
type: "Learning Path"
title: "Local deployment learning path"
description: "Learn the path from a local Kubernetes Deployment to a working request, then diagnose and recover from a failed image rollout."
tags: [cross-topic-guides, local-deployment-learning-path]
status: draft
maturity: draft
audience: "Beginning platform engineer"
maintainer: unassigned
sources:
  - id: kind-quick-start
    resource: https://kind.sigs.k8s.io/docs/user/quick-start/
    title: kind - Quick Start
  - id: kubernetes-deployment
    resource: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
    title: Kubernetes - Deployments
  - id: kubernetes-service
    resource: https://kubernetes.io/docs/concepts/services-networking/service/
    title: Kubernetes - Service
  - id: kubernetes-port-forward
    resource: https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/
    title: Kubernetes - Use Port Forwarding to Access Applications in a Cluster
  - id: kubernetes-patch
    resource: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_patch/
    title: Kubernetes - kubectl patch
  - id: git-restore
    resource: https://git-scm.com/docs/git-restore
    title: Git - git-restore
---

# Local deployment learning path

This is a **draft learning path** for a beginning platform engineer.
The previous version recorded an end-to-end run on 2026-09-19 using
Docker 29.8.0, kind v0.30.0, a Kubernetes v1.34.0 node image, and
kubectl v1.34.1. This revision changes the failure command and patch
file; that revised path has **not** been run in a cluster. It also
still needs the planned KB-14 reader test. The exercise does not
cover cloud load balancers, IAM, persistent storage, or production ingress.

## Goal

Create a local Kubernetes cluster, deploy a small web workload, break
it with a bad image tag, diagnose the failure, recover, and clean up.
By the end, you should be able to explain how a Deployment creates
Pods, how a Service finds ready Pods, and why a failed rollout does
not necessarily stop the older version.

This path intentionally stays local. You do not need AWS, EKS, Crossplane, or a paid account.

## Route through the exercise

| Step | Outcome to look for | Idea to keep |
| --- | --- | --- |
| Prepare | The local cluster has a ready node. | Your commands need the intended cluster context. |
| Deploy | Two web Pods are ready behind one Service. | A Deployment manages Pods; a Service selects them. |
| Observe | A local HTTP request returns the test page. | Port-forward reaches one selected Pod; it is a local check. |
| Break and diagnose | A new Pod cannot pull its image. | The desired update can fail while older Pods remain available. |
| Recover | The previous revision becomes available again. | Rollback changes desired state; verify the result. |
| Clean up | The namespace and named cluster are gone. | Remove only resources created for this exercise. |

## What you will create

| File | Purpose |
| --- | --- |
| [namespace.yaml](../kubernetes/examples/local-deployment-learning-path/namespace.yaml) | Creates an isolated namespace for the exercise. |
| [deployment.yaml](../kubernetes/examples/local-deployment-learning-path/deployment.yaml) | Runs a small two-replica web Deployment. |
| [service.yaml](../kubernetes/examples/local-deployment-learning-path/service.yaml) | Exposes the Pods inside the cluster with a stable Service. |
| [failing-image-patch.yaml](../kubernetes/examples/local-deployment-learning-path/failing-image-patch.yaml) | A strategic merge patch that changes only the web container image. |

## Concepts before commands

| Concept | Meaning in this exercise |
| --- | --- |
| Namespace | A named workspace for the exercise resources. |
| Pod | The smallest runnable workload unit. The Deployment creates Pods for you. |
| Deployment | Desired state for replicated Pods and rolling updates. |
| ReplicaSet | Controller object created by the Deployment to keep the desired number of Pods. |
| Service | A stable cluster endpoint that selects Pods by label; ready endpoints receive normal Service traffic. |
| Label | Key-value metadata used by the Service selector and troubleshooting commands. |
| Reconciliation | Kubernetes repeatedly compares actual state with desired state and tries to close the gap. |

## Prepare a local cluster

Install Docker, `kind`, `kubectl`, Git, and optionally `curl`
from their official documentation before starting. This route uses
Docker as the local container runtime. Make sure its daemon is
running. `kind` creates Kubernetes nodes as containers on that
runtime.[^kind-quick-start]

Run `kind get clusters` first. If `kb-local` already exists, stop
or choose a different name throughout the exercise. The commands
below assume that `kb-local` belongs only to this exercise.

```bash
kind create cluster --name kb-local
kubectl cluster-info --context kind-kb-local
kubectl --context kind-kb-local get nodes
```

What it does: creates a local Kubernetes cluster in Docker and
confirms `kubectl` can reach that named cluster. All later
`kubectl` commands specify the same context so a change to your
default context does not silently target another cluster.

Expected condition: one control-plane node is `Ready`.

## Copy the exercise files

From the repository root, create a small working copy:

```bash
mkdir -p /tmp/kb-local-path
cp knowledge/kubernetes/examples/local-deployment-learning-path/*.yaml /tmp/kb-local-path/
cd /tmp/kb-local-path
git init
git add .
git -c user.name="Local Lab" -c user.email="lab@example.invalid" commit -m "add local deployment exercise"
```

What it does: gives you an isolated Git repository where you can
inspect changes, practice recovery, and avoid editing the knowledge
base files. The example identity applies only to this local commit;
use your own identity if you intend to publish it.

## Deploy the app

```bash
kubectl --context kind-kb-local apply -f namespace.yaml
kubectl --context kind-kb-local apply -f deployment.yaml
kubectl --context kind-kb-local apply -f service.yaml
kubectl --context kind-kb-local rollout status deployment/kb-web -n kb-learning
kubectl --context kind-kb-local get pods -n kb-learning --show-labels
kubectl --context kind-kb-local get svc kb-web -n kb-learning
```

What it does: creates the namespace, Deployment, and Service, then waits until the Deployment is available.

Expected condition: two Pods are `Running` and `Ready`, and the
Service selector is `app.kubernetes.io/name=kb-web`. The Deployment
creates and replaces Pods; the Service's selector gives clients a
stable way to find them even when Pod names change.[^kubernetes-deployment]
[^kubernetes-service]

## Inspect the running app

```bash
kubectl --context kind-kb-local port-forward service/kb-web 8080:80 -n kb-learning
```

What it does: selects a Pod behind the Service and forwards local
port `8080` to it. In another terminal, open
`http://127.0.0.1:8080` or use `curl http://127.0.0.1:8080`.

A successful response shows that this local forwarding session
reached a selected Pod. It does not test an external load balancer
or prove every replica responds. Stop the port-forward with `Ctrl+C`
after testing.[^kubernetes-port-forward]

## Break the workload on purpose

Apply the failing strategic merge patch. It targets only the
`web` image field, leaving the readiness probe and resource
requests in the original Deployment unchanged.[^kubernetes-patch]

```bash
kubectl --context kind-kb-local patch deployment/kb-web -n kb-learning --type strategic --patch-file failing-image-patch.yaml
kubectl --context kind-kb-local rollout status deployment/kb-web -n kb-learning --timeout=60s
```

What it does: changes the container image to a deliberately
nonexistent tag so new Pods should fail to pull it. The rollout
status command should time out or report failure. If the image
unexpectedly exists or was cached, stop and inspect the actual
image and Pod events instead of assuming this lesson reproduced
an image-pull failure.

## Diagnose the failure

```bash
kubectl --context kind-kb-local get pods -n kb-learning -o wide
kubectl --context kind-kb-local describe deployment/kb-web -n kb-learning
kubectl --context kind-kb-local get events -n kb-learning --sort-by=.lastTimestamp
kubectl --context kind-kb-local describe pod -n kb-learning -l app.kubernetes.io/name=kb-web
```

What it does: shows Pod state, Deployment conditions, recent events,
and image-pull messages. Look for `ImagePullBackOff`, `ErrImagePull`,
or a message that the tag cannot be found. The default RollingUpdate
strategy has 25% `maxUnavailable` (rounded down) and 25%
`maxSurge` (rounded up). With two replicas, that permits one
extra new Pod and zero unavailable Pods, so the older ready
Pods should remain while the new Pod fails. This is not a guarantee
against an unrelated node or application failure.[^kubernetes-deployment]

Record a short note:

```text
Failure:
Evidence command:
Observed symptom:
Fix:
```

## Recover

```bash
kubectl --context kind-kb-local rollout undo deployment/kb-web -n kb-learning
kubectl --context kind-kb-local rollout status deployment/kb-web -n kb-learning
kubectl --context kind-kb-local get pods -n kb-learning
```

What it does: rolls back to the previous Deployment revision and waits for healthy Pods again.

Expected condition: the Deployment becomes available and the
new bad-image Pods disappear. Repeat the port-forward and HTTP
request if you want evidence of the user-visible path; rollout
status alone does not prove it.

## Practice Git recovery

Edit `deployment.yaml` in your temporary copy and change the image tag to another value. Stage it, then restore it intentionally:

```bash
git status --short
git add deployment.yaml
git diff --staged
git restore --staged deployment.yaml
git restore deployment.yaml
git status --short
```

What it does: practices the difference between unstaging a file and
discarding unstaged edits from the working tree. The second restore
discards your temporary edit, so inspect the diff first.[^git-restore]

## Clean up

> [!WARNING]
> The next command deletes the local exercise namespace and everything inside it.

```bash
kubectl --context kind-kb-local delete namespace kb-learning
kubectl --context kind-kb-local get namespace kb-learning
kind delete cluster --name kb-local
kind get clusters
```

What it does: removes the exercise resources and then removes the local cluster.

Expected condition: the namespace lookup reports `NotFound`, and
`kind get clusters` no longer lists `kb-local`.

## Understanding checks

- Which label connects the Service to the Pods?
- Which command showed the image-pull failure first?
- Why did the old Pods keep serving while the new rollout failed?
- What is the difference between `git restore --staged deployment.yaml` and `git restore deployment.yaml`?
- Which cleanup command removed the cluster itself?

## Deeper study

- [kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/)
  for cluster creation and cleanup.
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
  and [Services](https://kubernetes.io/docs/concepts/services-networking/service/)
  for rollout and routing behavior.
- [kubectl port-forward](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/)
  and [kubectl patch](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_patch/)
  for the two local access and change commands.
- [Git restore](https://git-scm.com/docs/git-restore)
  for staged versus working-tree recovery.

## Related links

- [Start here](../start-here.md)
- [Kubernetes fundamentals](../kubernetes/fundamentals/index.md)
- [kind custom clusters](../kubernetes/applications-and-tools/kind-custom-clusters.md)
- [Kubernetes common solutions](../kubernetes/troubleshooting/common-solutions.md)
- [Git undo and recovery](../git/troubleshooting/undo-and-recovery.md)
- [Back to cross-topic guides](index.md)
- [Back to Kubernetes index](../kubernetes/index.md)
- [Back to root index](../../README.md)

[^kind-quick-start]: [kind - Quick Start](https://kind.sigs.k8s.io/docs/user/quick-start/).
[^kubernetes-deployment]: [Kubernetes - Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).
[^kubernetes-service]: [Kubernetes - Service](https://kubernetes.io/docs/concepts/services-networking/service/).
[^kubernetes-port-forward]: [Kubernetes - Port Forwarding](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/).
[^kubernetes-patch]: [Kubernetes - kubectl patch](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_patch/).
[^git-restore]: [Git - git-restore](https://git-scm.com/docs/git-restore).
