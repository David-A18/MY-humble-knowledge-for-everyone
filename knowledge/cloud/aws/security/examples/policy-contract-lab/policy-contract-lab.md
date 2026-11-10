---
type: Tutorial
title: Review an IRSA policy contract before AWS testing
description: Catch unintended changes to a synthetic trust and read-permission fixture, then plan validation, simulation, and live access tests.
tags: [aws, security, iam, irsa, lab]
status: draft
maturity: draft
audience: Cloud and platform engineers
maintainer: unassigned
sources:
  - id: analyzer
    title: IAM Access Analyzer policy validation
    resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html
  - id: simulator
    title: IAM policy simulator and limitations
    resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html
  - id: simulate-cli
    title: SimulateCustomPolicy CLI
    resource: https://docs.aws.amazon.com/cli/latest/reference/iam/simulate-custom-policy.html
---

# Review an IRSA policy contract before AWS testing

This exercise reviews two synthetic policies before an AWS deployment. The local checker enforces the declared fixture shape and scope. It does not implement IAM evaluation, validate a real token, query an account, or prove effective permissions.

## Prerequisites and baseline

Use Python 3.10+ and the repository checkout. The local checks use only the standard library; authoring execution used Python 3.13.17. The optional AWS steps need supported AWS CLI v2, an authorized profile/Region, and IAM simulation/Access Analyzer permissions. No AWS CLI or account walkthrough was executed in this batch.

The [trust fixture](irsa-trust.json) binds synthetic account `123456789012`, one EKS issuer, audience `sts.amazonaws.com`, and subject `system:serviceaccount:irsa-lab:s3-reader`. The [permission fixture](read-policy.json) grants only `s3:GetObject` on `example-lab-bucket/public-lab/*`. These identifiers are teaching fixtures, not account resources to assume exist.

## Check IRSA subjects and S3 object prefixes locally

The local policy-contract checks catch accidental broadening of IRSA subjects, audiences, and S3 object prefixes. A passing contract is fixture-regression evidence; AWS authorization needs the separate validation and access tests below.

```bash
python knowledge/cloud/aws/security/examples/policy-contract-lab/check-contracts.py
python knowledge/cloud/aws/security/examples/policy-contract-lab/test-contracts.py
```

What it does: checks the two fixture contracts and runs ten mutation tests. Expected output includes `Both fixture contracts pass` and a successful ten-test result. Neither command reads credentials or performs network requests. JSON field ordering is tolerated; duplicate keys, unexpected fields/statements, changed actions, broadened prefixes/principals, missing claims, and changed trust operators are rejected.

For a learning change, copy the directory to a task-owned scratch location. Change `public-lab/*` to `public-lab*` and run `check-contracts.py --directory <scratch-directory>`. Expect a failure: the changed prefix can include unintended names. Change the audience to `pods.eks.amazonaws.com` and expect a trust-contract failure. Restore the fixtures and verify the baseline passes. These checks intentionally reject other valid IAM policy structures because they enforce this exercise's narrow contract.

## Validate with AWS services separately

Run from the repository root. These optional commands contact AWS, but do not attach policies or perform the simulated S3 operation. Keep review outputs private if you adapt fixtures to real infrastructure.

```bash
aws accessanalyzer validate-policy --policy-document file://knowledge/cloud/aws/security/examples/policy-contract-lab/read-policy.json --policy-type IDENTITY_POLICY --profile <profile> --region <region> --no-cli-pager
aws accessanalyzer validate-policy --policy-document file://knowledge/cloud/aws/security/examples/policy-contract-lab/irsa-trust.json --policy-type RESOURCE_POLICY --validate-policy-resource-type AWS::IAM::AssumeRolePolicyDocument --profile <profile> --region <region> --no-cli-pager
```

What it does: submits the policy documents for AWS syntax/best-practice findings. Review errors and security warnings, plus other findings; an empty list is not proof of intended access. Custom checks for new access are a separate feature with pricing, not implicitly part of this exercise.[^analyzer]

```bash
aws iam simulate-custom-policy --policy-input-list file://knowledge/cloud/aws/security/examples/policy-contract-lab/read-policy.json --action-names s3:GetObject s3:PutObject --resource-arns arn:aws:s3:::example-lab-bucket/public-lab/sample.txt arn:aws:s3:::example-lab-bucket/private/sample.txt --profile <profile> --no-cli-pager
```

What it does: simulates each action/resource combination against the supplied identity policy.[^simulate-cli] Expected `EvalDecision` values for this isolated policy are:

| Action | Resource suffix | Expected simulation |
| --- | --- | --- |
| GetObject | public-lab/sample.txt | allowed |
| GetObject | private/sample.txt | implicitDeny |
| PutObject | public-lab/sample.txt | implicitDeny |
| PutObject | private/sample.txt | implicitDeny |

This simulation omits real role trust, bucket/KMS/endpoint/organization configuration and does not test a JWT exchange. AWS simulator coverage and supported context differ from live enforcement; do not generalize this matrix into an account-wide authorization claim.[^simulator]

## Complete the live acceptance

Use the existing [EKS S3 lab](../../../../../cross-topic-guides/irsa-s3-access-on-eks.md) with actual task-owned identifiers and reviewed policies. Record the expected and observed caller, successful read, denied write, and rejected alternate service-account subject. Pre-create any negative-read target so a missing-object error cannot masquerade as denial. Test customer-managed KMS and cross-account paths separately if included in your real design.

A future general IAM sandbox should also test an applicable explicit deny against an allow, a restrictive boundary/session policy, missing context, and recovery access. The local fixture checker deliberately makes no claim about those evaluations. Keep these evidence levels separate in the report: local contract, AWS policy findings, AWS simulation, live credential exchange, and actual service authorization.

## Cleanup and troubleshooting

The local checker changes no files. Tests can create ignored bytecode caches. Remove only your scratch copy or redirected reports after keeping desired evidence. AWS validation/simulation creates no attached IAM policy or S3 object; the live EKS lab has its own cleanup. Never delete shared providers, roles, buckets, or credentials based on a fixture name.

A contract failure means this fixture changed; inspect the diff. An AWS validation finding needs its own explanation. A simulation mismatch needs the exact supplied policy/context. A live denial or unexpected success needs [AccessDenied diagnosis](../../iam-access-denied-troubleshooting.md), not a broader wildcard grant.

## Evidence and limits

Official sources reviewed on 2026-11-10. Ten local mutation tests and the baseline checker were executed with Python 3.13.17; AWS validation, simulation, role assumption and resource access were not executed. Hosted workflow results must be checked for the exact published revision.

[Back to this lab](index.md) | [Back to examples](../index.md) | [Back to AWS security](../../index.md)

[^analyzer]: [IAM Access Analyzer policy validation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html).
[^simulator]: [IAM policy simulator and limitations](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html).
[^simulate-cli]: [SimulateCustomPolicy CLI](https://docs.aws.amazon.com/cli/latest/reference/iam/simulate-custom-policy.html).
