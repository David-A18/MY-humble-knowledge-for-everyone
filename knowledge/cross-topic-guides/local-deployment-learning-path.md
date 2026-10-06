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
  - id: nginx-image
    resource: https://hub.docker.com/_/nginx
    title: Docker Hub - nginx Official Image
  - id: kubernetes-deployment
    resource: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
    title: Kubernetes - Deployments
  - id: kubernetes-service
    resource: https://kubernetes.io/docs/concepts/services-networking/service/
    title: Kubernetes - Service
  - id: kubernetes-endpointslices
    resource: https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/
    title: Kubernetes - EndpointSlices
  - id: kubernetes-port-forward
    resource: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_port-forward/
    title: Kubernetes - kubectl port-forward
  - id: kubernetes-patch
    resource: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_patch/
    title: Kubernetes - kubectl patch
  - id: kubernetes-wait
    resource: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_wait/
    title: Kubernetes - kubectl wait
  - id: kubernetes-describe
    resource: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_describe/
    title: Kubernetes - kubectl describe
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
By the end, you should be able to explain how a Deployment creates Pods,
how a Service selects Pods and which can normally receive traffic, and why
a failed rollout does not necessarily stop the older version.

This path runs the cluster locally. You do not need AWS, EKS, Crossplane,
or a paid account. The first run needs access to public image registries
for the kind node image and `nginx:1.27-alpine`.

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
| [namespace.yaml](../kubernetes/examples/local-deployment-learning-path/namespace.yaml) | Creates a named namespace for the exercise; the namespace does not by itself isolate network traffic. |
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
| [Service](../kubernetes/core-objects/how-a-service-selects-pods.md) | A stable in-cluster name and virtual IP whose selector matches Pods by label; normally ready endpoints receive Service traffic. |
| Label | Key-value metadata used by the Service selector and troubleshooting commands. |
| Reconciliation | Kubernetes repeatedly compares actual state with desired state and tries to close the gap. |

## Prepare a local cluster

Install Docker, `kind`, `kubectl`, Git, and optionally `curl`
from their official documentation before starting. This route uses
Docker as the local container runtime. Make sure its daemon is
running and that image downloads can reach their registries. `kind`
creates Kubernetes nodes as containers on that
runtime.[^kind-quick-start]

Run `kind get clusters` first. If `kb-local` already exists, stop
or choose a different name throughout the exercise. The commands
below assume that `kb-local` belongs only to this exercise.

```bash
kind create cluster --name kb-local --wait 5m
kubectl cluster-info --context kind-kb-local
kubectl --context kind-kb-local wait --for=condition=Ready node --all --timeout=120s
kubectl --context kind-kb-local get nodes
```

What it does: creates a local Kubernetes cluster in Docker and
confirms `kubectl` can reach that named cluster. All later
`kubectl` commands specify the same context so a change to your
default context does not silently target another cluster.

The first wait lets kind finish bootstrapping its control plane; the second
waits for the Node's `Ready` condition. Expected condition: one
control-plane node is `Ready`. If either wait times out, inspect the
cluster before deploying instead of treating `NotReady` as success.
[^kind-quick-start][^kubernetes-wait]

## Copy the exercise files

You need the example files on your computer. If you are reading online and
do not already have a clone, run these commands in a directory where
`knowledge-source` does not exist:

```bash
git clone https://github.com/David-A18/MY-humble-knowledge-for-everyone.git knowledge-source
cd knowledge-source
```

If you already have a clone, go to its root instead. Before continuing,
check that `/tmp/kb-local-path` does not already contain someone else's
files or an earlier exercise. If it does, stop and choose another path,
replacing `/tmp/kb-local-path` consistently in the commands below.
From the repository root, make the destination first:

```bash
mkdir /tmp/kb-local-path
```

Only continue if `mkdir` succeeds. It reports an error when that path
already exists, so this step cannot silently reuse an old Git copy.
Now copy the files and commit them in the temporary directory:

```bash
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
kubectl --context kind-kb-local describe svc kb-web -n kb-learning
```

What it does: creates the namespace, Deployment, and Service, then waits until the Deployment is available.

Expected condition: two Pods are `Running` and `Ready`. The Service
description shows `Selector: app.kubernetes.io/name=kb-web`. The Deployment
creates and replaces Pods; the Service's selector gives clients a
stable way to find them even when Pod names change.[^kubernetes-deployment]
[^kubernetes-service][^kubernetes-describe]

## Inspect the running app

```bash
kubectl --context kind-kb-local port-forward service/kb-web 8080:80 -n kb-learning
```

What it does: selects a Pod behind the Service and forwards local
port `8080` to it. In another terminal, open
`http://127.0.0.1:8080` or use `curl http://127.0.0.1:8080`.

A successful response shows the nginx default page, including
`Welcome to nginx!`, and that this local forwarding session
reached a selected Pod. It does not test an external load balancer
or send traffic through the Service's virtual IP. It also does not
prove every replica responds. Stop the port-forward with `Ctrl+C`
after testing.[^kubernetes-port-forward]

If local port `8080` is in use, use another free port such as
`18080:80` in the port-forward command and `18080` in the browser or
`curl` URL. Make the same substitution in the later failed-rollout
check. A local port-bind error is not an application failure.

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
an image-pull failure. A nonzero exit from this one status command is
the expected signal to continue with diagnosis, not a reason to skip it.

## Diagnose the failure

