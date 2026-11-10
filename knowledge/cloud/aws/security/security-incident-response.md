---
type: How-to Guide
title: Respond to suspected AWS credential compromise
description: Prepare a scoped response that preserves evidence, blocks new credentials,
  constrains issued sessions, and verifies recovery.
tags:
- aws
- security
- incident-response
status: draft
maturity: draft
audience: Cloud and platform engineers
maintainer: unassigned
sources:
- id: incident
  title: AWS incident response
  resource: https://docs.aws.amazon.com/security-ir/latest/userguide/incident-response.html
- id: revoke
  title: IAM role session revocation
  resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_revoke-sessions.html
- id: trail-history
  title: CloudTrail event history
  resource: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html
- id: pod-target
  title: EKS Pod Identity target roles and caching
  resource: https://docs.aws.amazon.com/eks/latest/userguide/pod-id-assign-target-role.html
---

# Respond to suspected AWS credential compromise

Use this procedure as a starting structure for an owned runbook. An incident response must name its commander, affected accounts/workloads, containment authority, evidence owner, communication path, and recovery decision. The customer still owns application and configuration responsibilities within AWS's shared model.[^incident]

## Establish and preserve the scope

Record the suspected principal/session, source workload or human access path, time window, resources, observed operations, and business impact. Preserve relevant audit records and volatile workload evidence in controlled storage before destroying the source. Use [CloudTrail coverage](cloudtrail-and-detection.md) to distinguish absence of evidence from evidence of absence.

Separate the actor's entry path from the credentials already obtained. A compromised Pod, IAM user's key, external issuer, and human federated session need different containment. An independent recovery principal and protected evidence destination should be prepared before an incident.

## Contain both issuance and issued access

| Boundary | Response decision to own and verify |
| --- | --- |
| Compromised workload/source | Isolate or replace the source while preserving required evidence and availability. |
| New sessions | Restrict the relevant trust/association/issuer or key path, including alternate ways to regain credentials. |
| Issued role sessions | Apply supported role-session restrictions and verify denied resource operations with affected credentials. |
| Resource exposure | Constrain targeted data/resource access with reviewed scope and rollback. |
| Backing secrets | Rotate compromised credentials at the real service and verify consumer adoption and old-value rejection. |

Trust removal alone does not retract temporary credentials already issued. IAM role-session revocation uses a time-conditioned deny affecting matching older sessions, not only one attacker. Service-linked roles and Identity Center-managed role sessions have documented differences.[^revoke] Plan the legitimate-workload impact and recovery path before applying a broad control.

For Pod Identity, association edits do not immediately invalidate agent-cached credentials. Document source and optional target roles and evaluate each relevant session boundary.[^pod-target] Restarting a Pod can refresh identity configuration but cannot prove a previously copied credential has stopped working.

## Verify recovery without erasing evidence

Prove the compromised path cannot obtain new effective access; prove old-session forbidden operations are denied; prove the recovered workload uses the intended caller and meets its allowed/denied matrix. `GetCallerIdentity` alone cannot prove session containment. Check data access, persistence, policy changes and other affected accounts within the incident's actual scope.

Retain the containment policy revision, timestamps and propagation observations. Restore legitimate access deliberately after removing the source of compromise. Document what was not visible because of missing data events or retention; do not infer a clean account from one empty Event history query.[^trail-history]

## Practice and cleanup

Run a tabletop first, then an explicitly scoped disposable-account drill with synthetic resources, separate recovery access, stop conditions and rollback. Retain evidence under the incident policy; remove only task-owned drill resources after recovery is proven. This page contains no executed containment command or claim of a completed incident drill.

## Evidence and limits

Official sources reviewed on 2026-11-10. This draft records source review and local fixture checks where stated. AWS account calls, live EKS credentials, key/secret changes, detection delivery, and incident containment were not executed. CLI examples require a supported AWS CLI v2 and authorized account access; no CLI runtime version was tested in this batch.

[Back to AWS security](index.md) | [Back to AWS](../index.md)

[^incident]: [AWS incident response](https://docs.aws.amazon.com/security-ir/latest/userguide/incident-response.html)
[^revoke]: [IAM role session revocation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_revoke-sessions.html)
[^trail-history]: [CloudTrail event history](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html)
[^pod-target]: [EKS Pod Identity target roles and caching](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-assign-target-role.html)
