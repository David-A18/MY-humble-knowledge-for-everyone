---
type: "Learning Path"
title: "Start here"
description: "Choose a first learning route in the knowledge base, then use the local platform path if you want a complete hands-on sequence without a cloud account."
tags: [start-here]
status: draft
maturity: draft
audience: "Curious learners and beginning engineers"
maintainer: unassigned
---

# Start here

Status: Draft
Audience: Curious learners and beginning engineers
Page type: Learning Path
Maintainer: Unassigned
Local route reading review: 2026-10-06 (Claude Opus 5.5 read-only reviews, including the new Terraform language and Kubernetes Service steps; primary sources checked separately; no new cluster or reader trial)
Applicable versions: Git 2.53.0 source reviewed; Kubernetes and Terraform exercise versions declared in linked guides
Validation evidence: The earlier local platform route was source reviewed and statically checked; its Kubernetes exercise was executed end to end with rootless Docker 29.8.0, kind v0.30.0, Kubernetes v1.34.0, and kubectl v1.34.1; its Terraform exercise was rerun locally with Terraform v1.13.1 on 2026-10-06. The current Kubernetes exercise has a revised failure step that has not been rerun. These results do not validate the newly broadened topic choices.
Known limitations: The broader entry route and new or rewritten explanations have not been independently reader-tested. Many listed areas remain partial; the local platform route is the only complete beginner exercise sequence documented here.
Next review: After KB-14 reader testing or by 2026-12-19

## Purpose

Use this page when you have a learning question but do not yet know where to
begin. Pick one topic below, read its plain-language explanation, try its
bounded example or exercise, then follow its official documentation links
when you want the full product or standard detail.

The knowledge base is a growing library, not a complete course in every
subject yet. A `draft` page is a useful starting point whose review is still
open. Check a page's scope and source links before using it for important
work.

## Choose your first question

| If you want to understand... | Start here | What you can explain afterward |
| --- | --- | --- |
| How a change moves through Git | [Git fundamentals](git/git-fundamentals.md) | Working tree, index, commit, branch, and remote are different places or pointers. |
| How Kubernetes keeps an application running | [Kubernetes fundamentals](kubernetes/fundamentals/kubernetes-fundamentals.md) | Desired state, controllers, Pods, and Services each have a role. |
| How a Kubernetes Service finds Pods | [How a Kubernetes Service selects Pods](kubernetes/core-objects/how-a-service-selects-pods.md) | Labels choose candidates; readiness and EndpointSlices shape normal traffic. |
| How Terraform decides what to change | [Terraform fundamentals](terraform/fundamentals/terraform-fundamentals.md) | Configuration, state, plan, and apply form a connected loop. |
| Why teams choose different databases | [Relational vs. document databases](databases/relational-vs-document-databases.md) | Relationships and document boundaries affect modeling choices. |
| How an outside web request reaches a service | [Gateway API and Ingress](kubernetes/applications-and-tools/gateway-api-and-ingress.md) | A route describes traffic; an implementation serves it. |
| How cloud costs get an owner | [Cost allocation basics](finops/cost-allocation-basics.md) | Direct, shared, and still unallocated cost need different decisions. |
| How a knowledge search finds evidence for an AI answer | [Retrieval and context efficiency](ai/ai-tooling/knowledge-bases/retrieval-and-context-efficiency.md) | Search finds candidates; fetching and checking sources support an answer. This route assumes some AI tooling context. |
| What “Bootstrap” means in web work | [Bootstrap and bootstrapping](programming-languages/bootstrap-and-bootstrapping.md) | The UI toolkit and first-time system setup are separate ideas. |

If your topic is absent, use the [topic map](index.md) and
[glossary](glossary.md). Planned areas are labelled as such in their indexes;
do not assume a thin section contains a complete learning path.

## How to use one page

1. Read the **purpose** and the short model before the details.
2. Trace its example or diagram and say what each part does in your own words.
3. Use its understanding questions to find what is still unclear.
4. Follow the page's official documentation links for deeper or current
   product behavior. Check draft, review, and freshness notes before acting.