```bash
kubectl --context kind-kb-local get pods -n kb-learning -o wide
kubectl --context kind-kb-local describe deployment/kb-web -n kb-learning
kubectl --context kind-kb-local get events -n kb-learning --sort-by=.lastTimestamp
kubectl --context kind-kb-local describe pod -n kb-learning -l app.kubernetes.io/name=kb-web
kubectl --context kind-kb-local get endpointslices -n kb-learning \
  -l kubernetes.io/service-name=kb-web -o yaml
```

What it does: shows Pod state, Deployment conditions, recent events,
image-pull messages, and the Service's endpoint records. Look for
`ImagePullBackOff`, `ErrImagePull`,
or a message that the tag cannot be found. The default RollingUpdate
strategy has 25% `maxUnavailable` (rounded down) and 25%
`maxSurge` (rounded up). With two replicas, that permits one
extra new Pod and zero unavailable Pods, so the older ready
Pods should remain while the new Pod fails. This is not a guarantee
against an unrelated node or application failure.[^kubernetes-deployment]

For this two-replica example, expect two older Pods with `1/1` ready
containers and one new Pod with `0/1` and an image-pull error. Pod
names and event timing will vary. If an old Pod is not ready, inspect
that separate problem rather than attributing everything to the bad tag.
In the EndpointSlice output, compare `endpoints[].addresses` with the
Pod IPs from `get pods -o wide`. The older Pods should have
`conditions.ready: true`; the new Pod may appear with `ready: false`
because its label matches even though it cannot serve. EndpointSlice
readiness shows which Pods are eligible for normal Service traffic;
it does not prove that a user request succeeded.[^kubernetes-endpointslices]

To check whether one selected Pod still answers during the failed
rollout, run this in one
terminal:

```bash
kubectl --context kind-kb-local port-forward service/kb-web 8080:80 -n kb-learning
```

Open `http://127.0.0.1:8080` or run `curl http://127.0.0.1:8080`
in another terminal.
If the default page still loads, the selected Pod answered.
Port-forward selects a Pod using the Service's selector;
it does not test routing through the Service's virtual IP or prove
every old replica answers. Stop the
port-forward with `Ctrl+C` before continuing.
If this port-forward fails, read its error and inspect Pod status before
concluding that in-cluster Service routing is broken. `kubectl port-forward`
does not identify the selected Pod in its normal success output. To check a
specific older ready Pod, use its name from `get pods -o wide` in the earlier
step and replace `<ready-pod-name>` below; stop any earlier forwarding session
first so local port `8080` is free:

```bash
kubectl --context kind-kb-local port-forward "pod/<ready-pod-name>" 8080:80 -n kb-learning
```

That still checks one Pod through a tunnel. The EndpointSlice readiness
check above is separate evidence about normal Service traffic.

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
kubectl --context kind-kb-local get endpointslices -n kb-learning \
  -l kubernetes.io/service-name=kb-web -o yaml
```

What it does: rolls back to the previous Deployment revision and waits for healthy Pods again.

Expected condition: the Deployment becomes available and the
new bad-image Pods disappear. Check that the current Pods appear as
ready EndpointSlice endpoints. Repeat the port-forward and HTTP request
if you want evidence that one selected Pod answers again; rollout
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
The temporary Git copy at `/tmp/kb-local-path` remains for practice;
review its contents before removing it or repeating the exercise.

## Understanding checks

- Which label connects the Service to the Pods?
- Which command showed the image-pull failure first?
- Why should the older Pods remain ready Service endpoints while the new
  rollout fails, and what did you observe?
- What is the difference between `git restore --staged deployment.yaml` and `git restore deployment.yaml`?
- Which cleanup command removed the cluster itself?

## Deeper study

- [kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/)
  for cluster creation and cleanup.
- [nginx official image](https://hub.docker.com/_/nginx)
  for the image used by the example Deployment.
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
  and [Services](https://kubernetes.io/docs/concepts/services-networking/service/)
  for rollout and routing behavior.
- [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/)
  for endpoint addresses and readiness during the rollout.
- [kubectl port-forward](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_port-forward/)
  and [kubectl patch](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_patch/)
  for the two local access and change commands.
- [kubectl describe](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_describe/)
  for reading the Service selector and Pod events.
- [Git restore](https://git-scm.com/docs/git-restore)
  for staged versus working-tree recovery.

## Related links

- [Start here](../start-here.md)
- [Kubernetes fundamentals](../kubernetes/fundamentals/index.md)
- [How a Kubernetes Service selects Pods](../kubernetes/core-objects/how-a-service-selects-pods.md)
- [kind custom clusters](../kubernetes/applications-and-tools/kind-custom-clusters.md)
- [Kubernetes common solutions](../kubernetes/troubleshooting/common-solutions.md)
- [Git undo and recovery](../git/troubleshooting/undo-and-recovery.md)
- [Back to cross-topic guides](index.md)
- [Back to Kubernetes index](../kubernetes/index.md)
- [Back to root index](../../README.md)

[^kind-quick-start]: [kind - Quick Start](https://kind.sigs.k8s.io/docs/user/quick-start/).
[^kubernetes-deployment]: [Kubernetes - Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).
[^kubernetes-service]: [Kubernetes - Service](https://kubernetes.io/docs/concepts/services-networking/service/).
[^kubernetes-endpointslices]: [Kubernetes - EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/).
[^kubernetes-port-forward]: [Kubernetes - kubectl port-forward](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_port-forward/).
[^kubernetes-patch]: [Kubernetes - kubectl patch](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_patch/).
[^kubernetes-wait]: [Kubernetes - kubectl wait](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_wait/).
[^kubernetes-describe]: [Kubernetes - kubectl describe](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_describe/).
[^git-restore]: [Git - git-restore](https://git-scm.com/docs/git-restore).
