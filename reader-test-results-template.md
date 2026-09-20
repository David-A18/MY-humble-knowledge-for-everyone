# Reader test results template

## Purpose

Use this template to record KB-14 reader-task testing without collecting unnecessary personal information.

Status: Draft
Audience: Maintainers running knowledge-base reader tests
Page type: Maintenance template
Maintainer: Unassigned
Last substantive review: 2026-09-19
Applicable versions: Use with the current [maintenance review queue](maintenance-review-queue.md)
Validation evidence: Template structure reviewed against KB-14 result fields; no reader session has been recorded yet
Known limitations: This template does not replace actual reader participation or prove findability by itself
Next review: After the first completed reader-test session

Use the [reader test facilitator guide](reader-test-facilitator-guide.md) to run the session. Copy this file for each reader-test session or paste the sections into an issue. Do not commit names, email addresses, employer details, private infrastructure details, screenshots with secrets, or terminal output containing credentials.

## Session summary

| Field | Value |
| --- | --- |
| Date | YYYY-MM-DD |
| Facilitator | Unassigned |
| Reader profile | Beginner, early practitioner, experienced engineer, or other broad category |
| Starting page | [Start here](knowledge/start-here.md) |
| Repository commit | Commit hash tested |
| Environment notes | Browser, terminal, operating system, or tool versions when relevant |
| Consent to record anonymous findings | Yes or no |

## Task results

| Task                                                                                                | Found page | Time to find | Result | Confusing term or step | Follow-up action |
| --------------------------------------------------------------------------------------------------- | ---------- | ------------ | ------ | ---------------------- | ---------------- |
| 1. Find how to undo an unstaged Git edit without rewriting shared history.                          |            |              |        |                        |                  |
| 2. Find the first local Kubernetes learning path and identify its prerequisites.                    |            |              |        |                        |                  |
| 3. Diagnose a Kubernetes workload restart using the documented route.                               |            |              |        |                        |                  |
| 4. Distinguish Crossplane provider, managed resource, XRD, Composition, and XR.                     |            |              |        |                        |                  |
| 5. Find how to validate a Velero restore before trusting it.                                        |            |              |        |                        |                  |
| 6. Choose whether Terraform or Crossplane is the better starting point for a reusable platform API. |            |              |        |                        |                  |
| 7. Find how to update kubeconfig and validate permissions before deploying to EKS.                  |            |              |        |                        |                  |
| 8. Explain when Kafka at-least-once processing can cause duplicate side effects.                    |            |              |        |                        |                  |
| 9. Identify the next step after finishing the local beginner route.                                 |            |              |        |                        |                  |
| 10. Report one confusing term, missing prerequisite, or blocked step.                               |            |              |        |                        |                  |

Use these result values consistently:

- `Completed`: the reader found the intended page and completed the task.
- `Partially completed`: the reader found useful information but needed help or missed part of the task.
- `Blocked`: the reader could not proceed because of missing, confusing, inaccurate, or unavailable information.
- `Skipped`: the task was not attempted.

## Observed blockers

| Blocker | Affected task | Evidence | Proposed follow-up |
| ------- | ------------- | -------- | ------------------ |
|         |               |          |                    |

Record repeated blockers as issues or small documentation tasks. Include the page, environment or version when relevant, expected result, and actual result.

## Terms to clarify

| Term or phrase | Page | Reader interpretation | Suggested clarification |
| -------------- | ---- | --------------------- | ----------------------- |
|                |      |                       |                         |

## Follow-up issue checklist

- [ ] Create documentation-error issues for incorrect, outdated, unclear, or broken content.
- [ ] Create improvement issues for navigation, structure, or missing learning support.
- [ ] Link repeated blockers from [maintenance review queue](maintenance-review-queue.md) if they affect priority guides.
- [ ] Update [knowledge-base improvement plan](knowledge-base-improvement-plan.md) when KB-14 acceptance evidence exists.
- [ ] Update [ROADMAP.md](ROADMAP.md) only after observed reader outcomes justify a priority change.

## Related links

- [Reader test facilitator guide](reader-test-facilitator-guide.md)
- [Maintenance review queue](maintenance-review-queue.md)
- [Knowledge-base improvement plan](knowledge-base-improvement-plan.md)
- [Contributing](CONTRIBUTING.md)
- [Back to root index](README.md)