5. Move through the related links when the next question is different.

For a complete local practice sequence, use the route below.

## Complete local platform route

This path runs its cluster on your machine. It teaches a loop used in real work: make a
Git change, deploy a small workload, break it on purpose, diagnose the
symptom, recover, and clean up. It is one option within the wider library.

## Prerequisites

- A terminal and a text editor.
- Git installed.
- A local clone of this public repository for the example files; the local
  deployment guide shows how to make one if you are reading online.
- Docker installed and running.
- `kind` and `kubectl` installed for the Kubernetes exercise.
- Terraform 1.4.0 or newer installed for the Terraform exercise.
- Network access to download the kind node and `nginx:1.27-alpine` images on
  the first local cluster run.
- Enough local resources for one small Kubernetes cluster: at least 2 CPUs and 4 GB of free memory is a practical starting point.

Install the tools as you reach their steps: Docker, `kind`, and `kubectl`
are needed for step 5; Terraform is needed for steps 6 and 7. No cloud account
is required for these exercises.

## Local learning steps

| Step | Read or do this | Outcome |
| --- | --- | --- |
| 1 | [Git fundamentals](git/git-fundamentals.md) | Picture how a change moves from the working tree to the index, into a commit, and to a remote; see how branches and `HEAD` point at commits; tell a local commit from a push. |
| 2 | [Git undo and recovery](git/troubleshooting/undo-and-recovery.md) | Inspect first, then choose a safe restore, unstage, revert, or reset path. |
| 3 | [Kubernetes fundamentals](kubernetes/fundamentals/kubernetes-fundamentals.md) | Learn desired state, reconciliation, and how Deployments, ReplicaSets, Pods, labels, and Services connect. |
| 4 | [How a Kubernetes Service selects Pods](kubernetes/core-objects/how-a-service-selects-pods.md) | Separate label matching, endpoint readiness, ClusterIP routing, and port-forward. |
| 5 | [Local deployment learning path](cross-topic-guides/local-deployment-learning-path.md) | Deploy, break, diagnose, recover, and clean up a local workload. |
| 6 | [How values move through Terraform configuration](terraform/language/how-values-move-through-terraform.md) | Trace an input variable and a local value into a resource, then follow its result to a root output. |
| 7 | [Terraform local state lifecycle](terraform/examples/local-state-lifecycle/local-state-lifecycle.md) | Learn configuration, state, plan, apply, change, and destroy without a cloud account. |

If plan, apply, and state are new to you, read [Terraform
fundamentals](terraform/fundamentals/terraform-fundamentals.md) before step 6.

## Local route understanding checks

After the full local route, you should be able to answer:

- What is the difference between `HEAD`, the Git index, and the working tree?
- What is the difference between committing a change and pushing it?
- Why does a Deployment create Pods through a ReplicaSet instead of being a Pod itself?
- How does a Service choose which Pods receive traffic?
- What changed when the workload failed, and which command showed the reason?
- Which cleanup command proves the local Kubernetes resources are gone?
- Why does `var.release_version` feed the Terraform resource, while
  `release_summary` reads a result from it?
- Why can a Terraform plan propose changing back to a default after a
  previous plan used a one-command variable override?

## After the local route

After completing the local path, choose based on your goal:

| Goal | Next page | Extra prerequisites |
| --- | --- | --- |
| Learn AWS-hosted Kubernetes | [Deploying to EKS](cross-topic-guides/deploying-to-eks.md) | AWS sandbox account, IAM access, AWS CLI, and cost guardrails. |
| Learn infrastructure control planes | [Crossplane on AWS](cross-topic-guides/crossplane-on-aws.md) | Kubernetes context, Crossplane concepts, AWS sandbox account, and cleanup discipline. |
| Learn backup and recovery | [Velero](migrations/velero/index.md) | Kubernetes cluster, object storage, and backup/restore test space. |

## Related links

- [Knowledge-base improvement plan](../knowledge-base-improvement-plan.md)
- [Back to root index](../README.md)
