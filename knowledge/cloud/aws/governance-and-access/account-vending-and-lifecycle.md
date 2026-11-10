---
type: How-to Guide
title: Govern AWS account vending and retirement
description: Choose an account-provisioning owner and verify baseline, identity, audit,
  cost and retirement outcomes across asynchronous workflows.
tags:
- aws
- governance
- human-access
status: draft
maturity: draft
audience: Cloud administrators and platform engineers
maintainer: unassigned
sources:
- id: org-practices
  title: AWS multi-account practices
  resource: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_best-practices.html
- id: factory
  title: Control Tower Account Factory
  resource: https://docs.aws.amazon.com/controltower/latest/userguide/account-factory.html
- id: aft
  title: Account Factory for Terraform
  resource: https://docs.aws.amazon.com/controltower/latest/userguide/aft-overview.html
---

# Govern AWS account vending and retirement

An account creation API succeeding is only one step in making an account usable and governed. Assign one provisioning authority and track the request through baseline, access, evidence, workload handoff and eventual retirement. An account registry should retain immutable ID and lifecycle history rather than identifying accounts only by display name.

## Choose the provisioning workflow

| Option | Responsibility retained by the platform |
| --- | --- |
| Organizations APIs with owned automation | Account requests/status, OU placement, all baselines, identity, controls and recovery. |
| Control Tower Account Factory | Landing-zone/account baseline requirements, target OU eligibility, customization and operational ownership. |
| Account Factory for Terraform (AFT) | Terraform-driven request/customization pipelines on an existing Control Tower landing zone. |

Account Factory's current requirements include applicable OU baselines/enrollment; moving or creating an account does not imply every control is enabled everywhere.[^factory] AFT adds a provisioning/customization framework and a separate AFT management account, distinct from the Control Tower management account.[^aft] Avoid using two controllers to make conflicting changes to the same account baseline.

## Define request and acceptance

Record purpose, owner/cost owner, account contact ownership, environment, OU/control path, allowed Regions, data classification, human access, workload credentials, network/egress, logging destination, retention, and retirement decision. Use the organization's actual contact/root-access model rather than assuming a personal inbox and permanent member-root password.[^org-practices]

After asynchronous provisioning, verify the account ID, placement, baseline status, controls and evidence delivery. Test the intended operator's actual caller and allowed/denied operations. Verify budget/notification ownership and network access separately. A pipeline's successful Terraform apply is not proof that a new person can use the account safely.

## Operate updates and failures

Treat OU moves, baseline updates, email/identity changes and customizations as reviewed migrations. Capture request IDs, stage status and failure reasons. Reconcile desired account metadata with observed organization/control/identity state before retrying; a blind resubmission can duplicate requests or leave partial access. Trace cleanup ownership across account factory and customizations.

## Retire an account deliberately

Before closure, stop new workload intake; inventory resources, dependencies, commitments, billing, legal/data retention, backups/key decryptability, DNS/domains, access and security evidence. Test recovery/exports while access still exists. Assign owners for each residual obligation. Unenrolling from a landing zone or moving into a retiring OU does not delete resources, remove charges or close the account.

Use current AWS closure/recovery procedures and organization limits when actually retiring an authorized account. This guide provides no closure command or promise that reversal/retention is unlimited. A lab should clean up its task-owned workload/identity artifacts and leave account closure to that explicit lifecycle process.

## Evidence and limits

Official sources reviewed on 2026-11-10. These drafts describe current AWS behavior and an applied review process. No AWS account/API call, login, policy attachment, organization change, root session, account creation/closure, or user-session revocation was executed during authoring. CLI examples are source-reviewed AWS CLI v2 instructions; no AWS CLI runtime version was tested. The separate synthetic inventory lab validates local reconciliation only.

[Back to governance and access](index.md) | [Back to AWS](../index.md)

[^org-practices]: [AWS multi-account practices](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_best-practices.html).
[^factory]: [Control Tower Account Factory](https://docs.aws.amazon.com/controltower/latest/userguide/account-factory.html).
[^aft]: [Account Factory for Terraform](https://docs.aws.amazon.com/controltower/latest/userguide/aft-overview.html).
