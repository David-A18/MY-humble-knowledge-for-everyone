# External evidence request checklist

## Purpose

List the outside inputs needed to finish the remaining blocked work in the [knowledge-base improvement plan](knowledge-base-improvement-plan.md).

Status: Draft
Audience: Maintainers, facilitators, and sandbox owners who can provide evidence for blocked validation work
Page type: Maintenance checklist
Maintainer: Unassigned
Last substantive review: 2026-09-19
Applicable versions: Use with the current [maintenance review queue](maintenance-review-queue.md)
Validation evidence: Markdown lint and local link validation cover this checklist; no external evidence has been supplied yet
Known limitations: This checklist does not complete KB-04 or KB-14 by itself
Next review: When AWS sandbox evidence or reader-test results are available

Use this checklist before running the Crossplane AWS S3 lab or reader-task sessions. It keeps the remaining work public-safe and prevents maintainers from inventing validation evidence.

## KB-04 AWS and Crossplane sandbox evidence

KB-04 can finish only after an authorized non-production AWS sandbox run validates the Crossplane AWS S3 lab. Track the run in [issue #1](https://github.com/David-A18/MY-humble-knowledge-for-everyone/issues/1).

### Required before the run

- An authorized sandbox, training, or disposable AWS account.
- Confirmation that no production credentials, production data, or customer-specific resources are used.
- A cost guardrail or budget owner for the sandbox account.
- A region selected for the run.
- AWS CLI credentials that are valid for the sandbox account.
- If temporary STS credentials are used, confirmation that the session token is present in the credential file.
- Local tools for the lab runner: Docker, kind, kubectl, Helm, and AWS CLI.
- Permission to create, tag, inspect, and delete the temporary S3 bucket and public-access-block configuration used by the lab.

### AWS evidence to record

Use the [Crossplane AWS S3 lab validation template](kubernetes/crossplane/aws-s3-lab-validation-template.md) or the Crossplane AWS S3 validation issue form. Record public-safe summaries only:

- Repository commit tested.
- Tool versions and installed Crossplane/provider versions.
- Confirmation that the expected sandbox identity was used, without exposing account-sensitive details when redaction is needed.
- Provider installation and health.
- ProviderConfig Secret creation without printing values.
- Bucket readiness, AWS-side verification, tag verification, and public-access-block verification.
- Credential expiry or authentication-failure symptoms if they occur.
- Cleanup proof for the S3 bucket, Kubernetes resources, local credential file, and kind cluster.
- Remaining cost risk, if any.

> [!WARNING]
> Never paste access keys, secret keys, session tokens, private account details, or credential-bearing logs into the repository or public issues.

## KB-14 reader-test evidence

KB-14 can finish only after actual readers try the documented tasks and their anonymous outcomes are recorded. Track the sessions in [issue #2](https://github.com/David-A18/MY-humble-knowledge-for-everyone/issues/2).

### Required before the sessions

- 3-5 willing readers recruited through an authorized channel.
- Broad reader profiles only, such as beginner, early practitioner, or experienced engineer.
- Agreement that the session records documentation findings, not personal performance.
- A repository commit or branch selected for the test.
- A facilitator ready to use the [reader test facilitator guide](reader-test-facilitator-guide.md).
- A copy of the [reader test results template](reader-test-results-template.md) or the reader-test results issue form.

### Reader evidence to record

Record only what is needed to improve the knowledge base:

- Date and repository commit tested.
- Broad reader profile.
- Task number.
- First useful page found.
- Approximate time to find the page.
- Result: `Completed`, `Partially completed`, `Blocked`, or `Skipped`.
- Confusing term, missing prerequisite, or blocked step.
- Follow-up action or reason no change is needed.

> [!IMPORTANT]
> Do not record names, email addresses, employer details, private infrastructure details, screenshots with secrets, or terminal output containing credentials.

## After evidence is available

1. Update the relevant article review-information blocks with the actual evidence level.
2. Update [maintenance review queue](maintenance-review-queue.md) with resolved blockers, new review reasons, or new dates.
3. Update [knowledge-base improvement plan](knowledge-base-improvement-plan.md) KB-04 or KB-14 records.
4. Update [CHANGELOG.md](CHANGELOG.md) for meaningful validation evidence or content changes.
5. Run the repository validation checks before publishing.

## Related links

- [Maintenance review queue](maintenance-review-queue.md)
- [Crossplane AWS S3 lab validation template](kubernetes/crossplane/aws-s3-lab-validation-template.md)
- [Reader test facilitator guide](reader-test-facilitator-guide.md)
- [Reader test results template](reader-test-results-template.md)
- [Knowledge-base improvement plan](knowledge-base-improvement-plan.md)
- [Back to root index](README.md)
