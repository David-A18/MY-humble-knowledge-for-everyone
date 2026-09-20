---
type: "Explanation"
title: "Crossplane AWS S3 lab validation template"
description: "Record an authorized sandbox execution of the [Crossplane local AWS S3 lab](local-aws-s3-lab.md) without committing credentials, account-sensitive output, or private infrastructure details."
tags: [kubernetes, crossplane, aws-s3-lab-validation-template]
status: draft
maturity: draft
audience: "Maintainers validating Crossplane AWS authentication guidance"
maintainer: unassigned
---

# Crossplane AWS S3 lab validation template

## Purpose

Record an authorized sandbox execution of the [Crossplane local AWS S3 lab](local-aws-s3-lab.md) without committing credentials, account-sensitive output, or private infrastructure details.

Status: Draft
Audience: Maintainers validating Crossplane AWS authentication guidance
Page type: Validation template
Maintainer: Unassigned
Last substantive review: 2026-09-19
Applicable versions: Use with the Crossplane local AWS S3 lab and installed provider versions under test
Validation evidence: Template structure reviewed against KB-04 acceptance criteria; no sandbox execution has been recorded in this file
Known limitations: This template does not prove the lab works until a maintainer records an authorized sandbox run
Next review: After the first authorized sandbox execution

Copy this template into a private-safe issue, pull request note, or implementation record before running the lab. Redact account IDs when appropriate, never paste access keys or session tokens, and delete local credential files during cleanup.

## Sandbox scope

| Field | Value |
| --- | --- |
| Date | YYYY-MM-DD |
| Executor | Unassigned |
| AWS account type | Sandbox, training, or other non-production account |
| AWS region | To record |
| Cost guardrail checked | Yes or no |
| Cleanup owner | To record |
| Repository commit | To record |

## Tool and package versions

| Component | Version or evidence |
| --- | --- |
| AWS CLI | `aws --version` |
| Docker | `docker version` |
| kind | `kind version` |
| kubectl | `kubectl version --client=true` |
| Helm | `helm version --short` |
| Kubernetes server | `kubectl version` after cluster creation |
| Crossplane Helm chart | `helm list -n crossplane-system` |
| Crossplane core | `kubectl get deployment crossplane -n crossplane-system -o jsonpath='{.spec.template.spec.containers[0].image}'` |
| AWS S3 provider package | `kubectl get providers.pkg.crossplane.io provider-aws-s3 -o yaml` |
| Provider revision | `kubectl get providerrevisions.pkg.crossplane.io` |

## Identity and credential checks

Run identity checks without printing secret values.

```bash
aws sts get-caller-identity
aws configure list
```

Record only public-safe facts:

| Check | Result |
| --- | --- |
| Expected sandbox account confirmed | To record |
| Temporary credentials used | Yes or no |
| Session token present for STS credentials | Yes or no |
| Credentials file permission set to `600` | Yes or no |
| Credential file excluded from Git | Yes or no |
| Secret created without printing values | Yes or no |

## Execution checklist

| Step | Command or evidence | Result |
| --- | --- | --- |
| Create local kind cluster | `kind create cluster --name crossplane-lab` | To record |
| Install Crossplane | `helm install crossplane ...` | To record |
| Confirm Crossplane readiness | `kubectl get pods -n crossplane-system` | To record |
| Install AWS S3 provider | `kubectl apply -f provider-aws-s3.yaml` | To record |
| Confirm provider health | `kubectl get providers.pkg.crossplane.io` | To record |
| Create AWS credential Secret | `kubectl create secret generic aws-secret ...` | To record |
| Apply provider config | `kubectl apply -f provider-config.yaml` | To record |
| Server-side dry-run bucket | `kubectl apply --dry-run=server -f bucket.yaml` | To record |
| Apply bucket | `kubectl apply -f bucket.yaml` | To record |
| Observe Crossplane readiness | `kubectl get bucket.s3.aws.m.upbound.io ...` | To record |
| Verify bucket in AWS | `aws s3api head-bucket --bucket ...` | To record |
| Apply public-access block | `kubectl apply -f bucket-public-access.yaml` | To record |
| Verify tags and public access block | `aws s3api get-bucket-tagging ...` and `aws s3api get-public-access-block ...` | To record |
| Test drift correction | Record the safe drift action and reconciliation result | To record |
| Delete managed resources | `kubectl delete -f ...` | To record |
| Confirm AWS bucket deletion | `aws s3api head-bucket --bucket ...` should fail after cleanup | To record |
| Delete Secret and credential file | Record cleanup without printing values | To record |
| Delete local cluster | `kind delete cluster --name crossplane-lab` | To record |

## Expected evidence snippets

Record short public-safe summaries, not full secret-bearing output.

```text
Provider installed:
Provider healthy:
Bucket Ready condition:
AWS head-bucket result:
Public access block result:
Drift test result:
Cleanup result:
```

## Failure and expiry checks

Use this section if the lab fails or credentials expire during the run.

| Symptom | Evidence | Likely cause | Follow-up |
| --- | --- | --- | --- |
| Provider authentication error | To record | Missing or expired session token, wrong Secret key, or wrong provider config | To record |
| Provider unhealthy | To record | Package pull, revision, runtime, or permission issue | To record |
| Bucket not ready | To record | AWS permission, region, naming, or provider schema issue | To record |
| Cleanup incomplete | To record | Finalizers, bucket contents, or credential loss | To record |

## Cleanup proof

| Resource | Cleanup evidence |
| --- | --- |
| S3 bucket | To record |
| Bucket public access block | To record |
| Crossplane managed resources | To record |
| Kubernetes Secret | To record |
| Local credential file | To record |
| kind cluster | To record |
| Remaining AWS cost risk | None known, or describe follow-up |

## Publication update

After a successful run, update:

- [Crossplane local AWS S3 lab](local-aws-s3-lab.md) review-information block.
- [Crossplane providers and authentication](providers-and-authentication.md) review-information block if authentication behavior was validated.
- [Knowledge-base improvement plan](../../../knowledge-base-improvement-plan.md) KB-04 record.
- [Maintenance review queue](../../../maintenance-review-queue.md) if the blocked evidence is resolved.
- [CHANGELOG.md](../../../CHANGELOG.md) for the validation evidence update.

## Related links

- [Crossplane local AWS S3 lab](local-aws-s3-lab.md)
- [Crossplane providers and authentication](providers-and-authentication.md)
- [Maintenance review queue](../../../maintenance-review-queue.md)
- [Knowledge-base improvement plan](../../../knowledge-base-improvement-plan.md)
- [Back to Crossplane index](index.md)
- [Back to Kubernetes index](../index.md)
- [Back to root index](../../../README.md)
