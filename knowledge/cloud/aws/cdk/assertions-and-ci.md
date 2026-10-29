---
type: Explanation
title: CDK assertions and CI
description: Test infrastructure intent before CloudFormation deployment.
tags:
- cloud
- cdk
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: cdk-assertions
  resource: https://docs.aws.amazon.com/cdk/v2/guide/testing.html
  title: CDK assertions
- id: cdk-cli-compatibility
  resource: https://docs.aws.amazon.com/cdk/v2/guide/cli.html
  title: CDK CLI compatibility
---

# CDK assertions and CI

## Purpose

Test infrastructure intent before CloudFormation deployment.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Test properties that matter

Both supplied tests assert encryption, public-access blocking, versioning, TLS enforcement, and `Retain` on deletion/replacement. These detect weakened security or accidental destructive behavior. A template snapshot is useful for review but should not replace focused assertions.[^cdk-assertions][^cdk-cli-compatibility]

A meaningful negative test temporarily removes `blockPublicAccess` or changes removal policy to DESTROY and confirms tests fail; restore the intended code afterward. Keep such mutation in a temporary copy during automated validation.

## Pipeline shape

Install pinned dependencies -> run TypeScript and Python assertions -> synthesize both -> compare resource contracts -> scan/review templates -> publish redacted artifacts -> deploy using a scoped deployment role only in the deployment stage.

For federation-based CI authentication, use the repository's existing GitHub Actions OIDC guidance. Avoid long-lived AWS keys in workflow variables. Synthesis can execute arbitrary application code, so do not give untrusted pull-request jobs production credentials.

The [educational GitHub Actions workflow](examples/ci-workflow.yaml) installs pinned direct dependencies, runs both implementations, and compares synthesized resources. Action revisions are pinned to verified commits. It is supplied as an example, not installed in this repository's active workflows.

## Comparison boundary

Compare the S3 resource properties, deletion/update-replacement policy, and TLS-deny bucket policy across languages. Generated logical IDs should also be reviewed for changes. Test data-preservation assumptions separately from runtime AWS behavior; a correct synthesized template cannot prove every account policy permits deployment.

## Diagnostics

A jsii error often points to Node/runtime or library compatibility. A CLI cloud-assembly-schema mismatch means the CLI may be too old for the library. Keep CLI and construct-library versions explicitly recorded; their version numbers do not need to be numerically identical.

## Related links

- [CDK assertions](https://docs.aws.amazon.com/cdk/v2/guide/testing.html)
- [CDK CLI compatibility](https://docs.aws.amazon.com/cdk/v2/guide/cli.html)
- [GitHub Actions security](../../../git/github-actions/security-secrets-and-permissions.md)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^cdk-assertions]: [CDK assertions](https://docs.aws.amazon.com/cdk/v2/guide/testing.html).
[^cdk-cli-compatibility]: [CDK CLI compatibility](https://docs.aws.amazon.com/cdk/v2/guide/cli.html).
