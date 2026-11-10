---
type: Explanation
title: IAM OIDC provider and STS web identity
description: Understand issuer registration, token validation, role trust, temporary
  credentials, and the separate AWS authorization step.
tags:
- aws
- security
- iam
status: draft
maturity: draft
audience: Cloud and platform engineers
maintainer: unassigned
sources:
- id: web-identity
  title: STS AssumeRoleWithWebIdentity
  resource: https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithWebIdentity.html
- id: irsa
  title: IRSA security model
  resource: https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html
- id: irsa-sdk
  title: IRSA SDK integration
  resource: https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts-minimum-sdk.html
---

# IAM OIDC provider and STS web identity

An external OIDC issuer signs identity assertions. An IAM OIDC provider is the account-side representation of an issuer; creating it does not grant every token a role. A role's trust policy then limits which validated assertions may assume that role, and the role's permissions control later AWS operations.

## Follow the exchange

| Component | Responsibility |
| --- | --- |
| Issuer and signing keys | Publish discovery/key material and issue signed tokens. |
| Token claims | Carry issuer, audience, subject and validity information. |
| IAM OIDC provider | Register the trusted issuer and configured audiences in the relevant account. |
| Role trust | Permit the web-identity action only for intended provider and conditions. |
| STS exchange | Validate the token/trust and return temporary AWS credentials. |
| Service authorization | Evaluate the subsequent signed request under applicable policies. |

`AssumeRoleWithWebIdentity` uses the external token rather than requiring a pre-existing AWS access key. Its response contains temporary AWS credentials; do not publish either the input token or response.[^web-identity] Decoding a JWT's payload is not signature verification or proof that IAM accepts it.

## Apply the model to EKS

IRSA uses the cluster's issuer and projected service-account tokens. Narrow trust includes the actual issuer, `aud` and exact Kubernetes `sub`; a service-account annotation is only one integration component. Projected tokens have an audience and expiry, unlike legacy indefinitely valid service-account tokens.[^irsa]

The supported SDK performs token exchange and refresh through its provider chain. Credentials earlier in the selected chain can mask IRSA.[^irsa-sdk] See [credential lifecycle](credential-providers-and-session-lifecycle.md) rather than copying a token into a long-lived environment variable.

## Operate the boundaries

Keep issuer/key discovery, the operator's DNS/network path, and workload STS connectivity distinct. Inspect the currently documented EKS private-endpoint/resolver options; private networking is not solved by assuming every public issuer is unreachable. Do not loosen token trust to work around a DNS failure.

Use [IRSA trust](irsa-trust-and-permissions.md) for the exact policy example and [EKS workload identity](../../../cross-topic-guides/eks-workload-identity.md) for Pod Identity comparison. Other OIDC federation routes, such as [GitHub Actions](../../../git/github-actions/aws-oidc-federation.md), require their own subjects and controls. Reusing the EKS subject format for another issuer is incorrect.

## Evidence and limits

Official sources reviewed on 2026-11-10. This draft records source review and local fixture checks where stated. AWS account calls, live EKS credentials, key/secret changes, detection delivery, and incident containment were not executed. CLI examples require a supported AWS CLI v2 and authorized account access; no CLI runtime version was tested in this batch.

[Back to AWS security](index.md) | [Back to AWS](../index.md)

[^web-identity]: [STS AssumeRoleWithWebIdentity](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithWebIdentity.html)
[^irsa]: [IRSA security model](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html)
[^irsa-sdk]: [IRSA SDK integration](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts-minimum-sdk.html)
