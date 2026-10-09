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

## Purpose

Use this page when you have a learning question but do not yet know where to
begin. Pick one topic below, read its plain-language explanation, try its
example or exercise if it has one, then follow its official documentation links
when you want the full product or standard detail.

The knowledge base is a growing library, not a complete course in every
subject yet. A `draft` page is a useful starting point whose review is still
open. Check a page's scope and source links before using it for important
work.

You can read any explanation without installing tools. The software listed
later is needed only if you choose the hands-on local route.

## Choose your first question

| If you want to understand... | Start here | What you can explain afterward |
| --- | --- | --- |
| How a change moves through Git | [Git fundamentals](git/git-fundamentals.md) | Working tree, index, commit, branch, and remote are different places or pointers. |
| What cloud computing provides | [Cloud computing fundamentals](cloud/cloud-computing-fundamentals.md) | Provider infrastructure and your workload choices are distinct; scaling, reliability, and cost decisions affect each other. |
| How Kubernetes keeps an application running | [Kubernetes fundamentals](kubernetes/fundamentals/kubernetes-fundamentals.md) | Desired state, controllers, Pods, and Services each have a role. |
| How a Kubernetes Service finds Pods | [How a Kubernetes Service selects Pods](kubernetes/core-objects/how-a-service-selects-pods.md) | Labels choose candidates; readiness and EndpointSlices shape normal traffic. |
| How Terraform decides what to change | [Terraform fundamentals](terraform/fundamentals/terraform-fundamentals.md) | Configuration, state, plan, and apply form a connected loop. |
| Why teams choose different databases | [Relational vs. document databases](databases/relational-vs-document-databases.md) | Relationships and document boundaries affect modeling choices. |
| How an outside web request reaches a service | [Gateway API and Ingress](kubernetes/applications-and-tools/gateway-api-and-ingress.md) | A route describes traffic; an implementation serves it. |
| How cloud costs get an owner | [Cost allocation basics](finops/cost-allocation-basics.md) | Direct, shared, and still unallocated cost need different decisions. |
| What AI, ML, language models, and agents mean | [AI fundamentals](ai/ai-fundamentals.md) | Tell a trained model from the application around it, and explain why an answer needs checking. |
| How a knowledge search finds evidence for an AI answer | [Retrieval and context efficiency](ai/ai-tooling/knowledge-bases/retrieval-and-context-efficiency.md) | Search finds candidates; fetching and checking sources support an answer. Read [AI fundamentals](ai/ai-fundamentals.md) first if AI tooling is new to you. |
| What “Bootstrap” means in web work | [Bootstrap and bootstrapping](programming-languages/bootstrap-and-bootstrapping.md) | The UI toolkit and first-time system setup are separate ideas. |

If your topic is absent, use the [topic map](index.md) and
[glossary](glossary.md). Planned areas are labelled as such in their indexes;
do not assume a thin section contains a complete learning path.

## How to use one page

1. Read the opening summary and, if present, the short model before the details.
2. Trace its example or diagram and say what each part does in your own words.
3. Use its understanding questions, if present, to find what is still unclear.
4. Follow the page's official documentation links for deeper or current
   product behavior. Check draft, review, and freshness notes before acting.
5. Move through the related links when the next question is different.

For a complete local practice sequence, use the route below.

## End-to-end local practice route

This path runs its cluster on your machine. It teaches a loop used in real work: make a
Git change, deploy a small workload, break it on purpose, diagnose the
symptom, recover, and clean up. It is one option within the wider library.
The later Terraform exercise uses only local state; it does not manage the
Kubernetes workload you deployed.

### Prerequisites

