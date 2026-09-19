# Maintenance review queue

## Purpose

Track priority article reviews, blocked validation work, and reader-task testing for the knowledge base.

Status: Draft
Audience: Maintainers and contributors planning review work
Page type: Maintenance queue
Maintainer: Unassigned
Last substantive review: 2026-09-19
Applicable versions: Current repository state recorded in the [knowledge-base improvement plan](knowledge-base-improvement-plan.md)
Validation evidence: Markdown lint and local link validation passed for the queue introduction and external-evidence checklist batches
Known limitations: Reader trials have not started, and cloud, Crossplane, Velero, EKS, and broker integration checks still need suitable environments
Next review: When KB-14 reader testing starts, or by 2026-10-19

Use this queue with the [knowledge-base improvement plan](knowledge-base-improvement-plan.md). The plan defines acceptance criteria and records completed work packages. This queue is the working list for recurring maintenance and reader testing.

Use the [external evidence request checklist](external-evidence-request.md) to identify missing outside inputs, the [reader test facilitator guide](reader-test-facilitator-guide.md) to run sessions, and the [reader test results template](reader-test-results-template.md) or reader-test GitHub issue form to record results.

## How to use this queue

1. Pick an article whose next review date is due, whose upstream product changed, or whose blocked evidence is now available.
2. Read the article, parent index, [instructions](instructions.md), and any related official sources before editing.
3. Update the article's review-information block with the actual evidence level: source reviewed, statically checked, locally executed, or sandbox executed.
4. Record reader feedback or execution results in the article, plan record, changelog, or a linked issue as appropriate.
5. Keep personal reader details out of the repository. Record only the information needed to improve the documentation.

## Priority operational guide queue

| Guide | Owner | Next review | Reason | Current evidence | Open evidence |
| --- | --- | --- | --- | --- | --- |
| [Git undo and recovery](git/troubleshooting/undo-and-recovery.md) | Unassigned | 2026-12-19 | Safety-critical recovery guidance | Source reviewed against official Git documentation and locally reproduced in a disposable repository | Broader conflict, sparse-checkout, and submodule scenarios |
| [Crossplane local AWS S3 lab](kubernetes/crossplane/local-aws-s3-lab.md) | Unassigned | After sandbox AWS execution or 2026-12-19 | Real cloud resources and credentials | Crossplane and AWS STS source review plus [validation template](kubernetes/crossplane/aws-s3-lab-validation-template.md) | Live kind, Crossplane, provider, and AWS sandbox run |
| [Crossplane providers and authentication](kubernetes/crossplane/providers-and-authentication.md) | Unassigned | 2026-12-19 | Credential and provider behavior changes quickly | Crossplane v2.4 source review | Provider-controller authentication execution |
| [Terraform core workflow](terraform/commands/core-workflow.md) | Unassigned | 2026-12-19 | Core workflow used by learners | Terraform source review and local exercise execution | Remote backend, cloud provider, and policy behavior |
| [Terraform state management](terraform/fundamentals/state-management.md) | Unassigned | 2026-12-19 | State guidance is operationally sensitive | Terraform source review and local exercise execution | Backend-specific locking, drift, and recovery drills |
| [Kafka delivery guarantees and failure handling](databases/kafka/delivery-guarantees-and-failure-handling.md) | Unassigned | After broker-backed execution or 2026-12-19 | Messaging behavior needs runtime evidence | Kafka and kafka-python source review plus static Python syntax check | Broker-backed producer, consumer, retry, and replay tests |
| [Velero AWS S3 and EBS installation](migrations/velero/aws-s3-ebs-installation.md) | Unassigned | After sandbox EKS installation or 2026-12-19 | Backup tooling and AWS permissions | Velero, AWS plugin, and EKS source review | Live EKS, S3, EBS CSI, snapshot controller, and IAM execution |
| [Velero backup and restore workflows](migrations/velero/backup-restore-workflows.md) | Unassigned | After cluster-backed restore drill or 2026-12-19 | Restore commands must match reality | Velero source review | Live backup, schedule, restore, namespace mapping, and cleanup drill |
| [Velero migration and disaster recovery](migrations/velero/cluster-migration-and-disaster-recovery.md) | Unassigned | After cross-cluster restore drill or 2026-12-19 | Migration and DR claims need proof | Velero migration and restore source review | Source and destination clusters, shared storage, and application restore drill |
| [Deploying to EKS](cross-topic-guides/deploying-to-eks.md) | Unassigned | After sandbox EKS deployment or 2026-12-19 | Production-impact workflow | Amazon EKS and Kubernetes source review | Live kubeconfig, authorization, diff, apply, rollout, and rollback drill |

