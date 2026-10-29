---
type: Troubleshooting Guide
title: CDK deployment, updates, and troubleshooting
description: Review account changes and retain a recovery path before deploying.
tags:
- cloud
- cdk
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: cdk-bootstrap
  resource: https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html
  title: CDK bootstrap
- id: cdk-troubleshooting
  resource: https://docs.aws.amazon.com/cdk/v2/guide/troubleshooting.html
  title: CDK troubleshooting
- id: cloudformation-rollback-recovery
  resource: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html
  title: CloudFormation rollback recovery
---

# CDK deployment, updates, and troubleshooting

## Purpose

Review account changes and retain a recovery path before deploying.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Bootstrap and preview

A CDK bootstrap stack provides deployment infrastructure such as asset storage and roles. It is account/region-specific and shared by applications. Review trust and policies before creating it.[^cdk-bootstrap][^cdk-troubleshooting][^cloudformation-rollback-recovery]

> [!WARNING]
> Bootstrap and deploy create or modify AWS resources and can incur costs. Use a disposable account/region and verify identity. The lab bucket is retained after stack deletion and can continue incurring storage charges.

```bash
aws sts get-caller-identity
pnpm exec cdk bootstrap aws://ACCOUNT/REGION
pnpm exec cdk diff --app 'pnpm exec tsx app.ts'
pnpm exec cdk deploy --app 'pnpm exec tsx app.ts' KbDocsLab
```

What it does: verifies the operator, prepares a specified environment, previews, and deploys. Replace ACCOUNT/REGION with the intended environment and set CDK_DEFAULT_ACCOUNT/CDK_DEFAULT_REGION or the app environment consistently. Review security-sensitive changes and replacements before accepting deployment.

## Updates and removal

Changing a bucket's construct identity or replacement-sensitive properties can create new storage instead of updating the old resource. Retention protects data but does not migrate it. Versioning is useful recovery support, not a complete backup strategy.

```bash
pnpm exec cdk destroy --app 'pnpm exec tsx app.ts' KbDocsLab
```

What it does: deletes the stack after confirmation while retaining the bucket per its policy. Inventory retained resources separately. Do not add automatic object deletion to make cleanup convenient for a stateful production resource.

## Failure sequence

Read CloudFormation stack events before retrying. Distinguish IAM denial, service quota, unavailable name, asset publication, and resource rollback. Correct the underlying cause; repeated deployments do not repair a missing permission.

For UPDATE_ROLLBACK_FAILED follow AWS's documented recovery process and inspect drift afterward. Skipping resources or manual deletion can leave the stack inconsistent. Keep bootstrap resources under their shared owner rather than deleting them during application cleanup.

## Related links

- [CDK bootstrap](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html)
- [CDK troubleshooting](https://docs.aws.amazon.com/cdk/v2/guide/troubleshooting.html)
- [CloudFormation rollback recovery](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^cdk-bootstrap]: [CDK bootstrap](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html).
[^cdk-troubleshooting]: [CDK troubleshooting](https://docs.aws.amazon.com/cdk/v2/guide/troubleshooting.html).
[^cloudformation-rollback-recovery]: [CloudFormation rollback recovery](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html).
