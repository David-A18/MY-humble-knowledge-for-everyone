# Reader test facilitator guide

## Purpose

Run KB-14 reader-task sessions consistently, safely, and without collecting unnecessary personal information.

Status: Draft
Audience: Maintainers facilitating knowledge-base reader tests
Page type: Maintenance guide
Maintainer: Unassigned
Last substantive review: 2026-09-19
Applicable versions: Use with the current [maintenance review queue](maintenance-review-queue.md) and [reader test results template](reader-test-results-template.md)
Validation evidence: Guide structure reviewed against KB-14 acceptance criteria; no reader session has been recorded yet
Known limitations: This guide prepares reader testing but does not replace actual reader participation
Next review: After the first completed reader-test session

Use this guide with [Start here](start-here.md), the [maintenance review queue](maintenance-review-queue.md), and the [reader test results template](reader-test-results-template.md). The goal is to learn where readers get lost, which terms confuse them, and which tasks cannot be completed from the current navigation.

## Facilitator rules

- Recruit 3-5 willing readers through an authorized channel.
- Record broad experience level only: beginner, early practitioner, experienced engineer, or another general category.
- Do not record names, email addresses, employers, private infrastructure details, screenshots with secrets, access tokens, or credential-bearing terminal output.
- Ask readers to start from [Start here](start-here.md) unless a task says otherwise.
- Let the reader search and navigate naturally before giving hints.
- Record the first page they used for an answer, not the page you expected them to use.
- Treat confusion as product evidence, not as reader failure.

## Before the session

1. Choose the repository commit or branch the reader will test.
2. Open a fresh copy of the [reader test results template](reader-test-results-template.md) or prepare the reader-test issue form.
3. Confirm the reader knows the session is about improving the documentation.
4. Explain that they can stop or skip a task at any time.
5. Ask them to think aloud while searching, but do not ask for private work context.
6. Start a timer for each task when the reader begins looking for the answer.

## Standard prompt

Use this short prompt at the start of each session:

```text
We are testing whether this knowledge base helps people find practical answers.
Start from the Start here page. For each task, say what page you found, what you would do next, and anything confusing. You can skip any task. Please do not share secrets, customer details, employer names, or private infrastructure information.
```

What it does: keeps the session focused on documentation behavior and privacy before any task begins.

## Task script and expected routes

The expected route is not a grading key. If a reader reaches a different useful page, record that route and decide later whether navigation should change.

| Task | Reader prompt | Expected route or evidence | Completion signal |
| --- | --- | --- | --- |
| 1 | Find how to undo an unstaged Git edit without rewriting shared history. | [Git undo and recovery](git/troubleshooting/undo-and-recovery.md) or [Git issue-solving commands](git/commands/solve-issues.md) | Reader identifies `git restore <file>` for an unstaged working-tree edit and avoids history rewrite commands. |
| 2 | Find the first local Kubernetes learning path and identify its prerequisites. | [Start here](start-here.md) to [Local deployment learning path](cross-topic-guides/local-deployment-learning-path.md) | Reader names the local Kubernetes path and its required tools. |
| 3 | Diagnose a Kubernetes workload restart using the documented route. | [Kubernetes troubleshooting](kubernetes/troubleshooting/README.md), [daily kubectl usage](kubernetes/commands/daily-usage.md), or [Kubernetes workflows](kubernetes/commands/workflows.md) | Reader finds inspection commands such as `kubectl get pods`, `kubectl describe pod`, logs, events, or rollout status. |
| 4 | Distinguish Crossplane provider, managed resource, XRD, Composition, and XR. | [Crossplane component model](kubernetes/crossplane/component-model.md) or [XRDs, Compositions, and XR calls](kubernetes/crossplane/xrd-composition-and-xr-calls.md) | Reader can describe each component in their own words. |
| 5 | Find how to validate a Velero restore before trusting it. | [Velero backup and restore workflows](migrations/velero/backup-restore-workflows.md) | Reader finds restore inspection, logs, describe commands, workload checks, or restore drill guidance. |
| 6 | Choose whether Terraform or Crossplane is the better starting point for a reusable platform API. | [Terraform vs Crossplane](kubernetes/crossplane/terraform-vs-crossplane.md) | Reader identifies the decision criteria and chooses a direction with a reason. |
| 7 | Find how to update kubeconfig and validate permissions before deploying to EKS. | [Deploying to EKS](cross-topic-guides/deploying-to-eks.md) or [EKS operations](cross-topic-guides/eks-operations.md) | Reader finds kubeconfig update and authorization or access checks before deployment. |
| 8 | Explain when Kafka at-least-once processing can cause duplicate side effects. | [Kafka delivery guarantees and failure handling](databases/kafka/delivery-guarantees-and-failure-handling.md) | Reader explains that processing can succeed while offset commit fails, causing replay and duplicate side effects unless handlers are idempotent. |
| 9 | Identify the next step after finishing the local beginner route. | [Start here](start-here.md) or [Local deployment learning path](cross-topic-guides/local-deployment-learning-path.md) | Reader finds a next topic such as Terraform, Kubernetes troubleshooting, Crossplane, EKS, or Velero. |
| 10 | Report one confusing term, missing prerequisite, or blocked step. | Any page used during the session | Reader provides a specific term, instruction, prerequisite, or navigation step to improve. |

## Scoring rules

Use these values consistently in the results template:

- `Completed`: the reader found enough information to answer or complete the task without facilitator help.
- `Partially completed`: the reader found useful information but needed a hint, missed a safety condition, or could not explain part of the answer.
- `Blocked`: the reader could not proceed because navigation, terminology, prerequisites, commands, or accuracy stopped them.
- `Skipped`: the task was not attempted.

Record approximate time to find the first useful page. Round to the nearest minute. For very quick successes, use `<1 minute`.

## When to help

Let the reader search for up to two minutes before offering a neutral hint. A neutral hint names an area, not the answer.

Examples:

- “Try starting from the Kubernetes area.”
- “Look for the troubleshooting index.”
- “Check the Crossplane section.”

If a hint changes the result, mark the task `Partially completed` and record the hint in the confusing step or follow-up field.

## Turning results into work

After each session:

1. Remove any accidental personal or secret-bearing details from notes.
2. Copy the results into the [reader test results template](reader-test-results-template.md) or issue form.
3. Group repeated blockers by page, term, prerequisite, or navigation path.
4. Create small documentation-error or improvement issues for repeated blockers.
5. Update [maintenance review queue](maintenance-review-queue.md) if a priority guide needs a new review reason or earlier next review.
6. Update [knowledge-base improvement plan](knowledge-base-improvement-plan.md) only when actual KB-14 acceptance evidence exists.
7. Update [ROADMAP.md](ROADMAP.md) only when observed reader outcomes justify a priority change.

## Related links

- [Reader test results template](reader-test-results-template.md)
- [Maintenance review queue](maintenance-review-queue.md)
- [Knowledge-base improvement plan](knowledge-base-improvement-plan.md)
- [Contributing](CONTRIBUTING.md)
- [Back to root index](README.md)
