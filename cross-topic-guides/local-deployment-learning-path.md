# Local deployment learning path

Status: Draft
Audience: Beginning platform engineer
Page type: Tutorial
Maintainer: Unassigned
Last substantive review: 2026-09-19
Applicable versions: Docker 29.8.0 rootless daemon, kind v0.30.0, Kubernetes v1.34.0 node image, kubectl v1.34.1 client, and stable Namespace, Deployment, and Service APIs
Validation evidence: Executed end to end in a disposable kind cluster: created cluster, deployed namespace/Deployment/Service, verified Service with port-forward and curl, reproduced `ErrImagePull`, rolled back, practiced Git restore, deleted namespace, and deleted cluster
Known limitations: Uses local Kubernetes only; it does not teach cloud load balancers, IAM, persistent storage, or production ingress
Next review: After KB-14 reader testing or by 2026-12-19

## Goal

Create a local Kubernetes cluster, deploy a small web workload, break it with a bad image tag, diagnose the failure, recover, and clean up.

This path intentionally stays local. You do not need AWS, EKS, Crossplane, or a paid account.

## What you will create

| File | Purpose |
| --- | --- |
| [namespace.yaml](../kubernetes/examples/local-deployment-learning-path/namespace.yaml) | Creates an isolated namespace for the exercise. |
| [deployment.yaml](../kubernetes/examples/local-deployment-learning-path/deployment.yaml) | Runs a small two-replica web Deployment. |
| [service.yaml](../kubernetes/examples/local-deployment-learning-path/service.yaml) | Exposes the Pods inside the cluster with a stable Service. |
| [failing-image-patch.yaml](../kubernetes/examples/local-deployment-learning-path/failing-image-patch.yaml) | Breaks the Deployment by changing the image to a tag that should not exist. |

## Concepts before commands

| Concept | Meaning in this exercise |
| --- | --- |
| Namespace | A named workspace for the exercise resources. |
| Pod | The smallest runnable workload unit. The Deployment creates Pods for you. |
| Deployment | Desired state for replicated Pods and rolling updates. |
| ReplicaSet | Controller object created by the Deployment to keep the desired number of Pods. |
| Service | Stable virtual endpoint that selects ready Pods by label. |
| Label | Key-value metadata used by the Service selector and troubleshooting commands. |
| Reconciliation | Kubernetes repeatedly compares actual state with desired state and tries to close the gap. |

## Prepare a local cluster

Install Docker, `kind`, and `kubectl` from their official documentation before starting. Use a disposable cluster name so cleanup is simple.

```bash
kind create cluster --name kb-local
kubectl cluster-info --context kind-kb-local
kubectl get nodes
```

What it does: creates a local Kubernetes cluster in Docker and confirms `kubectl` can reach it.

Expected condition: one control-plane node is `Ready`.

## Copy the exercise files

From the repository root, create a small working copy:

```bash
mkdir -p /tmp/kb-local-path
cp kubernetes/examples/local-deployment-learning-path/*.yaml /tmp/kb-local-path/
cd /tmp/kb-local-path
git init
git add .
git commit -m "add local deployment exercise"
```

What it does: gives you an isolated Git repository where you can inspect changes, practice recovery, and avoid editing the knowledge base files during the exercise.

## Deploy the app

```bash
kubectl apply -f namespace.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl rollout status deployment/kb-web -n kb-learning
kubectl get pods -n kb-learning --show-labels
kubectl get svc kb-web -n kb-learning
```

What it does: creates the namespace, Deployment, and Service, then waits until the Deployment is available.

Expected condition: two Pods are `Running` and `Ready`, and the Service selector is `app.kubernetes.io/name=kb-web`.

## Inspect the running app

```bash
kubectl port-forward service/kb-web 8080:80 -n kb-learning
```

What it does: forwards local port `8080` to the Service. In another terminal, open `http://127.0.0.1:8080` or use `curl http://127.0.0.1:8080`.

Stop the port-forward with `Ctrl+C` after testing.

## Break the workload on purpose

Apply the failing patch:

```bash
kubectl apply -f failing-image-patch.yaml
kubectl rollout status deployment/kb-web -n kb-learning --timeout=60s
```

What it does: changes the container image to an invalid tag so the new Pods cannot pull the image. The rollout status command should time out or report failure.

## Diagnose the failure

```bash
kubectl get pods -n kb-learning -o wide
kubectl describe deployment/kb-web -n kb-learning
kubectl get events -n kb-learning --sort-by=.lastTimestamp
kubectl describe pod -n kb-learning -l app.kubernetes.io/name=kb-web
```

What it does: shows Pod state, Deployment conditions, recent events, and image-pull messages. Look for `ImagePullBackOff`, `ErrImagePull`, or a message that the tag cannot be found.

Record a short note:

```text
Failure:
Evidence command:
Observed symptom:
Fix:
```

## Recover

```bash
kubectl rollout undo deployment/kb-web -n kb-learning
kubectl rollout status deployment/kb-web -n kb-learning
kubectl get pods -n kb-learning
```

What it does: rolls back to the previous Deployment revision and waits for healthy Pods again.

Expected condition: the Deployment becomes available and the new bad-image Pods disappear.

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

What it does: practices the difference between unstaging a file and discarding unstaged edits from the working tree.

## Clean up

> [!WARNING]
> The next command deletes the local exercise namespace and everything inside it.

```bash
kubectl delete namespace kb-learning
kubectl get namespace kb-learning
kind delete cluster --name kb-local
```

What it does: removes the exercise resources and then removes the local cluster.

Expected condition: the namespace no longer exists and `kind get clusters` no longer lists `kb-local`.

## Understanding checks

- Which label connects the Service to the Pods?
- Which command showed the image-pull failure first?
- Why did the old Pods keep serving while the new rollout failed?
- What is the difference between `git restore --staged deployment.yaml` and `git restore deployment.yaml`?
- Which cleanup command removed the cluster itself?

## Related links

- [Start here](../start-here.md)
- [Kubernetes fundamentals](../kubernetes/fundamentals/README.md)
- [kind custom clusters](../kubernetes/applications-and-tools/kind-custom-clusters.md)
- [Kubernetes common solutions](../kubernetes/troubleshooting/common-solutions.md)
- [Git undo and recovery](../git/troubleshooting/undo-and-recovery.md)
- [Back to cross-topic guides](README.md)
- [Back to Kubernetes index](../kubernetes/README.md)
- [Back to root index](../README.md)