## Reader-task testing queue

KB-14 requires actual reader testing. Do not mark it complete until willing readers have run tasks and the results are recorded without unnecessary personal data.

### Participant criteria

Recruit 3-5 willing readers through an authorized channel. Aim for readers who want to learn practical platform, cloud, or DevOps work and who can use a terminal safely. Record experience level broadly, such as beginner, early practitioner, or experienced engineer.

### Test tasks

Ask each reader to start from [Start here](start-here.md) and answer or complete these tasks. The [reader test facilitator guide](reader-test-facilitator-guide.md) provides the session script, expected routes, scoring rules, and hint rules.

1. Find how to undo an unstaged Git edit without rewriting shared history.
2. Find the first local Kubernetes learning path and identify its prerequisites.
3. Diagnose a Kubernetes workload restart using the documented route.
4. Distinguish Crossplane provider, managed resource, XRD, Composition, and XR.
5. Find how to validate a Velero restore before trusting it.
6. Choose whether Terraform or Crossplane is the better starting point for a reusable platform API.
7. Find how to update kubeconfig and validate permissions before deploying to EKS.
8. Explain when Kafka at-least-once processing can cause duplicate side effects.
9. Identify the next step after finishing the local beginner route.
10. Report one confusing term, missing prerequisite, or blocked step.

### Result fields

Record only the fields needed for documentation improvement:

| Field | Use |
| --- | --- |
| Date | When the test happened. |
| Reader profile | Broad experience level only. |
| Task number | Which task was attempted. |
| Found page | Page the reader used. |
| Time to find | Approximate time, rounded to the nearest minute. |
| Result | Completed, partially completed, blocked, or skipped. |
| Confusing term or step | The smallest phrase or step that caused trouble. |
| Follow-up action | Issue, edit, or no change with reason. |

## Current blockers

- KB-04 needs authorized AWS and Crossplane sandbox execution before the temporary-credential path can be called fully validated; use the [external evidence request checklist](external-evidence-request.md) before the run, then use the [AWS S3 lab validation template](kubernetes/crossplane/aws-s3-lab-validation-template.md) or the Crossplane AWS S3 validation issue form to record the run.
- KB-14 needs actual reader participation; author testing is useful but does not satisfy reader-trial acceptance. Use the external evidence request checklist before recruiting readers, then use the reader-test facilitator guide to run sessions and the reader-test results template or reader-test GitHub issue form to record sessions.
- KB-15 is recorded in [ADR-0003](decision-records/adr-0003-searchable-site-decision.md): keep repository navigation as the canonical surface for now and reopen the static-site question after KB-14 produces reader evidence.

## Related links

- [External evidence request checklist](external-evidence-request.md)
- [Reader test facilitator guide](reader-test-facilitator-guide.md)
- [Reader test results template](reader-test-results-template.md)
- [Knowledge-base improvement plan](knowledge-base-improvement-plan.md)
- [Knowledge-base review](knowledge-base-review.md)
- [Contributing](CONTRIBUTING.md)
- [AI documentation instructions](instructions.md)
- [Roadmap](ROADMAP.md)
- [Back to root index](README.md)
