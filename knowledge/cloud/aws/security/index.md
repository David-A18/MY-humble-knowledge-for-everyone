# AWS security

Learn AWS identity and permissions first, then protect data, establish evidence, and practice recovery. This section contains source-reviewed drafts and local synthetic policy contracts; account-backed authorization and operations remain explicit follow-ups.

## Learning and operational routes

| Goal | Route |
| --- | --- |
| Understand effective permissions | [IAM policy evaluation and least privilege](iam-policy-evaluation-and-least-privilege.md) — Trust, grants, restrictive controls, and principal-specific behavior. |
| Establish actual caller and refresh | [Credential providers and sessions](credential-providers-and-session-lifecycle.md) — SDK precedence, token/session lifetime, and revocation boundaries. |
| Understand external federation | [OIDC provider and STS web identity](iam-oidc-provider-and-sts-web-identity.md) — Issuer registration and the credential exchange. |
| Learn IRSA | [Fundamentals](irsa-fundamentals.md), [trust and permissions](irsa-trust-and-permissions.md), [troubleshooting](irsa-troubleshooting.md). |
| Operate EKS associations | [Pod Identity operations](eks-pod-identity-operations.md) — Agent path, compute support, target roles and caches. |
| Protect encrypted data | [KMS boundaries](kms-encryption-and-access.md) — Key policy, data use, rotation and recovery. |
| Deliver and rotate application credentials | [Secrets Manager](secrets-manager-and-rotation.md) — Store selection, consumer refresh and rotation acceptance. |
| Establish audit/detection evidence | [CloudTrail and detection](cloudtrail-and-detection.md) — Management/data events, GuardDuty and Security Hub CSPM. |
| Investigate a failure | [AccessDenied diagnosis](iam-access-denied-troubleshooting.md) — Credential/trust/authorization stages and minimal correction. |
| Respond to compromised access | [Incident response](security-incident-response.md) — Evidence, new-session containment, issued-session controls and recovery. |
| Practice safely | [Examples](examples/index.md) — Local fixture contracts, AWS validation/simulation, and the live acceptance handoff. |

## Related sections

- [EKS identity comparison](../../../cross-topic-guides/eks-workload-identity.md) remains the choice entry point; the [IRSA S3 lab](../../../cross-topic-guides/irsa-s3-access-on-eks.md) defines allowed/denied checks.
- [AWS networking](../networking/index.md) covers endpoint/DNS and transport paths.
- [Kubernetes secret delivery](../../../kubernetes/applications-and-tools/platform-tooling/secret-management.md) covers platform delivery choices.
- [Governance and human access](../governance-and-access/index.md) covers account/OU design, federation, permission sets, organization guardrails, delegated IAM, root/emergency access and offboarding; its synthetic inventory evidence remains separate from live authorization.

## Evidence still needed

Run authorized IAM/IRSA/Pod Identity positive and negative tests, KMS/context and secret-consumer rotation drills, actual audit/notification delivery, and a controlled session-containment/recovery drill. Add independent review and ownership before promoting drafts. See the [section ledger](../../../../section-quality-progress.md) for precise scope and follow-ups.

[Back to AWS](../index.md) | [Back to knowledge](../../../index.md)
