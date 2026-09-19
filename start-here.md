# Start here

Status: Draft
Audience: Beginning platform engineer
Page type: Tutorial route
Maintainer: Unassigned
Last substantive review: 2026-09-19
Applicable versions: Git 2.53.0 source reviewed; Kubernetes and Terraform exercise versions declared in linked guides
Validation evidence: Source reviewed and statically checked; Kubernetes learning path executed end to end with rootless Docker 29.8.0, kind v0.30.0, Kubernetes v1.34.0, and kubectl v1.34.1; Terraform exercise locally executed with Terraform v1.13.1
Known limitations: Independent beginner testing belongs to the maintenance loop in the improvement plan
Next review: After KB-14 reader testing or by 2026-12-19

## Purpose

Use this route when you are beginning practical cloud and platform engineering and want one complete local path before touching AWS, EKS, Crossplane, or production-like infrastructure.

The first path keeps everything on your machine. It teaches the basic loop used in real work: make a Git change, deploy a small workload, break it on purpose, diagnose the symptom, recover, and clean up.

## Prerequisites

- A terminal and a text editor.
- Git installed.
- Docker installed and running.
- `kind` and `kubectl` installed for the Kubernetes exercise.
- Terraform installed for the Terraform exercise.
- Enough local resources for one small Kubernetes cluster: at least 2 CPUs and 4 GB of free memory is a practical starting point.

No cloud account is required for the first exercises.

## First learning route

| Step | Read or do this | Outcome |
| --- | --- | --- |
| 1 | [Git undo and recovery](git/troubleshooting/undo-and-recovery.md) | Understand working tree, index, `HEAD`, and safe restore behavior. |
| 2 | [Kubernetes fundamentals](kubernetes/fundamentals/README.md) | Learn Pods, Deployments, Services, namespaces, labels, and reconciliation. |
| 3 | [Local deployment learning path](cross-topic-guides/local-deployment-learning-path.md) | Deploy, break, diagnose, recover, and clean up a local workload. |
| 4 | [Terraform local state lifecycle](terraform/examples/local-state-lifecycle/README.md) | Learn configuration, state, plan, apply, change, and destroy without a cloud account. |

## Understanding checks

After the local deployment path, you should be able to answer:

- What is the difference between `HEAD`, the Git index, and the working tree?
- Why does a Deployment create Pods through a ReplicaSet instead of being a Pod itself?
- How does a Service choose which Pods receive traffic?
- What changed when the workload failed, and which command showed the reason?
- Which cleanup command proves the local Kubernetes resources are gone?

## Next routes

After completing the local path, choose based on your goal:

| Goal | Next page | Extra prerequisites |
| --- | --- | --- |
| Learn AWS-hosted Kubernetes | [Deploying to EKS](cross-topic-guides/deploying-to-eks.md) | AWS sandbox account, IAM access, AWS CLI, and cost guardrails. |
| Learn infrastructure control planes | [Crossplane on AWS](cross-topic-guides/crossplane-on-aws.md) | Kubernetes context, Crossplane concepts, AWS sandbox account, and cleanup discipline. |
| Learn backup and recovery | [Velero](migrations/velero/README.md) | Kubernetes cluster, object storage, and backup/restore test space. |

## Related links

- [Knowledge-base improvement plan](knowledge-base-improvement-plan.md)
- [Back to root index](README.md)