- A terminal and a text editor.
- Git installed.
- A local clone of the [public knowledge-base
  repository](https://github.com/David-A18/MY-humble-knowledge-for-everyone)
  for example files. The [local deployment
  guide](cross-topic-guides/local-deployment-learning-path.md#copy-the-exercise-files)
  shows how to make one if you are reading online.
- Docker installed and running.
- `kind` and `kubectl` installed for the Kubernetes exercise.
- Terraform 1.4.0 or newer installed for the Terraform exercise.
- Network access to download the kind node and `nginx:1.27-alpine` images on
  the first local cluster run.
- Enough local CPU, memory, and disk space for the kind node and the sample
  workload; check the [kind installation guide](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
  and Docker's resource settings for your machine.

Install the tools as you reach their steps: Docker, `kind`, and `kubectl`
are needed for step 5; Terraform is needed for step 8. No cloud account
is required for these exercises.

### Local learning steps

| Step | Read or do this | Outcome |
| --- | --- | --- |
| 1 | [Git fundamentals](git/git-fundamentals.md) | Picture how a change moves from the working tree to the index, into a commit, and to a remote; see how branches and `HEAD` point at commits; tell a local commit from a push. |
| 2 | [Git undo and recovery](git/troubleshooting/undo-and-recovery.md) | Skim the safe recovery choices now; return when step 5 gives you a Git change to inspect. |
| 3 | [Kubernetes fundamentals](kubernetes/fundamentals/kubernetes-fundamentals.md) | Learn desired state, reconciliation, and how Deployments, ReplicaSets, Pods, labels, and Services connect. |
| 4 | [How a Kubernetes Service selects Pods](kubernetes/core-objects/how-a-service-selects-pods.md) | Separate label matching, endpoint readiness, ClusterIP routing, and port-forward. |
| 5 | [Local deployment learning path](cross-topic-guides/local-deployment-learning-path.md) | Deploy, break, diagnose, recover, and clean up a local workload. |
| 6 | [Terraform fundamentals](terraform/fundamentals/terraform-fundamentals.md) | Understand configuration, providers, resources, state, plans, and apply before touching infrastructure. |
| 7 | [How values move through Terraform configuration](terraform/language/how-values-move-through-terraform.md) | Trace an input variable and a local value into a resource, then follow its result to a root output. |
| 8 | [Terraform local state lifecycle](terraform/examples/local-state-lifecycle/local-state-lifecycle.md) | Learn configuration, state, plan, apply, change, and destroy without a cloud account. |

Steps 1–4 prepare the ideas; step 5 is the Kubernetes and Git exercise. Steps
6–7 prepare the Terraform model; step 8 is a separate hands-on exercise. Use
the [Kubernetes cleanup](cross-topic-guides/local-deployment-learning-path.md#clean-up)
or [Terraform early-stop
instructions](terraform/examples/local-state-lifecycle/local-state-lifecycle.md#if-a-step-fails-or-you-stop-early)
if you stop partway through.

### Check what you learned

After the full local route, you should be able to answer:

- What is the difference between `HEAD`, the Git index, and the working tree?
- What is the difference between committing a change and pushing it?
- When a working-tree edit is unwanted, what would you inspect before using
  `git restore`?
- Why does a Deployment manage Pods through ReplicaSets instead of directly?
- How does a Service choose which Pods receive traffic?
- What changed when the workload failed, and which command showed the reason?
- Which cleanup command proves the local Kubernetes resources are gone?
- Why does `var.release_version` feed the Terraform resource, while
  `release_summary` reads a result from it?
- Why can a Terraform plan propose changing back to a default after a
  previous plan used a one-command variable override?
- Which managed resources remain in Terraform state after the tutorial's
  destroy step, and which local files remain on disk?

Return to the linked step page whenever an answer is unclear. The questions
are checks for your own understanding, not a scored test.

## After the local route

After completing the local path, choose based on your goal:

| Goal | Next page | Extra prerequisites |
| --- | --- | --- |
| Keep learning locally | [Terraform state management](terraform/fundamentals/state-management.md) | None for reading. |
| Learn AWS-hosted Kubernetes | [Deploying to EKS](cross-topic-guides/deploying-to-eks.md) | AWS sandbox account, IAM access, AWS CLI, and cost guardrails. |
| Learn infrastructure control planes | [Crossplane on AWS](cross-topic-guides/crossplane-on-aws.md) | Kubernetes context, Crossplane concepts, AWS sandbox account, and cleanup discipline. |
| Learn backup and recovery | [Velero](migrations/velero/index.md) | Kubernetes cluster, object storage, and backup/restore test space. |

The AWS and backup exercises can create billable resources. Read their
prerequisites and cleanup instructions before running commands.

## If a page is unclear

Report an incorrect step, unfamiliar term, or missing prerequisite through the
[documentation issue form](https://github.com/David-A18/MY-humble-knowledge-for-everyone/issues/new?template=documentation-error.yml).
Include the page link and what you expected; leave out secrets and private
work details. If a product's behavior may have changed, check its official
documentation linked from the page while the draft is corrected.

## Review information

- **Status:** Draft. This is a learning route, not a claim that every linked
  topic has completed review.
- **Audience:** Curious learners and beginning engineers.
- **Maintainer:** Unassigned.
- **Local route reading review:** Claude Opus 5.5 read the route on 2026-10-06,
  including the Terraform language and Kubernetes Service steps. Primary
  sources were checked separately; there was no new cluster run or reader
  trial in that review. Later edits to linked pages and to this page's topic
  choices were not part of that 2026-10-06 review.
- **Applicable versions:** Kubernetes and Terraform exercise versions are
  declared in their linked guides. Git behavior should be checked against
  the linked Git pages and official references for your installed version.
- **Validation evidence:** The earlier local route was source reviewed and
  statically checked. Its Kubernetes exercise ran end to end on 2026-09-19
  with Docker 29.8.0, kind v0.30.0, Kubernetes v1.34.0, and kubectl v1.34.1.
  The Terraform exercise was rerun locally with Terraform v1.13.1 on
  2026-10-06. The current Kubernetes exercise has a revised failure step that
  has not been rerun. These results do not validate the broader topic choices.
- **Known limitations:** The broader entry route and new or rewritten
  explanations have not been independently reader-tested. Many areas are
  partial; the local platform route is the only complete beginner exercise
  sequence documented here.
- **Next review:** After the planned reader sessions or by 2026-12-19.

[Back to knowledge index](index.md)
