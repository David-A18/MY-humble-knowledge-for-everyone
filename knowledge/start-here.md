---
type: Learning Path
title: Start here
description: Choose and complete a local beginner route through Git recovery, Kubernetes
  deployment and failure diagnosis, and Terraform state without an AWS account.
tags:
- learning
- local-development
- beginner
status: draft
audience: Beginning platform engineer
maintainer: unassigned
sources:
- id: kind-start
  title: kind quick start
  resource: https://kind.sigs.k8s.io/docs/user/quick-start/
- id: kubeconfig
  title: Kubernetes kubeconfig contexts
  resource: https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/
- id: git-restore
  title: git restore
  resource: https://git-scm.com/docs/git-restore
---

# Start here

This is the beginner route. On your own computer, and without a cloud account,
you will learn three tools that most platform teams use every day:

- **Git** keeps the history of your files, so you can undo mistakes safely.
- **Kubernetes** runs your applications in containers and keeps them running.
- **Terraform** creates and changes infrastructure from text files.

Each stage follows the same pattern: learn the idea, run a small example, break
it on purpose, find the cause, fix it, and clean up. Doing those steps teaches
far more than reading a list of commands.

## Purpose

Use [environment preflight](cross-topic-guides/local-learning-preflight.md) to choose a stage that your machine supports. You can do Git and Terraform practice without Docker. The Kubernetes stage uses local Linux containers and public registry downloads; none of these stages needs an AWS account.

## Prerequisites

| Stage | Requirement | Start when |
| --- | --- | --- |
| Git | Terminal, Git, isolated scratch copy | You can inspect a tracked file and make a local teaching commit. |
| Kubernetes | Bash, working Linux-container Docker, kind, compatible kubectl, registry access | Runtime and explicit target checks in preflight pass.[^kind-start][^kubeconfig] |
| Terraform | Terraform 1.4+ and isolated local directory | You are using the built-in `terraform_data` fixture, not a cloud backend/provider. |

Manual walkthrough commands use Bash. Native PowerShell users can run the Python Git/Terraform validators; see the preflight for the remaining platform-specific setup. Each exercise owns its own scratch directory/state or cluster, and has its own cleanup.

## First learning route

| Step | Read or do this | Check before moving on |
| --- | --- | --- |
| 1 | [Git undo and recovery](git/troubleshooting/undo-and-recovery.md) | Explain HEAD, index, and working tree. Unstage an edit without losing it, then restore only the disposable edit.[^git-restore] |
| 2 | [Kubernetes fundamentals](kubernetes/fundamentals/kubernetes-fundamentals.md) | Explain Pods, Deployments, ReplicaSets, readiness, labels and Services. |
| 3 | [Local Kubernetes deployment exercise](cross-topic-guides/local-deployment-learning-path.md) | Ready workload and HTTP; actual invalid-image diagnosis; recovered image/HTTP; namespace/cluster cleanup. |
| 4 | [Terraform local state lifecycle](terraform/local-state-lifecycle.md) | One state object, reviewed in-place update, correct output, and empty managed state after destroy. |

The Kubernetes and Terraform examples teach separate reconciliation/state systems; Terraform does not provision this kind cluster. A Git restore changes a file, a Kubernetes rollback changes a live Pod template, and Terraform apply changes the objects tracked by its selected state. Keep those boundaries visible when explaining what you recovered.

## Git restore, Kubernetes rollback, and Terraform state

Restoring `deployment.yaml` in Git does not roll back a live Kubernetes Deployment. The file's next apply is a separate action. A Kubernetes rollout undo does not restore the Git index or Terraform state, and this Terraform fixture has no binding to that Deployment. Identify the state system before choosing a recovery command.

## Understanding checks

Before moving to a cloud lab, explain which target each command used, which observation proved success, which failure was deliberate, and what was removed. Record versions, a short expected/observed result, failure reason, recovery result, cleanup, and any step you skipped. A timeout or missing executable does not count as the expected application failure.

If you can, ask a friend to follow the route on a fresh computer and note anything that confused them. Their questions show which steps need clearer explanations.

## Next routes

Choose the next integration only after reading its account, credential, cost and cleanup prerequisites:

| Goal | Next page | Additional preparation |
| --- | --- | --- |
| Explore AWS-hosted Kubernetes | [Deploying to EKS](cross-topic-guides/deploying-to-eks.md) | Authorized sandbox, AWS identity/network/cost controls and EKS permission checks. |
| Learn infrastructure control planes | [Crossplane on AWS](cross-topic-guides/crossplane-on-aws.md) | Existing cluster, Crossplane concepts, scoped provider credentials and external-resource cleanup. |
| Learn backup and recovery | [Velero](migrations/velero/index.md) | Owned cluster/object storage and a planned restore verification. |
| Continue Terraform locally | [Module/workspace](terraform/module-workspace-lab.md) and [provider alias](terraform/provider-alias-lab.md) labs | Finish the beginner lifecycle first; retain separate local states. |

## Evidence and current limits

Reviewed on 2026-11-10. Git recovery and Terraform lifecycle were executed on Windows with Git 2.55.0.windows.2, Python 3.13.17 and Terraform 1.17.1. Kubernetes versions and runtime evidence belong to the linked walkthrough and its exact revision's [CI workflow](../.github/workflows/local-learning-journey.yml); the local authoring host could not run Kubernetes. Earlier rootless/Terraform execution records in linked guides remain historical evidence. All route concepts remain draft/unassigned.

## Related links

- [Knowledge index](index.md)
- [Environment preflight](cross-topic-guides/local-learning-preflight.md)
- [Section review evidence](../governance/section-quality-progress.md)
- [Back to root index](../README.md)

[^kind-start]: [kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/).
[^kubeconfig]: [Kubernetes kubeconfig contexts](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/).
[^git-restore]: [git restore](https://git-scm.com/docs/git-restore).
