---
type: Explanation
title: KMS encryption and access boundaries
description: Separate transport encryption, envelope encryption, key administration,
  data use, rotation, and recovery.
tags:
- aws
- security
- kms
status: draft
maturity: draft
audience: Cloud and platform engineers
maintainer: unassigned
sources:
- id: kms-keys
  title: KMS key types
  resource: https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html
- id: kms-policy
  title: KMS key policies
  resource: https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html
- id: kms-rotate
  title: KMS key rotation
  resource: https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html
---

# KMS encryption and access boundaries

Encryption at rest, TLS in transit, and authorization solve different problems. A TLS connection can successfully deliver an authorization denial. An encrypted object can still be readable by an overprivileged principal. Select controls from the data flow and threat model, rather than treating an encryption checkbox as the complete access boundary.

## Know what a key controls

In envelope encryption, data is encrypted with a data key; KMS protects that key under a KMS key. AWS service integrations manage different details, so inspect the service's encryption configuration and context. Separate key administrators from data users where practical: managing lifecycle/policy and decrypting application data need different privileges.

| Key category | Operational choice |
| --- | --- |
| AWS owned | Service-owned key lifecycle; limited direct customer control/visibility. |
| AWS managed | Service-managed key in your account, tied to that service's supported uses. |
| Customer managed | You own policy/lifecycle and associated operating cost/responsibility. |

Use the supported key type for the actual service, cross-account requirement, and recovery policy.[^kms-keys] Customer-managed control creates a responsibility to protect access and recoverability, not an automatic security improvement.

## Follow authorization end to end

A KMS key has a regional key policy. IAM permission alone is ineffective unless the key policy enables that authorization path; key policies, IAM policies, and grants have distinct roles.[^kms-policy] For an SSE-KMS object read, check the S3 authorization path and the KMS authorization/context path separately.

```bash
aws kms describe-key --key-id <key-arn> --profile <profile> --region <region> --no-cli-pager
aws kms get-key-policy --key-id <key-arn> --policy-name default --profile <profile> --region <region> --no-cli-pager
```

What it does: inspects key state/identity and policy with separate read permissions. Confirm the Region and actual key ARN used by the data. A successful `DescribeKey` does not prove decrypt permission; policy output may contain sensitive architecture/principal information.

Where an integration supports them, service and encryption-context conditions can limit use to the intended data path. Test expected decryption and a mismatched resource/context in a disposable environment; do not copy condition keys from another service without verifying support.

## Rotation and recovery

Rotating KMS key material does not re-encrypt existing data or rotate a database password. KMS retains previous material for decryption under the same key; automatic/on-demand/manual options depend on key type and origin.[^kms-rotate] A key alias change directs supported future uses and does not migrate historical ciphertext.

Before disabling or scheduling deletion, inventory ciphertext, replicas, backups, application and disaster-recovery dependencies, recovery access, and retention. Key deletion can make retained ciphertext unrecoverable. This guide makes no key changes; cleanup for a future lab must preserve decryptability until disposable data and recovery obligations are resolved.

See [secret rotation](secrets-manager-and-rotation.md) for credential changes and [AccessDenied diagnosis](iam-access-denied-troubleshooting.md) for authorization evidence.

## Evidence and limits

Official sources reviewed on 2026-11-10. This draft records source review and local fixture checks where stated. AWS account calls, live EKS credentials, key/secret changes, detection delivery, and incident containment were not executed. CLI examples require a supported AWS CLI v2 and authorized account access; no CLI runtime version was tested in this batch.

[Back to AWS security](index.md) | [Back to AWS](../index.md)

[^kms-keys]: [KMS key types](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html)
[^kms-policy]: [KMS key policies](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)
[^kms-rotate]: [KMS key rotation](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)
