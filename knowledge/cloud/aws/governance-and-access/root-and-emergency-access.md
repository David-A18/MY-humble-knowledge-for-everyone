---
type: How-to Guide
title: Plan root and emergency access recovery
description: Prepare a tested recovery path that distinguishes management-root credentials,
  centralized member-root tasks, and federation outages.
tags:
- aws
- governance
- human-access
status: draft
maturity: draft
audience: Cloud administrators and platform engineers
maintainer: unassigned
sources:
- id: root-practices
  title: Root user security practices
  resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html
- id: root-central
  title: Centralized member-account root access
  resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-enable-root-access.html
- id: assume-root
  title: STS AssumeRoot
  resource: https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoot.html
- id: emergency
  title: Emergency access design
  resource: https://docs.aws.amazon.com/singlesignon/latest/userguide/emergency-access.html
---

# Plan root and emergency access recovery

Begin with the failure you need to survive: a lost ordinary role, Identity Center disruption, external-IdP outage, organization-policy lockout, or a task requiring root capabilities. These are different recovery problems. An emergency role must be available under its intended failure conditions, with owned credential custody, multi-person activation where appropriate, monitoring and return-to-normal steps.

## Separate root cases

Management/standalone-account root credentials need protected recovery channels, strong authentication/MFA where credentials exist, no routine access keys, and restricted use for tasks requiring root.[^root-practices] Do not turn root into the daily administrator simply because a normal assignment is broken.

With centralized root access, eligible member accounts can have root credentials removed and password recovery prevented; newly created member accounts in the enabled model need not have root credentials by default.[^root-central] A blanket checklist saying every member account must retain a password/MFA recovery kit is therefore wrong. Record which model actually applies, and protect the management/delegated-administrator authority that controls it.

`AssumeRoot` provides short-lived, task-scoped member-account credentials under documented prerequisites. It requires the appropriate management/delegated IAM authority, a Regional STS endpoint, a supported task policy and at most a 15-minute session.[^assume-root] It is not a general unrestricted admin session, nor a procedure to run casually to inspect an account. This guide deliberately includes no root-session invocation.

## Design the independent access path

| Failure | Dependency to evaluate |
| --- | --- |
| Identity Center unavailable, IdP available | Preconfigured direct federation to critical operations roles can address that failure. |
| IdP also unavailable | That same direct-federation path still depends on the IdP; design a separately controlled break-glass method. |
| Member SCP denial | A member emergency role remains subject to applicable organization limits; recovery needs authority at the policy-owning level. |
| Stale generated role reference | KMS/EKS or other resource recovery may need an independent role/reference strategy. |
| Lost recovery mailbox/MFA custody | Account recovery contacts and custody must be available independently of the affected administrator. |

AWS's emergency federation guidance requires the relevant IAM data plane and external IdP to remain available and recommends preparing/testing before an outage.[^emergency] Current resiliency features do not remove the need to map those dependencies. Do not disable broad controls during normal operations to create an undocumented permanent back door.

## Exercise and close the activation

Run a tabletop, then a bounded sandbox exercise with synthetic resources and a named recovery owner. Verify activation through the assumed failed dependency, intended and forbidden operations, detection/acknowledgement, time limits, evidence retention and restoration of ordinary access. Test custody and absence of a key dependency; a successful normal login is insufficient.

After the drill, remove task-specific grants/credentials under the approved recovery design, validate expiry/revocation behavior, restore intended guardrails and retain evidence. Never delete management/root recovery material as incidental cleanup. See [incident response](../security/security-incident-response.md) for issued-session containment.

## Evidence and limits

Official sources reviewed on 2026-11-10. These drafts describe current AWS behavior and an applied review process. No AWS account/API call, login, policy attachment, organization change, root session, account creation/closure, or user-session revocation was executed during authoring. CLI examples are source-reviewed AWS CLI v2 instructions; no AWS CLI runtime version was tested. The separate synthetic inventory lab validates local reconciliation only.

[Back to governance and access](index.md) | [Back to AWS](../index.md)

[^root-practices]: [Root user security practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html).
[^root-central]: [Centralized member-account root access](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-enable-root-access.html).
[^assume-root]: [STS AssumeRoot](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoot.html).
[^emergency]: [Emergency access design](https://docs.aws.amazon.com/singlesignon/latest/userguide/emergency-access.html).
