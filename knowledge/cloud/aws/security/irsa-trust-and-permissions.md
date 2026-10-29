---
type: Explanation
title: IRSA trust and permission policies
description: Separate who may assume a role from what an assumed role may do.
tags:
- cloud
- security
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: associate-service-account-and-iam-role
  resource: https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html
  title: Associate service account and IAM role
- id: sts-web-identity
  resource: https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithWebIdentity.html
  title: STS web identity
- id: iam-policy-evaluation
  resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html
  title: IAM policy evaluation
---

# IRSA trust and permission policies

## Purpose

Separate who may assume a role from what an assumed role may do.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Two independent policies

The role trust policy permits STS web-identity role assumption from a specific federated issuer, token audience, namespace, and service account. The role permission policy allows AWS operations against resources. Both must succeed. Organization SCPs, permission boundaries, resource policies, and KMS policies can further restrict effective permissions.[^associate-service-account-and-iam-role][^sts-web-identity][^iam-policy-evaluation]

## Narrow trust example

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Federated": "arn:aws:iam::123456789012:oidc-provider/oidc.eks.eu-west-1.amazonaws.com/id/REPLACE"},
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "oidc.eks.eu-west-1.amazonaws.com/id/REPLACE:aud": "sts.amazonaws.com",
        "oidc.eks.eu-west-1.amazonaws.com/id/REPLACE:sub": "system:serviceaccount:irsa-lab:s3-reader"
      }
    }
  }]
}
```

What it does: binds one issuer to one workload identity. Replace the example account and issuer with actual values. Condition keys omit `https://`. Different partitions and regions require the appropriate ARN and issuer.

## Minimal object permission

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::YOUR-LAB-BUCKET/public-lab/*"
  }]
}
```

What it does: permits reading one prefix. It does not permit listing the bucket or writing/deleting objects. Encrypted objects may additionally require narrowly scoped KMS decryption rights and key-policy access.

## Design checks

Use exact subjects instead of namespace-wide wildcards unless a reviewed requirement justifies sharing. Keep one role per practical permission boundary. Check cross-account trust and resource policy separately; trusting an issuer does not automatically authorize an S3 bucket in another account.

Credential revocation and policy propagation are not instantaneous. Changing trust prevents future assumptions but already-issued sessions may persist within their applicable controls and lifetime. Plan incident response accordingly.

## Diagnostic sequence

Confirm the cluster's actual issuer, IAM OIDC provider, annotation, audience, and token subject. Then inspect the attached permission policy and resource/KMS restrictions. An STS denial belongs to the trust path; a later S3 denial belongs to authorization or the resource configuration.

## Related links

- [Associate service account and IAM role](https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html)
- [STS web identity](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithWebIdentity.html)
- [IAM policy evaluation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^associate-service-account-and-iam-role]: [Associate service account and IAM role](https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html).
[^sts-web-identity]: [STS web identity](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithWebIdentity.html).
[^iam-policy-evaluation]: [IAM policy evaluation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html).
