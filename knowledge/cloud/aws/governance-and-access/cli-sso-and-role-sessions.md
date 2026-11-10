---
type: How-to Guide
title: Use human AWS CLI sessions safely
description: Configure a refreshable permission-set SSO profile, establish the actual
  caller, and distinguish local logout from session containment.
tags:
- aws
- governance
- human-access
status: draft
maturity: draft
audience: Cloud administrators and platform engineers
maintainer: unassigned
sources:
- id: cli-sso
  title: AWS CLI SSO configuration
  resource: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html
- id: sessions
  title: Identity Center session types and termination
  resource: https://docs.aws.amazon.com/singlesignon/latest/userguide/authconcept.html
- id: account-access
  title: IAM account access manager
  resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/account-access-manager.html
---

# Use human AWS CLI sessions safely

This procedure targets Identity Center **permission-set** access with an existing approved assignment. It does not create an identity source, permission set, account or IAM role. Collect the approved portal/issuer URL, Identity Center Region, account ID and account-role name before configuring a named profile.

## Configure and establish the caller

```bash
aws configure sso --profile learning-readonly
aws sso login --profile learning-readonly
aws sts get-caller-identity --profile learning-readonly --no-cli-pager
```

What it does: writes a local named profile through the wizard, authenticates interactively, and reports the effective account/role. Use the current SSO token-provider configuration rather than legacy non-refreshable settings.[^cli-sso] The profile name is a local label, not a security boundary. Compare the actual account/role to the intended assignment before a resource operation.

The Identity Center Region selects the SSO service configuration; the workload service Region is a separate choice. PKCE/device authorization and browser requirements depend on the CLI version and options. Follow the official wizard for that version; do not paste login codes or token-cache contents into issue reports.[^cli-sso]

## Verify the resource operation

`GetCallerIdentity` identifies the credentials and needs no ordinary permission grant; it does not prove S3/KMS/EKS access. Use the [credential lifecycle guide](../security/credential-providers-and-session-lifecycle.md) and test an agreed allowed/denied operation on a disposable resource. Check explicit/static credentials, SDK providers and application profile selection if the caller is unexpected.

## Track separate session lifetimes

The IdP/Identity Center interactive session, application sessions, and issued IAM role credentials have different termination behavior. Portal sign-out or disabling a user is not proof that every already-issued IAM role session lost service access.[^sessions] Do not add long-lived keys to hide a refresh or assignment failure.

```bash
aws sso logout
```

What it does: signs out local cached SSO sessions according to the CLI workflow; it can affect more than one configured SSO profile.[^cli-sso] It is not an incident-wide revocation procedure for credentials copied elsewhere. Coordinate normal logout with your own sessions, and use [offboarding](access-review-and-offboarding.md) for administrative containment.

Current **account access manager** has a distinct documented browser/`aws login` experience and account-role mapping.[^account-access] Confirm the selected model and supported CLI before using instructions from one model in the other. This guide does not claim that its `configure sso` sequence applies to every workforce access method.

## Troubleshooting and cleanup

For an absent role, inspect identity provisioning, exact account assignment and provisioning result. For expired credentials, inspect the chosen provider and session state. For a live service denial, inspect the applicable policy context. Use [governance diagnosis](governance-access-troubleshooting.md). Retain useful version/error evidence, then remove only a task-created profile/report if no longer needed; do not erase another user's shared configuration or cache.

## Evidence and limits

Official sources reviewed on 2026-11-10. These drafts describe current AWS behavior and an applied review process. No AWS account/API call, login, policy attachment, organization change, root session, account creation/closure, or user-session revocation was executed during authoring. CLI examples are source-reviewed AWS CLI v2 instructions; no AWS CLI runtime version was tested. The separate synthetic inventory lab validates local reconciliation only.

[Back to governance and access](index.md) | [Back to AWS](../index.md)

[^cli-sso]: [AWS CLI SSO configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html).
[^sessions]: [Identity Center session types and termination](https://docs.aws.amazon.com/singlesignon/latest/userguide/authconcept.html).
[^account-access]: [IAM account access manager](https://docs.aws.amazon.com/IAM/latest/UserGuide/account-access-manager.html).
